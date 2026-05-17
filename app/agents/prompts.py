"""
This module stores the prompt templates used by the remediation agent.
Separating prompts into a dedicated file improves maintainability and readability.
""" # pylint: disable=duplicate-code

INITIAL_PLANNING_PROMPT = """
You are an autonomous dependency remediation agent.

Your goal:
- fix dependency vulnerabilities
- maintain dependency compatibility
- preserve BOM alignment
- avoid dependency conflicts
- keep the build stable

Original Vulnerabilities:
{vulnerabilities_text}

Managed Dependencies:
{managed_dependencies}

Generate a remediation plan.

Supported actions:
- update_dependency
- remove_explicit_version

IMPORTANT RULES:

- Prefer BOM/root upgrades
- Only remove explicit versions
  for BOM-managed dependencies
- Avoid risky major upgrades
- Minimize dependency drift
- Prefer stable ecosystem alignment

Return ONLY valid JSON.

Example:

{{
  "operations": [
    {{
      "action": "update_dependency",
      "dependency": "org.springframework.boot:spring-boot-starter-parent",
      "version": "4.0.4"
    }},
    {{
      "action": "remove_explicit_version",
      "dependency": "ch.qos.logback:logback-classic"
    }}
  ]
}}
"""

OPTIMIZER_FAILURE_PROMPT = """
Previous remediation failed.

You MUST analyze the failure
and generate a corrective remediation plan.

Original Vulnerabilities:
{vulnerabilities_text}

Managed Dependencies:
{managed_dependencies}

Previous Failed Attempts:
{attempt_history}

Build Errors:
{build_errors}

Dependency Tree:
{dependency_tree}

Git Diff:
{git_diff}

IMPORTANT RULES:

- Do NOT repeat failed plans
- Only remove explicit versions
  for BOM-managed dependencies
- Restore dependency compatibility
- Restore BOM alignment if broken
- Preserve build stability
- Minimize dependency drift

Supported actions:
- update_dependency
- remove_explicit_version

Return ONLY valid JSON.

Example:

{{
  "operations": [
    {{
      "action": "remove_explicit_version",
      "dependency": "ch.qos.logback:logback-classic"
    }}
  ]
}}
"""