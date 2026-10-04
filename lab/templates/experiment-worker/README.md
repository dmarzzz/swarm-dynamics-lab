# Experiment worker template

This is a distributed **scripted toy**, useful for learning the hub registration, queue, worker and analysis interfaces. Copying it does not satisfy the lab's research gates or make a production launcher. Start a new question or material revision with [the setup runbook](../../../5-experiments/toolkit/agent-experiments/EXPERIMENT-SETUP.md), write the prospective plan before experimental implementation, and maintain the linked setup record in the owned study directory.

For discovery and supported study adapters, use [experiment operations](../../../5-experiments/toolkit/agent-experiments/OPERATIONS.md). This template is not a registered native adapter. The private `swarm-labs-agentops` repository defines infrastructure ownership, claims and the reporting contract; access to the template is not authority to provision or spend.

The toy compares plurality quorum, which counts votes, with provenance-aware quorum, which counts distinct evidence roots. Agents select among K options while some copy one upstream source. Its outcomes demonstrate the programmed mechanism, not an LLM result or general swarm advantage.

## Files and implementation boundaries

| File | Existing function |
|---|---|
| `experiment.yaml` | Hub registration fields, parameter schema and metrics |
| `design.yaml` | Toy arms, task splits, stage counts, seeds and primary contrast |
| `preregistration.md` | Design template; all stages still need a public prospective plan |
| `src/sim.py` | Scripted environment, policies and evaluator |
| `src/selftest.py` | Offline pairing, blindness, task, manipulation and split checks |
| `src/coordinator.py` | Registration and queueing; legacy preregistration guard applies only to S2 |
| `src/worker.py` | Executes queued blocks and uploads saved episode records |
| `src/analyze.py` | Downloads saved evidence, computes contrasts and plots |
| `run-workers.sh` | Starts indefinitely restarting workers; optional reboot persistence |

The current coordinator only **warns** if S1 lacks a finished S0. A finished job is not evidence that qualification thresholds passed. Its S2 check covers committed design files and TODOs; it is not an immutable public-plan, current-source, budget or allocation preflight. `--reopen` does not itself verify a prospective amendment. Do not use those legacy checks as admission for a real experiment.

The worker's append-only output and reporting recovery help preserve artifacts, but do not guarantee exactly-once model calls or effects. A restarted/requeued block can execute again and append duplicate episodes. `run-workers.sh` restarts after exit and can persist across reboot. Indefinite restarts, `--forever` and `--at-boot` are unsuitable for paid or stateful work until the adapter enforces duplicate detection, cumulative budget, pending-call reconciliation, bounded lifetime and current authority. A reporting outage should be repaired from saved evidence, not by repeating collection.

## Adapt the template in order

1. **Establish the research scope.** Follow root `AGENTS.md` for the applicable survey, hypothesis and different-researcher review gates. Label exploratory notes honestly. S0/S1 names do not exempt an exploratory run from review, public-plan, qualification, budget or allocation requirements. For Vishesh's studies, follow the owner's single researcher-review instruction; routine implementation repairs do not automatically require another sign-off.
2. **Write the design before implementation.** Create `SETUP.md` from the [setup template](../../../5-experiments/toolkit/agent-experiments/templates/experiment-setup.md), referencing the plan, preceding post-mortem and exact next action. Freeze independent units, controls, treatment, primary endpoint, missingness, seed/task splits, resource limits and claim boundaries. Define what each stage means in this study; the toy uses S1 for development and S2 for its held-out comparison.
3. **Copy into the permitted study location.** Formal experiments use `scripts/lab.py new experiment`; owned exploratory notes remain explicitly exploratory. Set registration owner/ID and replace template placeholders. Copying does not register a public plan or reserve infrastructure.
4. **Implement and check the instrument.** Adapt the simulator contract below, complete the agent/context/run specifications, and run appropriate offline fixtures. Preserve truth separation, treatment fidelity, all-assigned denominators and actual context records. Test missing/duplicate outcomes, changed source/configuration, timeouts, uncertain calls, exhausted budget and reporting failure before native execution.
5. **Wire admission into the actual dispatch path.** Before every attempt and stage, read the preceding post-mortem and commit the pre-run assessment. Publish and verify the exact immutable plan, experiment TLDR and condition-specific TLDRs. Require current qualification, source/dependency match, cumulative spending authority and fresh exclusive allocation. Before new provisioning for Vishesh, verify Dmarz's approved account identity and authoritative state/project privately. Missing or stale evidence must stop queueing/model loading/calls, not merely emit a warning.
6. **Run only the admitted stage.** Use a finite worker with declared calls, tokens, dollars, time and concurrency limits. Reserve before dispatch, retain uncertain charges and all failures, and keep qualification and scientific conclusions separate. No automatic S0-to-S1 or S1-to-S2 escalation follows from a successful exit. Preserve holdout protection; amendments and repairs receive explicit lineage rather than overwriting old outcomes.
7. **Reconcile, report and release.** Audit assigned → started → terminal → graded → analyzed; retain unstarted and partial units. Recompute from saved raw decisions, check the visualization, record actual versus reserved cost, complete the post-mortem and verify durable artifact readback. Stop only the owning experiment's workers and release its claim through the applicable infrastructure workflow.

For a real launcher, use the [lifecycle contract](../../../5-experiments/toolkit/agent-experiments/AGENT-LIFECYCLE.md) and record which requirements are implemented versus still manual. This README corrects the operating guidance; the template runtime has not been retrofitted with those gates.

## Manual command reference

These are the existing template interfaces for operators adapting it. Commands that register, claim or queue work require the completed gates above; they are not an alternate launch path around missing admission. They are separate from the supported adapters in `scripts/experiment.py`.

Create the formal study only after its applicable research gate, then copy the template files from the public repository root:

```sh
export SWARM_SOURCE=<researcher>/<agent-name>
python3 scripts/lab.py new experiment <id> --agent "$SWARM_SOURCE"
cp -r lab/templates/experiment-worker/{experiment.yaml,design.yaml,preregistration.md,src,run-workers.sh} 5-experiments/<id>/
```

In the authorized private operations checkout, inspect current allocations before obtaining the experiment's exclusive claim. Keep account verification and private inventory there. For Vishesh, follow the [machine workflow](../../../5-experiments/studies/vishesh/experiment-machine-workflow.md); an unavailable authorized allocation is a blocker, not permission to use the local default cloud account.

```sh
python3 scripts/agentops.py claims
python3 scripts/agentops.py claim <you>-<id> --servers <approved-available-host> --by "$SWARM_SOURCE" \
    --until 6h --experiment <id> --note "<admitted-stage>"
```

The six-hour value is the legacy example, not a default authorization: set expiry to the authorized stage window and verify the merged claim. Deploy the intended frozen source into an isolated checkout and verify its hashes. From that study directory, the existing interfaces are:

```sh
python3 src/selftest.py
python3 src/coordinator.py register
python3 src/coordinator.py stage S0
python3 src/worker.py
python3 src/coordinator.py status
python3 src/analyze.py --stage S0
```

Only use queue/worker commands after implementing and checking the required dispatch gates. `worker.py` without `--forever` stops when its queue is empty; it is not itself a time/cost cap. `coordinator.py --dry-run` is also not guaranteed offline: stage checks can query the hub. Repeat admission before queueing S1 or S2. Adapt analysis to the declared independent unit and examine failures before considering the next stage.

After stopping the exact owning workers and verifying artifacts, release the claim in the private operations checkout:

```sh
python3 scripts/agentops.py release <you>-<id> --note "<stage> reconciled and artifacts verified"
```

If a legacy tmux worker was used, stop only its verified experiment session and remove its associated reboot entry if present. Do not indiscriminately kill a shared session. Authorized fleet owners handle machine teardown. File external deliverables through `.flightdeck/fd.py add` under the root repository's delivery rules.

## Preserve the simulator contract

`run_episode(task_id, seed, world, dose, arms, cfg)` returns one record per arm. Preserve these properties when replacing the toy:

- **Explicit randomness:** use named, stable random streams. Pair exogenous worlds and corresponding baseline observations across arms. Hosted model responses are not guaranteed deterministic even with identical settings.
- **Truth separation:** actors receive only allowed observations; protected truth enters evaluation after the decision. A prompt instruction alone is not an access boundary.
- **Complete outcomes:** retain valid, invalid, failed, timed-out and unstarted assignments. An infrastructure retry keeps episode identity and cost; a bad answer is not an invisible retry opportunity.
- **Declared dependence:** identify the independent unit and task/world clusters. Repeated seeds, agents, votes and arms are not automatically independent samples.

Rename worlds, arms, parameters and metrics consistently. The template's `worker.py` metric names and statistical procedures are examples; choose endpoints and analysis appropriate to the new design. Test the task and evaluator using known correct and deliberately wrong policies. Passing software fixtures is not native model qualification.

## Reporting and evidence metadata

Complete the [visualization mapping](../../../5-experiments/toolkit/agent-experiments/templates/visualization-mapping.md) before collection. Bind events, units, denominators, missing states and evaluator reveal to recorded evidence. Test the renderer using fixtures marked **SCRIPTED — NOT MODEL EVIDENCE**. The worker does not implement a study-specific replay automatically.

Every study README needs `evidence_confidence` and `sample_size_summary` under the [shared rubric](../../../5-experiments/EVIDENCE-METADATA.md). Register the assessment in `5-experiments/evidence-metadata.json` and render with `python3 scripts/experiment_evidence.py --write`. Give the claim, rationale and source date; distinguish independent task roots from calls and repeated outcomes. These fields describe evidence, not launch permission or automatic hub display.

Use the [pre-run assessment](../../../5-experiments/toolkit/agent-experiments/templates/pre-run.md) before each attempt and the [post-mortem](../../../5-experiments/toolkit/agent-experiments/templates/post-mortem.md) afterward, including failures. A valid adverse result is reported; a defect receives a bounded repair with acceptance evidence. Publication, process compliance and scientific interpretation remain separate.

## What the toy demonstrates

When the shared source is wrong, the scripted plurality rule often commits wrongly and the provenance rule waits for distinct roots. When that source is right, the provenance rule can add delay without an accuracy benefit. This is a property of the programmed rule and constructed worlds. It motivates a possible question but does not establish that real agents, real provenance or a new scenario will behave the same way.
