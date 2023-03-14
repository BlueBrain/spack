import re

from llnl.util import tty

import spack.config
import spack.environment as ev
import spack.repo
from spack.util.executable import which
from spack.util.naming import simplify_name

description = """Modify package recipes for use in CI pipelines.

This accepts zero or more expressions of the form PKG_{BRANCH,COMMIT,TAG}=VALUE
and uses them to modify package recipes in the current Spack tree.

If a branch or tag is given, this is immediately translated into a commit hash
and processing continues as if a commit had been given to start with. If the
optional --write-commit-file=FILE argument is given then FILE will contain the
results of this translation in the form of one PKG_COMMIT=HASH declaration per
line.

For each expression the upper case package name (PKG) is transformed into the
name of a Spack package, and the `develop` version of that package is modified:
 - to be the preferred version, and
 - to refer to the given commit.

If PKG cannot be uniquely mapped to a Spack package, or if multiple expressions
are given for the same Spack package, an error code is returned.
"""
section = "extensions"
level = "short"


def get_commit(package_name, ref, ref_type):
    """Get commit for a package based on references.

    Translate any branches or tags into commit hashes and then use those
    consistently. This guarantees different jobs in a pipeline all get the
    same commit, and means we can handle provenance information (what did
    @develop mean) in one place.
    """
    git = which("git")
    if not git:
        raise Exception("Git is required")
    if ref_type == "commit":
        return ref
    else:
        if ref_type == "branch":
            remote_ref = "refs/heads/" + ref
        else:
            assert ref_type == "tag"
            remote_ref = "refs/tags/" + ref
        spack_package = spack.repo.path.get_pkg_class(package_name)
        remote_refs = git("ls-remote", spack_package.git, remote_ref, output=str).splitlines()
        assert len(remote_refs) < 2
        if len(remote_refs) == 0:
            raise Exception(
                "Could not find {} {} on remote {} (tried {})".format(
                    ref_type, ref, spack_package.git, remote_ref
                )
            )
        commit, ref_check = remote_refs[0].split()
        assert remote_ref == ref_check
        tty.info("{}: resolved {} {} to {}".format(package_name, ref_type, ref, commit))
        return commit


def setup_parser(subparser):
    subparser.add_argument(
        "--ignore-packages",
        nargs="*",
        type=str,
        default=[],
        help="PACKAGE specifications to ignore if passed as positional arguments.",
    )
    subparser.add_argument(
        "--write-commit-file",
        default=None,
        type=str,
        help="File to write {PACKAGE}_COMMIT=1234 values to.",
    )
    subparser.add_argument(
        "modifications",
        nargs="*",
        type=str,
        help="PACKAGE_{BRANCH,COMMIT,TAG}=foo values",
    )


def configure_pipeline(parser, args):
    # Parse all of our inputs before trying to modify any recipes.
    modifications = {}
    packages_to_ignore = set(args.ignore_packages)
    mod_pattern = re.compile("^([^=]+)_(BRANCH|COMMIT|TAG)=(.*)$", re.IGNORECASE)
    for mod_str in args.modifications:
        match = mod_pattern.match(mod_str)
        if not match:
            raise Exception("Could not parse: {}".format(mod_str))
        package_name = match.group(1)
        ref_type = match.group(2).lower()
        val = match.group(3)
        # Handle --ignore-packges arguments
        if package_name in packages_to_ignore:
            tty.info("{}: ignoring {}".format(package_name, mod_str))
            continue
        # Try and transform the input name, which is probably all upper case
        # and may contain underscores, into a Spack-style name that is all
        # lower case and contains hyphens.
        spack_package_name = simplify_name(package_name)
        # Check if this package exists
        try:
            spack.repo.path.get_pkg_class(spack_package_name)
        except spack.repo.UnknownPackageError:
            raise Exception(
                "Could not find a Spack package corresponding to {}, tried {}".format(
                    package_name, spack_package_name
                )
            )
        if spack_package_name in modifications:
            raise Exception(
                "Parsed multiple modifications for Spack package {} from: {}".format(
                    spack_package_name, " ".join(args.modifications)
                )
            )
        modifications[spack_package_name] = {
            "bash_name": package_name,
            "ref_type": ref_type,
            "ref": val,
            "commit": get_commit(spack_package_name, val, ref_type),
        }

    if args.write_commit_file is not None:
        with open(args.write_commit_file, "w") as ofile:
            for spack_package_name, info in modifications.items():
                ofile.write("{}_COMMIT={}\n".format(info["bash_name"], info["commit"]))

    env = ev.active_environment()
    if env:
        scope = env.env_file_config_scope_name()
    else:
        scope = spack.config.default_modify_scope(section="packages")

    # Now modify the Spack configuration to require the given packages
    for spack_package_name, info in modifications.items():
        new_version = "git.{}=develop".format(info["commit"])
        config_path = "packages:{}:version".format(spack_package_name)
        tty.info("setting {} in {}: {}".format(config_path, scope, new_version))
        full_path = "{}:['{}']".format(config_path, new_version)
        spack.config.add(full_path, scope=scope)
