# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [0.2.0] - 2025-01-12
### Added
- Full VOD download via `--full` flag.
- 'Single' video downloads via `-s` flag, be it full VOD downloads or section downloads.
- 'Bulk' video downloads via offset file, be it full VOD downloads or section downloads. Downloads are concurrent by default.

### Changed
- Offset file is not mandatory anymore, instead it is a flag via `-o` or `--offsetfile`

## [0.1.0] - 2025-01-09
#### Added
- `Offset` and `dl` folder
- Readme
- Changelog