# Post-mortem: jev-qualification-01

Healing Helping Hands / vishesh/codex-regrowth-docs / S0 / 2026-10-04 UTC. Source 8be7fece2b16035609fde1d4832c1320aab5f0a0. Pre-run: jev-qualification-01-pre.md. Disposition: repair-and-rerun for an option-order transport defect; semantic gate passed.

60 assigned, started, completed, graded and analyzed; 20/20 for SUPPORT, REFUTE and UNCERTAIN. No schema, provider or snapshot mismatch. Actual charge $0.001091832. All responses were served by TypeSafe as typesafe/jev-1.13-20260917. Reservations, including the prior calls, remain in the same local ledger. Credentials remained local and did not enter the remote worker or artifacts.

A source review after execution found a measurement-control defect: the relay used sorted-key canonical JSON for both request hashing and transmission. That reordered the criteria keys and erased the intended option-order rotation. The 60/60 result stands for the interface actually transmitted; it does not establish robustness to option ordering. Do not conceal this or treat those same cases as fresh after repair.

Repair: keep wire JSON insertion order; hash the exact wire representation; include a documented request-group identifier that is not passed to the model, so repeated documents in distinct scout positions/seeds remain separate counted calls. Test order preservation and duplicate rejection offline. The next pilot must first pass a new 60-case qualification with fresh phrasings and correctly recorded wire order. Preserve this attempt, model pins, competence gates and cumulative dollar cap.

A confusion matrix and class counts are the relevant view. There are no swarm frames in this qualification. Model comparisons across these differing development/qualification sets remain descriptive, not a paired superiority test.
