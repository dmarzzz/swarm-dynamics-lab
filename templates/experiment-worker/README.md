# Experiment worker template

A small distributed experiment that already meets the lab's requirements: the prior-art gate in
AGENTS.md, and the design rules in vishesh's design guide
(`researchers/vishesh/notes/seo-poisoning/experimental-design.md`, *Experimental design* §0–§8). Copy it,
replace the simulator, and follow the steps in order. The infrastructure side (servers, claims, the hub) is
in the private `swarm-labs-agentops` repo: its `AGENTS.md`, plus `docs/REPORTING.md` for the hub contract.

The example is deliberately trivial so that every piece is visible. It is a quorum of agents deciding
among K options while some of them copy one shared upstream source (from the `quorum` project brief and
the root-counting idea in the dissent design). Plurality quorum counts votes; provenance-aware quorum
counts distinct evidence roots. It runs in milliseconds per episode. It is a toy, not a result.

```
experiment.yaml       hub registration: id, title, parameter schema, metrics, primary metric
design.yaml           the frozen design: arms, fixed config, splits, stages S0/S1/S2, seeds, primary contrast
preregistration.md    hypotheses, contrasts, effect sizes, units, metrics, retry policy, seeds (committed before S2)
src/sim.py            the environment + the arms. The only file that knows the toy; replace it
src/selftest.py       offline checks: determinism, pairing, blindness, clean task, manipulation, splits
src/coordinator.py    register; queue a stage from design.yaml; S2 guarded by the committed pre-registration
src/worker.py         takes queued runs from the hub, runs every arm on the same draws, uploads episodes.jsonl
src/analyze.py        pulls episodes from the hub; paired per-task contrasts, cluster bootstrap, McNemar; figure
run-workers.sh        one worker per core in tmux on a server
results/              local outputs (episodes/, pulled/, <stage>.md, <stage>_cells.csv, <stage>_tradeoff.png)
```

## The steps, in order

**0. Read.** This file, the design guide's *Experimental design* section, and `docs/REPORTING.md` in
swarm-labs-agentops. Set your agent id: `export SWARM_SOURCE=<researcher>/<tool>-<n>`.

**1. Clear the gate.** Experiments need an `accepted` hypothesis, which needs a reviewed survey (swarm-lab
AGENTS.md: *The prior-art gate*, *Hypotheses*, *Experiments*). Until then, build and test in
`researchers/<you>/notes/<id>/` as a labelled hunch, and run S0 and S1 only. S2 waits for the gate.

**2. Copy.** Once the hypothesis is accepted:
```bash
python3 scripts/lab.py new experiment <id> --agent $SWARM_SOURCE     # experiments/<id>/README.md
cp -r templates/experiment-worker/{experiment.yaml,design.yaml,preregistration.md,src,run-workers.sh} experiments/<id>/
```
Set `id` in `experiment.yaml` to `<id>` and `owner` to you. In the experiment README, fill **Setup**
(environment, versions, hardware), and make **Protocol** and **Metrics** point at `design.yaml` and
`preregistration.md`.

**3. Replace the simulator** (`src/sim.py`) and keep its contract:
- `run_episode(task_id, seed, world, dose, arms, cfg)` returns one record per arm.
- **Deterministic** given `(task_id, seed)`, with every random draw seeded from them.
- **Paired**: every arm in an episode gets the same draws (common random numbers).
- **Blind**: arms see only what agents report; ground truth enters only in `evaluate()`, after the decision.
- **Total**: an exception becomes `validity.ok = false` and is recorded, never retried.
- A **task** is the cluster unit: its truth must not depend on the seed.

Rename the worlds, arms, parameters and metrics to yours; `worker.py`'s `metrics()` names the per-arm
metrics the dashboard shows.

**4. Fill the design.** `design.yaml`: arms, fixed `cfg`, task splits (dev and holdout never overlap),
stages, seed lists, and the one `primary_contrast`. `preregistration.md`: every section. Then run
`python3 src/selftest.py` until it passes, and adapt its checks to your simulator.

**5. Claim servers** (swarm-labs-agentops):
```bash
python3 scripts/agentops.py claim <you>-<id> --servers sim-01,sim-02 --by $SWARM_SOURCE \
    --until 6h --experiment <id> --note "S0+S1"
```

**6. Register, run S0, start workers.** On each claimed server (the code is pulled from git, so commit
and push first):
```bash
git clone https://github.com/dmarzzz/swarm-lab /srv/swarm/swarm-lab 2>/dev/null; cd /srv/swarm/swarm-lab && git pull
cd experiments/<id>
python3 src/coordinator.py register          # once
python3 src/coordinator.py stage S0          # clean-task validation
./run-workers.sh                             # one worker per core, in tmux "workers"
```
Watch the hub dashboard. S0 must show the clean task done (both arms commit and are mostly right). If
not, fix the simulator before going on.

**7. S1 development.** `python3 src/coordinator.py stage S1`, then `python3 src/analyze.py --stage S1`.
Use S1 to debug, and to estimate the discordant-pair rate and the variance of the per-task difference.
Write the sample size into `preregistration.md` §4 and `design.yaml` `stages.S2.tasks`.

**8. Pre-register.** Commit and push `design.yaml` and `preregistration.md` with no TODOs left. This is
the point of no return: `stage S2` refuses uncommitted or TODO-bearing files, stamps their commit on every
S2 run, and refuses to open the holdout twice.

**9. S2 primary.** `python3 src/coordinator.py stage S2`, workers as in step 6 (they keep polling if
started with `--forever`), then `python3 src/analyze.py --stage S2`. The results table marks the
**PRIMARY** row, and everything else is labelled exploratory. Copy `results/S2.md` into the experiment
README's **Results** section, interpret under **Analysis**, and update the hypothesis status (`supported`
or `refuted`).

**10. Release and ship.** `python3 scripts/agentops.py release <you>-<id> --note "S2 done"`. Stop workers
with `tmux kill-session -t workers`. File figures that leave the team through `.flightdeck/fd.py add`
(AGENTS.md: *Deliverables*).

## Where each requirement is met

| Requirement (design guide / AGENTS.md) | Where |
|---|---|
| Episode is the unit of analysis; task is the cluster; seeds within a task are not independent | `sim.task()` (truth per task), `analyze.cluster_bootstrap` resamples whole tasks |
| Paired arms, common random numbers | `sim.run_episode` draws once and scores every arm; `selftest` checks it |
| Ground truth held apart from the decision | `sim.evaluate()` runs after the rule; `selftest` checks reports carry no truth |
| Primary contrast declared in advance; the rest exploratory | `design.yaml primary_contrast`; `analyze` marks PRIMARY |
| Pre-registration committed before the first real run | `coordinator.prereg_commit()` guards S2 and stamps `prereg` on runs |
| Stages S0 clean validation, S1 development, S2 holdout opened once | `design.yaml stages`; `coordinator` refuses a second S2 |
| Seeds fixed, never chosen after looking | `design.yaml` seed lists; `selftest` checks they exist |
| Failed episodes recorded and counted, never retried | `sim.run_episode` try/except; `invalid` column in results |
| One JSON record per episode, append-only, with provenance | `worker.execute` writes `results/episodes/*.jsonl` with `run`, `prereg`, `code`, `worker` |
| Paired binary outcome: McNemar; continuous: paired per-task difference | `analyze.mcnemar_exact`, `analyze` diff + CI |
| Protocol and Metrics before the first run (AGENTS.md *Experiments*) | step 2 and step 8 |
| Report every run including failures | the hub keeps every run; `analyze` counts invalid episodes |
| Rerunnable by someone else's agent | seeds + `code` commit + `prereg` commit on every record |

## What the toy shows (S1, dev tasks)

In W2_FALSE (the shared source is wrong), plurality quorum commits to the wrong option in most episodes
and the provenance-aware quorum almost never does. The provenance rule pays in delay: it waits for more
independent roots. In W1_TRUE (the shared source is right), the provenance rule is slower for no accuracy
gain. That tradeoff is the kind of result the template is built to measure honestly. It is a property of
the rule written into the toy (see the quorum brief's *Interpretation risk*), not a finding about agents.
