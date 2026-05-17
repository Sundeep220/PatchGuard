from app.services.repository_workspace_service import (
    RepositoryWorkspaceService
)


def main():

    workspace_root = (
        "/tmp/patchpilot/local-test"
    )

    repo_path = (
        f"{workspace_root}/spring-petclinic"
    )

    print("\n=== STEP 1: CREATE WORKSPACE ===\n")

    workspace = (
        RepositoryWorkspaceService
        .create_workspace(
            workspace_root
        )
    )

    print(f"Workspace created:\n{workspace}")

    print("\n=== STEP 2: CLONE REPOSITORY ===\n")

    RepositoryWorkspaceService.clone_repository(
        repo_url=(
            "https://github.com/"
            "spring-projects/"
            "spring-petclinic.git"
        ),

        target_path=repo_path,

        branch="main"
    )

    print(
        f"Repository cloned successfully:\n"
        f"{repo_path}"
    )

    print("\n=== STEP 3: CREATE BRANCH ===\n")

    branch_name = (
        "patchpilot/test-remediation"
    )

    RepositoryWorkspaceService.create_branch(
        repo_path=repo_path,
        branch_name=branch_name
    )

    print(
        f"Branch created successfully:\n"
        f"{branch_name}"
    )

    print("\n=== STEP 4: CLEANUP WORKSPACE ===\n")

    RepositoryWorkspaceService.cleanup_workspace(
        workspace_root
    )

    print(
        f"Workspace cleaned successfully:\n"
        f"{workspace_root}"
    )

    print("\n=== TEST COMPLETED SUCCESSFULLY ===\n")


if __name__ == "__main__":

    main()