# Experiment setup record: capture-memory-mix / claude-pool recovery

Adapted from the shared [setup template](../../../../toolkit/agent-experiments/templates/experiment-setup.md). This record is retrospective for the pool attempt and current for offline recovery only. **BLOCKED, not launch authorization.** Follow [EXPERIMENT-SETUP.md](../../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md), [RUN-REVIEW.md](../../../../toolkit/agent-experiments/RUN-REVIEW.md) and [OPERATIONS.md](../../../../toolkit/agent-experiments/OPERATIONS.md). Vishesh-only budget/reviewer waivers in the template do not apply.

## Ownership and question

- Owner: shadow. Historical lane mix-claude-pool. Recovery operator/controller: shadow/sol-mix-astra, Astra,2026-10-04. Independent design reviewer: absent, not supplied by the recovery operator.
- Question: after committed agents are removed, do two memory1 survivors among six improve original-convention return versus all-full memory? Same four scripted roots, paired schedules,20 rounds.
- Status: exploratory diagnostic, no accepted formal hypothesis or behavioral finding claimed. Parent [hypothesis](../../../../../4-hypotheses/shadow-capture-memory.md) remains proposed.
- Prior evidence: parent [README](../README.md), [reading-rule finding](../reading-rule/FINDING.md), [reading-rule post-mortem](../reading-rule/POSTMORTEM-R2.md), [freeze finding](../../capture-memory/freeze-claude/FINDING.md). Same-parent historical model cohorts are not pooled with this lane.
- Current gate: G3 blocked for any new call. Exact next action: publish saved-data closeout and park; later obtain independent review and resolve all admission gaps, not restart the frozen runner.

## Gate evidence

| Gate | Status | Evidence, date and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates |blocked|Parent proposed hypothesis; no lane-specific independent review found,2026-10-04,shadow/sol-mix-astra|Obtain applicable independent review and retain exploratory scope|
| G1 Prospective design |gap|Historical PREREG exists locally but is absent from pre-call source commit8c4ce07e|Publish future plan before dispatch; current recovery cannot fix old chronology|
| G2 Instrument and offline checks |fail|audit_saved.py shows last-item copier passes old11/12 gate with12/12 parseable choices|Prospectively define and test competence/non-copying criterion|
| G3 Current attempt admission |blocked|RECOVERY-ASSESSMENT.md, missing review and dollar ledger, no new dispatch|Reconcile historical exposure and implement reviewed worst-case reservation gate|
| G4 Qualification |blocked|0/12 valid control assignments,20 terminal transport errors|Fresh reviewed qualification after admission, not response substitution|
| G5 Reconciliation and closeout |pass for saved-data recovery|POSTMORTEM.md and deterministic audit; no scientific pass claimed|Preserve package and report blockers|

## Design and instrument index

- Historical plan: PREREG.md preserved verbatim, with publication correction in RECOVERY-ASSESSMENT.md and FINDING.md.
- Source: run.py and scripted-reference.json at8c4ce07e1597e9be8316c940ff91027701efbe4f. Native/source/root hashes in recovery-summary.json. No actor source changed.
- Units: four fixed paired roots160-163, seed1; N12 before removal, six honest survivors; two arms,20 logical rounds; eight episodes,456 scientific decisions,12 controls. No sampled root outcome observed.
- Precision: four-root descriptive bootstrap only; no general population or model-family inference. Qualification histories are separate from scientific roots; original control gate insufficient.
- Model/config: requested claude-sonnet-5-5, max_tokens16, pool Messages interface, concurrency4, no returned-model identity. Raw chronological names, no separate last-answer field, no actor tools or controller memory.
- Startup/fork: root clone, seeded two-of-six short-agent selection; checker recomputes masks and actual planned interaction counts without importing runner. No duplicate execution or resume.
- Offline check: `python3 5-experiments/studies/shadow/capture-memory-mix/claude-pool/audit_saved.py --check`. Separate same-owner implementation, not independent researcher review.
- Bypass audit: frozen run.py's non-prepare entry dispatches without review/public-plan/dollar ledger checks and must not be reused. It also restarts request IDs and overwrites historical summary files. No code repair was represented as tested live admission.
- Visualization mapping: offline counts/assignment tables only. No native temporal history exists, so replay is not applicable. A future admitted run must map root/arm logical-round traces to original-share curves with failures visibly missing.

## Current attempt admission

Manual native study. No automatic operations adapter assumed and none used to launch or to claim review completion.

| Operation | Exact command or unsupported reason | Evidence |
|---|---|---|
| Inspect / offline validation |python3 5-experiments/studies/shadow/capture-memory-mix/claude-pool/audit_saved.py --check|Hashes, assignments and gate negative control|
| Prepare / dispatch / resume |Blocked; no model command authorized by recovery|RECOVERY-ASSESSMENT.md|
| Saved-data analysis |python3 5-experiments/studies/shadow/capture-memory-mix/claude-pool/audit_saved.py|recovery-summary.json and assignments.csv|
| Stop / closeout |No matching worker found; no new worker spawned|Native STOP plus process inspection, POSTMORTEM.md|

- Public preflight: no verified historical plan receipt; no new registered stage. Recovery publication is not prospective admission.
- Budget: USD5 hard recovery lane ceiling, inherited cost/usage unknown, no verified historical reservations. EntireUSD5 administratively held,USD0 admissible new spend. Hold does not prove a billing upper bound. No other lane allocation touched.
- Caps: <=1000 historical lane attempts,20 observed; no new attempts, retries or health probes. Calls stop23:30Z; report push target23:40Z,2026-10-04.
- Resources: local saved-data recovery, no infrastructure provisioned, no fleet claim required for offline audit, no model credential read.
- Provider amendment: none executed. A later admitted switch must prospectively specify anthropic/claude-sonnet-5.5 on OpenRouter with fallbacks off, preserve inherited exposure and qualify the route.
- Go/no-go: NO-GO for calls, shadow/sol-mix-astra,2026-10-04, for review/registration/qualification/budget gaps.

## Attempt and repair history

| Attempt / stage | Evidence | Assigned / started / terminal / valid / analyzed | Disposition |
|---|---|---|---|
| Historical pool qualification |requests.jsonl, responses.jsonl, qualification.json, STOP.json|12 assignments /8 assignments (20 attempts) /20 attempt terminals /0 valid /0 behavioral|Blocked|
| Historical science |Fixed roots and scripted-reference allocation|8 episodes /0 /0 /0 /0|Unstarted|
| Astra recovery |RECOVERY-ASSESSMENT.md, audit_saved.py, POSTMORTEM.md|Saved records only,0 new model calls|Closeout complete, park|

Issues: transport errors retained; parse-only gate defect demonstrated offline; missing preregistration and dollar reservations cannot be retrospectively repaired. No reviewer independence fabricated. See POSTMORTEM issue dispositions and eleven-dimension review.

## Closeout and successor handoff

- Current finding: FINDING.md. Behavioral evidence_confidence0/4,0/4 observed paired roots. All failures and unstarted assignments retained.
- Actual costs/tokens unknown for20 historical attempts; recovery incremental experimental API spendUSD0. Hash inventory and machine-readable counts in recovery-summary.json.
- Original five recovered files and frozen source remain unchanged. Commit only owned claude-pool files with wakesync author and Sol coauthor. Main is concurrent: check, rebase, push and verify saved bytes. No shared metadata registry or joint submission edits.
- No native model frame or animation; tables explicitly distinguish missing outcomes from zero. No worker to stop or new claim to release.
- Exact next-session action: read this record, RECOVERY-ASSESSMENT.md and POSTMORTEM.md before considering a successor. Obtain required independent review, prospectively publish a fixed non-copying/competence gate and reviewed budgeted instrument, reconcile inherited costs and refresh all G3 admission. Do not restart run.py or use old parseability as qualification. No post-deadline calls authorized.
