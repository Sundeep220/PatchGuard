import re

from app.agents.schemas import (
    DependencyGraph,
    ResolvedDependency
)


# Service for parsing raw Maven dependency tree output into a structured DependencyGraph.
class DependencyGraphService:
    """
    Service for parsing raw Maven dependency tree output into a structured DependencyGraph.
    """

    @staticmethod
    def parse_dependency_tree(
        dependency_tree: str
    ) -> DependencyGraph:
        """
        Parses the raw text output of 'mvn dependency:tree' into a structured DependencyGraph object.
        It extracts groupId, artifactId, version, scope, and estimates the depth of each dependency.

        Args:
            dependency_tree (str): The raw string output from 'mvn dependency:tree'.
        
        Returns:
            DependencyGraph: A Pydantic model representing the parsed dependency graph.
        """

        dependencies = []

        lines = dependency_tree.splitlines()

        # Regex pattern to extract groupId, artifactId, version, and scope from a dependency line.
        pattern = re.compile(
            r"([a-zA-Z0-9_.-]+):"
            r"([a-zA-Z0-9_.-]+):"
            r"[a-zA-Z0-9_.-]+:"
            r"([a-zA-Z0-9_.-]+):"
            r"([a-zA-Z]+)"
        )

        for line in lines:

            # Attempt to match the pattern in each line
            match = pattern.search(line)

            if not match:
                continue

            group_id = match.group(1)

            artifact_id = match.group(2)

            version = match.group(3)

            scope = match.group(4)

            # Estimate dependency depth based on indentation characters
            # Estimate depth
            depth = (
                line.count("|")
                + line.count("+-")
                + line.count("\\-")
            )

            dependencies.append(
                ResolvedDependency(
                    group_id=group_id,
                    artifact_id=artifact_id,
                    version=version,
                    scope=scope,
                    depth=depth
                )
            )

        return DependencyGraph(
            dependencies=dependencies
        )