import os
import re
import subprocess
import sys
import textwrap
from unittest.mock import MagicMock, patch

import pytest
from packaging import version

sys.modules["spack"] = MagicMock()
sys.modules["spack.bootstrap"] = ""
sys.modules["spack.package_base"] = ""

from src.bumper import COMMIT_BRANCH, Bumper

MOCK_BRANCH_NAMES = ["some-branch", "some-other-branch", "yet-another-branch"]


@pytest.fixture
def bumper():
    return Bumper()


@pytest.fixture
def github_api_key():
    if "GITHUB_API_KEY" not in os.environ:
        os.environ["GITHUB_API_KEY"] = "api_key"

    yield

    os.environ.pop("GITHUB_API_KEY")


@pytest.fixture
def ci_job_token():
    if "CI_JOB_TOKEN" not in os.environ:
        os.environ["CI_JOB_TOKEN"] = "test_token"

    yield

    os.environ.pop("CI_JOB_TOKEN")
    if "SAVE_CI_JOB_TOKEN" in os.environ:
        os.environ["CI_JOB_TOKEN"] = os.environ["SAVE_CI_JOB_TOKEN"]
        os.environ.pop("SAVE_CI_JOB_TOKEN")


@pytest.fixture
def no_ci_job_token():
    if "CI_JOB_TOKEN" in os.environ:
        os.environ["SAVE_CI_JOB_TOKEN"] = os.environ["CI_JOB_TOKEN"]
        os.environ.pop("SAVE_CI_JOB_TOKEN")

    yield

    if "SAVE_CI_JOB_TOKEN" in os.environ:
        os.environ["CI_JOB_TOKEN"] = os.environ["SAVE_CI_JOB_TOKEN"]
        os.environ.pop("SAVE_CI_JOB_TOKEN")


@pytest.fixture
def maybe_ci_job_token(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def clean_test_file():
    yield
    subprocess.run("git checkout -- tests/test_package_file.py", shell=True)


@pytest.fixture
def maybe_commit_branch(request):
    if request.param:
        MOCK_BRANCH_NAMES.append(COMMIT_BRANCH)
        yield
        MOCK_BRANCH_NAMES.remove(COMMIT_BRANCH)
    else:
        yield


@pytest.mark.parametrize(
    "possible_urls",
    [
        (
            "github.com/BlueBrain/brayns.git",
            "https://github.com/BlueBrain/brayns.git",
            "https://github.com/BlueBrain/brayns.git",
        ),
        (
            "bbpgitlab.epfl.ch/nse/brainbuilder.git",
            "ssh://bbpgitlab.epfl.ch/nse/brainbuilder.git",
            "https://gitlab-ci-token:test_token@bbpgitlab.epfl.ch/nse/brainbuilder.git",
        ),
    ],
)
@pytest.mark.parametrize("maybe_ci_job_token", ["ci_job_token", "no_ci_job_token"], indirect=True)
def test_build_git_url(bumper, possible_urls, maybe_ci_job_token):
    git_url = bumper.build_git_url(possible_urls[0])

    if "CI_JOB_TOKEN" in os.environ:
        assert git_url == possible_urls[2]
    else:
        assert git_url == possible_urls[1]


def test_get_source_lines(bumper):
    test_file = __file__
    with open(__file__, "r") as fp:
        test_lines = fp.readlines()
    source = bumper.get_source_lines(test_file)
    assert test_lines == source


def test_get_source_lines_nonexistent_file(bumper):
    source_file = "/tmp/this/file/does/not/exist"
    with pytest.raises(ValueError, match=f"Source file {source_file} does not exist"):
        bumper.get_source_lines(source_file)


@patch("src.bumper.Bumper.get_spack_package")
def test_get_latest_spack_version(mock_get_spack_package, bumper):
    spack_version = MagicMock()
    spack_version.string = "1.2.4"
    spack_package = MagicMock()
    spack_package.versions = {spack_version: {"tag": "v1.2.4"}}
    mock_get_spack_package.return_value = spack_package
    bumper.packages = {"test_package": {}}
    latest_spack_version = bumper.get_latest_spack_version("test_package")
    assert latest_spack_version == version.parse("1.2.4")


def test_get_latest_spack_version_no_tags(bumper):
    bumper.packages = {"test_package": {}}
    err_msg = (
        "Could not determine versions for test_package. Only tag-based versions are supported."
    )
    with pytest.raises(
        ValueError,
        match=err_msg,
    ):
        bumper.get_latest_spack_version("test_package")


@patch("src.bumper.subprocess")
@patch("src.bumper.logger")
@patch("src.bumper.Bumper.get_spack_package")
def test_get_latest_source_version(mock_get_spack_package, mock_logger, mock_subprocess, bumper):
    spack_package = MagicMock()
    spack_package.git = 'git = "ssh://git@bbpgitlab.epfl.ch/hpc/test_package.git"'
    mock_get_spack_package.return_value = spack_package
    command_result = MagicMock()
    command_result.stdout = textwrap.dedent(
        """\
        non-version
        v1.2.3
        test-v1.2.0
        test-v1.2.3
        test-1.2.4
        v1.2.5
        1.2.6
        """
    ).encode()
    mock_subprocess.run = MagicMock(return_value=command_result)
    bumper.packages = {
        "test_package": {"tag_regex": re.compile(r"test-v\d+\.\d+\.\d+"), "tag_strip": "test-"}
    }
    latest_source_tag, latest_source_version = bumper.get_latest_source_version("test_package")
    assert latest_source_tag == "test-v1.2.3"
    assert latest_source_version == version.parse("v1.2.3")
    mock_logger.debug.assert_called_with(
        "Version tags for test_package: ['test-v1.2.0', 'test-v1.2.3']"
    )


@patch("src.bumper.subprocess")
@patch("src.bumper.logger")
@patch("src.bumper.Bumper.get_spack_package")
def test_get_latest_source_version_no_tag_regex_specified(
    mock_get_spack_package, mock_logger, mock_subprocess, bumper
):
    spack_package = MagicMock()
    spack_package.git = 'git = "ssh://git@bbpgitlab.epfl.ch/hpc/test_package.git"'
    mock_get_spack_package.return_value = spack_package
    command_result = MagicMock()
    listed_tags = textwrap.dedent(
        """\
        non-version
        v1.2.3
        test-v1.2.3
        """
    )
    command_result.stdout = listed_tags.encode()
    mock_subprocess.run = MagicMock(return_value=command_result)
    bumper.packages = {"test_package": {}}
    retval = bumper.get_latest_source_version("test_package")
    assert retval == (None, None)
    mock_logger.critical.assert_called_with(
        f"No tag_regex specified for test_package. These are all the tags available: {listed_tags}"
    )


@patch("src.bumper.Bumper.get_spack_package")
def test_get_latest_source_version_no_git_repo(mock_get_spack_package, bumper):
    spack_package = MagicMock(spec=[])
    mock_get_spack_package.return_value = spack_package
    with pytest.raises(ValueError, match="Could not find git source for test_package"):
        bumper.get_latest_source_version("test_package")


@patch("src.bumper.Bumper.get_latest_spack_version")
@patch("src.bumper.Bumper.get_latest_source_version")
@patch("src.bumper.Bumper.add_spack_version")
@patch("src.bumper.Bumper.repo")
@patch("src.bumper.Bumper.commit")
@patch("src.bumper.Bumper.file_pull_request")
def test_process_packages_no_new_version(
    mock_file_pull_request,
    mock_commit,
    mock_repo,
    mock_add_spack_version,
    mock_get_latest_source_version,
    mock_get_latest_spack_version,
    bumper,
):
    mock_get_latest_spack_version.return_value = version.parse("1.2.3")
    mock_get_latest_source_version.return_value = "1.2.3", version.parse("1.2.3")
    bumper.packages = {"test_package": {}}
    bumper.process_packages()
    mock_get_latest_spack_version.assert_called_once()
    mock_get_latest_source_version.assert_called_once()
    mock_add_spack_version.assert_not_called()


@pytest.mark.parametrize(
    "mocks", [((None, None), version.parse("1.2.3")), (("v1.2.3", version.parse("1.2.3")), None)]
)
@patch("src.bumper.Bumper.get_latest_spack_version")
@patch("src.bumper.Bumper.get_latest_source_version")
@patch("src.bumper.Bumper.repo")
def test_process_packages_missing_versions(
    mock_repo, mock_get_latest_source_version, mock_get_latest_spack_version, mocks, bumper
):
    mock_get_latest_source_version.return_value = mocks[0]
    mock_get_latest_spack_version.return_value = mocks[1]
    bumper.packages = {"test_package": {}}
    with pytest.raises(
        RuntimeError,
        match=re.escape(
            "Some packages had either no spack or source control versions: ['test_package']"
        ),
    ):
        bumper.process_packages()


@patch("src.bumper.Bumper.get_latest_spack_version")
@patch("src.bumper.Bumper.get_latest_source_version")
@patch("src.bumper.Bumper.add_spack_version")
@patch("src.bumper.Bumper.commit")
@patch("src.bumper.Bumper.repo")
@patch("src.bumper.Bumper.file_pull_request")
def test_process_packages(
    mock_file_pull_request,
    mock_repo,
    mock_commit,
    mock_add_spack_version,
    mock_get_latest_source_version,
    mock_get_latest_spack_version,
    bumper,
):
    mock_get_latest_spack_version.return_value = version.parse("1.2.2")
    mock_get_latest_source_version.return_value = ("v1.2.3", version.parse("1.2.3"))
    bumper.packages = {"test_package": {}}
    bumper.process_packages()
    mock_add_spack_version.assert_called_once()
    mock_commit.assert_called_once()


def test_add_spack_version(bumper, clean_test_file):
    source_file = "tests/test_package_file.py"
    target_file = "tests/test_package_file_new_version.py"
    bumper.add_spack_version("test_package", "test-v1.5.0", version.parse("1.5.0"), source_file)

    with open(source_file, "r") as fp:
        source = fp.read()

    with open(target_file, "r") as fp:
        target = fp.read()

    assert source == target


class Index:
    def commit(self, *args, **kwargs):
        pass


class Repo:
    """
    Used to mock git.Repo
    """

    def __init__(self, *args, **kwargs):
        self.heads = [Ref(f"{branch_name}") for branch_name in MOCK_BRANCH_NAMES]
        self._remotes = []
        self.index = Index()
        self.push_success = kwargs.get("push_success", True)

    def remote(self, name="origin"):
        try:
            _remote = next(r for r in self._remotes if r.name == name)
        except StopIteration:
            _remote = Remote(name, push_success=self.push_success)
            self._remotes.append(_remote)

        return _remote

    def create_head(self, branch_name):
        self.heads.append(Ref(branch_name))


class Remote:
    """
    Used to mock git.Repo.remote
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.refs = [Ref(f"{self.name}/{branch_name}") for branch_name in MOCK_BRANCH_NAMES]
        self.push_success = kwargs.get("push_success", True)

    def push(self, *args, **kwargs):
        return [Result(success=self.push_success)]

    def __repr__(self):
        return f"Remote: <{self.name}>"


class Ref:
    """
    Used to mock both ref and head, as we need the same functionality
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def checkout(self):
        pass

    def __repr__(self):
        return f"<{self.name}>"


class Result:
    def __init__(self, success=True):
        self.FAST_FORWARD = 256
        self.NEW_HEAD = 2
        self.REMOTE_REJECTED = 16
        self.ERROR = 1024

        self.flags = 0

        if success:
            self.flags |= self.FAST_FORWARD
        else:
            self.flags |= self.ERROR
            self.flags |= self.REMOTE_REJECTED
            self.summary = "Remote rejected"


@pytest.mark.parametrize("maybe_commit_branch", [True, False], indirect=True)
def test_checkout_branch(maybe_commit_branch, bumper):
    mock_repo = Repo()
    repo = MagicMock(wraps=mock_repo)
    repo.heads = mock_repo.heads

    bumper.checkout_branch(repo, COMMIT_BRANCH)
    if COMMIT_BRANCH in MOCK_BRANCH_NAMES:
        repo.create_head.assert_not_called()
    else:
        repo.create_head.assert_called_with(COMMIT_BRANCH)


@patch("src.bumper.Bumper.checkout_branch")
@patch("src.bumper.Bumper.repo")
def test_commit(mock_repo, mock_checkout_branch, bumper):
    fake_repo = Repo()
    repo = MagicMock(wraps=fake_repo)
    repo.heads = mock_repo.heads
    mock_repo.return_value = repo

    bumper.commit(["test_package"])
    repo.index.commit.assert_called_once()


@patch("src.bumper.Bumper.checkout_branch")
@patch("src.bumper.Bumper.repo")
def test_failed_push(mock_repo, mock_checkout_branch, bumper):
    fake_repo = Repo(push_success=False)
    repo = MagicMock(wraps=fake_repo)
    repo.heads = mock_repo.heads
    mock_repo.return_value = repo

    with pytest.raises(RuntimeError, match="Undesirable push result: 1040 - Remote rejected"):
        bumper.commit(["test_package"])


@patch("src.bumper.Bumper.repo")
@patch("src.bumper.requests")
@pytest.mark.parametrize("already_exists", [True, False])
def test_file_pull_request(mock_requests, mock_repo, github_api_key, bumper, already_exists):
    fake_repo = Repo(push_success=False)
    repo = MagicMock(wraps=fake_repo)
    repo.heads = mock_repo.heads
    mock_repo.return_value = repo
    mock_session = MagicMock()
    mock_get = MagicMock()
    if already_exists:
        pull_requests = [
            {"_links": {"self": {"href": "https://github.com/bluebrain/spack/pulls/1"}}}
        ]
    else:
        pull_requests = []
    mock_get.json.return_value = pull_requests
    mock_session.get.return_value = mock_get
    mock_requests.Session.return_value = mock_session

    bumper.file_pull_request(["test_package", "another_package"])

    if already_exists:
        mock_session.post.assert_not_called()
    else:
        mock_session.post.assert_called_once()
        mock_session.post.assert_called_with(
            "https://api.github.com/repos/bluebrain/spack/pulls",
            json={
                "title": "test_package, another_package: new releases",
                "body": "Bumper found new releases, please check carefully and add new "
                "dependencies, remove obsolete dependencies, ...",
                "head": COMMIT_BRANCH,
                "base": "develop",
            },
        )


@patch("src.bumper.Repo")
@pytest.mark.parametrize("remote_exists", [True, False])
def test_repo(mock_repo, bumper, github_api_key, remote_exists):
    repo = MagicMock()
    mock_repo.return_value = repo
    if remote_exists:
        repo.remote.return_value = Remote("github")
    else:
        repo.remote.side_effect = ValueError("No such remote")
        bumper_repo = bumper.repo()

    bumper_repo = bumper.repo()
    assert bumper_repo == repo

    if remote_exists:
        repo.create_remote.assert_not_called()
    else:
        repo.create_remote.assert_called_once()
        repo.create_remote.assert_called_with(
            "github", "https://bbp-hpcteam:${GITHUB_API_KEY}@github.com/bluebrain/spack"
        )
