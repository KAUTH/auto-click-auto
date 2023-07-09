class AutoClickAutoError(Exception):
    """Custom exception with an error message for `auto_click_auto`."""

    def __init__(self, message):
        super().__init__(message)


class ShellConfigurationFileNotFoundError(AutoClickAutoError):
    """Exception raised when the shell configuration file does not exist."""

    pass


class ShellTypeNotSupportedError(AutoClickAutoError):
    """Exception raised when the shell type is not supported."""

    pass
