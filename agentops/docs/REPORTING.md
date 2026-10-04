# Experiments, runs and the hub

Every simulation reports to one place, the **hub** (`hub-01`, see `python3 scripts/agentops.py list`).
The hub has an API, a run queue, artifact storage with hourly off-box backups, and a dashboard.
This file is the contract that coordinators and workers follow.

## Start from the template

`lab/templates/experiment-worker/` in <your-org>/swarm-dynamics-lab is a complete distributed experiment built on this
contract: experiment.yaml, a frozen design.yaml, a pre-registration, a coordinator that queues S0/S1/S2
(S2 guarded by the committed pre-registration), a worker that runs paired arms and uploads episodes, and
an analysis with cluster-bootstrap CIs and McNemar. Its README lists the steps in order. Copy it, then
replace `src/sim.py`.

## The model

| Thing | What it is | Example |
|------|------------|---------|
| **experiment** | One type of simulation, with a parameter schema and the metrics it reports. | `boids-noise` |
| **run** | One execution of an experiment with fixed parameters. Has a status, progress, a metrics timeline and artifacts. | `boids-noise/3f2a91c0` with `{n: 200, eta: 0.4, seed: 2}` |
| **planned run** (task) | A run in the queue that no worker has taken yet. Coordinators enqueue sweeps; workers take them. | 30 planned runs from a 10 x 3 grid |
| **artifact** | A file a run produced: plot, CSV, JSON, log, video, checkpoint. Rendered on the dashboard and backed up. | `plots/order.png` |
| **event** | One report: start, progress, metric, log, artifact, done, fail. The timeline of a run. | |
| **claim** | "I am using these servers", recorded in git (`claims/`). For servers, not runs. | `alice-boids-sweep` on `sim-01` |

Run status goes `planned -> assigned -> running -> done | failed | cancelled`. A running run with no
report for 10 minutes shows as **stale**.

## Ids

- Experiment id: lowercase with dashes, the same as the experiment directory in the research repo
  (`experiments/<id>/` in <your-org>/swarm-dynamics-lab).
- Run id: `<experiment>/<suffix>`. The queue picks a random suffix; pick your own when you have a better
  name (`boids-noise/n200-eta0.4-s2`).
- Source: who is reporting, `<person>/<tool>-<n>`, the same agent id as in the research repo (`alice/claude-1`,
  `bob/codex-2`). Set `SWARM_SOURCE`.

## On a server: nothing to set up

Every server has `swarm-report` on the PATH, `import swarm_report` in Python, and the hub address and
team token in `/etc/swarm/report.env`. Just set `SWARM_SOURCE`.

From a laptop: `eval "$(task hub:env)"`, or copy `hub/swarm_report.py` next to your code and export
`SWARM_HUB_URL` and `SWARM_HUB_TOKEN`.

## 1. Register the experiment (once, and whenever its definition changes)

`experiments/<id>/experiment.yaml` in the research repo, then `swarm-report register experiments/<id>/experiment.yaml`:

```yaml
id: boids-noise
title: "Boids: order vs noise"
description: Vicsek-style flock. Sweep noise eta and flock size n; measure the order parameter.
owner: alice
params:
  n:    {type: int,   default: 200, description: flock size}
  eta:  {type: float, description: angular noise, 0..1}
  seed: {type: int}
metrics: [order, collisions]
primary_metric: order        # the sparkline on the dashboard
url: https://github.com/<your-org>/swarm-dynamics-lab/tree/main/5-experiments/boids-noise
```

## 2. Coordinator: queue the runs

```bash
swarm-report enqueue -e boids-noise -p n=200 --grid eta=0,0.1,0.2,0.3,0.4,0.5 --grid seed=1,2,3
```

```python
import swarm_report as sr
sr.enqueue("boids-noise", [{"n": 200, "eta": e / 10, "seed": s} for e in range(11) for s in (1, 2, 3)])
```

## 3. Worker: take runs until the queue is empty

```python
import swarm_report as sr

def simulate(run):
    p = run.params                                  # {"n": 200, "eta": 0.4, "seed": 2}
    for step in range(1, 1001):
        ...
        run.progress(step, 1000, order=order, collisions=c)   # sent at most every 2 s
    run.artifact("out/order.png", "plots/order.png")
    run.artifact("out/trace.csv")
    run.done(message=f"final order {order:.3f}", order=order)

sr.work("boids-noise", simulate)    # done on return, failed on exception, then the next run
```

`sr.work(..., stop_when_empty=False)` keeps polling for new work. Run one worker per core or per
container. `next_run()` hands each planned run to exactly one worker.

Shell workers:

```bash
while RUN=$(swarm-report next -e boids-noise); do
  ID=$(jq -r .run <<<"$RUN"); ETA=$(jq -r .params.eta <<<"$RUN")
  swarm-report start -r "$ID"
  ./sim --eta "$ETA" --out out/ && swarm-report done -r "$ID" -M order=$(cat out/order) \
    || swarm-report fail -r "$ID" -m "exit $?"
  swarm-report artifact -r "$ID" out/order.png
done
```

Runs outside the queue: `with sr.start("boids-noise", params={...}) as run: ...`.

## What to report

- `progress` with `step`/`total` and the metrics that matter. A sample every few seconds is plenty.
- Artifacts for anything a person would want to look at or that took compute to make. Images, video,
  CSV/TSV, JSON, text and logs render inline. HTML and SVG download instead of rendering, for safety.
  Max 512 MB per file. Larger outputs (checkpoints, datasets) go somewhere else; report their location with
  `run.log(...)` or `url=`.
- `done` with the final metrics and one line on what happened; `fail` with the reason.
- Never put secrets in params, messages or artifacts. The dashboard shows them all to the team.

## For the public live site (optional)

The lab ran a public live page over the hub (a static site that reads the hub through a small proxy with the
read-only token). That site is not part of this template. If you build one, these optional conventions make
it read better:

- `params.<name>.label` names an axis ("density"); `params.<name>.value_labels` renames values
  (`{"0": "off"}`). The two swept params with the most distinct values become the heat map's axes; `seed`,
  `rep` and `trial` fold into each cell.
- A run that uploads `frame.json` every 2 to 5 s (overwrite the same name) gets a live view:
  `{"L": <box side>, "t": <step>, "x": [...], "y": [...], "th": [<heading, radians>]}`, at most 20,000 points.
- `frame.json` with `"kind": "deliberation"` draws a three-agent deliberation view instead
  of points: agents, roles, votes, which value of the contested fact each endorses, the latest message, false
  endorsements per round and a running tally. The site proxy rebuilds it from a typed whitelist (short strings,
  enums, numbers; IP-like text masked).
- `replay.json` (`{"kind": "deliberation-replay", "frames": [<deliberation frame>, ...]}`, at most 3,000 frames, under
  8 MB) adds a replay player (play, pause, scrub, 1x/4x/16x) to the run page. Upload it at the end of a run, or
  backfill it later from saved events; it is the only JSON artifact besides `frame.json` that the public site reads.
- One image per finished run (PNG, JPEG, WebP or GIF, for example `final_frame.png`) fills the experiment's
  contact sheet. Other artifact types stay private to the team.

- `url` in the registration is the experiment's plan. A GitHub folder link (for example
  `https://github.com/<your-org>/swarm-dynamics-lab/tree/main/5-experiments/<id>`) is shown as a link
  to its `README.md` on every run, and the page reads that README's question, setup, protocol and metrics
  sections. A run can point at its own plan with a GitHub `url=` on its reports. Without a `url` the page
  looks for `experiments/<id>/README.md`.
- The plan section groups runs by role. `stage` (or `phase`) params become a stage picker (S0, S1, S2);
  params with several values are the conditions compared; `seed(s)`, `task(s)`, `rep`, `trial`, `chunk` and
  `shard` are replicates folded into each condition; list and object params and single values are fixed
  settings. Override any of these with `params.<name>.role: stage | condition | replicate | fixed`.
- A run with `params.kind: analysis` (or tag `analysis`) is a stage's analysis: its message and image
  artifacts appear under the plan instead of as a condition.

## HTTP API

Everything needs `Authorization: Bearer $SWARM_HUB_TOKEN`.

| Method | Path | Body / query |
|--------|------|--------------|
| POST | `/api/v1/experiments` | `{id, title, description, owner, params, metrics, primary_metric, url}` (or a list) |
| GET | `/api/v1/experiments` | |
| POST | `/api/v1/runs` | `{experiment, params, run?, priority?, tags?}` or a list: queue planned runs |
| POST | `/api/v1/runs/next` | `{experiment?, source, host}`: returns `{"run": {...}}` or `{"run": null}` |
| GET | `/api/v1/runs` | `?experiment=&status=&host=&source=&limit=` |
| GET | `/api/v1/runs/<run>` | params, metrics, `series`, `artifacts`, `events` |
| POST | `/api/v1/report` | event or list: `{kind, experiment?, run?, source, role, host, step, total, progress, metrics, message, status, url, data}` |
| PUT | `/api/v1/artifacts?run=&name=` | raw file bytes; `Content-Type` is kept |
| GET | `/a/<run>/<name>` | the artifact |
| GET | `/api/v1/events` | `?experiment=&run=&host=&kind=&kinds=a,b&since=<id>&limit=` |
| GET | `/api/v1/state` | everything the dashboard shows |

`kind` is one of plan, start, progress, metric, log, artifact, done, fail, heartbeat, claim, release.
A start event may carry `data.params` for runs that did not come from the queue.

## Backups and restore

Every hour the hub takes a consistent SQLite snapshot and copies it, plus every artifact, to the private
Spaces bucket in `secrets/hub.sops.env`. The copy never deletes, and DB snapshots are kept for 14 days.
To restore onto a fresh `hub-01`:

```bash
task provision HOST=hub-01                       # empty hub
ssh hub-01
sudo systemctl stop swarm-hub
R="sudo rclone --config /etc/swarm-hub-rclone.conf"; B=spaces:<bucket>
sudo rm -f /var/lib/swarm-hub/hub.db-wal /var/lib/swarm-hub/hub.db-shm
$R copyto $B/db/latest.db /var/lib/swarm-hub/hub.db     # or db/hub-<time>.db for an older point
$R copy $B/artifacts /var/lib/swarm-hub/artifacts
sudo chown -R swarm-hub: /var/lib/swarm-hub && sudo systemctl start swarm-hub
```
