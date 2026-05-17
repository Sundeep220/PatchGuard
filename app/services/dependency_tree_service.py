from app.services.terminal_service import (
    TerminalService
)


# Service for generating and retrieving the Maven dependency tree.
class DependencyTreeService:
    """
    Service for generating and retrieving the Maven dependency tree.
    """

    @staticmethod
    def get_dependency_tree(
        project_path: str
    ):
        """
        Generates the Maven dependency tree for a given project.
        
        Args:
            project_path (str): The root directory of the Maven project.
        
        Returns:
            str: The raw output of the 'mvn dependency:tree' command.
        
        Raises:
            Exception: If the Maven command fails to generate the dependency tree.
        """

        result = (
            TerminalService.run_command( # nosec B603 - mvn dependency:tree is safe here as arguments are hardcoded.
                [
                    "mvn",
                    "dependency:tree"
                ],
                project_path
            )
        )

        # Check if the command executed successfully
        if result["return_code"] != 0:

            raise Exception(
                f"""
Failed to generate dependency tree.

STDOUT:
{result['stdout']}

STDERR:
{result['stderr']}
"""
            )

        return result["stdout"]