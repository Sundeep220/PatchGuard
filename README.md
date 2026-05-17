# PatchPilot AI

## Autonomous Dependency Remediation & Governance Platform

PatchPilot AI is an AI-driven dependency remediation platform designed for enterprise Spring Boot applications. The system autonomously analyzes vulnerability reports, determines safe remediation strategies, applies dependency upgrades, validates builds/tests, and generates merge requests for human review.

Built using:

* Python
* OpenAI Agents SDK
* Spring Boot
* Maven
* Git/GitLab
* MCP (Model Context Protocol)
* Evaluator–optimizer agent loops
* Dependency graph intelligence

The platform integrates with:

* GitLab Dependency Scanning
* GitHub Dependabot
* Snyk
* OSV scanners
* CI/CD pipelines

Its goal is to eliminate manual dependency remediation workflows and reduce sprint-end merge blockers caused by HIGH and CRITICAL vulnerabilities. 

---

# Problem Statement

Modern enterprise applications rely heavily on:

* Spring Boot starters
* Maven dependencies
* BOM-managed libraries
* transitive dependencies
* third-party ecosystems

Security scanners such as:

* GitLab Dependency Scanning
* Dependabot
* Snyk

frequently detect:

* HIGH vulnerabilities
* CRITICAL vulnerabilities
* transitive dependency risks

These vulnerabilities often:

* block merge requests
* delay releases
* create operational overhead
* require repetitive manual remediation

Developers typically must:

* analyze vulnerability reports
* identify safe upgrade paths
* update dependencies
* resolve version conflicts
* validate builds/tests
* create remediation PRs/MRs

This becomes repetitive, time-consuming engineering work.

---

# Solution Overview

PatchPilot AI automates the entire dependency remediation lifecycle using AI-driven orchestration combined with deterministic execution and runtime validation.

## Automated Workflow

```text
Dependency Scan Report
        ↓
Planner Agent
        ↓
Remediation Plan
        ↓
Patch Engine
        ↓
Build/Test Validation
        ↓
Dependency Graph Analysis
        ↓
Risk Evaluation
        ↓
Retry / Optimization Loop
        ↓
GitLab Merge Request
```

The platform continuously:

* ingests vulnerability reports
* analyzes dependency ecosystems
* reasons about safe upgrade paths
* applies dependency updates
* validates compatibility
* evaluates remediation risk
* retries failed strategies
* generates remediation summaries
* creates merge requests for review

---

# Core Architecture

```text
                    ┌─────────────────────┐
                    │ GitLab CI Pipeline  │
                    └──────────┬──────────┘
                               │
                    Vulnerability Reports
                               │
                               ▼
                ┌──────────────────────────┐
                │     PatchPilot API       │
                │      FastAPI Backend     │
                └──────────┬───────────────┘
                           │
                           ▼
                ┌──────────────────────────┐
                │  OpenAI Agents Runtime   │
                └──────────┬───────────────┘
                           │
                    Planner Agent
                           │
                           ▼
                    MCP Tool Layer

        • GitLab Integration
        • Filesystem Operations
        • Maven Execution
        • Dependency Analysis
        • Git Operations

                           │
                           ▼

                 Isolated Repository Clone
```

---

# Core Engineering Concepts

## Evaluator–Optimizer Architecture

PatchPilot follows an evaluator–optimizer architecture instead of relying on single-shot AI generation.

```text
Vulnerability Report
        ↓
Planner Agent
        ↓
Remediation Plan
        ↓
Patch Execution
        ↓
Build/Test Evaluation
        ↓
Dependency Analysis
        ↓
Failure Feedback
        ↓
Optimizer Retry
```

The system:

* evaluates remediation results
* analyzes failures
* retries corrective strategies
* avoids repeating failed actions

This architecture mirrors modern autonomous coding systems such as:

* Devin
* SWE-agent
* Windsurf
* Copilot Agent Mode

---

## Autonomous Planning

The planner agent:

* analyzes vulnerabilities
* reasons about dependency ecosystems
* generates remediation strategies
* adapts after failures
* orchestrates multi-step dependency operations

Example remediation plan:

```json
{
  "operations": [
    {
      "action": "update_dependency",
      "dependency": "com.fasterxml.jackson.core:jackson-databind",
      "version": "2.17.3"
    },
    {
      "action": "remove_explicit_version",
      "dependency": "com.fasterxml.jackson.core:jackson-databind"
    }
  ]
}
```

---

## BOM-Aware Dependency Intelligence

PatchPilot dynamically analyzes Maven ecosystems using:

```bash
mvn help:effective-pom
```

This enables detection of:

* BOM-managed dependencies
* inherited versions
* parent-managed libraries
* transitive ownership

The system intelligently determines when:

* explicit versions should be updated
* versions should be removed
* parent BOM upgrades are safer

---

## Dependency Graph Intelligence

PatchPilot parses Maven dependency trees into structured dependency graphs supporting:

* resolved dependencies
* scopes
* transitive relationships
* graph depth analysis
* duplicate dependency detection
* ecosystem drift analysis

The platform can identify:

* shadowed dependencies
* duplicate major versions
* conflicting ecosystems
* dependency version drift

Example:

```text
Jackson 2.x + Jackson 3.x
```

classified as:

```text
WARNING
```

instead of immediate failure.

---

## Runtime Validation & Risk Governance

After remediation, the platform performs:

* Maven build validation
* test execution
* residual vulnerability verification
* semantic version risk analysis
* compatibility checks

The governance layer supports:

* confidence scoring
* warning classifications
* risk-aware remediation evaluation

instead of simplistic binary pass/fail validation.

---

## Rollback & Recovery

Before each remediation attempt:

* Git checkpoints are created

On remediation failure:

* automatic rollback is applied

This prevents repository corruption and enables safe autonomous retries.

---

# Major Components

| Component                        | Responsibility                              |
| -------------------------------- | ------------------------------------------- |
| Planner Agent                    | Generates remediation strategies            |
| Patch Engine                     | Applies deterministic dependency operations |
| PomService                       | Safely modifies pom.xml                     |
| EffectivePomService              | BOM-aware dependency analysis               |
| DependencyGraphService           | Parses dependency trees                     |
| EvaluatorService                 | Runtime validation and governance           |
| VulnerabilityVerificationService | Detects residual vulnerable versions        |
| RiskAnalysisService              | Confidence and risk scoring                 |
| SemanticVersionService           | Upgrade risk analysis                       |
| OutputParserService              | Structured LLM output sanitization          |
| CheckpointService                | Git rollback and recovery                   |
| TerminalService                  | Shell/Maven execution                       |
| GitService                       | Git diff and MR integration                 |

---

# Technology Stack

## AI & Orchestration

| Area               | Technology                   |
| ------------------ | ---------------------------- |
| Agent Framework    | OpenAI Agents SDK            |
| Protocol           | MCP (Model Context Protocol) |
| LLM                | GPT-5.5                      |
| Structured Outputs | Pydantic                     |

---

## Backend

| Area          | Technology |
| ------------- | ---------- |
| API           | FastAPI    |
| Async Runtime | asyncio    |
| Validation    | Pydantic   |
| Logging       | structlog  |

---

## Java Ecosystem

| Area       | Technology   |
| ---------- | ------------ |
| Framework  | Spring Boot  |
| Build Tool | Apache Maven |
| Testing    | JUnit        |

---

## DevOps & Infrastructure

| Area       | Technology |
| ---------- | ---------- |
| SCM        | GitLab     |
| CI/CD      | GitLab CI  |
| Containers | Docker     |

---

## Observability

| Area       | Technology |
| ---------- | ---------- |
| Tracing    | Langfuse   |
| Metrics    | Prometheus |
| Dashboards | Grafana    |

---

# Security & Governance

## Human-in-the-Loop Approval

PatchPilot never auto-merges changes.

Workflow:

```text
AI creates MR
→ developer reviews
→ developer approves
→ merge occurs
```

---

## Sandboxed Execution

All remediation operations run inside:

* isolated repository clones
* restricted environments
* containerized workflows

---

## Auditability

The platform tracks:

* vulnerabilities analyzed
* dependency changes
* commands executed
* validation results
* merge requests created

---

# Current Scope

PatchPilot intentionally focuses on a single ecosystem to maintain high-quality remediation intelligence.

| Area       | Stack                      |
| ---------- | -------------------------- |
| Language   | Java                       |
| Framework  | Spring Boot                |
| Build Tool | Maven                      |
| SCM        | GitLab                     |
| Scanner    | GitLab Dependency Scanning |
| Runtime    | Python                     |

The platform currently trusts external scanners such as:

* GitLab Dependency Scanning
* Dependabot
* Snyk

and focuses specifically on intelligent remediation orchestration rather than vulnerability discovery itself.

---

# Key Capabilities

PatchPilot currently supports:

* autonomous dependency remediation
* Maven ecosystem reasoning
* BOM-aware upgrades
* dependency graph intelligence
* rollback recovery
* runtime validation
* evaluator–optimizer retry loops
* residual vulnerability verification
* semantic version risk analysis
* risk-aware governance
* structured remediation planning

---

# Why This Project Is Strong

PatchPilot demonstrates advanced AI systems engineering concepts including:

* evaluator–optimizer loops
* autonomous remediation
* deterministic execution
* runtime validation
* dependency graph intelligence
* rollback recovery
* failure-aware planning
* semantic version reasoning
* structured tool orchestration
* enterprise DevSecOps workflows

This goes significantly beyond:

* generic chatbot applications
* basic RAG demos
* wrapper-style AI projects

because it solves a real enterprise software supply chain security problem.

---

# Future Enhancements

Potential future capabilities include:

* compatibility risk scoring
* changelog analysis
* Slack/MS Teams notifications
* organization-wide remediation
* multi-repository orchestration
* advanced regression analysis
* automated rollback strategies
* semantic migration analysis

---

# Final Vision

PatchPilot AI aims to become:

> An autonomous dependency remediation and governance platform for enterprise software ecosystems.

The platform proactively:

* fixes vulnerabilities
* reduces manual remediation effort
* improves engineering velocity
* prevents merge blockers
* integrates directly into enterprise DevSecOps workflows

through intelligent AI-driven orchestration combined with deterministic runtime validation.
