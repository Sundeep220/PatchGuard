from git import Repo


# Service for interacting with Git repositories.
# Provides methods to retrieve information like the current Git diff.
class GitService:
    """
    Service for interacting with Git repositories.
    Provides methods to retrieve information like the current Git diff.
    """

    @staticmethod
    def get_diff(repo_path: str):
        """
        Generates the Git diff for the specified repository.

        Args:
            repo_path (str): The path to the Git repository.
        Returns:
            str: The raw Git diff output.
        """
        repo = Repo(repo_path)

        return repo.git.diff()