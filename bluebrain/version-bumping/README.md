# Automatic version bumping

For some packages we want the spack recipe to be updated automatically when a new version is released.
While the script is rather simplistic and adds only the new version number, it will at the very least alert a human that something needs to happen for these packages.

It gets run in the scheduled gitlab pipeline (once a month at the time of writing).

## Configuration

Configuration is done within the bumper script itself. Any package you want to bump automatically should be added to the `PACKAGES` directory (line 35 at the time of writing).

The main key is the package name as it appears in Spack.
The value is another dictionary, which can take two keys:
  * `tag_regex` is required and describes the pattern a tag should follow in the package's git repository to be considered a released version.
    *YOU SHOULD NOT USE GROUPS IN THIS REGEX*
    It takes the format `re.compile(r"<regex>")`
  * `tag_strip` is optional and specifies a string to strip from the repository tag when converting to a `packaging.version` object. Example: brainbuilder tags take the format `brainbuilder-v1.2.3`, `packaging.version` needs `v1.2.3` (or even just `1.2.3`), so `tag_strip` can be set to `brainbuilder-`.

`COMMIT_BRANCH` and `VERSION_BUMPER_EMAIL` can be changed if necessary. It is recommended to leave the other variables alone.

## Testing

When making changes, please make sure to update the unit tests as well! They haven't been configured to run in gitlab, but are present to provide at least a small measure of confidence when developing.

A `requirements-test.txt` file has been provided for dependency installation.

Once you've created your virtualenv, activated it, and installed the dependencies, you can use the following command from within the `bluebrain/version-bumping` directory to run the tests:

`coverage run --source=src -m pytest -vs tests/`

This will also provide you with a .coverage file that can be used by the coveragepy vim plugin, or you can use `coverage report` to show code coverage.
