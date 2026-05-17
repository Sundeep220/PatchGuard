# PatchPilot

# Final Detailed Enterprise Integration Plan

This is the FINAL consolidated implementation and integration plan for PatchPilot based on all architectural discussions and refinements.

PatchPilot is now designed as:

# an autonomous dependency remediation platform integrated into existing enterprise GitLab CI/CD ecosystems.

It:

* consumes existing enterprise dependency scanning reports
* autonomously remediates HIGH/CRITICAL vulnerabilities
* validates fixes locally
* creates remediation branches and MRs automatically
* preserves existing enterprise CI/CD governance

This architecture is:

* production realistic
* CI/CD native
* governance safe
* enterprise compatible
* incrementally deployable

---

# 1. FINAL ARCHITECTURE OVERVIEW

---

# High-Level System Design

```text id="j8v2tk"
Enterprise Scheduled Pipeline
        ↓
Enterprise Build Stage
        ↓
Enterprise Security Scans
(SAST / Dependency Scan / Container Scan / KICS)
        ↓
Dependency Scan Artifact Generated
        ↓
PatchPilot Remediation Job Starts Automatically
        ↓
PatchPilot Repository Cloned
        ↓
PatchPilot Reads Vulnerability Report
        ↓
PatchPilot Creates Ephemeral Workspace
        ↓
PatchPilot Clones Target Repository
        ↓
PatchPilot Creates Remediation Branch
        ↓
PatchPilot Runs Autonomous Remediation Engine
        ↓
PatchPilot Runs Local Maven Validation
        ↓
PatchPilot Commits Changes
        ↓
PatchPilot Pushes Remediation Branch
        ↓
GitLab Automatically Starts Enterprise CI
        ↓
Build
Unit Tests
Integration Tests
SAST
Dependency Scanning
Container Scanning
Quality Gates
        ↓
PatchPilot Creates Merge Request
        ↓
Human Review + Merge
```

This is the FINAL architecture.

---

# 2. REPOSITORY STRUCTURE

---

# Repository A

# PatchPilot Platform Repository

Example:

```text id="x5m7qp"
platform/patchpilot
```

Contains:

* AI agents
* remediation engine
* evaluator loop
* GitLab integration
* orchestration logic
* dependency governance intelligence
* MR generation
* Git operations

This is:

# the autonomous remediation platform

---

# Repository B

# Target Spring Boot Repository

Example:

```text id="u8v2tx"
backend/payment-service
```

Contains:

* actual application code
* existing GitLab CI/CD
* enterprise governance
* deployment pipelines

PatchPilot integrates INTO this repo’s pipeline.

VERY important distinction.

---

# 3. FINAL EXECUTION MODEL

We selected:

# Embedded GitLab CI Runner Architecture

Meaning:

# PatchPilot runs INSIDE GitLab CI automatically.

NOT:

* manual execution
* external webhook service
* centralized orchestrator server

This is the correct architecture for current scope.

---

# 4. EXISTING ENTERPRISE REALITY

The enterprise already has:

* existing `.gitlab-ci.yml`
* build stages
* test stages
* deploy stages
* centralized security scanning
* compliance pipelines
* organization-managed GitLab policies

Examples:

* SAST
* dependency scanning
* container scanning
* KICS
* quality gates

PatchPilot MUST:

# integrate safely into this ecosystem

NOT replace it.

---

# 5. FINAL PIPELINE STRATEGY

---

# IMPORTANT:

# PatchPilot should NOT run on every pipeline

PatchPilot ONLY runs on:

# scheduled remediation pipelines

This prevents:

* remediation noise
* feature branch interference
* accidental deploy interactions
* race conditions

VERY important production safeguard.

---

# 6. SCHEDULED PIPELINE CONFIGURATION

Inside GitLab:

## CI/CD

→ Schedules
→ New Schedule

---

# Configuration

Pipeline Name:

```text id="g3m8vk"
PatchPilot Dependency Remediation
```

Branch:

```text id="w7v1tx"
master
```

Frequency:

```text id="k5m2qp"
every 2–3 days
```

Variables:

```yaml id="p9x4rm"
PATCHPILOT_PIPELINE=true
```

This variable becomes:

# the orchestration trigger.

---

# 7. FINAL `.gitlab-ci.yml` INTEGRATION

PatchPilot EXTENDS existing enterprise pipelines.

It DOES NOT replace them.

---

# Existing Enterprise Pipeline

Example:

```yaml id="v6m1tk"
stages:
  - build
  - test
  - deploy
```

---

# Updated Enterprise Pipeline

```yaml id="n2v8qp"
stages:
  - build
  - test
  - patchpilot_remediation
  - deploy
```

Existing stages remain untouched.

VERY important.

---

# 8. FINAL PATCHPILOT JOB

Example:

```yaml id="y4m7tx"
patchpilot_remediation:
  stage: patchpilot_remediation

  image: python:3.12

  rules:
    - if: '$PATCHPILOT_PIPELINE == "true"'

  before_script:
    - git clone https://gitlab.com/platform/patchpilot.git
    - cd patchpilot
    - pip install -r requirements.txt

  script:
    - python run_patchpilot_ci.py

  artifacts:
    when: always
    paths:
      - reports/
```

IMPORTANT:

* normal developer pipelines skip this job
* ONLY scheduled remediation pipelines run it

VERY important.

---

# 9. FINAL ARTIFACT FLOW

Enterprise security scans already generate:

```text id="r8v2qp"
gl-dependency-scanning-report.json
```

PatchPilot:

# consumes this artifact directly

NO GitLab API needed for:

* pipeline discovery
* artifact lookup

This simplifies architecture significantly.

---

# 10. FINAL PATCHPILOT ORCHESTRATOR

File:

```text id="f5m8tx"
run_patchpilot_ci.py
```

This becomes:

# the autonomous orchestration entrypoint

---

# Responsibilities

```text id="z1v7rk"
1. Read GitLab environment variables
2. Detect scheduled remediation execution
3. Read dependency scan artifact
4. Parse vulnerabilities
5. Filter HIGH/CRITICAL vulnerabilities
6. Create ephemeral remediation workspace
7. Clone target repository
8. Create remediation branch
9. Run autonomous remediation engine
10. Run local Maven validation
11. Commit remediation changes
12. Push remediation branch
13. Create merge request
14. Exit
```

NO manual execution.

---

# 11. PATCHPILOT EXECUTION FLOW

# STEP BY STEP

---

# STEP 1

Enterprise scheduled pipeline starts.

---

# STEP 2

Enterprise build + security scans execute.

---

# STEP 3

Dependency scanning artifact generated:

```text id="q4m2vk"
gl-dependency-scanning-report.json
```

---

# STEP 4

PatchPilot remediation job starts automatically.

---

# STEP 5

PatchPilot repository cloned:

```bash id="t7v1tx"
git clone https://gitlab.com/platform/patchpilot.git
```

---

# STEP 6

PatchPilot starts:

```bash id="p8m4qp"
python run_patchpilot_ci.py
```

---

# STEP 7

PatchPilot reads:

* GitLab environment variables
* vulnerability artifact

---

# STEP 8

PatchPilot creates ephemeral remediation workspace:

```text id="m6v2rk"
tmp/patchpilot/<pipeline-id>
```

---

# STEP 9

PatchPilot clones TARGET repository into isolated workspace.

Example:

```bash id="x9m7tx"
git clone https://gitlab.com/backend/payment-service.git
```

This becomes:

# the isolated remediation workspace

VERY important.

---

# STEP 10

PatchPilot creates remediation branch:

```text id="k3v8qp"
patchpilot/remediation-<pipeline-id>
```

Example:

```text id="g5m1vk"
patchpilot/remediation-182734
```

---

# STEP 11

PatchPilot runs autonomous remediation engine.

Uses:

* evaluator–optimizer loop
* BOM analysis
* dependency graph intelligence
* risk-aware validation
* rollback recovery

ALL inside isolated workspace.

---

# STEP 12

PatchPilot runs local validation:

```bash id="w8m2tx"
mvn clean test
```

This provides:

# fast-feedback validation

VERY important.

---

# STEP 13

If remediation succeeds:

* commit changes
* push remediation branch

Else:

* rollback
* retry remediation loop

---

# STEP 14

GitLab automatically starts enterprise CI on remediation branch.

This executes:

* build
* unit tests
* integration tests
* SAST
* dependency scanning
* container scanning
* quality gates

This remains:

# final enterprise validation authority

VERY important.

---

# STEP 15

PatchPilot creates merge request.

---

# 12. MERGE REQUEST STRATEGY

---

# MR Title

Examples:

```text id="r2m7vk"
[PatchPilot] Fix HIGH vulnerabilities in Jackson + Logback
```

OR:

```text id="d6v1tx"
[PatchPilot] Remediate 3 HIGH dependency vulnerabilities
```

---

# MR Description Includes

| Section                | Content               |
| ---------------------- | --------------------- |
| vulnerabilities fixed  | CVEs                  |
| dependencies updated   | versions              |
| confidence score       | evaluator output      |
| warnings               | ecosystem coexistence |
| validation results     | mvn clean test        |
| dependency graph notes | BOM restoration       |
| semantic version risks | upgrade risks         |

VERY important for developer trust.

---

# 13. VALIDATION STRATEGY

| Validation Layer            | Responsibility            |
| --------------------------- | ------------------------- |
| PatchPilot local validation | fast remediation feedback |
| Enterprise GitLab CI        | authoritative validation  |
| Human review                | governance + approval     |

This is the correct enterprise model.

---

# 14. SAFETY & GOVERNANCE CONTROLS

---

# Hard Limits

| Limit                         | Purpose                    |
| ----------------------------- | -------------------------- |
| max retries                   | prevent infinite loops     |
| max files changed             | prevent hallucinated edits |
| only pom.xml changes          | safety                     |
| only dependency modifications | scope control              |

---

# MR-Only Policy

Initially:

# PatchPilot NEVER auto-merges

ONLY:

* create branch
* create MR
* wait for human approval

Critical enterprise safeguard.

---

# 15. TESTING & ROLLOUT STRATEGY

We use:

# staged rollout testing

VERY important.

---

# STAGE 1 — Local Simulation

Run:

```bash id="u7m4qp"
python run_patchpilot_ci.py
```

using:

* mocked GitLab variables
* local vulnerability report
* local sandbox repo

NO real GitLab integration yet.

---

# STAGE 2 — Dry Run Mode

Variable:

```text id="c9v2rk"
PATCHPILOT_DRY_RUN=true
```

Behavior:

* no push
* no MR creation
* simulate entire orchestration flow

---

# STAGE 3 — Sandbox GitLab Repository

Test:

* scheduled pipeline
* enterprise scans
* remediation
* MR generation
* CI validation

WITHOUT touching production repos.

---

# STAGE 4 — Controlled Production Rollout

Initial rollout:

* one repo
* one team
* manual approvals only

THEN:

* expand gradually
* onboard more repos
* add governance policies

This is the correct enterprise rollout strategy.

---

# 16. FUTURE EVOLUTION

# (NOT CURRENT SCOPE)

Potential future:

* Dockerized PatchPilot runtime
* internal container registry
* multi-language remediation providers
* centralized remediation platform

But:

# NOT current implementation scope

Correct scoping decision.

---

# 17. FINAL IMPLEMENTATION ORDER

---

# STEP 1

Build:

# `run_patchpilot_ci.py`

CI orchestration entrypoint.

---

# STEP 2

Integrate:

# `.gitlab-ci.yml`

Add:

* PatchPilot remediation stage
* scheduled pipeline rules

---

# STEP 3

Build:

# RepositoryWorkspaceService

Capabilities:

* isolated workspace creation
* repo cloning
* remediation branches
* cleanup

---

# STEP 4

Integrate:

# existing remediation engine

Reuse:

* planner agent
* evaluator loop
* graph intelligence
* BOM analysis
* risk-aware governance

NO rewrite required.

---

# STEP 5

Build:

# GitLabService

Capabilities:

* push remediation branches
* create merge requests
* add MR comments

---

# STEP 6

Build:

# MR generation layer

Generate:

* titles
* descriptions
* remediation summaries
* confidence reports
* warnings

---

# STEP 7

Execute:

# staged rollout testing

Flow:

* local simulation
* dry run
* sandbox GitLab repo
* controlled production rollout

---

# 18. FINAL ARCHITECTURE SUMMARY

```text id="b4m8vk"
Enterprise Scheduled Pipeline
        ↓
Enterprise Security Scans
        ↓
Dependency Scan Artifact Generated
        ↓
PatchPilot Remediation Job Starts
        ↓
PatchPilot Repo Cloned
        ↓
PatchPilot Creates Isolated Workspace
        ↓
PatchPilot Clones Target Repository
        ↓
PatchPilot Creates Remediation Branch
        ↓
PatchPilot Runs Autonomous Remediation
        ↓
PatchPilot Runs Local Maven Validation
        ↓
PatchPilot Pushes Remediation Branch
        ↓
GitLab Automatically Runs Enterprise CI
        ↓
Build
Unit Tests
Integration Tests
SAST
Dependency Scanning
Container Scanning
Quality Gates
        ↓
PatchPilot Creates Merge Request
        ↓
Human Review + Merge
```

This is now the FINAL reviewed enterprise-grade integration architecture for PatchPilot.
