import functools
import os
import re
import subprocess
import textwrap
from unittest.mock import MagicMock, patch

import pytest
from packaging import version
from src.bumper import COMMIT_BRANCH, Bumper

MOCK_BRANCH_NAMES = ["some-branch", "some-other-branch", "yet-another-branch"]


@pytest.fixture
def bumper():
    return Bumper()


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
        source = bumper.get_source_lines(source_file)


def test_get_latest_spack_version(bumper):
    bumper.packages = {"test_package": {}}
    latest_spack_version = bumper.get_latest_spack_version(
        "test_package", "tests/test_package_file.py"
    )
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
        latest_spack_version = bumper.get_latest_spack_version(
            "test_package", "tests/test_package_no_tag_versions.py"
        )


@patch(
    "src.bumper.Bumper.get_source_lines",
    return_value=['git = "ssh://git@bbpgitlab.epfl.ch/hpc/test_package.git"'],
)
@patch("src.bumper.subprocess")
@patch("src.bumper.logger")
def test_get_latest_source_version(mock_logger, mock_subprocess, mock_get_source_lines, bumper):
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
    latest_source_tag, latest_source_version = bumper.get_latest_source_version(
        "test_package", "tests/test_package_file.py"
    )
    assert latest_source_tag == "test-v1.2.3"
    assert latest_source_version == version.parse("v1.2.3")
    mock_logger.debug.assert_called_with(
        "Version tags for test_package: ['test-v1.2.0', 'test-v1.2.3']"
    )


@patch(
    "src.bumper.Bumper.get_source_lines",
    return_value=['git = "ssh://git@bbpgitlab.epfl.ch/hpc/test_package.git"'],
)
@patch("src.bumper.subprocess")
@patch("src.bumper.logger")
def test_get_latest_source_version_no_tag_regex_specified(
    mock_logger, mock_subprocess, mock_get_source_lines, bumper
):
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
    retval = bumper.get_latest_source_version("test_package", "tests/test_package_file.py")
    assert retval == (None, None)
    mock_logger.critical.assert_called_with(
        f"No tag_regex specified for test_package. These are all the tags available: {listed_tags}"
    )


def test_get_latest_source_version_no_git_repo(bumper):
    with pytest.raises(ValueError, match="Could not find git source for test_package"):
        bumper.get_latest_source_version("test_package", "tests/test_package_file.py")


@patch("src.bumper.Bumper.get_latest_spack_version")
@patch("src.bumper.Bumper.get_latest_source_version")
@patch("src.bumper.Bumper.add_spack_version")
@patch("src.bumper.Bumper.get_repo")
@patch("src.bumper.Bumper.commit")
def test_process_packages_no_new_version(
    mock_commit,
    mock_get_repo,
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
@patch("src.bumper.Bumper.get_repo")
def test_process_packages_missing_versions(
    mock_get_repo, mock_get_latest_source_version, mock_get_latest_spack_version, mocks, bumper
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
@patch("src.bumper.Bumper.get_repo")
def test_process_packages(
    mock_get_repo,
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
        self._remote = None
        self.index = Index()

    def remote(self):
        if not self._remote:
            self._remote = Remote("origin")

        return self._remote

    def create_head(self, branch_name):
        self.heads.append(Ref(branch_name))


class Remote:
    """
    Used to mock git.Repo.remote
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.refs = [Ref(f"{self.name}/{branch_name}") for branch_name in MOCK_BRANCH_NAMES]

    def push(self, *args, **kwargs):
        pass

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
def test_commit(mock_checkout_branch, bumper):
    mock_repo = Repo()
    repo = MagicMock(wraps=mock_repo)
    repo.heads = mock_repo.heads

    bumper.commit(repo)
    repo.index.commit.assert_called_once()
