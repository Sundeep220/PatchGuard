# Service for parsing and manipulating dependency strings.
class DependencyService:
    """
    Service for parsing and manipulating dependency strings.
    """

    @staticmethod
    def parse_dependency(
        dependency: str
    ):
        """
        Parses a dependency string in the format "groupId:artifactId"
        into its constituent parts.

        Args:
            dependency (str): The dependency string to parse.
        Returns:
            dict: A dictionary containing 'group_id' and 'artifact_id'.
        Raises:
            Exception: If the dependency string format is invalid.
        """

        parts = dependency.split(":")

        # Validate that the dependency string has exactly two parts
        if len(parts) != 2:
            raise Exception(
                f"Invalid dependency format: {dependency}"
            )

        return {
            "group_id": parts[0],
            "artifact_id": parts[1]
        }