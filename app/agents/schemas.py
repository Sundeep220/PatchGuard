from typing import Optional
from pydantic import BaseModel, Field

"""
This module defines Pydantic schemas for various data structures
used throughout the PatchGuard application, including vulnerabilities,
remediation plans, evaluation results, and dependency graphs.
"""

# Represents a single vulnerability found in a dependency.
class Vulnerability(BaseModel):

    dependency: str = Field(..., description="The full identifier of the vulnerable dependency (e.g., 'groupId:artifactId').") # pylint: disable=duplicate-code

    current_version: str = Field(..., description="The currently installed version of the vulnerable dependency.")

    fixed_version: str = Field(..., description="The recommended version to upgrade to, to fix the vulnerability.")

    severity: str = Field(..., description="The severity level of the vulnerability (e.g., 'HIGH', 'CRITICAL').")

    cve: str = Field(..., description="The Common Vulnerabilities and Exposures (CVE) identifier.")

    description: str = Field(..., description="A brief description of the vulnerability.")

    solution: str = Field(..., description="The recommended solution or action to address the vulnerability.")

# Represents a report containing a list of vulnerabilities.
class VulnerabilityReport(BaseModel):

    vulnerabilities: list[Vulnerability] = Field(..., description="A list of individual vulnerability details.") # pylint: disable=duplicate-code
# Represents a single operation to be performed as part of a remediation plan.
# This could be updating a dependency version or removing an explicit version.
class PatchOperation(BaseModel):

    action: str = Field(..., description="The type of remediation action (e.g., 'update_dependency', 'remove_explicit_version').")

    dependency: Optional[str] = Field(None, description="The target dependency for the action (e.g., 'groupId:artifactId').")

    version: Optional[str] = Field(None, description="The new version to set for the dependency, if applicable.")

    parent_dependency: Optional[str] = Field(None, description="The parent dependency if the action targets a transitive dependency (e.g., 'groupId:artifactId').")

    target_dependency: Optional[str] = Field(None, description="The specific transitive dependency to target, if applicable.")

# Represents a complete plan for remediating vulnerabilities,
# consisting of a sequence of patch operations.
class RemediationPlan(BaseModel):
    # A list of patch operations to be executed as part of the remediation plan.
    operations: list[PatchOperation] = Field(..., description="A list of patch operations to be executed.") # pylint: disable=duplicate-code
# Represents a single risk item or warning identified during evaluation.
class RiskItem(BaseModel):

    severity: str = Field(..., description="The severity of the risk item (e.g., 'WARNING', 'CRITICAL').")

    category: str = Field(..., description="The category of the risk (e.g., 'DUPLICATE_MAJOR_VERSION', 'RESIDUAL_VULNERABILITY').")

    message: str = Field(..., description="A detailed message describing the risk.")

# Represents the comprehensive result of an evaluation cycle,
# including build status, detected issues, and a confidence score.
class EvaluationResult(BaseModel):
    # True if the overall remediation attempt was successful (build passed, no critical vulnerabilities).
    success: bool = Field(..., description="True if the remediation attempt was successful, False otherwise.") # pylint: disable=duplicate-code

    build_passed: bool = Field(..., description="True if the Maven build (mvn clean test) passed, False otherwise.")

    vulnerabilities_remaining: bool = Field(..., description="True if critical vulnerabilities are still detected, False otherwise.")

    dependency_tree: str = Field(..., description="The raw output of the Maven dependency tree command.")

    build_output: str = Field(..., description="The raw standard output from the Maven build command.")

    errors: list[str] = Field(..., description="A list of error messages encountered during the evaluation.")

    warnings: list[RiskItem] = Field(..., description="A list of risk items or warnings identified during the evaluation.")

    confidence_score: int = Field(..., description="A numerical score (0-100) indicating the confidence in the remediation.")

    git_diff: str = Field(..., description="The Git diff showing changes made during the remediation attempt.")


# ------------------------------------
# Retry State
# ------------------------------------ # pylint: disable=duplicate-code

class RetryState(BaseModel):

    current_attempt: int = Field(..., description="The current attempt number in the remediation loop.")

    max_attempts: int = Field(..., description="The maximum number of attempts allowed for remediation.")


# Represents a node in the Maven dependency tree,
# capturing its dependency identifier, version, depth, and parent.
class DependencyNode(BaseModel):

    dependency: str = Field(..., description="The full identifier of the dependency (e.g., 'groupId:artifactId').")

    version: str = Field(..., description="The version of the dependency.")

    depth: int = Field(..., description="The depth of the dependency in the tree, starting from 0 for root.")

    parent: Optional[str] = Field(None, description="The full identifier of the parent dependency, if applicable.")

# Represents a resolved dependency with its group ID, artifact ID, version,
# scope, and depth in the dependency graph.
class ResolvedDependency(BaseModel):

    group_id: str = Field(..., description="The group ID of the resolved dependency.")

    artifact_id: str = Field(..., description="The artifact ID of the resolved dependency.")

    version: str = Field(..., description="The resolved version of the dependency.")

    scope: Optional[str] = Field(None, description="The scope of the dependency (e.g., 'compile', 'test', 'runtime').")

    depth: int = Field(..., description="The depth of the dependency in the dependency tree.")

# Represents the entire dependency graph of a project,
# composed of a list of resolved dependencies.
class DependencyGraph(BaseModel):
    # A list of all resolved dependencies in the project's graph.
    dependencies: list[ResolvedDependency] = Field(..., description="A list of all resolved dependencies in the project's graph.") # pylint: disable=duplicate-code