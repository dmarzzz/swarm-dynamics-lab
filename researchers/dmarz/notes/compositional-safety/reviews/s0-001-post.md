# Post-mortem: s0-001

- Experiment / owner / stage: compositional-safety / dmarz / S0, 2026-10-04 UTC.
- Parent: first server attempt. Pre-run: [s0-001-pre.md](s0-001-pre.md).
- Source: `84fad81e3b8732e195a24f9ef4cf1a09ef76c7b5`; full hashes in the hub manifest. Scripted backend, no model.
- Disposition: advance to bounded Q0 after the documented pre-model scheduling repair.

## What ran and what happened

84 planned → 84 started → 84 terminal → 84 graded → 84 analyzed. Unique episode IDs reconciled to all assignments; no missing or duplicate episodes. 84/84 valid, 84/84 safe completions, zero committed violations, six structural fingerprints. Each of D1/D2/D3 completed 28/28 safely across C/S/F/R/P/G/H. This is scripted solvability under privileged state, not evidence of model competence or the scientific effect.

Elapsed 94.49 seconds. Zero model calls, tokens, actual or reserved API spend. Twelve bundle runs plus one analysis run are done on the hub. Reproduction: `python3 src/worker.py S0 s0-001` at the recorded revision in a fresh output location; never reuse the original attempt ID/accounting for a model request. Summary: [records/s0-001-summary.json](../records/s0-001-summary.json).

## Visualization review

Twelve live progress images, twelve final PNGs and twelve GIF replays were uploaded, with per-bundle traces. The analysis run carries manifest, episodes, dispatch/trace logs, source hashes and summary. Remote artifact counts are four per bundle and eight on analysis; reporting spool is empty. Every downloaded file matches its recorded SHA256; every GIF decodes with multiple frames at 1600×900. A D2 control visualization was visually checked against the raw event scorer. Zero violations and completed labels match this run's reference outcomes. No rendering failures. GIFs show event order, not actual model latency. The reference policy rarely needs information retrieval, so this cannot validate the cost or effectiveness of a model's coordination.

## Experiment-quality assessment

Execution and reporting passed. The initial reference's privileged knowledge concealed a scheduling risk: finding a public source last among seven and applying three packaging steps can need 35 turns for a compliant history-only team. A new explicit regression fails under 24 and completes under 40. This is a design defect caught before any model data, not a failed model result. The original 24-turn S0 manifest/results remain unchanged. Q0 now has a 40-turn ceiling and stronger per-baseline competence gates.

The task grammar remains small; six shapes cannot support scaled causal inference. H has complete state and atomic enforcement, which is an expected engineering bound. No novelty, strategic incentives or transfer claim is justified. Existing survey/prior-defense and generalization work remains open; the user's internal-review override is recorded without fabricating outside endorsement.

## Failure and repair ledger

| ID / kind | Evidence | Cause / repair | Acceptance | Status |
|---|---|---|---|---|
| D-01 / design | History-only source-last fixture needs 35 turns | 24-turn cap assumed privileged discovery; increase Q0/P1 cap to 40 | New regression completes in exactly 35, 10-test suite passes | Closed before Q0 |
| D-02 / qualification | Pooled baseline averages can hide one weak architecture | Require .8 per domain separately in C and S | Analyzer changed before model observations | Ready for Q0 |
| E-01 / environment | Non-login SSH lacks provisioned module path | Explicit PYTHONPATH to installed reporting module, isolated pinned venv | 84 server episodes and all 13 hub records verified | Closed |

## Next run

Q0 q0-001 uses disjoint roots 200–202, D1/D2 only, C/S, both variants and the pinned Haiku model. Maximum 960 requests; no retry. Current cumulative study limits are 8,192 requests/$185 reserved inside the owner's shared $500 authorization, not an independent new $500 allocation. Qualification must pass current source hashes before P1. On capability failure, inspect action traces and isolate the failed skill; do not rerun unchanged for a luckier score. The next pre-run freezes the specific model and resource/visualization mapping.
