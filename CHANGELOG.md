# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

- Add support for more sites


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
