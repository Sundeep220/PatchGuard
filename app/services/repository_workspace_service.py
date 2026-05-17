import shutil

from pathlib import Path

from app.services.terminal_service import (
    TerminalService
)


# Service for managing isolated Git repository workspaces.
# This includes creating, cloning, branching, and cleaning up workspaces.
class RepositoryWorkspaceService:
    """
    Service for managing isolated Git repository workspaces.
    This includes creating, cloning, branching, and cleaning up workspaces,
    ensuring that remediation efforts are isolated and reversible.
    """

    @staticmethod
    def create_workspace(
        workspace_root: str
    ):
        """
        Creates a new, empty directory to serve as the root for a remediation workspace.
        If the directory already exists, it ensures it's available.

        Args:
            workspace_root (str): The path where the workspace directory should be created.
        
        Returns:
            Path: The Path object representing the created workspace root.
        """

        workspace = Path(workspace_root)

        workspace.mkdir(
            # Create parent directories if they don't exist.
            parents=True,
            exist_ok=True
        )

        return workspace

    @staticmethod
    def clone_repository(
        repo_url: str,
        target_path: str,
        branch: str = "master"
    ):
        """
        Clones a Git repository into a specified target path within the workspace.
        If the target path already exists, it will be removed before cloning.

        Args:
            repo_url (str): The URL of the Git repository to clone.
            target_path (str): The local path where the repository should be cloned.
            branch (str): The specific branch to checkout after cloning (defaults to "master").
        
        Returns:
            Path: The Path object representing the cloned repository.
        
        Raises:
            Exception: If the git clone command fails.
        """

        target = Path(target_path)

        if target.exists():
            # Remove existing directory to ensure a clean clone if it already exists.
            shutil.rmtree(target)

        result = (
            TerminalService.run_command(
                [
                    "git",
                    "clone",
                    "--branch",
                    branch,
                    repo_url,
                    target_path
                ],
                # Run command from the current working directory (where the script is executed).
                "."
            )
        )

        if result["return_code"] != 0:

            raise Exception(
                f"""
                    Failed to clone repository.

                    STDOUT:
                    {result['stdout']}

                    STDERR:
                    {result['stderr']}
                """
                )

        # Add the cloned repository to Git's safe.directory list to prevent security warnings.
        TerminalService.run_command( # nosec B603 - git config is safe here
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                str(target.resolve())
            ],
            # Run command from the current working directory.
            "."
        )

        return target

    @staticmethod
    def create_branch(
        repo_path: str,
        branch_name: str
    ):
        """
        Creates and checks out a new Git branch in the specified repository.

        Args:
            repo_path (str): The path to the Git repository.
            branch_name (str): The name of the new branch to create and checkout.
        
        Raises:
            Exception: If the git checkout command fails.
        """

        result = (
            TerminalService.run_command( # nosec B603 - git checkout is safe here
                [
                    "git",
                    "checkout",
                    "-b",
                    branch_name
                ],
                # Run command within the target repository directory.
                repo_path
            )
        )

        if result["return_code"] != 0:

            raise Exception(
                f"""
                Failed to create branch.

                STDOUT:
                {result['stdout']}

                STDERR:
                {result['stderr']}
                """
            )

    @staticmethod
    def cleanup_workspace(
        workspace_root: str
    ):
        """
        Removes the entire workspace directory, including all cloned repositories and temporary files.
        This is typically called after a remediation attempt is complete or failed.

        Args:
            workspace_root (str): The path to the root of the workspace to be cleaned up.
        """

        workspace = Path(workspace_root)

        if workspace.exists():
            # Recursively remove the directory and its contents.
            # This operation is irreversible.
            shutil.rmtree(workspace)