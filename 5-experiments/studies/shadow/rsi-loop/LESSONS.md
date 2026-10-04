# Evidence to bounded changes

These are curated lessons, not model-generated ground truth. A lesson is a hypothesis about a reusable repair. It requires a provenance link, a counterexample and a fresh acceptance test. Never feed an evaluator's hidden labels to a worker.

## L0: observe command return status, not just the wrapper flag

- Evidence: local development trace projection `shadow-audit-dev`, in `results/episodes.json`: seven explicit nonzero exits, zero wrapper errors. No source text exported.
- Diagnosis: OpenClaw can serialize a completed shell/process call with `isError=false` even when `details.exitCode` is nonzero.
- Change: `trace_loop.py` B1 preserves wrapper errors and separately recognizes typed nonzero exit results. `BRIEF-v1.md` tells the worker to inspect and classify those results.
- Counterexamples: grep returning 1, a deliberate negative-control test, a running job with no terminal code. Nonzero is an observation, not a research-quality label.
- Acceptance: frozen R0 replay, 40/40 recognized versus B0 0/40, no new flags on 702 clean zero exits, one wrapper error retained. This validates the parser change only. No next model run has tested the brief instruction.
- Promotion: parser is available as an offline tool. Scientific or agent-performance promotion is blocked.

## L1: an invalid member does not erase a valid quorum

- Evidence: [independent discussion benchmark review, F1](../review-discussion-benchmark-v3.md), source reviewed at `0f5044a` and `883d310`.
- Diagnosis: scoring all vote metrics through an all-ballots-valid predicate can erase a real 2-of-3 decision when the third ballot is invalid.
- Candidate change: before launch, require mutations for all-valid, one-invalid-with-quorum, lost-quorum and missing-parent cases. Score the decision separately from the validity flag; preserve unknown outcomes and assigned denominators.
- Counterexample: a genuinely missing decision must not be invented from a failed ballot.
- Acceptance: a different researcher derives expected results for a new scorer/task family, then checks candidate and baseline blind. Not run here. This lesson does not certify the current upstream scorer, which may have changed since review.

## L2: failure type is evidence; raw error text is a leak risk

- Evidence: same review, F2. A provider adapter computed `public_reason`, but the journal dropped it.
- Candidate change: require typed `error_class`, `dispatched`, usage completeness and attempt lineage on failure records; copy a vetted enum from `public_reason`, never the exception body. Unknown stays `unknown`.
- Counterexample: stringifying an exception can expose response bodies, URLs or credentials. Guessing a failure class from prose can misclassify a schema failure as infrastructure.
- Acceptance: separately authored timeout, 429, credit, schema and interrupted-stream fixtures each reconcile to the expected class; unknown/no-usage fixture remains unknown. Not run here.

## L3: qualification failure is not a null hypothesis result

- Evidence: [next-experiments reconciliation](../../dmarz/next-experiments-2026-10-04/README.md), especially the market and native influence cohorts; [run assessment and repair cycle](../../../toolkit/agent-experiments/RUN-REVIEW.md).
- Candidate change: brief must distinguish execution complete, instrument qualified, valid negative result and remaining repair. Preserve every assigned attempt across model/prompt changes.
- Counterexample: a valid adverse model decision is not a parser bug and must not be tuned away on evaluation data.
- Acceptance: independent blind review of new analysis tasks, with equal credit for warranted null and positive conclusions. Not run here.
