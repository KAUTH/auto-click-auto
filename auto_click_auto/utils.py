import os
from typing import List, Optional

from auto_click_auto.constants import ShellType
from auto_click_auto.exceptions import (
    ShellConfigurationFileNotFoundError,
    ShellEnvVarNotFoundError,
    ShellTypeNotSupportedError,
)


def create_file(file_path: str) -> None:
    """
    Check if the file and the directories of the given file path exist and if
    not create them.

    :param file_path: The path of the file the check and creation is done for.
    :return: `None`
    """

    if not os.path.exists(file_path):
        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            # Recursive directory creation
            os.makedirs(directory, exist_ok=True)

        try:
            # Open for exclusive creation
            with open(file_path, 'x'):
                pass

        # To avoid race conditions we handle here as well whether the file
        # exists.
        except FileExistsError:
            pass


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


def remove_shell_configuration(
    shell_config_file: str,
    config_string: str,
    verbose: Optional[bool] = False
) -> None:
    """
    Remove the given string from the specified shell configuration file.
    This function is used to clean files from configuration added by
    `auto-click-auto`.

    :param shell_config_file: The shell configuration file to remove the string
    from.
    :param config_string: The desired configuration string to be removed. This
    string will be split based on the newline characters and used to match
    them in their order. The last splitted text will be searched for with and
    without newline.
    :param verbose: `True` to print whether the configuration is removed from
    the file, `False` otherwise.
    """

    delimiter = "\n"
    lines_to_remove = config_string.split(delimiter)
    number_lines_to_remove = len(lines_to_remove)

    if number_lines_to_remove == 0:
        return None

    try:
        strings_in_file = check_strings_in_file(
            file_path=shell_config_file, search_strings=lines_to_remove
        )
    except ShellConfigurationFileNotFoundError as err:
        if verbose is True:
            print(err)

        return None

    # Check if any of the strings exist, independent of order, and exit early
    # if not.
    if strings_in_file is False:
        return None

    with open(shell_config_file) as file:
        lines = file.readlines()

    lines_to_remove_with_delimeter = [
        line + delimiter for line in lines_to_remove
    ]
    # Keep the delimeter for the last splitted part.
    lines_to_remove_ends_without_delimeter = [
        line + delimiter
        if index < (number_lines_to_remove - 1) else line
        for index, line in enumerate(lines_to_remove)
    ]

    new_lines = [""]
    i = 0

    while i < len(lines):
        if (
            lines[i:i + number_lines_to_remove] ==
            lines_to_remove_with_delimeter
            or
            lines[i:i + number_lines_to_remove] ==
            lines_to_remove_ends_without_delimeter
        ):
            # Skip the lines that match the sequence.
            i += number_lines_to_remove
            print(
                "Removing old tab autocomplete configuration from " +
                f"{shell_config_file} ..."
            )
        else:
            new_lines.append(lines[i])
            i += 1

    if len(new_lines) > 0:
        with open(shell_config_file, 'w') as file:
            file.writelines(new_lines)


def add_shell_configuration(
    shell_config_file: str,
    config_string: str,
    verbose: Optional[bool] = False,
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

        with open(shell_config_file, "a") as file:
            file.write(
                "\n\n# Shell completion configuration for the Click Python " +
                "package"
            )
            # Source the file in the shell config file
            file.write(f"\n{config_string}")

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
    """
    Attempt to detect the shell type using the `SHELL` environment variable.

    :raise ShellEnvVarNotFoundError: When the `SHELL` environment variable is
    not set in the system.
    :raise ShellTypeNotSupportedError: When the shell value returned from the
    `SHELL` environment variable does not belong to one of the supported
    shells.
    """

    try:
        shell_env_var = os.environ["SHELL"]

    except KeyError:
        raise ShellEnvVarNotFoundError(
            "Could not infer the shell type from the 'SHELL' environment "
            "variable."
        )

    try:
        shell_value = shell_env_var.split("/")[-1]
        return ShellType(shell_value)

    except ValueError:
        raise ShellTypeNotSupportedError(
            f"{shell_value} is not one of the supported shell types "
            f"({ShellType.get_all_values()})."
        )
