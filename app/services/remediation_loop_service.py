import asyncio
import json

from agents import Runner

from app.agents.patch_agent import (
    # Assuming patch_agent is an agent instance or function
    # that can be run by the agents.Runner.
    patch_agent
)
from app.agents.prompts import (
    INITIAL_PLANNING_PROMPT, OPTIMIZER_FAILURE_PROMPT
)

from app.agents.schemas import (
    RemediationPlan,
    RetryState
)

from app.services.patch_engine import (
    PatchEngine
)

from app.services.evaluator_service import (
    EvaluatorService
)

from app.services.checkpoint_service import (
    CheckpointService
)

from app.services.output_parser_service import (
    OutputParserService
)

from app.services.effective_pom_service import (
    EffectivePomService
)


# Manages the iterative remediation loop for fixing dependency vulnerabilities.
# This service orchestrates the agent, applies patches, evaluates results,
# and handles retries and rollbacks.
class RemediationLoopService:
    """
    Manages the iterative remediation loop for fixing dependency vulnerabilities.
    This service orchestrates the agent, applies patches, evaluates results,
    and handles retries and rollbacks.
    """

    @staticmethod
    async def run_loop(
        project_path: str,
        pom_path: str,
        vulnerabilities_text: str,
        report
    ):
        """
        Executes the main remediation loop.
        
        Args:
            project_path (str): The root directory of the vulnerable Maven project.
            pom_path (str): The path to the project's pom.xml file.
            vulnerabilities_text (str): A text description of the initial vulnerabilities.
            report: The initial vulnerability report object (type not specified, assuming it has .vulnerabilities).
        
        Returns:
            EvaluationResult: The final evaluation result if remediation is successful.
        
        Raises:
            Exception: If max remediation attempts are exceeded.
        """

        # ------------------------------------
        # Generate effective pom
        # ------------------------------------

        effective_pom = (
            EffectivePomService.generate_effective_pom( # Generate the effective POM to understand managed dependencies.
                project_path
            )
        )

        managed_dependencies = (
            EffectivePomService.get_managed_dependencies(
                effective_pom
            )
        )

        # Initialize retry state and history for the iterative loop
        retry_state = RetryState(
            current_attempt=0,
            max_attempts=10 # Define maximum attempts for the remediation loop.
        )

        # Stores a history of attempts, including the plan, success status, and errors
        # This is crucial for the optimizer agent to learn from past failures.
        attempt_history = []

        last_evaluation = None

        while (
            retry_state.current_attempt
            < retry_state.max_attempts
        ):

            # Log current attempt number
            print(
                f"\n=== Attempt "
                f"{retry_state.current_attempt + 1} ==="
            )

            # ------------------------------------
            # Create git checkpoint
            # ------------------------------------
            # A checkpoint allows rolling back changes if an attempt fails.
            # This ensures that each attempt starts from a clean, known state.
            CheckpointService.create_checkpoint(
                project_path
            )

            # ------------------------------------
            # INITIAL PLANNING PROMPT
            # ------------------------------------

            if retry_state.current_attempt == 0:
                # For the first attempt, use the initial planning prompt to generate a remediation plan.
                agent_prompt = INITIAL_PLANNING_PROMPT.format(
                    vulnerabilities_text=vulnerabilities_text,
                    managed_dependencies=sorted(managed_dependencies)
                )

            # ------------------------------------
            # OPTIMIZER FAILURE PROMPT
            # ------------------------------------

            else:
                # For subsequent attempts, use the optimizer prompt,
                # providing feedback from the previous failed attempt.
                # This allows the agent to learn from past mistakes and generate a corrective plan.
                agent_prompt = OPTIMIZER_FAILURE_PROMPT.format(
                    vulnerabilities_text=vulnerabilities_text,
                    managed_dependencies=sorted(managed_dependencies),
                    attempt_history=json.dumps(attempt_history, indent=2),
                    build_errors=last_evaluation.errors,
                    dependency_tree=last_evaluation.dependency_tree,
                    git_diff=last_evaluation.git_diff
                )

            # ------------------------------------
            # Run agent
            # ------------------------------------

            result = await Runner.run(
                patch_agent,
                # The agent receives the prompt and generates a remediation plan in JSON format.
                agent_prompt
            )

            print("\n=== RAW AGENT OUTPUT ===\n")

            print(result.final_output)

            # ------------------------------------
            # Parse + sanitize JSON
            # ------------------------------------

            # Attempt to extract and validate the JSON remediation plan from the agent's raw output.
            try:

                sanitized_output = (
                    OutputParserService.extract_json(
                        result.final_output
                    )
                )

                plan = (
                    # Validate the extracted JSON against the RemediationPlan Pydantic schema.
                    RemediationPlan
                    .model_validate_json(
                        sanitized_output
                    )
                )

            except Exception as e:

                raise Exception(
                    f"""
Invalid remediation output.

Error:
{e}

Raw Output:
{result.final_output}
"""
                )

            # ------------------------------------
            # Apply remediation plan
            # ------------------------------------

            # Log the generated plan and apply its operations to the pom.xml file.
            print(
                "\nApplying remediation plan:"
            )

            print(plan)

            PatchEngine.apply_plan(
                pom_path,
                plan
            )

            # ------------------------------------
            # Evaluate remediation
            # ------------------------------------

            # Evaluate the project's state after applying the patch, checking build status and residual vulnerabilities.
            evaluation = (
                EvaluatorService.evaluate(
                    project_path,
                    vulnerabilities=report.vulnerabilities
                )
            )

            last_evaluation = evaluation

            # ------------------------------------
            # Save attempt history
            # ------------------------------------

            # Record the outcome of the current attempt for future agent reasoning and optimization.
            attempt_history.append({
                "attempt":
                    retry_state.current_attempt + 1,

                "plan":
                    plan.model_dump(),

                "success":
                    evaluation.success,

                "errors":
                    evaluation.errors
            })

            # ------------------------------------
            # SUCCESS
            # ------------------------------------

            # If the build passed and no critical vulnerabilities remain, the remediation is considered successful.
            if evaluation.build_passed:

                print(
                    "\n=== REMEDIATION SUCCESSFUL ==="
                )

                print(
                    f"\nConfidence Score: "
                    f"{evaluation.confidence_score}/100"
                )

                if evaluation.warnings:

                    print("\nWarnings:")

                    for warning in evaluation.warnings:

                        print(
                            f"\n[{warning.severity}] "
                            f"{warning.category}"
                        )

                        print(
                            warning.message
                        )

                return evaluation

            # ------------------------------------
            # FAILURE
            # ------------------------------------

            # If the build failed, log the errors and prepare for rollback to the previous checkpoint.
            print(
                "\n=== BUILD FAILED ==="
            )

            print(
                "\nErrors:"
            )

            print(
                evaluation.errors
            )

            # ------------------------------------
            # Rollback failed changes
            # ------------------------------------

            # Revert changes made in the current attempt to restore the project to its state before this attempt.
            print(
                "\nRolling back failed changes..."
            )

            CheckpointService.rollback(
                project_path
            )

            # Increment the attempt counter and continue the loop if max attempts are not reached.
            retry_state.current_attempt += 1

        raise Exception(
            "Max remediation attempts exceeded."
        )