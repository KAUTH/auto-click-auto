# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add tests for QA

## [0.1.0-alpha.2] - 2023-07-17

### Changed

- Function `enable_click_shell_completion` now has the `shells` positional argument set by default to `None`

## [0.1.0-alpha.1] - 2023-07-17

### Added

- Function `enable_click_shell_completion` to automatically add autocomplete support
for the Bash, Zsh, and Fish shells
- Decorator `enable_click_shell_completion_option` to easily add an option to Click commands for autocomplete
support