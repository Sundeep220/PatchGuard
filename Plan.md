# PatchPilot

## Final Enterprise Production Integration Plan (Reviewed & Refined)

This is the FINAL reviewed architecture based on all discussions and refinements.

PatchPilot is now designed as:

# an autonomous dependency remediation worker integrated into existing enterprise GitLab CI/CD ecosystems.

It:

* DOES NOT replace enterprise pipelines
* DOES NOT replace enterprise security governance
* DOES NOT perform its own scanning

Instead:

# it consumes enterprise dependency scanning outputs and autonomously remediates vulnerabilities.

This architecture is now:

* production realistic
* enterprise compatible
* governance friendly
* rollout safe
* CI/CD native



---

# 1. FINAL PROJECT GOAL

PatchPilot automatically:

✅ consumes dependency scanning reports
✅ filters HIGH/CRITICAL vulnerabilities
✅ runs autonomous dependency remediation
✅ validates fixes locally
✅ creates remediation branches
✅ creates merge requests automatically
✅ integrates into existing enterprise GitLab pipelines

WITHOUT developers manually:

* analyzing reports
* fixing dependency versions
* resolving BOM conflicts
* creating remediation MRs

---

# 2. FINAL EXECUTION MODEL

# (IMPORTANT)

We selected:

# Option 1 — Embedded GitLab CI Runner Architecture

Meaning:

# PatchPilot runs INSIDE GitLab CI automatically.

NOT:

```text id="x7m2qp"
manual local execution
```

and NOT:

```text id="p4v8tk"
external webhook server
```

This is the correct architecture for current scope.

---

# 3. IMPORTANT ENTERPRISE REALITY

The enterprise already has:

* existing `.gitlab-ci.yml`
* build stages
* test stages
* deploy stages
* company-managed security policies
* dependency scanning
* SAST
* KICS
* container scanning
* quality gates
* Sonar

These are usually injected using:

* centralized templates
* compliance pipelines
* enterprise GitLab policies

PatchPilot MUST:

# integrate into this ecosystem safely

NOT replace it.

VERY important architectural principle.

---

# 4. FINAL ENTERPRISE PIPELINE FLOW

Current enterprise pipeline already looks conceptually like:

```text id="j8v1tx"
build
   ↓
unit tests
   ↓
enterprise security scans
   ↓
deploy
```

Where:

* dependency scanning artifacts already exist
* security policies already run automatically

GOOD.

PatchPilot becomes:

# a downstream remediation consumer

---

# 5. FINAL PATCHPILOT EXECUTION FLOW

```text id="r4m8vk"
Scheduled Enterprise Pipeline
        ↓
Build Stage
        ↓
Enterprise Security Scans
        ↓
Dependency Scan Report Generated
        ↓
PatchPilot Remediation Job Starts Automatically
        ↓
Reads Vulnerability Report Artifact
        ↓
Creates Ephemeral Workspace
        ↓
Runs Autonomous Remediation Engine
        ↓
Runs Local Maven Validation
        ↓
Commits Changes
        ↓
Pushes Remediation Branch
        ↓
Creates Merge Request
        ↓
Existing Enterprise Pipeline Runs Again
        ↓
Unit Tests
Integration Tests
SAST
Dependency Scanning
Container Scanning
Quality Gates
        ↓
Human Review + Merge
```

This is the FINAL architecture.

---

# 6. FINAL PIPELINE STRATEGY

---

# IMPORTANT:

# PatchPilot should NOT run on every pipeline

PatchPilot ONLY runs on:

# dedicated scheduled remediation pipelines

This prevents:

* remediation noise
* accidental feature-branch remediation
* deploy pipeline interference
* race conditions

VERY important.

---

# 7. SCHEDULED PIPELINE CONFIGURATION

Inside GitLab:

## CI/CD

→ Schedules
→ New Schedule

---

## Configuration

Pipeline Name:

```text id="f5m2qp"
PatchPilot Dependency Remediation
```

Branch:

```text id="z8v1tk"
master
```

Frequency:

```text id="u4m7rx"
every 2–3 days
```

Variables:

```yaml id="q9x3vp"
PATCHPILOT_PIPELINE=true
```

This variable becomes:

# the orchestration trigger

---

# 8. FINAL `.gitlab-ci.yml` INTEGRATION

We DO NOT rewrite existing pipelines.

We EXTEND them safely.

---

# Existing Pipeline Example

```yaml id="h2m8tw"
stages:
  - build
  - test
  - deploy
```

---

# Updated Enterprise Pipeline

```yaml id="y6v2qp"
stages:
  - build
  - test
  - patchpilot_remediation
  - deploy
```

IMPORTANT:

* existing stages remain untouched
* enterprise governance remains authoritative

---

# 9. FINAL PATCHPILOT JOB

Example:

```yaml id="p8m4tx"
patchpilot_remediation:
  stage: patchpilot_remediation

  image: python:3.12

  rules:
    - if: '$PATCHPILOT_PIPELINE == "true"'

  before_script:
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

# 10. IMPORTANT ARCHITECTURAL IMPROVEMENT

Initially we considered:

# PatchPilot querying pipelines manually

We REMOVED that design.

Why?

Because:

# PatchPilot already runs INSIDE the correct scheduled pipeline.

This simplifies architecture massively.

---

# 11. FINAL ARTIFACT FLOW

Enterprise security scans already generate:

```text id="x5m1vk"
gl-dependency-scanning-report.json
```

PatchPilot:

# directly consumes this artifact inside CI workspace

NO GitLab API needed for:

* artifact retrieval
* pipeline searching

This is MUCH cleaner.

---

# 12. FINAL PATCHPILOT ORCHESTRATOR

File:

```text id="t2v8qp"
run_patchpilot_ci.py
```

This becomes:

# the autonomous orchestration entrypoint

---

# Responsibilities

```text id="g7m2tx"
1. Read GitLab environment variables
2. Detect scheduled remediation context
3. Read dependency scanning artifact
4. Parse vulnerabilities
5. Filter HIGH/CRITICAL vulnerabilities
6. Create ephemeral remediation workspace
7. Create remediation branch
8. Run autonomous remediation engine
9. Run local Maven validation
10. Commit changes
11. Push remediation branch
12. Create merge request
13. Exit
```

NO manual execution.

---

# 13. LOCAL VALIDATION STRATEGY

PatchPilot MUST still run:

```bash id="v4m8rk"
mvn clean test
```

locally BEFORE pushing changes.

---

# WHY THIS IS CRITICAL

Without local validation:

* broken MRs get generated
* CI pipelines fail constantly
* developer trust decreases

So:

# PatchPilot provides fast-feedback validation

while:

# enterprise GitLab CI remains final validation authority

VERY important distinction.

---

# 14. FINAL VALIDATION MODEL

| Layer                       | Responsibility            |
| --------------------------- | ------------------------- |
| PatchPilot local validation | fast remediation feedback |
| Enterprise GitLab CI        | authoritative validation  |
| Human review                | governance + approval     |

This is the correct enterprise model.

---

# 15. REMEDIATION WORKSPACE STRATEGY

PatchPilot NEVER edits directly inside:

```text id="q3v7tk"
CI checkout workspace
```

Instead:

```text id="w9m2xp"
tmp/patchpilot/<pipeline-id>
```

Benefits:

* isolation
* rollback safety
* deterministic builds
* concurrent remediation support

VERY important.

---

# 16. REMEDIATION BRANCH STRATEGY

Branch format:

```text id="m8v1qp"
patchpilot/remediation-<pipeline-id>
```

Example:

```text id="f6m4tx"
patchpilot/remediation-182734
```

Guarantees uniqueness.

---

# 17. MERGE REQUEST STRATEGY

---

# MR Title

Dynamic format:

```text id="y1x8vk"
[PatchPilot] Fix HIGH vulnerabilities in Jackson + Logback
```

OR:

```text id="t5m2qp"
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

VERY important for trust and reviewability.

---

# 18. SAFETY & GOVERNANCE CONTROLS

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
* wait for human review

Critical enterprise safeguard.

---

# 19. TESTING & ROLLOUT STRATEGY

We DO NOT deploy directly to production repos.

We use:

# staged rollout testing

VERY important.

---

# STAGE 1 — Local Simulation

Run:

```bash id="z2m7tx"
python run_patchpilot_ci.py
```

using:

* mocked GitLab variables
* local vulnerability report
* local sandbox repo

Validates:

* orchestration flow
* remediation engine
* branch creation
* MR payload generation

NO GitLab integration yet.

---

# STAGE 2 — Dry Run Mode

Add:

```text id="k8v3qp"
PATCHPILOT_DRY_RUN=true
```

Behavior:

* no actual push
* no actual MR creation
* simulate entire workflow locally

VERY important safety stage.

---

# STAGE 3 — Sandbox GitLab Repository

Create:

# dedicated test repository

Test:

* scheduled pipeline
* enterprise scans
* PatchPilot remediation
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
* add governance policies
* onboard more repos

This is EXACTLY how enterprise rollout should happen.

---

# 20. MULTI-REPO SUPPORT

PatchPilot already supports:

# generic Spring Boot repositories

because:

* effective POM analysis is dynamic
* dependency graph parsing is dynamic
* remediation engine is generic
* evaluator logic is generic

GOOD architecture decision.

---

# 21. FUTURE EXTENSIBILITY

# (NOT CURRENT SCOPE)

Potential future providers:

| Ecosystem | Provider       |
| --------- | -------------- |
| Maven     | MavenProvider  |
| Gradle    | GradleProvider |
| npm       | NpmProvider    |
| pip       | PythonProvider |

But:

# not part of current implementation scope

Correct scoping decision.

---

# 22. FINAL IMPLEMENTATION ORDER

---

# STEP 1

Build:

# `run_patchpilot_ci.py`

Autonomous CI orchestration entrypoint.

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

* clone repo
* create remediation branches
* cleanup workspaces
* isolated execution

---

# STEP 4

Integrate:

# existing autonomous remediation engine

Reuse:

* planner agent
* evaluator loop
* dependency graph intelligence
* BOM analysis
* risk-aware governance

NO rewrite required.

---

# STEP 5

Build:

# GitLabService

Capabilities:

* create merge requests
* push remediation branches
* add MR comments

---

# STEP 6

Build:

# MR generation layer

Generate:

* title
* description
* remediation summary
* confidence score
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

# 23. FINAL ARCHITECTURE

```text id="n5m8vk"
Scheduled Enterprise Pipeline
        ↓
Build Stage
        ↓
Enterprise Security Scans
        ↓
Dependency Scan Report Generated
        ↓
PatchPilot Remediation Job Starts Automatically
        ↓
Reads Vulnerability Artifact
        ↓
Creates Ephemeral Workspace
        ↓
Runs Autonomous Remediation Engine
        ↓
Runs Local Maven Validation
        ↓
Commits Changes
        ↓
Pushes Remediation Branch
        ↓
Creates Merge Request
        ↓
Existing Enterprise CI Executes Again
        ↓
Build
Unit Tests
Integration Tests
SAST
Dependency Scanning
Container Scanning
Quality Gates
        ↓
Human Review + Merge
```

This is now the FINAL reviewed enterprise-grade implementation architecture for PatchPilot.
