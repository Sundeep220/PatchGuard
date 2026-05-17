import subprocess
from pathlib import Path


# Service for executing shell commands and capturing their output.
# Provides a standardized way to interact with the underlying operating system.
class TerminalService:
    """
    Service for executing shell commands and capturing their output.
    Provides a standardized way to interact with the underlying operating system.
    """

    @staticmethod
    def run_command(
        command: list[str],
        cwd: str
    ):
        """
        Runs a shell command and captures its standard output and standard error.

        Args:
            command (list[str]): A list of strings representing the command and its arguments.
            cwd (str): The current working directory for the command execution.
        Returns:
            dict: A dictionary containing the return code, stdout, and stderr of the command.
        """
        # nosec B603 - subprocess.run is used with a list of arguments, which is safer than a shell string.
        result = subprocess.run(
            command,
            cwd=Path(cwd),
            capture_output=True,
            text=True
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }