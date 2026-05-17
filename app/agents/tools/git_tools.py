from agents import function_tool

from app.services.git_service import GitService

"""
This module provides agent tools for interacting with Git repositories.
"""


@function_tool
def get_git_diff(repo_path: str) -> dict:
    """
    Retrieves the Git diff for the current changes in the specified repository.
    This tool is useful for the agent to understand what modifications have been made
    and to include them in remediation summaries or failure analysis.

    Args:
        repo_path (str): The path to the Git repository.

    Returns:
        dict: A dictionary containing the Git diff string under the key "diff".
    """

    diff = GitService.get_diff(repo_path)

    return {
        "diff": diff
    }