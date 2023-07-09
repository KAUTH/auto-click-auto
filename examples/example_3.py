# Adjusted example of a simple Click program, as given in
# https://click.palletsprojects.com/en/8.1.x/#.

# In this case, we make shell completion a command (or subcommand of a
# group).
# Run: `python3 example_3.py config shell-completion`

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


if __name__ == '__main__':
    cli()
