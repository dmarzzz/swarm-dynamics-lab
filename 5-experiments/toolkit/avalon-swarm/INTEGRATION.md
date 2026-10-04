# Avalon Swarm tooling integration

This import is an **offline engineering prototype and exploratory design resource**, not an accepted team hypothesis, a registered experiment, or an LLM result. It was built before contribution to this repository at the contributor's explicit request. The design choices and thresholds remain provisional.

## Fit with existing work

The closest existing lane is [Avalon swarm hunches](../../studies/dmarz/avalon-swarm-hunches.md) and its [survey task](../../../lab/tasks/survey-avalon-swarm.md). The separate [design task](../../../lab/tasks/design-avalon-swarm.md) explicitly requests a design brief without building a simulation. This imported prototype neither changes that instruction nor completes that task. It is available for later comparison if the team chooses to use it.

The existing hunches cover operator-owned Sybil clusters, communication graphs, concurrent quests, detector roles, fork/merge, and scaling curves. This prototype implements sparse council communication, local Avalon-inspired missions, scripted deceptive claims, audited correction, and consensus failure scoring. It does **not** implement operator-owned Sybil clusters, fork/merge, learned detection, or real-model agents. Overlap with the existing idea is acknowledged; no novelty is claimed.

Use the [shared experiment toolkit](../agent-experiments/INTEGRATION.md) for production study bookkeeping. The repository's source catalogue, survey gate, hypothesis acceptance, and experiment registration requirements continue to apply. Before real collection, promote the chosen design through those gates and freeze its protocol and metrics in the approved experiment directory.

## Offline validation

From the repository root:

```sh
(cd 5-experiments/toolkit/avalon-swarm && python3 -m unittest discover -s tests -v)
python3 5-experiments/toolkit/avalon-swarm/report.py
```

The tests require only the Python standard library. They cover replay, role visibility, routing bounds, repair, legal actions, truth-consensus thresholds, false consensus, fragmentation, and absorbing failure after a patience deadline.

To regenerate the current scripted scale check and original recovery examples, use new output directories under ignored data:

```sh
python3 5-experiments/toolkit/avalon-swarm/benchmark.py --sweep --recovery repair --out data/avalon-consensus-v02
python3 5-experiments/toolkit/avalon-swarm/results/reference-v01/benchmark.py --n 100 --recovery-sweep --replicates 5 --out data/avalon-recovery-v01
```

The second command uses the archived source to reproduce the historical version 0.1 pilot and its event logs. Version 0.2 retains the original seeded worlds but changes scoring and log content. Compare matching versions and seeds. Timing measurements are host-specific.

Committed results contain small plans, world outcomes, source hashes, and a historical source snapshot. Full generated event logs and caches are excluded. The report verifies source identity, planned outcomes, paired initialization, routing limits, and consensus scoring invariants; it does not certify a scientific effect or a production isolation boundary.

## Interpretation

At default version 0.2 thresholds, all fifteen scripted scale-check worlds fail the truth-consensus gate at round five. Execution still completes so recovery trajectories remain visible. This is a stress test of simple policies, not evidence that an LLM swarm necessarily collapses. The defaults need development-set calibration before held-out model evaluation.

No credentials, network calls, provider integration, model results, paid runs, or external actions are part of this tool. Agent and role IDs in results are synthetic. Protocol citations are a focused reading trail, not a substitute for the canonical source catalogue or a completed novelty review.
