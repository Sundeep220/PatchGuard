import xml.etree.ElementTree as ET
import tempfile
from pathlib import Path

from app.services.terminal_service import (
    TerminalService
)


# Service for interacting with Maven's effective POM.
# Provides methods to generate the effective POM and extract information from it.
class EffectivePomService:

    # Namespace for Maven POM XML elements
    # This is crucial for correctly parsing XML with namespaces
    NAMESPACE = {
        "m": "http://maven.apache.org/POM/4.0.0"
    }

    @staticmethod
    def generate_effective_pom(
        project_path: str
    ):
        """
        Generates the effective POM for a given Maven project and saves it to a temporary file.
        The effective POM is the result of merging all active profiles and inheritance.
        
        Args:
            project_path (str): The root directory of the Maven project.
        
        Returns:
            str: The path to the generated temporary effective POM file.
        
        Raises:
            Exception: If the Maven command fails to generate the effective POM.
        """

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".xml",
            delete=False
        )

        # The path where the effective POM XML will be written
        output_path = temp_file.name

        # Run the Maven help:effective-pom goal to generate the effective POM
        result = (
            TerminalService.run_command(
                [
                    "mvn",
                    "help:effective-pom",
                    f"-Doutput={output_path}"
                ],
                project_path
            )
        )

        # Check if the command executed successfully
        if result["return_code"] != 0:

            raise Exception(
                f"""
Failed to generate effective pom.

STDOUT:
{result['stdout']}

STDERR:
{result['stderr']}
"""
            )

        return output_path

    @staticmethod
    def get_managed_dependencies(
        effective_pom_path: str
    ):
        """
        Extracts a set of managed dependencies (groupId:artifactId) from an effective POM.
        Managed dependencies are typically defined in the <dependencyManagement> section.
        
        Args:
            effective_pom_path (str): The path to the effective POM XML file.
        
        Returns:
            set[str]: A set of strings, each representing a managed dependency
                      in the format "groupId:artifactId".
        """
        # Parse the effective POM XML file

        # Parse the effective POM XML file
        tree = ET.parse(
            effective_pom_path
        )

        root = tree.getroot()

        managed = set()
        # Find all <dependency> elements within the <dependencyManagement> section
        # using the defined Maven namespace.
        
        # Find all <dependency> elements within the <dependencyManagement> section
        # using the defined Maven namespace.

        dependencies = root.findall(
            ".//m:dependencyManagement/"
            "m:dependencies/"
            "m:dependency",
            EffectivePomService.NAMESPACE
        )
        # Iterate through found dependencies and extract groupId and artifactId
        
        # Iterate through found dependencies and extract groupId and artifactId

        for dep in dependencies:

            gid = dep.find(
                "m:groupId",
                EffectivePomService.NAMESPACE
            )

            aid = dep.find(
                "m:artifactId",
                EffectivePomService.NAMESPACE
            )

            # If both groupId and artifactId are present, add to the managed set
            if gid is not None and aid is not None:

                managed.add(
                    f"{gid.text}:{aid.text}"
                )

        return managed