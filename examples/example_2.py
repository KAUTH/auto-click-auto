# Adjusted example of a simple Click program, as given in
# https://click.palletsprojects.com/en/8.1.x/#.

# In this case, we make shell completion an option, `--autocomplete` by
# default.
# Run: `python3 example_2.py --autocomplete`

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


if __name__ == '__main__':
    hello()
