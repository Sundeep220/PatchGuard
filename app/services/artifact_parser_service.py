import json

from pathlib import Path

from app.agents.schemas import (
    Vulnerability,
    VulnerabilityReport
)


# Service for parsing vulnerability reports from various artifact formats.
# Currently supports GitLab Dependency Scanning reports.
class ArtifactParserService:
    """
    Service for parsing vulnerability reports from various artifact formats.
    Currently supports GitLab Dependency Scanning reports, extracting relevant
    vulnerability information and filtering by severity.
    """

    @staticmethod
    def parse_gitlab_dependency_report(
        report_path: str
    ) -> VulnerabilityReport:
        """
        Parses a GitLab Dependency Scanning report JSON file into a structured VulnerabilityReport.
        It filters vulnerabilities to include only HIGH and CRITICAL severities.

        Args:
            report_path (str): The file path to the GitLab Dependency Scanning JSON report.
        
        Returns:
            VulnerabilityReport: A Pydantic model instance containing filtered vulnerabilities.
        
        Raises:
            Exception: If the report file is not found.
        """

        report_file = Path(report_path)

        if not report_file.exists():

            raise Exception(
                f"""
Dependency scanning report not found:

{report_path}
"""
            )

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # List to store parsed Vulnerability objects.
        vulnerabilities: list[Vulnerability] = []

        # Iterate through each vulnerability entry in the report.
        for vuln in data.get(
            "vulnerabilities",
            []
        ):
            # Extract and normalize severity.

            severity = (
                vuln.get("severity", "")
                .upper()
            )

            if severity not in [ # Filter: Only process HIGH or CRITICAL vulnerabilities.
                "HIGH",
                "CRITICAL"
            ]:
                continue

            identifiers = vuln.get(
                # Extract identifiers to find CVE.
                "identifiers",
                []
            )

            cve = "UNKNOWN"

            # Search for CVE identifier.
            for identifier in identifiers:
                # Look for an identifier with type 'cve'.
                if (
                    identifier.get("type")
                    == "cve"
                ):

                    cve = (
                        identifier.get(
                            "value",
                            "UNKNOWN"
                        )
                    )

                    break

            # Extract dependency name (groupId:artifactId).
            dependency: str = (
                vuln.get("location", {})
                .get("dependency", {})
                .get("package", {})
                .get("name", "")
            )

            # Extract current version of the vulnerable dependency.
            current_version: str = (
                vuln.get("location", {})
                .get("dependency", {})
                .get("version", "")
            )

            # Extract fixed version from the solution field.
            fixed_version: str = (
                vuln.get("solution", "")
            )

            vulnerabilities.append(
                Vulnerability(
                    dependency=dependency,
                    current_version=
                        current_version,

                    fixed_version=
                        fixed_version,

                    severity=severity,

                    cve=cve,

                    description=vuln.get(
                        "description",
                        ""
                    ),

                    solution=vuln.get(
                        "solution",
                        ""
                    )
                )
            )

        # Return the compiled VulnerabilityReport.
        return VulnerabilityReport(
            vulnerabilities=vulnerabilities
        )