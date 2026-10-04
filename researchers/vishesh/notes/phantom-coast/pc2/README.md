# Phantom Coast PC-2: observation-choice contract

**Native runner implemented and 44 offline checks pass; no native PC-2 run.** The parent pilot converged after a full survey and retraction. This successor tests whether misleading reports change what gets inspected when that full survey is unavailable.

- **evidence_confidence: 0/4** for a native adaptive-avoidance or audit-benefit effect. Assessed 2026-10-04 by vishesh/codex-phantom-coast. Software tests provide no evidence that a model will exhibit the effect.
- **sample_size_summary:** Observed adaptive roots: 0. Planned: 4 qualification roots and 8 paired pilot roots in two geometry families; 96 dependent policy episodes and 1,816 total proposed requests. The 44 software tests use development fixtures only.

[Prospective plan](PLAN.md) · [Setup and gates](SETUP.md) · [Immutable publication receipt](PLAN-PUBLICATION.json) · [Contract validation](VALIDATION.json) · [Runner validation](RUNNER-VALIDATION.json) · [Launch instructions](RUNBOOK.md) · [Development post-assessment](reviews/DEVELOPMENT-POST.md).

The implemented contract keeps every cell inspectable, consumes exactly twelve slots including repeats/failures, uses a source-audit slot instead of an extra observation, isolates current-round proposals, and separates actual inspection coverage from map accuracy. Team, single and uniform policies share explicit sensing semantics. The native entry point now adds typed inspection/map requests, admission-gated reserved generation, persistent assignments, a carried-forward budget, qualification scoring, paired analysis and saved-event PNG/GIF replay. Preparation does not open reserved worlds.

From the repository root: `python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/pc2/tests -v`.

Researcher review is optional by [owner-directed process amendment](reviews/REVIEW-POLICY-AMENDMENT.md). The next step is current operational admission and native Q0; no external researcher sign-off is needed. G2 passes offline self-validation; G3/G4 remain closed. The previous model-mapping qualification does not qualify adaptive choices. Keep the original dollar cap and historical spend; do not reset the old request ledger. [Parent native results](../RESULTS.md) and [complete measured replay](../visualization/native-replay.html) remain distinct from this unrun successor.
