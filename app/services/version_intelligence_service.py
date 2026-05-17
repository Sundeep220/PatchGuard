from collections import defaultdict

from app.agents.schemas import (
    DependencyGraph,
    RiskItem
)


# Provides intelligence services related to dependency versions,
# such as detecting duplicate major versions or shadowed dependencies.
class VersionIntelligenceService:
    """
    Provides intelligence services related to dependency versions,
    such as detecting duplicate major versions or shadowed dependencies.
    """

    @staticmethod
    def detect_duplicate_major_versions(
        graph: DependencyGraph
    ):
        """
        Detects if multiple major versions of the same artifact are present in the dependency graph.
        This can lead to unexpected behavior or conflicts.

        Args:
            graph (DependencyGraph): The resolved dependency graph of the project.
        
        Returns:
            list[RiskItem]: A list of warnings for duplicate major versions found.
        """

        warnings = []

        versions = defaultdict(set)

        for dep in graph.dependencies: # Iterate through each resolved dependency in the graph.

            # Use artifact_id as the key to group versions of the same dependency
            key = dep.artifact_id

            major = (
                dep.version.split(".")[0]
            )

            versions[key].add(major)


        for dep_name, majors in versions.items():

            if len(majors) > 1:

                warnings.append(
                    RiskItem(
                        severity="WARNING",
                        category="DUPLICATE_MAJOR_VERSION",
                        message=(
                            f"Multiple major versions "
                            f"detected for "
                            f"{dep_name}: "
                            f"{sorted(majors)}"
                        )
                    )
                )

        return warnings

    @staticmethod
    def detect_shadowed_dependencies(
        graph: DependencyGraph
    ):
        """
        Detects if multiple versions of the same dependency (groupId:artifactId) are resolved
        in the dependency graph. This can indicate shadowing or unexpected version resolution.

        Args:
            graph (DependencyGraph): The resolved dependency graph of the project.
        
        Returns:
            list[RiskItem]: A list of warnings for shadowed dependencies found.
        """

        warnings = []

        versions = defaultdict(set)

        for dep in graph.dependencies: # Iterate through each resolved dependency in the graph.
            # Use groupId:artifactId as the key to group all resolved versions

            key = (
                f"{dep.group_id}:"
                f"{dep.artifact_id}"
            )

            versions[key].add(dep.version)

        for dep_name, found_versions in versions.items():

            if len(found_versions) > 1:

                warnings.append(
                    RiskItem(
                        severity="WARNING",
                        category="SHADOWED_DEPENDENCY",
                        message=(
                            f"Multiple resolved versions "
                            f"detected for "
                            f"{dep_name}: "
                            f"{sorted(found_versions)}"
                        )
                    )
                )

        return warnings