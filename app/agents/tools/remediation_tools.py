from agents import function_tool

from app.services.remediation_service import (
    RemediationService
)
from app.services.dependency_tree_service import (
    DependencyTreeService
)
from app.services.vulnerability_service import (
    VulnerabilityService
)
from app.services.dependency_graph_service import (
    DependencyGraphService
)

"""
This module provides agent tools for generating remediation plans.
"""


@function_tool
def build_remediation_plan( # pylint: disable=too-many-locals
    project_path: str,
    report_path: str,
    pom_path: str
) -> dict:
    """
    Builds a high-level remediation plan based on a vulnerability report and the project's dependency tree.
    This tool orchestrates the parsing of vulnerability data and dependency information
    to suggest a set of actions to fix vulnerabilities.

    Args:
        project_path (str): The root directory of the Maven project.
        report_path (str): The file path to the vulnerability report (e.g., JSON).
        pom_path (str): The path to the project's pom.xml file.

    Returns:
        dict: A dictionary representation of the generated RemediationPlan.
    """

    report = (
        VulnerabilityService.load_report(
            report_path
        )
    )
    dependency_tree = (
        DependencyTreeService.get_dependency_tree(
            project_path
        )
    )
    dependency_graph = (
        DependencyGraphService.parse_dependency_tree( # Changed from dependency_nodes to dependency_graph
            dependency_tree
        )
    )
    remediation_plan = (
        RemediationService.build_remediation_plan(
            report,
            dependency_graph, # Pass the structured graph
            pom_path
        )
    )

    return remediation_plan.model_dump()