![PyPI - Downloads](https://img.shields.io/pypi/dm/auto-click-auto)
[![Functional Tests](https://github.com/KAUTH/auto-click-auto/workflows/Functional%20tests/badge.svg)](https://github.com/KAUTH/auto-click-auto/actions/workflows/functional-tests.yml?query=workflow%3A%22Functional+tests%22)
[![pypi](https://img.shields.io/pypi/v/auto-click-auto.svg)](https://pypi.python.org/pypi/auto-click-auto)
[![GitHub license](https://img.shields.io/github/license/KAUTH/auto-click-auto)](https://github.com/KAUTH/auto-click-auto/blob/master/LICENSE)

# auto-click-auto
Automatically enable tab autocompletion for shells in Click CLI applications.

`auto-click-auto` is a small Python library that is used to quickly and easily add tab shell completion support for
_Bash_ (version 4.4 and up), _Zsh_, and _Fish_, for [Click](https://click.palletsprojects.com/en/8.1.x/#) CLI programs.

## Installation
```commandline
pip install auto-click-auto
```

## Usage
There are two functions that `auto-click-auto` makes available: `enable_click_shell_completion` (general use)
and `enable_click_shell_completion_option` (to be used as a decorator).

In the function docstrings, you can find a detailed analysis of the available parameters and their use.

`auto-click-auto` will print the relative output when a shell completion is activated for the first time and can be
set to an extra verbosity if you want to display information about already configured systems or debug.

Here are some typical ways to enable autocompletion with `auto-click-auto`:

1) **Check on every run of the CLI program if autocompletion is configured and enable it in case that it is not**

This way you can seamlessly enable shell autocompletion without the user having to run any extra commands.

Example:
```python
import click

from auto_click_auto import enable_click_shell_completion
from auto_click_auto.constants import ShellType


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

    enable_click_shell_completion(
        program_name="example-1", shells={ShellType.BASH, ShellType.FISH},
    )
```

2) **Make shell completion a Click command option**

Example:
```python
import click

from auto_click_auto import enable_click_shell_completion_option


@click.command()
@enable_click_shell_completion_option(program_name="example-2")
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
```

3) **Make shell completion a command (or subcommand of a group)**

This implementation option might be useful if you already have a "configuration" command in your CLI program.

Example:
```python
import click

from auto_click_auto import enable_click_shell_completion
from auto_click_auto.constants import ShellType


@click.group()
def cli():
    """Simple CLI program."""
    pass


@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple command that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@cli.group()
def config():
    """Program configuration."""
    pass


@config.command()
def shell_completion():
    """Activate shell completion for this program."""
    enable_click_shell_completion(
        program_name="example-3",
        shells={ShellType.BASH, ShellType.FISH, ShellType.ZSH},
        verbose=True,
    )
```

## Examples
To run the examples, fork this repository and follow the instructions at
https://github.com/KAUTH/auto-click-auto/tree/main/examples.

## Implementation
`auto-click-auto` enables tab autocompletion based on [Click's documentation](https://click.palletsprojects.com/en/8.1.x/shell-completion/).

## Name
`auto-click-auto`, as the name suggests, _auto_matically provides tab _auto_completion support for _Click_ CLI
applications.

## Why `auto-click-auto`?
In the search for other tools that enable shell completion for Click we come across a lot of repositories with example
code or gists. This adds a bit of complexity to adapting the code and adding it to our use case quickly.

A very nice tool is [`click-completion`](https://github.com/click-contrib/click-completion), which provides enhanced
completion for Click. `click-completion`:
- Adds automatic completion support for fish, Zsh, Bash and PowerShell
- Currently, has one extra dependency, in addition to Click
- Can customize the completion

However, it is important to note that this repository could be duplicating currently integrated Click functionality and
might need to be archived. You can monitor the issue
[here](https://github.com/click-contrib/click-completion/issues/41).

In summary, `auto-click-auto`:
- Has one specific purpose, it "automatically" enables shell completion for Click programs
- Does not have any 3rd party dependencies, besides Click
- Provides an option for seamless enabling of the shell completion
- Comes ready with ways to add shell completion as a command option or subcommand
- Has simple examples of how to quickly use the library

## Changelog
https://github.com/KAUTH/auto-click-auto/blob/main/CHANGELOG.md

## Contributing
You can always submit a PR if you want to suggest improvements or fix issues.
Check out the open issues at https://github.com/KAUTH/auto-click-auto/issues.
