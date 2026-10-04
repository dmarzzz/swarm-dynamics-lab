# Experiment setup record: sybil-split-xmodel v1

Status: prepared, not launched. This record follows [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. The builder made no model call.

## Ownership and question

- **Ownership.**
  - Owner: dmarz.
  - Builder: dmarz/pipeline-split-qwen (Claude Code, offline on dmarz's Mac), working for dmarz/fleet-monitor.
  - Operator: whoever takes the queued request. The server and the model are launcher parameters.
  - Review independence: none. dmarz did not name this study. The fleet monitor chose it under dmarz's instructions of 2026-10-04 to keep experiments running and ship tonight, and, after the Anthropic limit at 11:44Z, to "use opus 5 or an oai model". dmarz waived cross-researcher review for these exploratory runs. dmarz/fleet-monitor's check is a same-researcher check only. The run is not independently reviewed.
- **Question.** Does the parent's identity-splitting contrast hold for two other models reading byte-identical packets?
  - The models are `qwen/qwen3.7-flash` (reasoning disabled) and `gpt-6-sol` (reasoning effort low), each run as its own chain and never pooled.
  - The primary is the parent's.
  - Claim boundary: model plus configuration differ from the parent's; simulated identities; the parent's limits apply, including that k changes both the partition and the attacker's internal links.
- **Research status.** Exploratory, in researcher notes. Survey and hypothesis gates are not met, and S2 is disabled.
- **Prior study and lessons.**
  - The parent [sybil-split-opus](../sybil-split-opus/README.md), [post-run review](../sybil-split-opus/reviews/chain-001-post.md): complete_valid_result, primary +0.410 on Opus 5.5.
  - [Pipeline lessons](../pipeline/LESSONS.md): caps and timeouts sized before qualification; one-call probe; read failing answers before any repair.
  - The fleet monitor's lesson of 2026-10-04: test whether a harmless variant of a correct answer would fail a structural validator. Done here with stubs (README, "Answer validation").

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | README and preregistration, 2026-10-04, dmarz/pipeline-split-qwen | formal gates not met; S2 disabled |
| G1 Plan written before implementation | partial | the design was frozen by the fleet monitor's brief (12:00Z) before any code was written, but README, preregistration and design.yaml were committed together with the code in 0ca09f04. No outcome of this study existed then, and none exists now: no model call has been made | none; recorded as a process note |
| G2 Instrument and offline checks | pass (offline, builder's own checks) | see [reviews/chain-001-pre.md](reviews/chain-001-pre.md): selftest 97 OK; offline S0 1,853/1,853 valid, 0 violations, byte identity with the parent proven; manifest current; rehearsals for both models | live routes and the server's Python untested until launch |
| G3 Current attempt admission | pending | pre-run review, status ready | fleet monitor's same-researcher check; run request; exclusive claim per chain; launcher setup |
| G4 Qualification before scientific escalation | pending | P0 and Q0 per model, software-gated | run |
| G5 Reconciliation and closeout | pending | none | run |

## Design and instrument index

- **Plan:** [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [RUN.md](RUN.md), [VISUALIZATION.md](VISUALIZATION.md), [READY.yaml](READY.yaml), [manifest.json](manifest.json).
- **Independent units:** 24 comparison roots per family (the parent's: ring 8233-8256, community 8351-8374), per model.
- **Sample size:** the parent's, 2,688 S1 calls per model. No power claim.
- **Splits and seeds:** all of the parent's: engineering ring 4919-4934 and community 4821-4836, qualification 5139-5148, comparison as above; holdout 10000-19999 unopened. No fresh seed is drawn, so no seed scan applies: reuse of the parent's roots is the design.
- **Agent definition:** one stateless synthesizer call per assignment. The prompt is the parent's plus the answer-shape paragraph. Validation is in `src/study.py`. The adapters `src/provider.py` (OpenRouter) and `src/openai_provider.py` (OpenAI) are the pipeline's reference adapters, copied unchanged.
- **Versions:** requirements.txt pinned. The source hash covers design.yaml, experiment.yaml, requirements.txt and every `src/*.py`.

## Current attempt admission

Ready for the same-researcher check; not admitted.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| 001 / sybil-split-opus chain-001 | S0, P0, Q0, S1 per model | [reviews/chain-001-pre.md](reviews/chain-001-pre.md) | nothing has run | none |

## Closeout

Nothing to close: no run exists.
