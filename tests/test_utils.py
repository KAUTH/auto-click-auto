import os

import pytest

from auto_click_auto.utils import remove_shell_configuration


@pytest.fixture
def shell_config_file(tmp_path):
    config_file = tmp_path / ".zshrc"
    config_file.touch()
    return str(config_file)


class TestRemoveShellConfiguration:
    def test_removes_exact_matching_block(self, shell_config_file):
        with open(shell_config_file, "w") as file:
            file.write("keep1\nREMOVE_A\nREMOVE_B\nkeep2\n")

        remove_shell_configuration(shell_config_file, "REMOVE_A\nREMOVE_B")

        with open(shell_config_file) as file:
            assert file.read() == "keep1\nkeep2\n"

    def test_does_not_rewrite_file_on_substring_only_match(
        self, shell_config_file
    ):
        # Issue #16: Used to match this line as a substring of
        # the guarded command, even though it is not an exact line match, and
        # the file would be rewritten (and corrupted) regardless.
        original_content = (
            "some line\n"
            'command -v foo > /dev/null 2>&1 && eval "$(_FLOW_COMPLETE='
            'bar)"\n'
            "other\n"
        )
        with open(shell_config_file, "w") as file:
            file.write(original_content)

        os.chmod(shell_config_file, 0o444)
        try:
            remove_shell_configuration(
                shell_config_file, 'eval "$(_FLOW_COMPLETE=bar)"'
            )
        finally:
            os.chmod(shell_config_file, 0o644)

        with open(shell_config_file) as file:
            assert file.read() == original_content

    def test_does_not_prepend_blank_line_when_nothing_removed(
        self, shell_config_file
    ):
        original_content = "keep1\nkeep2\n"
        with open(shell_config_file, "w") as file:
            file.write(original_content)

        remove_shell_configuration(shell_config_file, "NOT_PRESENT")

        with open(shell_config_file) as file:
            assert file.read() == original_content

    def test_missing_file_does_not_raise(self, tmp_path):
        missing_file = str(tmp_path / "does-not-exist")

        remove_shell_configuration(missing_file, "some string")

    def test_missing_file_verbose_prints_message(self, tmp_path, capsys):
        missing_file = str(tmp_path / "does-not-exist")

        remove_shell_configuration(missing_file, "some string", verbose=True)

        assert missing_file in capsys.readouterr().out

    def test_removes_only_the_matching_block(self, shell_config_file):
        with open(shell_config_file, "w") as file:
            file.write("before\nSTART\nMIDDLE\nEND\nafter\n")

        remove_shell_configuration(shell_config_file, "START\nMIDDLE\nEND")

        with open(shell_config_file) as file:
            assert file.read() == "before\nafter\n"
