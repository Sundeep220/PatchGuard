from app.agents.schemas import (
    EvaluationResult,
    Vulnerability
)

from app.services.git_service import (
    GitService
)

from app.services.terminal_service import (
    TerminalService
)

from app.services.dependency_tree_service import (
    DependencyTreeService
)

from app.services.risk_analysis_service import (
    RiskAnalysisService
)

from app.services.dependency_graph_service import (
    DependencyGraphService
)

from app.services.vulnerability_verification_service import (
    VulnerabilityVerificationService
)

from app.services.version_intelligence_service import (
    VersionIntelligenceService
)

from app.services.semantic_version_service import (
    SemanticVersionService
)


# Service responsible for evaluating the state of a Maven project
# after a remediation attempt. It runs Maven commands, analyzes
# dependency trees, checks for risks, and calculates a confidence score.
class EvaluatorService:
    """
    Service responsible for evaluating the state of a Maven project
    after a remediation attempt. It runs Maven commands, analyzes
    dependency trees, checks for risks, and calculates a confidence score.
    """

    @staticmethod
    def evaluate(
        project_path: str,
        vulnerabilities: list[Vulnerability] | None = None
    ) -> EvaluationResult:
        """
        Evaluates the current state of the Maven project.
        
        Args:
            project_path (str): The root directory of the Maven project.
            vulnerabilities (list[Vulnerability] | None): A list of known vulnerabilities
                                                          to check against the current dependency graph.
        
        Returns:
            EvaluationResult: An object containing the evaluation outcome,
                              including build status, errors, warnings, and confidence score.
        """

        # ------------------------------------
        # Run Maven validation
        # ------------------------------------
        # Execute 'mvn clean test' to build the project and run its tests.
        # This is the primary indicator of build stability.

        build_result = (
            TerminalService.run_command(
                ["mvn", "clean", "test"],
                project_path
            )
        )

        # ------------------------------------
        # Generate dependency tree
        # ------------------------------------
        # Obtain the full dependency tree to analyze the project's dependencies.

        try:

            dependency_tree = (
                DependencyTreeService.get_dependency_tree(
                    project_path
                )
            )

        except Exception as e:

            dependency_tree = (
                f"DEPENDENCY_TREE_FAILED:\n{str(e)}"
            )

        # ------------------------------------
        # Parse dependency graph
        # ------------------------------------
        # Convert the raw dependency tree text into a structured graph for easier analysis.

        dependency_graph = (
            DependencyGraphService.parse_dependency_tree(
                dependency_tree
            )
        )

        # ------------------------------------
        # Git diff
        # ------------------------------------
        # Get the git diff to understand what changes were applied in the current attempt.

        git_diff = (
            GitService.get_diff(
                project_path
            )
        )

        # ------------------------------------
        # Build errors
        # ------------------------------------
        # Collect any errors from the Maven build process.

        errors = []

        if build_result["return_code"] != 0:

            errors.append(
                build_result["stderr"]
            )

        # ------------------------------------
        # Risk analysis
        # ------------------------------------
        # Perform various risk analyses based on the current project state.

        warnings = []

        # Ecosystem coexistence
        warnings.extend(
            RiskAnalysisService
            .analyze_dependency_tree(
                dependency_tree
            )
        )

        # Duplicate major versions
        warnings.extend(
            VersionIntelligenceService
            .detect_duplicate_major_versions(
                dependency_graph
            )
        )

        # Shadowed dependencies
        warnings.extend(
            VersionIntelligenceService
            .detect_shadowed_dependencies(
                dependency_graph
            )
        )

        # Check for any residual vulnerabilities if an initial list was provided.
        # Residual vulnerabilities
        if vulnerabilities:

            warnings.extend(
                VulnerabilityVerificationService
                .detect_residual_vulnerabilities(
                    dependency_graph,
                    vulnerabilities
                )
            )

        # ------------------------------------
        # Semantic version risk analysis
        # ------------------------------------
        # Assess the risk associated with semantic version changes for vulnerabilities.

        if vulnerabilities:

            for vuln in vulnerabilities:

                risk = (
                    SemanticVersionService
                    .assess_upgrade_risk(
                        vuln.current_version,
                        vuln.fixed_version
                    )
                )

                if risk:
                    warnings.append(risk)

        # ------------------------------------
        # Confidence scoring
        # ------------------------------------
        # Calculate a confidence score based on build status and detected warnings.

        confidence_score = (
            RiskAnalysisService
            .calculate_confidence_score(
                build_passed=(
                    build_result["return_code"] == 0
                ),
                warnings=warnings
            )
        )

        # ------------------------------------
        # Residual CRITICAL vulnerabilities
        # ------------------------------------
        # Determine if any critical vulnerabilities still exist after remediation.

        residual_critical = any(
            (
                warning.category
                == "RESIDUAL_VULNERABILITY"
            )
            for warning in warnings
        )

        # ------------------------------------
        # Final success logic
        # ------------------------------------
        # Define overall success based on build passing and no critical vulnerabilities remaining.

        success = (
            build_result["return_code"] == 0
            and not residual_critical
        )

        return EvaluationResult(
            success=success,
            build_passed=(
                build_result["return_code"] == 0
            ),
            vulnerabilities_remaining=
                residual_critical,
            dependency_tree=dependency_tree,
            build_output=build_result["stdout"],
            errors=errors,
            warnings=warnings,
            confidence_score=confidence_score,
            git_diff=git_diff
        )