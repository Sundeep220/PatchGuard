from app.agents.schemas import (
    RiskItem
)


# Provides utilities for analyzing semantic versioning risks during dependency upgrades.
class SemanticVersionService:
    """
    Provides utilities for analyzing semantic versioning risks during dependency upgrades.
    """

    @staticmethod
    def assess_upgrade_risk(
        current_version: str,
        target_version: str
    ):
        """
        Assesses the risk of an upgrade based on semantic versioning rules.
        Currently, it flags major version upgrades as a warning.

        Args:
            current_version (str): The current version string (e.g., "1.2.3").
            target_version (str): The target version string for the upgrade.
        """

        # Extract major version components
        current_major = (
            current_version.split(".")[0]
        )

        target_major = (
            target_version.split(".")[0]
        )

        # If major versions differ, it's a potential breaking change and should be flagged as a warning.
        if current_major != target_major:

            return RiskItem(
                severity="WARNING",
                category="SEMANTIC_VERSION_RISK",
                message=(
                    f"Major version upgrade: "
                    f"{current_version} "
                    f"→ "
                    f"{target_version}"
                )
            )

        return None