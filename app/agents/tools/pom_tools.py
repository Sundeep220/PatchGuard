from agents import function_tool

from app.services.pom_service import (
    PomService
)

"""
This module provides agent tools for modifying Maven POM files.
"""


@function_tool
def update_maven_dependency( # pylint: disable=too-many-arguments
    pom_path: str,
    group_id: str,
    artifact_id: str,
    new_version: str
) -> dict:
    """
    Updates the version of a specified Maven dependency (parent or direct) in the pom.xml.
    This tool allows the agent to apply version upgrades as part of a remediation plan.

    Args:
        pom_path (str): The path to the project's pom.xml file.
        group_id (str): The groupId of the dependency to update.
        artifact_id (str): The artifactId of the dependency to update.
        new_version (str): The new version string to set.

    Returns:
        dict: A dictionary indicating the status of the operation and a list of changes made.
    """
    changes = (
        PomService.update_dependency_version(
            pom_path=pom_path,
            group_id=group_id,
            artifact_id=artifact_id,
            new_version=new_version
        )
    )

    return {
        "status": "success",
        "changes": changes
    }