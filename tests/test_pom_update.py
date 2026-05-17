from app.services.pom_service import PomService

"""
This test script demonstrates how to use the PomService to update a dependency version.
It updates a specific dependency in a sample pom.xml and prints the changes.
"""

# Update the version of a specific dependency (e.g., the parent) in the pom.xml
changes = PomService.update_dependency_version(
    "sandbox/vulnerable-spring-app/pom.xml",
    group_id="org.springframework.boot",
    artifact_id="spring-boot-starter-parent",
    new_version="3.2.5" # Example new version
)
print(f"Changes applied: {changes}")