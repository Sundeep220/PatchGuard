from app.services.terminal_service import (
    TerminalService
)
from git import Repo


# Service for interacting with Git repositories.
# Provides methods to configure identity, get diffs, commit, push, and get current branch.
class GitService:
    """
    Service for interacting with Git repositories.
    Provides methods to configure identity, get diffs, commit, push, and get current branch.
    """

    @staticmethod
    def configure_git_identity():
        """
        Configures the global Git user email and name for the PatchPilot automation user.
        This is important for commits made by the agent.
        """

        # Set global user email.
        # nosec B603 - git config is safe here as arguments are hardcoded.
        TerminalService.run_command(
            [
                "git",
                "config",
                "--global",
                "user.email",
                "patchpilot@automation.local"
            ],
            "."
        )

        # Set global user name.
        # nosec B603 - git config is safe here as arguments are hardcoded.
        TerminalService.run_command(
            [
                "git",
                "config",
                "--global",
                "user.name",
                "PatchPilot"
            ],
            "."
        )

    @staticmethod
    def get_diff(
        project_path: str
    ):
        """
        Generates the Git diff for the current changes in the specified repository.

        Args:
            project_path (str): The path to the Git repository.
        
        Returns:
            str: The raw Git diff output.
        """

        # nosec B603 - git diff is safe here as arguments are hardcoded.
        # The command is executed within the specified project_path, which is controlled.
        result = (
            TerminalService.run_command(
                [
                    "git",
                    "diff"
                ],
                project_path
            )
        )

        return result["stdout"]

    @staticmethod
    def commit_changes(
        project_path: str,
        message: str
    ):
        """
        Stages all changes and commits them to the repository with a given message.

        Args:
            project_path (str): The path to the Git repository.
            message (str): The commit message.
        
        Raises:
            Exception: If staging or committing changes fails.
        """

        # Stage all changes.
        # nosec B603 - git add is safe here as arguments are hardcoded.
        # The command is executed within the specified project_path, which is controlled.
        add_result = (
            TerminalService.run_command(
                [
                    "git",
                    "add",
                    "."
                ],
                project_path
            )
        )

        if add_result["return_code"] != 0:

            raise Exception(
                f"""
Failed to stage changes.

STDERR:
{add_result['stderr']}
"""
            )

        # Commit staged changes.
        # nosec B603 - git commit is safe here as arguments are hardcoded.
        commit_result = (
            TerminalService.run_command(
                [
                    "git",
                    "commit",
                    "-m",
                    message
                ],
                project_path
            )
        )

        if commit_result["return_code"] != 0:

            raise Exception(
                f"""
Failed to commit changes.

STDERR:
{commit_result['stderr']}
"""
            )

    @staticmethod
    def push_branch(
        project_path: str,
        branch_name: str
    ):
        """
        Pushes the specified branch to the 'origin' remote.

        Args:
            project_path (str): The path to the Git repository.
            branch_name (str): The name of the branch to push.
        
        Raises:
            Exception: If pushing the branch fails.
        """

        # Push the branch to the remote.
        # nosec B603 - git push is safe here as arguments are hardcoded.
        # The command is executed within the specified project_path, which is controlled.
        result = (
            TerminalService.run_command(
                [
                    "git",
                    "push",
                    "origin",
                    branch_name
                ],
                project_path
            )
        )

        if result["return_code"] != 0:

            raise Exception(
                f"""
Failed to push remediation branch.

STDOUT:
{result['stdout']}

STDERR:
{result['stderr']}
"""
            )

    @staticmethod
    def get_current_branch(
        project_path: str
    ):
        """
        Retrieves the name of the current active Git branch.

        Args:
            project_path (str): The path to the Git repository.
        
        Returns:
            str: The name of the current branch, stripped of whitespace.
        """

        # Get the current branch name.
        # nosec B603 - git branch is safe here as arguments are hardcoded.
        result = (
            TerminalService.run_command(
                [
                    "git",
                    "branch",
                    "--show-current"
                ],
                project_path
            )
        )

        return result["stdout"].strip()