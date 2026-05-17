from app.services.git_service import GitService

"""
This test script demonstrates how to use the GitService to get a Git diff.
It's useful for verifying changes in a local repository.
"""

# Get the Git diff for the specified repository path
diff = GitService.get_diff(
    "sandbox/vulnerable-spring-app"
)
print(diff)