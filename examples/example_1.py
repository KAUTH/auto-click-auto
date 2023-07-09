# Adjusted example of a simple Click program, as given in
# https://click.palletsprojects.com/en/8.1.x/#.

# In this case, we try to enable shell completion on every run.
# Run: `python3 example_1.py`

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


if __name__ == '__main__':
    hello()
