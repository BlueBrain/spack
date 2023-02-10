#!/usr/bin/env python

# requires: gitpython

import os
import textwrap
from argparse import ArgumentParser

from git import Repo

KEYWORDS = ["nopackage", "deploy", "docs"]
EXISTING_PACKAGES = []


def all_packages_mentioned(prefixes: list[str], changed_packages: list[str]) -> bool:
    pass


def prefix_invalid(line: str) -> bool:
    packages = line.split(":")[0].split(",")
    for package in map(str.strip, packages):
        if package not in EXISTING_PACKAGES and package not in KEYWORDS:
            return True

    return False


def docs_changed(changed_files: list[str]) -> bool:
    """
    Check whether anything changed in docs
    """

    return any('documentation' in changed_file for changed_file in changed_files)


def deploy_changed(changed_files: list[str]) -> bool:
    """
    Check whether anything related to deploy changed
    """

    return (any('yml' in changed_file for changed_file in changed_files) or
            any('yaml' in changed_file for changed_file in changed_files))


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


def main(title: str, changed_files: list[str]):
    repo = Repo(".")

    faulty_commits = []

    if prefix_invalid(title):
        msg = textwrap.dedent(
            f"""\
            * Pull Request Title
              > {title}

              Pull request title needs to be compliant as well, '
              as it will be used for the merge/squash commit'
            """
        )
        faulty_commits.append(msg)

    commit = next(repo.iter_commits())
    print(f"Checking commit: {commit.message} (parents: {commit.parents})")
    prefixes = collect_prefixes()

    for line in commit.message.splitlines():
        if ":" in line:
            prefix = commit.message.splitlines()[0]
            if prefix_invalid(prefix):
                quoted_commit_message = textwrap.indent(commit.message, prefix="  > ")
                msg = f"* {commit.hexsha}\n{quoted_commit_message}"
                faulty_commits.append(msg)

    if faulty_commits:
        warning = "These commits are not formatted correctly. "
        warning += "Please amend them to start with one of:\n"
        warning += "* \\<package>: \n"
        warning += "* \\<package>, <package>, ...: \n"
        warning += f'* {", ".join(keyword + ":" for keyword in KEYWORDS)}\n\n'
        warning += "### Faulty commits:\n"
        faulty_commits.insert(0, warning)
        with open("faulty_commits.txt", "w") as fp:
            fp.write("\n".join(faulty_commits))
        with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
            fp.write("faulty-commits=true")


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

    main(args.title)
