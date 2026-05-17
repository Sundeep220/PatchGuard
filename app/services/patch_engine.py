from app.agents.schemas import (
    PatchOperation,
    RemediationPlan
)

from app.services.pom_service import (
    PomService
)

from app.services.dependency_service import (
    DependencyService
)


# Orchestrates the application of remediation operations to the project's POM file.
# It acts as a deterministic layer between the agent's plan and the actual file modifications.
class PatchEngine:
    """
    Orchestrates the application of remediation operations to the project's POM file.
    It acts as a deterministic layer between the agent's plan and the actual file modifications.
    """

    @staticmethod
    def apply_operation(
        pom_path: str,
        operation: PatchOperation
    ):
        """
        Applies a single patch operation to the POM file.

        Args:
            pom_path (str): The path to the project's pom.xml file.
            operation (PatchOperation): The operation to apply (e.g., update_dependency, remove_explicit_version).
        
        Returns:
            dict: A dictionary indicating the status of the operation.
        """

        # Handle the 'update_dependency' action.
        if operation.action == "update_dependency":

            parsed = (
                DependencyService.parse_dependency(
                    operation.dependency
                )
            )

            return (
                PomService.update_dependency_version(
                    pom_path=pom_path,
                    group_id=parsed["group_id"],
                    artifact_id=parsed["artifact_id"],
                    new_version=operation.version
                )
            )

        # Handle 'remove_explicit_version' action
        elif ( # Handle the 'remove_explicit_version' action.
            operation.action
            == "remove_explicit_version"
        ):

            parsed = (
                DependencyService.parse_dependency(
                    operation.dependency
                )
            )

            return (
                PomService.remove_dependency_version(
                    pom_path=pom_path,
                    group_id=parsed["group_id"],
                    artifact_id=parsed["artifact_id"]
                )
            )

        raise Exception(
            f"Unsupported operation: "
            f"{operation.action}"
        )
    

    @staticmethod
    def apply_plan(
        pom_path: str,
        plan: RemediationPlan
    ):
        """
        Applies a complete remediation plan, consisting of multiple operations, to the POM file.

        Args:
            pom_path (str): The path to the project's pom.xml file.
            plan (RemediationPlan): The plan containing a list of patch operations.
        
        Returns:
            list[dict]: A list of results, one for each applied operation.
        """

        results = []

        for operation in plan.operations:

            result = (
                PatchEngine.apply_operation(
                    pom_path,
                    operation
                )
            )

            results.append(result)

        return results