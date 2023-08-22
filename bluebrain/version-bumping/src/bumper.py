#!/usr/bin/env python

import logging
import os
import re
import subprocess
from logging.handlers import RotatingFileHandler

import requests
from git import Actor, Repo
from packaging import version

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(fmt="%(asctime)s :: %(levelname)s :: %(msg)s")
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)
logger.addHandler(sh)
fh = RotatingFileHandler("./bumper.log", maxBytes=50000)
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
logger.addHandler(fh)
logger.handlers[-1].doRollover()

SPACK_VERSION_REX = re.compile(r"version\(['\"](?P<version>[^'\"]+)['\"],.*")
GIT_REGEX = re.compile(r"^git *= *['\"][a-z]+://([a-z]+@)?(?P<git_url>[^'\"]+)['\"]")

# See README for the same explanation.
# Main key is the package name as it appears in Spack
# The sub dictionary has a required key "tag_regex", which is a regular expression that
# specifies which tags in the git repository are used as released versions.
# DO NOT USE GROUPS IN THIS REGEX
# "tag_strip" is an optional key, specifiying a string to remove (string.replace) from anywhere
# in the repository tag when turning it into a packaging.version object.
PACKAGES = {
    "brayns": {"tag_regex": re.compile(r"\d+\.\d+\.\d+")},
    "brainbuilder": {
        "tag_regex": re.compile(r"brainbuilder-v\d+\.\d+\.\d+"),
        "tag_strip": "brainbuilder-",
    },
    "synapsetool": {"tag_regex": re.compile(r"v\d+\.\d+\.\d+")},
    "regiodesics": {"tag_regex": re.compile(r"\d+\.\d+\.\d+")},
    "touchdetector": {"tag_regex": re.compile(r"\d+\.\d+\.\d+")},
    "spykfunc": {"tag_regex": re.compile(r"v\d+\.\d+\.\d+")},
}

COMMIT_BRANCH = "automatic-version-bumps"
VERSION_BUMPER_EMAIL = "erik.heeren@epfl.ch"


class Bumper:
    def __init__(self):
        self.packages = self.get_packages()
        self._repo = None

    def get_packages(self):
        """
        Fetch the list of packages and the information on how to deal with them
        """
        return PACKAGES

    def get_source_lines(self, package_file):
        """
        Read a source file and return the contents as a list of lines
        """
        if os.path.exists(package_file):
            with open(package_file, "r") as fp:
                src = fp.readlines()
            return src
        else:
            raise ValueError(f"Source file {package_file} does not exist")

    def get_latest_spack_version(self, package, package_file):
        """
        Get the latest version of a package in spack
        """
        logger.info(f"===> Getting latest spack version for {package}")
        src = self.get_source_lines(package_file)
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

    def build_git_url(self, package_git_url):
        """
        Given the package's git URL, build one we can use
        """
        if "github.com" in package_git_url:
            package_git_url = f"https://{package_git_url}"
        else:
            if "CI_JOB_TOKEN" in os.environ:
                logger.debug("CI_JOB_TOKEN found - running on gitlab")
                package_git_url = (
                    f"https://gitlab-ci-token:{os.environ['CI_JOB_TOKEN']}@{package_git_url}"
                )
            else:
                logger.debug("CI_JOB_TOKEN not found - SSH should be configured on your machine")
                package_git_url = f"ssh://{package_git_url}"

        return package_git_url

    def get_latest_source_version(self, package, package_file):
        """
        Get the latest version of a package in source control
        """
        logger.info(f"===> Getting latest source control version for {package}")
        src = self.get_source_lines(package_file)
        try:
            git_line = next(line.strip() for line in src if line.strip().startswith("git"))
        except StopIteration:
            raise ValueError(f"Could not find git source for {package}")
        git_repo = re.match(GIT_REGEX, git_line).groupdict()["git_url"]
        logger.debug(f"{package} lives in {git_repo}")
        git_repo = self.build_git_url(git_repo)
        proc = subprocess.run(
            f"git ls-remote --tags {git_repo} | awk -F '/' '{{print $3}}'",
            shell=True,
            capture_output=True,
        )
        repo_tags = proc.stdout.decode()
        if "tag_regex" not in self.packages[package]:
            logger.critical(
                f"No tag_regex specified for {package}. These are all the tags available: {repo_tags}"
            )
            return None, None
        repo_release_tags = re.findall(self.packages[package]["tag_regex"], repo_tags)

        logger.debug(f"Version tags for {package}: {repo_release_tags}")

        return max(
            [
                (
                    repo_release_tag,
                    version.parse(
                        repo_release_tag.replace(self.packages[package].get("tag_strip", ""), "")
                    ),
                )
                for repo_release_tag in repo_release_tags
            ],
            key=lambda x: x[1],
        )

    def add_spack_version(self, package, latest_source_tag, latest_source_version, package_file):
        logger.info(f"===> Adding version {latest_source_version} for {package}")
        source_lines = self.get_source_lines(package_file)
        for idx, line in enumerate(source_lines):
            if line.strip().startswith("version("):
                spaces = " " * (len(line) - len(line.lstrip()))
                new_line = (
                    f'{spaces}version("{latest_source_version}", tag="{latest_source_tag}")\n'
                )
                logger.info(new_line)
                source_lines.insert(idx, new_line)
                break

        with open(package_file, "w") as fp:
            fp.write("".join(source_lines))

    def checkout_branch(self, repo, branch_name):
        """
        Check out the branch, creating it if necessary
        """
        logger.info(f"===> Checking out {branch_name}")
        remote = repo.remote()
        existing_branches = [ref.name for ref in remote.refs]
        remote_ref_name = f"{remote.name}/{branch_name}"
        try:
            remote_ref = next(ref for ref in remote.refs if ref.name == remote_ref_name)
            logger.debug(f"{branch_name} already exists, checkout only")
            remote_ref.checkout()
        except StopIteration:
            logger.debug(f"{branch_name} does not exist yet - creating")
            repo.create_head(branch_name)
            new_branch = next(head for head in repo.heads if head.name == branch_name)
            new_branch.checkout()

    def commit(self, packages):
        """
        Commit outstanding changes, creating the branch if necessary
        """
        logger.info(f"===> Committing and pushing")
        repo = self.repo()
        self.checkout_branch(repo, COMMIT_BRANCH)
        author = Actor("Version Bumper Script", VERSION_BUMPER_EMAIL)
        prefix = ", ".join(packages)
        commit_message = f"{prefix}: new versions"
        logger.debug(f"Committing with message {commit_message}")
        repo.index.commit(commit_message, author=author, committer=author)
        result = repo.remote().push(refspec=f"{COMMIT_BRANCH}:{COMMIT_BRANCH}")
        if result[0].flags not in [result[0].FAST_FORWARD, result[0].NEW_HEAD]:
            raise RuntimeError(f"Undesirable push result: {result[0].flags} - {result[0].summary}")

    def repo(self):
        """
        Instantiate the repo if it isn't done yet, and add the github remote if necessary
        """
        # TODO: make sure "." is correct
        if not self._repo:
            self._repo = Repo(".")
            try:
                remote = self._repo.remote("github")
            except ValueError:
                remote = self._repo.create_remote(
                    "github",
                    "https://bbp-hpcteam:${GITHUB_API_KEY}@github.com/bluebrain/spack",
                )
        return self._repo

    def file_pull_request(self, packages):
        logger.info(f"===> Filing pull request")
        url = "https://api.github.com/repos/bluebrain/spack"
        session = requests.Session()
        session.headers = {
            "Authorization": f"token {os.environ['GITHUB_API_KEY']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        logger.debug(f"Getting pull requests with head {COMMIT_BRANCH}")
        pulls = session.get(f"{url}/pulls?base=develop&head={COMMIT_BRANCH}").json()
        if not pulls:
            logger.debug("PR doesn't exist yet - filing")
            data = {
                "title": f"{', '.join(packages)}: new releases",
                "body": "Bumper found new releases, please check carefully and add new "\
                "dependencies, remove obsolete dependencies, ...",
                "head": f"{COMMIT_BRANCH}",
                "base": "bluebrain:develop",
            }
            response = session.post(f"{url}/pulls", json=data)

            logger.debug("Pull request made")
            logger.debug(response)
            logger.debug(response.content)
            response.raise_for_status()
        else:
            logger.debug("Pull request already exists: {pulls[0]['_links']['self']['href']}")

    def process_packages(self):
        """
        Check packages for newer versions and update recipes if necessary

        For all subscribed packages:
          1. check what the latest version is
          2. check where it lives
          3. check what the latest version in source control is
          4. if newer: add a version call to the package recipe
        """

        missing_versions = []
        updated_packages = []
        repo = self.repo()
        for package in self.packages:
            package_file = f"bluebrain/repo-bluebrain/packages/{package}/package.py"
            latest_spack_version = self.get_latest_spack_version(package, package_file)
            latest_source_tag, latest_source_version = self.get_latest_source_version(
                package, package_file
            )
            logger.info(f"Tag: {latest_source_tag}")
            logger.info(f"Version: {latest_source_version}")
            if latest_spack_version and latest_source_version:
                logger.info(f"  Latest spack version: {latest_spack_version}")
                logger.info(f"  Latest source control version: {latest_source_version}")
                bigger = latest_source_version > latest_spack_version
                if bigger:
                    logger.info(f"Newer version available for {package}: {latest_source_version}")
                    updated_packages.append(package)
                    self.add_spack_version(
                        package, latest_source_tag, latest_source_version, package_file
                    )
                    repo.index.add([package_file])
            else:
                missing_versions.append(package)

        if missing_versions:
            raise RuntimeError(
                f"Some packages had either no spack or source control versions: {missing_versions}"
            )

        if repo.index.diff("HEAD"):
            self.commit(updated_packages)
            self.file_pull_request(updated_packages)


if __name__ == "__main__":
    bumper = Bumper()
    bumper.process_packages()
