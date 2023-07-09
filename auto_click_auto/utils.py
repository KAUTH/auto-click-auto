import os
from typing import List, Optional

from auto_click_auto.constants import ShellType
from auto_click_auto.exceptions import (
    ShellConfigurationFileNotFoundError,
    ShellTypeNotSupportedError,
)


def check_strings_in_file(file_path: str, search_strings: List[str]) -> bool:
    """
    Check if the given search strings are in the specified file.

    :param file_path: The path of the file the search is done for.
    :param search_strings: The strings that are searched for in the file.
    :return: `True`, if any of the strings are found in the file, and `False`
    otherwise.
    """

    try:
        with open(file_path) as file:
            return any(
                search_string in line for line in file
                for search_string in search_strings
            )

    except FileNotFoundError:
        raise ShellConfigurationFileNotFoundError(
            f"The {file_path} configuration file does not exist."
        )


def add_shell_configuration(
        shell_config_file: str,
        config_string: str,
        verbose: Optional[bool] = False
) -> None:
    """
    Add the given configuration in the specified shell configuration file, if
    the string is not already present.

    :param shell_config_file: The shell configuration file to add the string
    to.
    :param config_string: The desired configuration string.
    :param verbose: `True` to print whether the configuration is already in the
    file, `False` otherwise.
    """

    try:
        string_in_file = check_strings_in_file(
                file_path=shell_config_file, search_strings=[config_string]
        )
    except ShellConfigurationFileNotFoundError as err:
        if verbose is True:
            print(err)

        return None

    if not string_in_file:
        print(
            f"Adding tab autocomplete configuration in {shell_config_file} ..."
        )

        os.system(
            "echo '# Shell completion configuration for the Click Python "
            f"package' >> {shell_config_file}"
        )
        # Source the file in the shell config file
        os.system(f"echo '{config_string}' >> {shell_config_file}")

        print(
            "Restart or create a new shell session for the changes to take "
            "effect."
        )

    elif string_in_file and verbose is True:
        print(
            "Tab autocomplete configuration already setup in "
            f"{shell_config_file}."
        )


def detect_shell() -> ShellType:
    shell_env_var = os.environ["SHELL"]

    try:
        shell_value = shell_env_var.split("/")[-1]
        return ShellType(shell_value)

    except ValueError:
        raise ShellTypeNotSupportedError(
            f"{shell_value} is not one of the supported shell types "
            f"({ShellType.get_all_values()})."
        )
