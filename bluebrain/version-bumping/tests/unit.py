import os
import re
import textwrap
from unittest.mock import MagicMock, patch

import pytest
from packaging import version
from src.bumper import Bumper


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
def test_process_packages_no_new_version(
    mock_add_spack_version, mock_get_latest_source_version, mock_get_latest_spack_version, bumper
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
def test_process_packages_missing_versions(
    mock_get_latest_source_version, mock_get_latest_spack_version, mocks, bumper
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
def test_process_packages(mock_add_spack_version, mock_get_latest_source_version, mock_get_latest_spack_version, bumper):
    mock_get_latest_spack_version.return_value = version.parse("1.2.2")
    mock_get_latest_source_version.return_value = ("v1.2.3", version.parse("1.2.3"))
    bumper.packages = {"test_package": {}}
    bumper.process_packages()
    mock_add_spack_version.assert_called_once()
