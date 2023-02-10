#!/usr/bin/env python

# requires: gitpython

import fileinput
import json
import os
import textwrap
from argparse import ArgumentParser

from git import Repo

KEYWORDS = ["nopackage", "deploy", "docs"]
EXISTING_PACKAGES = []


def get_changed_packages(changed_files: list[str]) -> list[str]:
    """
    Return all packages changed by the commit
    """

    changed_packages = []
    changed_package_paths = [path for path in changed_files if "/packages/" in path]
    for package_path in changed_package_paths:
        path_components = package_path.split("/")
        changed_packages.append(path_components[path_components.index("packages") + 1])

    return changed_packages


def get_unmentioned_packages(
    prefixes: list[str], changed_files: list[str]
) -> list[str]:
    unmentioned_packages = []

    changed_packages = get_changed_packages(changed_files)

    for package in changed_packages:
        if package not in prefixes:
            unmentioned_packages.append(package)

    return unmentioned_packages


def one_package_mentioned(prefixes: list[str], changed_files: list[str]) -> list[str]:
    """Check whether at least one changed package is mentioned"""

    changed_packages = get_changed_packages(changed_files)
    return len([prefix for prefix in prefixes if prefix in changed_packages]) > 0


def collect_prefixes(message: str) -> list[str]:
    """
    Collect all prefixes in the commit message
    """
    prefixes = []

    for line in message.splitlines():
        if ":" in line:
            prefix = message.splitlines()[0]
            prefix_items = [item.strip() for item in prefix.split(",")]
            prefixes.extend(prefix_items)

    return prefixes


def main(title: str, changed_files: list[str]) -> None:
    print(
        "Setting fail state to make sure we catch any script failures- we'll clean up at the end"
    )
    with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
        fp.write("script-failure=true\n")
    repo = Repo(".")

    commit_message_issues = []

    commit = next(repo.iter_commits())
    print(f"Checking commit: {commit.message} (parents: {commit.parents})")
    quoted_commit_message = textwrap.indent(commit.message, prefix="  > ")

    prefixes = collect_prefixes(title)
    docs_changed = any(
        "documentation" in changed_file for changed_file in changed_files
    )
    deploy_changed = any(
        "yml" in changed_file for changed_file in changed_files
    ) or any("yaml" in changed_file for changed_file in changed_files)

    minimal_prefix_present = False
    if one_package_mentioned(prefixes, changed_files):
        minimal_prefix_present = True
    elif docs_changed and "docs" in prefixes:
        minimal_prefix_present = True
    elif deploy_changed:
        minimal_prefix_present = True

    if not minimal_prefix_present:
        unmentioned_packages = get_unmentioned_packages(prefixes, changed_files)
        if unmentioned_packages:
            msg = textwrap.dedent(
                f"""\
                * The following packages were changed but not mentioned:
                  {", ".join(unmentioned_packages)}
                  You can simply use the above list followed by a colon, \
                  then explain what you changed.
                  Alternatively, you can use one line per package \
                  to describe the change per package.
                """
            )
            commit_message_issues.append(msg)

        if docs_changed and "docs" not in prefixes:
            msg = textwrap.dedent(
                """\
                * Docs were changed but not mentioned in the commit message.
                  Please use the `docs:` prefix to explain this change.
                """
            )
            commit_message_issues.append(msg)

        if deploy_changed and "deploy" not in prefixes:
            msg = textwrap.dedent(
                """\
                * Deploy files were changed but not mentioned in the commit message.
                  Please use the `deploy:` prefix to explain this change.
                """
            )
            commit_message_issues.append(msg)

    if commit_message_issues:
        warning = textwrap.dedent(
            f"""\
            There are one or more issues with the commit message of commit {commit.hexsha}.
            Commit message:
            {quoted_commit_message}
            Please satisfy at least one of the checks (one package, docs, or deploy).
            Issues:
            """
        )
        commit_message_issues.insert(0, warning)
        with open("commit_message_issues.txt", "w") as fp:
            fp.write("\n".join(commit_message_issues))
        with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
            fp.write("faulty-commits=true")

    with fileinput.FileInput(os.environ["GITHUB_OUTPUT"], inplace=True) as file:
        for line in file:
            print(line.replace("script-failure=true", "script-failure=false"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument(
        "--changed-files",
        required=True,
        help="JSON formatted list of files changed in PR",
    )

    args = parser.parse_args()

    for spack_repo in [
        "./var/spack/repos/builder.test",
        "./var/spack/repos/builtin",
        "./var/spack/repos/builtin.mock",
        "./var/spack/repos/tutorial",
        "./bluebrain/repo-bluebrain",
        "./bluebrain/repo-patches",
    ]:
        try:
            EXISTING_PACKAGES.extend(next(os.walk(f"{spack_repo}/packages"))[1])
        except StopIteration:
            print(f"No packages under {spack_repo}")
            pass

    main(args.title, json.loads(args.changed_files))
