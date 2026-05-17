from agents import function_tool

from app.services.terminal_service import TerminalService

"""
This module provides agent tools for executing terminal commands,
specifically for Maven operations.
"""


@function_tool
def run_maven_tests(project_path: str) -> dict:
    """
    Executes 'mvn clean test' in the specified Maven project directory.
    This tool is crucial for the agent to validate the build and tests
    after applying a remediation plan.

    Args:
        project_path (str): The root directory of the Maven project.

    Returns:
        dict: A dictionary containing the return code, stdout, and stderr
              of the Maven command execution.
    """

    # nosec B603 - mvn clean test is safe here as arguments are hardcoded.
    # The command is executed within the specified project_path, which is controlled.
    result = TerminalService.run_command(
        ["mvn", "clean", "test"],
        project_path
    )

    return result