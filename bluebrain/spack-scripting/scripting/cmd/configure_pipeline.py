import os
import re

from llnl.util import tty
from llnl.util.filesystem import filter_file

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


def add_develop_version(recipe_path, spack_package_class_name):
    tty.info("class {}: adding `develop` version".format(spack_package_class_name))
    # Pattern to match the specified line
    pattern = re.compile(r'class {}'.format(re.escape(spack_package_class_name)))

    # Content to be appended
    append_content = 'version(\'develop\')'

    # Read the file and store its lines
    with open(recipe_path, 'r') as file:
        lines = file.readlines()

    # Check if the pattern exists in any line
    for i, line in enumerate(lines):
        if pattern.match(line):
            # Append the content to the matching line
            lines[i] = '{}\n    {}\n'.format(line.rstrip(), append_content)

    # Write the updated content back to the file
    with open(recipe_path, 'w') as file:
        file.writelines(lines)


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
        }

    # Translate any branches or tags into commit hashes and then use those
    # consistently. This guarantees different jobs in a pipeline all get the
    # same commit, and means we can handle provenance information (what did
    # @develop mean) in one place.
    git = which("git")
    if not git:
        raise Exception("Git is required")
    for spack_package_name, info in modifications.items():
        if info["ref_type"] == "commit":
            info["commit"] = info["ref"]
        else:
            if info["ref_type"] == "branch":
                remote_ref = "refs/heads/" + info["ref"]
            else:
                assert info["ref_type"] == "tag"
                remote_ref = "refs/tags/" + info["ref"]
            spack_package = spack.repo.path.get_pkg_class(spack_package_name)
            remote_refs = git("ls-remote", spack_package.git, remote_ref, output=str).splitlines()
            assert len(remote_refs) < 2
            if len(remote_refs) == 0:
                raise Exception(
                    "Could not find {} {} on remote {} (tried {})".format(
                        info["ref_type"], info["ref"], spack_package.git, remote_ref
                    )
                )
            commit, ref_check = remote_refs[0].split()
            assert remote_ref == ref_check
            tty.info(
                "{}: resolved {} {} to {}".format(
                    spack_package_name, info["ref_type"], info["ref"], commit
                )
            )
            info["commit"] = commit

    if args.write_commit_file is not None:
        with open(args.write_commit_file, "w") as ofile:
            for spack_package_name, info in modifications.items():
                ofile.write("{}_COMMIT={}\n".format(info["bash_name"], info["commit"]))

    # Now modify the Spack recipes of the given packages
    for spack_package_name, info in modifications.items():
        spack_package = spack.repo.path.get_pkg_class(spack_package_name)
        spack_recipe = os.path.join(spack_package.package_dir, spack.repo.package_file_name)
        # Using filter_file seems neater than calling sed, but it is a little
        # more limited. First, remove any existing branch/commit/tag from the
        # develop version.
        tty.info("{}@develop: remove branch/commit/tag".format(spack_package_name))

        def search_file_with_regex(file, regex_pattern: str) -> bool:
            regex = re.compile(regex_pattern)
            for line in file:
                match = regex.search(line)
                if match:
                    return True
            return False

        with open(spack_recipe) as spack_recipe_file:
            # Check if `develop` version exists in the spack recipe. If not, add a
            # `develop` version declaration that can be filtered later with the proper
            # commit and arguments
            if search_file_with_regex(spack_recipe_file,
                                      "version\\s*\\(\\s*(['\"]{1})develop\\1(.*?)"):
                filter_file(
                    "version\\s*\\(\\s*(['\"]{1})develop\\1(.*?)"
                    + ",\\s*(branch|commit|tag)=(['\"]{1})(.*?)\\4(.*?)\\)",
                    "version('develop'\\2\\6) # old: \\3=\\4\\5\\4",
                    spack_recipe,
                )
            else:
                add_develop_version(spack_recipe, spack_package.__name__)
        # Second, insert the new commit="sha" part
        tty.info('{}@develop: use commit="{}"'.format(spack_package_name, info["commit"]))
        filter_file(
            "version\\('develop'",
            "version('develop', commit='{}'".format(info["commit"]),
            spack_recipe,
        )
        # Third, make sure that the develop version, and only the develop
        # version, is flagged as the preferred version. Start by getting a list
        # of versions that are already explicitly flagged as preferred.
        already_preferred = {
            str(v)
            for v, v_info in spack_package.versions.items()
            if v_info.get("preferred", False)
        }
        # Make sure the develop version has an explicit preferred=True.
        if "develop" not in already_preferred:
            tty.info("{}@develop: add preferred=True".format(spack_package_name))
            filter_file("version\\('develop'", "version('develop', preferred=True", spack_recipe)
        # Make sure no other versions have an explicit preferred=True.
        for other_version in already_preferred - {"develop"}:
            tty.info("{}@{}: remove preferred=True".format(spack_package_name, other_version))
            escaped_version = re.escape(other_version)
            filter_file(
                "version\\s*\\(\\s*(['\"]{1})"
                + escaped_version
                + "\\1(.*?),\\s*preferred=True(.*?)\\)",
                "version('{version}'\\2\\3)".format(version=other_version),
                spack_recipe,
            )
