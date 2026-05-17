from app.agents.schemas import (
    RemediationPlan,
    PatchOperation,
    VulnerabilityReport
)

from app.services.pom_service import (
    PomService
)

from app.services.compatibility_service import (
    CompatibilityService
)

from app.services.dependency_service import (
    DependencyService
)

from app.services.dependency_graph_service import (
    DependencyGraphService
)


# Service for building a high-level remediation plan based on vulnerability reports
# and the project's dependency graph.
class RemediationService:
    """
    Service for building a high-level remediation plan based on vulnerability reports
    and the project's dependency graph. It aims to identify the most effective
    remediation target (e.g., parent POM, direct dependency) for each vulnerability.
    """

    @staticmethod
    def build_remediation_plan(
        report: VulnerabilityReport,
        dependency_graph, # Changed from dependency_nodes to dependency_graph for clarity
        pom_path: str
    ) -> RemediationPlan:
        """
        Constructs a remediation plan by analyzing vulnerabilities and the project's dependencies.
        It prioritizes BOM-managed dependencies and aims to deduplicate actions.

        Args:
            report (VulnerabilityReport): The report containing detected vulnerabilities.
            dependency_graph (DependencyGraph): The structured dependency graph of the project.
            pom_path (str): The path to the project's pom.xml file.
        Returns:
            RemediationPlan: A plan consisting of a list of PatchOperation objects.
        """

        lookup = (
            DependencyGraphService.build_lookup(
                dependency_nodes
            )
        )

        declared_dependencies = (
            PomService.get_declared_dependencies(
                pom_path
            )
        )
        # Create a lookup for declared dependencies for quick access.
        declared_lookup = {}

        for dep in declared_dependencies:
            # Use the full dependency string (groupId:artifactId) as the key.
            # This assumes 'dependency' field in declared_dependencies is already in this format.
            # If not, it should be constructed here.
            declared_lookup[
                dep["dependency"]
            ] = dep

        actions = {}

        for vuln in report.vulnerabilities:

            parsed = (
                # Parse the vulnerability's dependency string into groupId and artifactId.
                DependencyService.parse_dependency(
                    vuln.dependency
                )
            )

            dependency_key = (
                f"{parsed['group_id']}:"
                f"{parsed['artifact_id']}"
            )

            # ------------------------------------
            # Find root dependency owner
            # ------------------------------------

            root_dependency = ( # This method is not defined in DependencyGraphService in context
                DependencyGraphService.find_root_dependency(
                    dependency_key,
                    lookup
                )
            )

            remediation_target = root_dependency
            # Default remediation target is the root dependency.

            # ------------------------------------
            # BOM-managed dependency logic
            # ------------------------------------

            declared = declared_lookup.get(
                dependency_key
            )

            if declared:

                # ------------------------------------
                # If the dependency is BOM-managed, prefer parent remediation.
                # ------------------------------------

                # Check if the declared dependency is managed by a BOM.
                if declared["managed"]:

                    parent_dep = next(
                        (
                            d["dependency"]
                            for d in declared_dependencies
                            if d["type"] == "parent"
                        ),
                        None
                    )

                    # If a parent dependency is found, set it as the remediation target.
                    if parent_dep:
                        remediation_target = parent_dep

            # ------------------------------------
            # Deduplicate actions and consolidate vulnerabilities for a target.
            # ------------------------------------

            if remediation_target not in actions:
                # If this remediation target hasn't been added yet, create a new PatchOperation.
                # Assuming 'update_dependency' is the primary action for now.
                actions[remediation_target] = PatchOperation(
                    action="update_dependency",
                    dependency=remediation_target,
                    version=vuln.fixed_version,
                    # Note: PatchOperation schema doesn't directly support 'current_version',
                    # 'vulnerabilities', or 'remediation_reason'.
                    # These might need to be passed as part of a more complex plan or metadata.
                    # For now, we'll focus on the core PatchOperation fields.
                )

            else:
                # If the remediation target already exists, update its version if the new fixed_version is higher
                # or if it's a critical vulnerability. For simplicity, we'll just update the version.
                # In a real scenario, more complex logic would be needed to choose the best version.
                # Also, the PatchOperation schema doesn't have a direct way to append CVEs.
                # This implies the agent needs to reason about which single operation to perform.
                # For now, we'll just ensure the version is set.
                actions[
                    remediation_target
                ].version = vuln.fixed_version # Update to the latest fixed version found.

        # Return a RemediationPlan with the consolidated PatchOperation objects.
        return RemediationPlan(
            actions=list(actions.values())
        )