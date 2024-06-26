# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.5] - 2024-06-26

### Changed

- Explicitly export `enable_click_shell_completion` and `enable_click_shell_completion_option`
functions. This way, we comply with the "no-implicit-reexport" strictness in type checking
when importing these functions (https://github.com/KAUTH/auto-click-auto/pull/14)
Functionality has not changed.

## [0.1.4] - 2024-01-15

### Added

- Parametrized functional testing for Ubuntu environments for Python 3.9, 3.10, 3.11 (https://github.com/KAUTH/auto-click-auto/pull/10)

### Fixed

- Autocomplete did not work properly for Python 3.11 environments.
Users can manually delete incorrectly created fish configuration file
~/.config/fish/completions/{program_name}.ShellType.FISH, created from this
bug (https://github.com/KAUTH/auto-click-auto/issues/9)

## [0.1.3] - 2023-12-28

### Fixed

- `auto-click-auto` now adds a check in the shell configuration for whether the program is
executable. This will keep shell sessions free from "command not found" errors when
the autocompleted program is not installed system-wide. This fix also removes old
configuration from the relevant shell config files (https://github.com/KAUTH/auto-click-auto/issues/12)

## [0.1.2] - 2023-12-17

### Fixed

- To avoid race conditions (e.g., when running parallel tests) we handle whether a file
exists at the proper moment so that we don't crash when attempting to create configuration
files that already exist (#11)

## [0.1.1] - 2023-08-31

### Fixed

- MacOS not always supported OS issue (#4)

## [0.1.0] - 2023-08-31

### Added

- Functional testing for Ubuntu environments

### Fixed

- Program names with "-" were not correctly added to shell autocomplete configurations
- click's [fix](https://github.com/pallets/click/issues/2567) for fish autocomplete not working on click 8.1.4

## [0.1.0-alpha.5] - 2023-08-02

### Added

- The fish configuration file for custom completions, ~/.config/fish/completions/{program_name}.fish
(notice it's specific to the program name), is created if it doesn't already exist. ~/.bashrc and
~/.zshrc configuration files, which are used to set up shell completion, are generic and we can assume
the users have already created them.

## [0.1.0-alpha.4] - 2023-07-26

### Fixed

- Handle exception when `auto-click-auto` cannot infer the shell type from the `SHELL` environment variable

## [0.1.0-alpha.3] - 2023-07-17

### Added

- Package typing information

## [0.1.0-alpha.2] - 2023-07-17

### Changed

- Function `enable_click_shell_completion` now has the `shells` positional argument set by default to `None`

## [0.1.0-alpha.1] - 2023-07-17

### Added

- Function `enable_click_shell_completion` to automatically add autocomplete support
for the Bash, Zsh, and Fish shells
- Decorator `enable_click_shell_completion_option` to easily add an option to Click commands for autocomplete
support