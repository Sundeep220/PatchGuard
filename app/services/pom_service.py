import xml.etree.ElementTree as ET
from pathlib import Path


# Service for interacting with Maven POM (Project Object Model) files.
# Provides methods to read, modify, and update dependencies within a pom.xml.
class PomService:
    """
    Service for interacting with Maven POM (Project Object Model) files.
    Provides methods to read, modify, and update dependencies within a pom.xml.
    """

    # Namespace for Maven POM XML elements, essential for correct XML parsing.
    NAMESPACE = {
        "m": "http://maven.apache.org/POM/4.0.0"
    }

    @staticmethod
    def remove_dependency_version(
        pom_path: str,
        group_id: str,
        artifact_id: str
    ):
        """
        Removes the explicit <version> tag from a dependency in the pom.xml.
        This is typically used for BOM-managed dependencies where the version
        should be inherited from dependencyManagement.

        Args:
            pom_path (str): The path to the project's pom.xml file.
            group_id (str): The groupId of the dependency.
            artifact_id (str): The artifactId of the dependency.
        
        Returns:
            dict: A status dictionary indicating success.
        
        Raises:
            Exception: If the dependency with an explicit version is not found.
        """

        pom_file = Path(pom_path)

        tree = ET.parse(pom_file)

        root = tree.getroot()

        # Find all <dependency> elements in the POM

        dependencies = root.findall(
            ".//m:dependency",
            PomService.NAMESPACE
        )

        removed = False
        # Iterate through dependencies to find the target and remove its version

        for dep in dependencies:

            gid = dep.find(
                "m:groupId",
                PomService.NAMESPACE
            )

            aid = dep.find(
                "m:artifactId",
                PomService.NAMESPACE
            )

            version = dep.find(
                "m:version",
                PomService.NAMESPACE
            )

            if (
                gid is not None
                and aid is not None
                and version is not None
            ):

                # If groupId and artifactId match, remove the version element
                if (
                    gid.text == group_id
                    and aid.text == artifact_id
                ):

                    dep.remove(version)

                    removed = True

        # If no version was removed, raise an exception
        if not removed:
            raise Exception(
                f"Dependency version not found: "
                f"{group_id}:{artifact_id}"
            )

        tree.write(
            # Write the modified tree back to the POM file
            pom_file,
            encoding="utf-8",
            xml_declaration=True
        )

        return {
            "status": "success"
        }

    @staticmethod
    def get_declared_dependencies(
        pom_path: str
    ):
        """
        Retrieves a list of dependencies explicitly declared in the pom.xml,
        including parent and direct dependencies.

        Args:
            pom_path (str): The path to the project's pom.xml file.
        
        Returns:
            list[dict]: A list of dictionaries, each representing a declared dependency
                        with its group ID, artifact ID, version, and whether it's managed.
        """

        pom_file = Path(pom_path)

        tree = ET.parse(pom_file)

        root = tree.getroot()

        # List to store all found dependencies

        dependencies = []

        # ------------------------------------
        # Parent dependency
        # ------------------------------------

        parent = root.find(
            # Find the <parent> element
            "m:parent",
            PomService.NAMESPACE
        )

        if parent is not None:

            gid = parent.find(
                "m:groupId",
                PomService.NAMESPACE
            )

            aid = parent.find(
                "m:artifactId",
                PomService.NAMESPACE
            )

            version = parent.find(
                "m:version",
                PomService.NAMESPACE
            )
            # Add parent dependency details to the list

            dependencies.append({
                "dependency":
                    f"{gid.text}:{aid.text}",
                "version":
                    version.text,
                "managed":
                    True,
                "type":
                    "parent"
            })

        # ------------------------------------
        # Normal dependencies
        # ------------------------------------

        # Find all direct <dependency> elements
        deps = root.findall(
            ".//m:dependency",
            PomService.NAMESPACE
        )

        for dep in deps:

            # Extract groupId, artifactId, and version for each direct dependency
            gid = dep.find(
                "m:groupId",
                PomService.NAMESPACE
            )

            aid = dep.find(
                "m:artifactId",
                PomService.NAMESPACE
            )

            version = dep.find(
                "m:version",
                PomService.NAMESPACE
            )
            # Determine if the dependency is managed (version is not explicitly declared)

            dependencies.append({
                "dependency":
                    f"{gid.text}:{aid.text}",
                "version":
                    version.text if version is not None else None,
                "managed":
                    version is None,
                "type":
                    "dependency"
            })

        return dependencies

    @staticmethod
    def update_dependency_version(
        pom_path: str,
        group_id: str,
        artifact_id: str,
        new_version: str
    ):
        """
        Updates the version of a specified dependency (parent or direct) in the pom.xml.
        It only updates explicitly declared versions and skips BOM-managed ones.

        Args:
            pom_path (str): The path to the project's pom.xml file.
            group_id (str): The groupId of the dependency to update.
            artifact_id (str): The artifactId of the dependency to update.
            new_version (str): The new version string to set.
        
        Returns:
            list[dict]: A list of dictionaries detailing the changes made.
        
        Raises:
            Exception: If the specified dependency is not found or updated.
        """

        pom_file = Path(pom_path)

        ET.register_namespace(
            "",
            "http://maven.apache.org/POM/4.0.0"
        )

        tree = ET.parse(pom_file)

        root = tree.getroot()

        updated = False
        # List to track all changes made

        changes = []

        # ------------------------------------
        # Update parent
        # ------------------------------------

        parent = root.find(
            "m:parent",
            PomService.NAMESPACE
        )
        # Check if the target dependency is the parent

        if parent is not None:

            gid = parent.find(
                "m:groupId",
                PomService.NAMESPACE
            )

            aid = parent.find(
                "m:artifactId",
                PomService.NAMESPACE
            )

            version = parent.find(
                "m:version",
                PomService.NAMESPACE
            )

            if (
                gid.text == group_id
                and aid.text == artifact_id
            ):

                # Update parent version
                old_version = version.text

                version.text = new_version

                updated = True

                changes.append({
                    "dependency":
                        f"{group_id}:{artifact_id}",
                    "old_version":
                        old_version,
                    "new_version":
                        new_version
                })

        # ------------------------------------
        # Update explicit dependencies ONLY
        # ------------------------------------

        # Find all direct <dependency> elements
        dependencies = root.findall(
            ".//m:dependency",
            PomService.NAMESPACE
        )

        for dep in dependencies:

            gid = dep.find(
                "m:groupId",
                PomService.NAMESPACE
            )

            aid = dep.find(
                "m:artifactId",
                PomService.NAMESPACE
            )

            version = dep.find(
                "m:version",
                PomService.NAMESPACE
            )

            # IMPORTANT: Skip BOM-managed dependencies (those without an explicit <version> tag)
            if version is None:
                continue

            if (
                gid.text == group_id
                and aid.text == artifact_id
            ):
                # Update direct dependency version

                old_version = version.text

                version.text = new_version

                updated = True

                changes.append({
                    "dependency":
                        f"{group_id}:{artifact_id}",
                    "old_version":
                        old_version,
                    "new_version":
                        new_version
                })

        # If no dependency was updated, raise an exception
        if not updated:
            raise Exception(
                f"Dependency not found: "
                f"{group_id}:{artifact_id}"
            )

        tree.write(
            # Write the modified tree back to the POM file
            pom_file,
            encoding="utf-8",
            xml_declaration=True
        )

        return changes