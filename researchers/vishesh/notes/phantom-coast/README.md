# Phantom Coast: PC-1

**Latest design iteration:** [review and changes](ITERATION-02.md), [PC-2 prospective plan](pc2/PLAN.md), and [complete measured PC-1 replay](visualization/native-replay.html). PC-2 has 20 passing software checks and no native outcomes.

**Native Q0 and S0 completed.** [Results](RESULTS.md): 540 valid map requests, no final history disagreement across six pilot worlds, $0.162723246 API cost. [Public experiment and replays](https://swarm-live.pages.dev/#/x/phantom-coast). The existing Mars host was released after verified delivery. See [current status](LIVE-READINESS.md) and [setup evidence](SETUP.md). Historical offline files below remain instrument-development evidence, not native outcomes.

The assessment below predates S0 and is retained at its stated evidence cutoff; the new results above do not imply an independent review upgrade.

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `b51e3f1f` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Native Jev passed the clean synthetic mapping screen; the history-persistence effect remains unestablished. Basis: All 18 clean maps were valid and correct across six generated worlds. This qualifies the clean mapping contract only; 648 cell choices and three observers per world are dependent, and no history-persistence cohort result is tracked at this cutoff.
- **sample_size_summary:** Q0: 6 world roots × 3 observers = 18/18 valid maps, 648/648 cells correct. Gated S0 plans 6 new paired worlds and 522 map requests; no S0 effect result tracked.
<!-- experiment-evidence:end -->

- [Prospective plan](PLAN.md): paired worlds, eight swarm trajectories, pooled/deterministic baselines, qualification criteria, and separately gated adaptive extension.
- [Historical offline assessment](REPORT.md): evaluation against the handoff and plan, with explicit launch blockers.
- [Fixture replay](visualization/index.html): saved deterministic software fixtures, including missing responses. Download/open locally or serve this folder; GitHub does not render the HTML as a running page.
- [Validation receipt](VALIDATION.json), [pre-assessment](reviews/OFFLINE-01-PRE.md), [post-assessment](reviews/OFFLINE-01-POST.md).
- [Public plan receipt](PLAN-PUBLICATION.json): immutable content verified; no run registration claimed.

From the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/tests -v
python3 researchers/vishesh/notes/phantom-coast/src/build_replay.py
```

Both commands are offline software validation. They make zero model calls. The default generator rejects qualification and holdout seeds. The separate native worker requires explicit stage, spending, source, public-plan and fresh allocation bindings. The replay is a development fixture, not evidence that a model fails or recovers.

Source layout: `instrument.py` builds actor packets, validates responses, tracks source identity, computes fixed-quorum maps and missingness bounds, schedules development assignments, and reconciles outcomes. `build_replay.py` renders saved fixtures using `replay-template.html`. Tests check semantic invariants, fault accounting and hand-calculated scoring.
