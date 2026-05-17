from git import Repo


class CheckpointService:

    @staticmethod
    def create_checkpoint(
        repo_path: str
    ):

        repo = Repo(repo_path)

        repo.git.add(all=True)

        try:
            repo.index.commit(
                "checkpoint"
            )
        except:
            pass

    @staticmethod
    def rollback(
        repo_path: str
    ):
        """
        Rolls back the repository to the last committed state, discarding all uncommitted changes.
        This is used to revert a failed remediation attempt.

        Args:
            repo_path (str): The path to the Git repository.
        """

        repo = Repo(repo_path)

        # Hard reset to discard all changes since the last commit
        repo.git.reset(
            "--hard"
        )