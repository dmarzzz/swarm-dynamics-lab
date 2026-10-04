# Experiment setup record: [study ID / version]

## Default experiment spending authorization

Owner directive, 2026-10-04 UTC: when the owner directs launching a Vishesh-owned experiment without specifying a budget, USD 2 total is already approved. Do not ask again for approval of that default amount. An explicit experiment-specific budget takes precedence, including a smaller cap; existing budgets are not reset or topped up. Phantom Coast retains its explicit USD 5 total cap and accumulated spend.

The default is cumulative per experiment, covering all stages, qualification, attempts, retries, coordinator/model/tool charges and incremental infrastructure costs. A new stage, restart, machine, ledger or renamed continuation does not create another USD 2 allowance. Carry actual spend and unresolved reservations forward. Record the default owner directive as the budget authority, resolve a concrete cap and request envelope before launch, reserve costs before dispatch and stop at the remaining limit. Any increase beyond the applicable cap needs owner authorization.

This standing budget approval applies when an experiment is directed to launch; it does not start experiments automatically, authorize other researchers' spending or replace public-plan, qualification, source/runtime, credential or approved-account/allocation checks. Generic shared templates remain disabled until the operator fills the study-specific budget and admission evidence; use this default as that budget authority rather than requesting a redundant USD 2 confirmation.


## Researcher review is optional for Vishesh-owned experiments

Owner directive, 2026-10-04 UTC: skip the researcher-review step for Vishesh-owned experiments, including Phantom Coast. No independent researcher, design, dossier or researcher sign-off is required to prepare, qualify or launch these experiments. This supersedes the earlier single-review requirement and conflicting researcher-approval launch gates in study plans and runbooks. The owning agent completes the pre-run assessment, resolves known substantive defects and records limitations; optional feedback must not become a blocking approval step.

Keep prospective plans and public registration, offline checks, bounded native qualification, honest analysis, original spending limits, secure credentials, current exclusive approved-account allocation, and source/runtime verification. Continue prior-art work and record research scope honestly, but do not reintroduce the skipped reviewer as a research-scope sign-off. A waived review is recorded as not required by owner direction, never as passed, independent validation or formal hypothesis acceptance. Preserve historical reviews and immutable plans. Other researchers' policies are unchanged. Update legacy launcher review gates before use rather than supplying a fabricated approval receipt.


Status: DRAFT — not launch authorization. Follow [the setup runbook](../EXPERIMENT-SETUP.md); update this link when copying into the study. Replace bracketed fields. Preserve historical receipts and attempts.

## Ownership and question

- Owner / operator / design reviewer / review independence: [fill]
- Question, intended decision, primary contrast and claim boundary: [fill]
- Research status: [hunch / exploratory instrument / accepted hypothesis / replication]
- Prior art, survey/hypothesis gates and reviews: [evidence links and unresolved requirements]
- Previous study/post-mortem and lessons incorporated: [links]
- Current stage / next action / exact blocker and responsible owner: [fill]

## Gate evidence

Use pending, pass, fail or blocked. Record reviewer and timestamp beside evidence. Do not mark pass while required evidence is missing. Repeat G3 and G5 for every attempt.

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pending | | |
| G1 Plan written before implementation | pending | | |
| G2 Instrument and offline checks | pending | | |
| G3 Current attempt admission | pending | | |
| G4 Qualification before scientific escalation | pending | | |
| G5 Reconciliation and closeout | pending | | |

## Design and instrument index

- Plan and amendment history: [path, version/hash, creation/publication times]
- Scenario contracts, controls, primary metric and analysis plan: [links]
- Independent units; agents/world; worlds/scenario/arm; paired assignment count: [fill]
- Sample-size or pilot precision justification; claim limitations: [fill]
- Development / S0 / repair / S1 / held-out split: [manifest; avoid exposing sealed labels]
- Agent definition, effective prompts, context/access and source snapshots: [paths/hashes]
- Model/provider/config/source/evaluator/dependency versions: [manifest]
- Startup/reset/fork script and command; leakage and treatment-diff checks: [evidence]
- Offline known-answer, negative-control, fault and replay checks: [evidence]
- Launcher gate integration and bypass audit: [entry points checked, evidence, remaining gaps]
- Visualization mapping, history retention and supported public fallback: [link]

## Current attempt admission

Operations entry: [registry study ID or explicitly manual]. Follow the
[operations guide](../OPERATIONS.md), correcting this link when copying the template. Reference
existing records rather than maintaining a second copy of their status.

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | | |
| Prepare named stage | | |
| Dispatch named stage | | |
| Resume interrupted execution | | |
| Analyze saved evidence and rebuild visuals | | |
| Stop this study and close out | | |

Keep private configuration, allocation receipts and ledger paths in local context. A registered
command is not an approved attempt. Record the prepared packet, configuration delta and parent
attempt when using the shared interface; preserve its consumed/ambiguous state after interruption.

- Attempt / parent / stage / pre-run assessment / status: [fill]
- Exact immutable public plan URL, revision and expected hash: [fill]
- Registered experiment TLDR: [question, treatment, comparator, metrics, limitations]
- Condition-specific run TLDRs and run-ID/arm/seed bindings: [manifest]
- Public preflight receipt and actual page verification time/evidence: [fill]
- Qualified source match or bounded diagnostic scope: [fill]
- Existing budget authority reference; reservation; calls/tokens/spend/time/concurrency caps: [non-secret metadata]
- Shared remaining quota, deadline, retry and stopping rules: [fill]
- Dedicated exclusive allocation, claim/expiry and workload verification: [approved public metadata only]
- If provisioning: approved-account match, intended state/project and exact plan verification: [status and private receipt reference only; no account IDs]
- Deployment/source/dependency/output-destination verification: [receipt]
- Credentials: [exact project-specific store alias/account and availability status only, never values]
- Credential transfer: [Swarm Lab credential policy version, registered destination/access and exclusive claim verified, SSH host identity checked, single-key payload validated, memory-only lifetime/core dumps disabled; no general-key fallback]
- Frozen assigned manifest and exact execution command: [no secrets in arguments]
- Go/no-go decision, decision-maker, time and unresolved blockers: [fill]

A ready assessment does not override a failed runtime check. A fresh current admission is required before each stage and attempt.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

| Issue / type | Evidence and cause confidence | Repair and owner | Acceptance check | Verified closure or blocker |
|---|---|---|---|---|

## Closeout

- Execution / response validity / qualification / scientific conclusion / process compliance / reporting status: [separate fields]
- All outcomes and failed attempts retained; raw-to-summary and visual audit: [links]
- Actual costs, remaining reservation and reconciliation: [non-secret evidence]
- Missingness, exclusions, deviations and retrospective documents: [links]
- Frozen artifact inventory; durable upload/readback verification: [links]
- Experiment workers stopped; claim released after uploads; authorized teardown handoff: [status]
- Next action, acceptance criteria and required authority: [fill]
