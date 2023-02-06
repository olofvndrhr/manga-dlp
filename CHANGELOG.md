# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add support for more sites

## [2.2.19] - 2023-02-XX

### Added

- First version of the chapter cache (very basic functionality)

### Changed

- Simplified chapter download loop

## [2.2.18] - 2023-01-21

### Fixed

- Fixed manga titles on non english language
- Fixed title & filename fixing to not use `ascii` but `uft8`

### Added

- Fallback title to english of none was found in requested language
- More debug logs
- More tests

### Changed

- Now uses the first found alt-title. Before it was the last
- Removed `sys.exit` in the api

## [2.2.17] - 2023-01-15

### Fixed

- Set a timeout of 10 seconds for the api requests

### Added

- `--name-format` and `--name-format-none` flags to add a custom naming scheme for the downloaded files. See
  docs: https://manga-dlp.ivn.sh/download/
- More debug log messages
- More tests for the custom naming scheme
- More type hints

### Changed

- Make `--format` a `click.Choice` option
- In the `--format` option the leading dot is now invalid. `--format .cbz` -> `--format cbz`
- Changed empty values from the api from None to an empty string
- Minor code readability improvements

## [2.2.16] - 2022-12-30

### Fixed

- Log level is now fixed and should not default to 0
- Docker schedule should now work again

### Changed

- Integrate logging logs to loguru via custom sink
- Simplify docker shell scripts

## [2.2.15] - 2022-12-29

### Added

- `--warn` and `--loglevel` flags

### Removed

- Remove `--lean` and `--verbose` flags and remove custom log levels

### Changed

- Move from standard library logging to [loguru](https://loguru.readthedocs.io/en/stable/index.html)
- Move from standard library argparse to [click](https://click.palletsprojects.com/en/8.1.x/)

## [2.2.14] - 2022-10-06

### Changed

- Changed logging format to ISO 8601
- Small logging corrections

## [2.2.13] - 2022-08-15

### Added

- Option to run custom hooks before and after each chapter/manga download
- _Tests for the new hooks_
- _Docs for the new hooks_
- _Tests for mkdocs generation_

### Changed

- Verbose and Debug logging now have a space as a seperator between log level-name and log-level
- APIs now have an attribute with their name (for the hooks) - `api.api_name`
- Docs moved to Cloudflare pages (generated with mkdocs)

## [2.1.12] - 2022-07-25

### Fixed

- Image publishing with `hatch` on pypi should now work again
- The schedule fixer for the new `.sh` schedule should now work correctly

### Added

- More CI tests: `pylint`, `pylama` and `autoflake`
- New function in `get_release_notes.sh` to get the latest version
- Docstrings for `MangaDLP` and the api module `Mangadex`

### Changed

- CI workflow is now faster and runs natively on arm64 (before it was buildx/emulation)
- `Pylint`/`pylama` code improvements
- Version management is now done with `hatch` (in `__about__.py`)

## [2.1.11] - 2022-07-18

### Fixed

- The `--read` option now filters empty lines, so it will not generate an error anymore
- An error which was caused by the interactive input method when you did not specify a chapter or to list them
- Some typos

### Added

- Options to configure the default schedule in the docker container via environment variables
- Section the the docker [README.md](docker/README.md) for the new environment variables
- `autoflake` test in `justfile`
- Some more things which get logged

### Changed

- **BREAKING**: renamed the default schedule from `daily` to `daily.sh`. Don't forget to fix your bind-mounts to
  overwrite
  the default schedule
- Added the `.sh` suffix to the s6 init scripts for better compatibility
- Adjusted the new logging implementation. It shows now more info about the module the log is from, and some other
  improvements

## [2.1.10] - 2022-07-14

### Fixed

- Removed some unused files

### Added

- `logger.py` for all log related settings and functions

### Changed

- Logging of output. The script now uses the `logging` library

## [2.1.9] - 2022-06-26

### Fixed

- Timeouts in tests, due to api limitations. Now added a wait time between tests
- Pytest path

### Added

- `--lean` flag for less output
- [justfile](https://github.com/casey/just) for setting up a dev environment and testing the code
- [asdf](https://github.com/asdf-vm/asdf) for version management
- Dev requirements in [contrib/requirements_dev.txt](contrib/requirements_dev.txt)
- `README` in [contrib](contrib)

### Changed

- Handling of verbosity and logging. Now there are 4 types of verbosity: `normal`, `lean`, `verbose` and `debug`
- CI/CD pipeline for testing and releases
- Coverage testing now also done with `tox`
- Default verbosity of docker container is now `--lean`
- Reorganised [pyproject.toml](pyproject.toml)

## [2.1.8] - 2022-06-22

### Fixed

- Interactive input

## [2.1.7] - 2022-06-22

### Added

- tox version testing
- New pre-release tests
- Build info's with hatch
- [Pypi](https://pypi.org/project/manga-dlp/) build with hatch
- Pypi section in `README.md`
- [Snyk](https://app.snyk.io/org/olofvndrhr-t6h/project/aae9609d-a4e4-41f8-b1ac-f2561b2ad4e3) test results
  in `README.md`

### Changed

- Moved code from `manga-dlp.py` to `input.py` for uniformity
- The default entrypoint is now `mangadlp.input:main`

## [2.1.6] - 2022-06-21

### Fixed

- Docker labels are now working
- Global variables are now fully uppercase
- Some errors with static types

### Added

- bump2version config for releases
- More tests with: `mypy` and `isort`
- New issue templates

### Changed

- Release workflow now is based on configuration files
- Switched from `setup.py` to `pyproject.toml`
- `README.md` now has sorted badges
- Imports are now sorted with `isort`
- Static types are now checked with `mypy`
- Release note generation is now simplified

## [2.1.5] - 2022-06-18

### Fixed

- Image names now have a suffix, as some comic readers have problems with no
  suffix [fixes issue #2]

### Added

- `--format` section in the README

## [2.1.4] - 2022-05-29

### Fixed

- Docker container now works again
- Fixed cron in docker container

### Changed

- Docker container scheduling is now more practical

## [2.1.3] - 2022-05-29

### Fixed

- Error-chapters and skipped-chapters list are now shown again
- The Interactive input version now matches `--version`

### Added

- Ability to list chapters with interactive input

### Changed

- Replace `exit()` with `sys.exit()`
- Renamed class methods to not look like dunder methods
- Script execution moved from `os.system()` to `subprocess.call()`

## [2.1.2] - 2022-05-20

### Fixed

- List chapters when none were specified
- Typos

### Added

- Ability to download whole volumes

### Changed

- Moved processing of list with links to input.py
- Updated README for volume and chapter selection

## [2.1.1] - 2022-05-18

### Fixed

- Progress bar on verbose output
- Sonarqube link for CI
- A few typos
- Removed unnecessary escapes from file rename regex

### Added

- API template

### Changed

- Updated docker baseimage
- Rewrote app.py to a class

## [2.1.0] - 2022-05-16

### Fixed

- Detection of files. Now it will skip them again

### Added

- Ability to save the chapters as pdf (only on amd64/x86)
- New output formats: rar, zip
- Progress bar to show image download
- Interactive input if no command line flags are given
- Better KeyboardInterrupt handling
- Better error handling
- Removed duplicate code

### Changed

- How the variables are used inside the script
- Variables have now the same name as in other scripts (mostly)
- Better retrying when a task fails

## [2.0.8] - 2022-05-13

### Changed

- Rewrote parts of script to be easier to maintain
- Moved the input script to the base folder
- Moved all arguments to a class
- Docker container creation

## [2.0.7] - 2022-05-13

### Changed

- Changed CI/CD Platform from Drone-CI to Woodpecker-CI
- Release title is now only the version

## [2.0.6] - 2022-05-11

### Fixed

- Filenames on windows (ntfs). Removed double quote from file and folder names

## [2.0.5] - 2022-05-11

### Fixed

- Better error handling on "KeyboardInterrupt"
- Release notes now fixed

### Added

- New test cases

## [2.0.4] - 2022-05-10

### Added

- New test cases for more coverage
- Github release
- Updated docker baseimage

## [2.0.3] - 2022-05-10

### Fixed

- Test cases now work again
- Sonarqube settings

### Added

- Coverage report in sonarqube
- Gitea release

## [2.0.2] - 2022-05-09

### Fixed

- Restart failed api requests
- Added wait time for image gathering, as to stop api rate limiting from mangadex
- "--wait" options now works properly again

## [2.0.1] - 2022-05-09

### Fixed

- Regex for removing illegal characters in the filenames now doesn't remove quotes
- Updated docker baseimage and fixed the mangadlp tag in it
- Update license for 2022

### Added

- Quick start section in README
- Preperation for pypi

## [2.0.0] - 2022-05-09

### Fixed

- Support for new mangadex api

### Changed

- Code is now formatted with [black](https://github.com/psf/black)
- Now also supports just the uuid for managex (not a full link)
