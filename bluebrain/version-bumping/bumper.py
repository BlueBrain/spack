#!/usr/bin/env python

import logging
import os
import re
import subprocess
from logging.handlers import RotatingFileHandler

from packaging import version

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(fmt="%(asctime)s :: %(levelname)s :: %(msg)s")
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)
logger.addHandler(sh)
fh = RotatingFileHandler("./bumper.log", backupCount=5)
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
logger.addHandler(fh)
logger.handlers[-1].doRollover()

SPACK_VERSION_REX = re.compile("version\(['\"](?P<version>[^'\"]+)['\"],.*")
GIT_REGEX = re.compile("^git *= *['\"][a-z]+://([a-z]+@)?(?P<git_url>[^'\"]+)['\"]")

# Main key is the package name as it appears in Spack
# The sub dictionary has a required key "tag_regex", which is a regular expression that
# specifies which tags in the git repository are used as released versions.
# DO NOT USE GROUPS IN THIS REGEX
# "tag_strip" is an optional key, specifiying a string to remove (string.replace) from anywhere
# in the repository tag when turning it into a packaging.version object.
PACKAGES = {
    "brayns": {"tag_regex": re.compile("\d+\.\d+\.\d+")},
    "brainbuilder": {
        "tag_regex": re.compile("brainbuilder-v\d+\.\d+\.\d+"),
        "tag_strip": "brainbuilder-",
    },
    "synapsetool": {"tag_regex": re.compile("v\d+\.\d+\.\d+")},
    "regiodesics": {"tag_regex": re.compile("\d+\.\d+\.\d+")},
    "touchdetector": {"tag_regex": re.compile("\d+\.\d+\.\d+")},
    "spykfunc": {"tag_regex": re.compile("v\d+\.\d+\.\d+")},
}


def get_source_lines(package_file):
    if os.path.exists(package_file):
        with open(package_file, "r") as fp:
            src = fp.readlines()
        return src
    else:
        raise ValueError(f"Source file {package_file} does not exist")


def get_latest_spack_version(package, package_file):
    """Get the latest version of a package in spack"""
    logger.info(f"===> Getting latest spack version for {package}")
    src = get_source_lines(package_file)
    version_lines = [
        line.strip() for line in src if line.strip().startswith("version") and "tag=" in line
    ]
    if not version_lines:
        raise ValueError(
            f"Could not determine versions for {package}. Only tag-based versions are supported."
        )
    spack_versions = [
        re.match(SPACK_VERSION_REX, version_line).groupdict()["version"]
        for version_line in version_lines
    ]
    logger.debug(f"{package} versions:")
    for spack_version in spack_versions:
        logger.debug(f"  * {spack_version}")

    return max([version.parse(spack_version) for spack_version in spack_versions])


def get_latest_source_version(package, package_file):
    """
    Get the latest version of a package in source control
    """
    logger.info(f"===> Getting latest source control version for {package}")
    src = get_source_lines(package_file)
    try:
        git_line = next(line.strip() for line in src if line.strip().startswith("git"))
    except StopIteration:
        raise ValueError(f"Could not find git source for {package}")
    git_repo = re.match(GIT_REGEX, git_line).groupdict()["git_url"]
    logger.debug(f"{package} lives in {git_repo}")
    if "github.com" in git_repo:
        git_repo = f"https://{git_repo}"
    else:
        if "CI_JOB_TOKEN" in os.environ:
            logger.debug("CI_JOB_TOKEN found - running on gitlab")
            git_repo = f"https://gitlab-ci-token:{os.environ['CI_JOB_TOKEN']}@{git_repo}"
        else:
            logger.debug("CI_JOB_TOKEN not found - SSH should be configured on your machine")
            git_repo = f"ssh://{git_repo}"
    proc = subprocess.run(
        f"git ls-remote --tags {git_repo} | awk -F '/' '{{print $3}}'",
        shell=True,
        capture_output=True,
    )
    repo_tags = proc.stdout.decode()
    if "tag_regex" not in PACKAGES[package]:
        logger.critical(
            f"No tag_regex specified for {package}. These are all the tags available: {repo_tags}"
        )
        return
    repo_release_tags = re.findall(PACKAGES[package]["tag_regex"], repo_tags)

    logger.debug(f"Version tags for {package}: {repo_release_tags}")

    return max(
        [
            (
                repo_release_tag,
                version.parse(
                    repo_release_tag.replace(PACKAGES[package].get("tag_strip", ""), "")
                ),
            )
            for repo_release_tag in repo_release_tags
        ],
        key=lambda x: x[1],
    )


def add_spack_version(package, latest_source_version):
    pass


def main():
    """Check packages for newer versions and update recipes if necessary

    For all subscribed packages:
      1. check what the latest version is
      2. check where it lives
      3. check what the latest version in source control is
      4. if newer: add a version call to the package recipe
    """

    missing_versions = []
    for package in PACKAGES:
        package_file = f"bluebrain/repo-bluebrain/packages/{package}/package.py"
        latest_spack_version = get_latest_spack_version(package, package_file)
        latest_source_tag, latest_source_version = get_latest_source_version(package, package_file)
        if latest_spack_version and latest_source_version:
            logger.info(f"  Latest spack version: {latest_spack_version}")
            logger.info(f"  Latest source control version: {latest_source_version}")
            bigger = latest_source_version > latest_spack_version
            if bigger:
                logger.info(f"Newer version available for {package}: {latest_source_version}")
            add_spack_version(package, latest_source_version)
        else:
            missing_versions.append(package)

    if missing_versions:
        raise RuntimeError(
            f"Some packages had either no spack or source control versions: {missing_versions}"
        )


if __name__ == "__main__":
    main()
