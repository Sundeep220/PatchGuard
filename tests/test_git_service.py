from app.services.git_service import (
    GitService
)

GitService.configure_git_identity()

GitService.commit_changes(
    project_path=
        "/tmp/patchpilot/local-test/"
        "spring-petclinic",

    message=
        "[PatchPilot] Test remediation commit"
)