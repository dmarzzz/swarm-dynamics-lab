# Phantom Coast: PC-1

**Design and offline instrument complete; no native experiment run.** DM-01 asks whether a false map can alter the evidence a swarm gathers. The first stage isolates history-dependent judgment before testing that adaptive loop.

- [Prospective plan](PLAN.md): paired worlds, eight swarm trajectories, pooled/deterministic baselines, qualification criteria, and separately gated adaptive extension.
- [Assessment and remaining work](REPORT.md): evaluation against the handoff and plan, with explicit launch blockers.
- [Fixture replay](visualization/index.html): saved deterministic software fixtures, including missing responses. Download/open locally or serve this folder; GitHub does not render the HTML as a running page.
- [Validation receipt](VALIDATION.json), [pre-assessment](reviews/OFFLINE-01-PRE.md), [post-assessment](reviews/OFFLINE-01-POST.md).
- [Public plan receipt](PLAN-PUBLICATION.json): immutable content verified; no run registration claimed.

From the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/phantom-coast/tests -v
python3 researchers/vishesh/notes/phantom-coast/src/build_replay.py
```

Both commands are offline software validation. They make zero model calls. The generator rejects qualification and holdout seeds, and there is no live dispatcher. The replay is a development fixture, not evidence that a model fails or recovers.

Source layout: `instrument.py` builds actor packets, validates responses, tracks source identity, computes fixed-quorum maps and missingness bounds, schedules development assignments, and reconciles outcomes. `build_replay.py` renders saved fixtures using `replay-template.html`. Tests check semantic invariants, fault accounting and hand-calculated scoring.
