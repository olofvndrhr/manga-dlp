# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add support for more sites

## [2.1.5] - 2022-06-17

### Fixed

- Image names now have a suffix, as some comic readers have problems with no suffix

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
