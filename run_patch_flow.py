import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

from app.services.vulnerability_service import (
    VulnerabilityService
)

from app.services.remediation_loop_service import (
    RemediationLoopService
)

"""
This script orchestrates the entire patch flow for a vulnerable Spring Boot application.
It loads a vulnerability report, formats it, and then initiates the remediation loop.
"""


async def main():

    report = (
        VulnerabilityService.load_report(
            "sandbox/vulnerability_report.json"
        )
    )
    # Format the vulnerability report into a human-readable text for the agent

    vulnerability_text = "\n".join(
        [
            f"""
Dependency: {v.dependency}
Current Version: {v.current_version}
Fixed Version: {v.fixed_version}
Severity: {v.severity}
Solution: {v.solution}
"""
            for v in report.vulnerabilities
        ]
    )
    # Run the main remediation loop
    result = await (
        RemediationLoopService.run_loop(
            project_path=
                "sandbox/vulnerable-spring-app",

            pom_path=
                "sandbox/vulnerable-spring-app/pom.xml",

            vulnerabilities_text=
                vulnerability_text,

            report=report
        )
    )

    print("\n=== FINAL RESULT ===\n")

    print(result)


asyncio.run(main())