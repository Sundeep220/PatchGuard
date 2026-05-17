from pydantic import BaseModel


# Pydantic model representing the entire execution context for a PatchPilot run.
# It encapsulates all necessary configuration and runtime state.
class PatchPilotContext(BaseModel):
    """
    Pydantic model representing the entire execution context for a PatchPilot run.
    It encapsulates all necessary configuration and runtime state,
    primarily derived from environment variables and internal logic.
    """ # pylint: disable=duplicate-code

    # -----------------------------------
    # GitLab Pipeline Context
    # -----------------------------------

    project_id: str

    # Unique identifier for the current GitLab CI pipeline.
    pipeline_id: str

    # URL of the GitLab project being remediated.
    project_url: str

    # The default branch of the target repository (e.g., 'main' or 'master').
    default_branch: str

    # -----------------------------------
    # PatchPilot Execution Config
    # -----------------------------------

    # If True, the system will perform a dry run without pushing changes or creating MRs.
    dry_run: bool

    # Maximum number of remediation attempts before giving up.
    max_retries: int

    # Prefix used for generating remediation branch names (e.g., 'patchpilot/remediation').
    branch_prefix: str

    # -----------------------------------
    # Runtime Workspace State
    # -----------------------------------

    workspace_root: str
    
    # Absolute path to the cloned target repository within the ephemeral workspace.
    target_repo_path: str

    # The full name of the remediation branch to be created (e.g., 'patchpilot/remediation-12345').
    remediation_branch: str

    # -----------------------------------
    # Vulnerability Report
    # -----------------------------------

    # The filename or path to the vulnerability report artifact (e.g., 'gl-dependency-scanning-report.json').
    vulnerability_report_path: str