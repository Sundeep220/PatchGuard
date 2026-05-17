import re

from app.agents.schemas import (
    RiskItem
)


# Provides methods for analyzing various risks within a Maven project's dependency tree.
# This includes detecting ecosystem conflicts, duplicate major versions, and calculating a confidence score.
class RiskAnalysisService:
    """
    Provides methods for analyzing various risks within a Maven project's dependency tree.
    This includes detecting ecosystem conflicts, duplicate major versions, and calculating a confidence score.
    """

    @staticmethod
    def analyze_dependency_tree(
        dependency_tree: str
    ):
        """
        Analyzes the raw dependency tree for potential issues like conflicting ecosystems.

        Args:
            dependency_tree (str): The raw output of 'mvn dependency:tree'.
        """

        warnings = []

        # ------------------------------------ # Check for Jackson ecosystem duplication (2.x and 3.x coexisting).
        # Jackson ecosystem duplication
        # ------------------------------------

        jackson2 = (
            "com.fasterxml.jackson"
            in dependency_tree
            # Checks for the presence of Jackson 2.x group ID
        )

        jackson3 = (
            "tools.jackson"
            in dependency_tree
        )

        # If both Jackson 2.x and 3.x are detected, it's a potential conflict
        if jackson2 and jackson3:

            warnings.append(
                RiskItem(
                    severity="WARNING",
                    category="DEPENDENCY_ECOSYSTEM",
                    message=(
                        "Jackson 2.x and "
                        "Jackson 3.x ecosystems "
                        "coexist. "
                        "This may be intentional "
                        "for transitional compatibility."
                    )
                )
            )

        # ------------------------------------ # Detects multiple instances of 'logback-classic' which might indicate version conflicts.

        duplicate_logback = (
            len(
                re.findall(
                    r"logback-classic",
                    dependency_tree
                )
            ) > 1
        )

        if duplicate_logback:

            warnings.append(
                RiskItem(
                    severity="WARNING",
                    category="DUPLICATE_DEPENDENCY",
                    message=(
                        "Multiple Logback dependencies "
                        "detected."
                    )
                )
            )

        return warnings

    @staticmethod
    def calculate_confidence_score(
        build_passed: bool,
        warnings: list[RiskItem]
    ):
        """
        Calculates a confidence score based on the build status and detected warnings.
        A passing build starts at 100, and points are deducted for each warning.

        Args:
            build_passed (bool): True if the Maven build passed, False otherwise.
            warnings (list[RiskItem]): A list of detected risk items.

        Returns:
            int: The calculated confidence score (0-100).
        """

        # If the build failed, confidence is 0
        if not build_passed:
            return 0

        score = 100 # Start with a perfect score if the build passed.

        for warning in warnings:
            # Deduct points based on severity of the warning
            if warning.severity == "CRITICAL":
                score -= 50
            elif warning.severity == "WARNING":
                score -= 10

        return max(score, 0)