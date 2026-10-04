# Always five: how a fleet of coding agents keeps five experiments running

Written on 2026-10-04 by an AI agent at the operator's request, from the operator's description of the arrangement in use that night. The author of this document measured nothing. Durations and counts were observed by the monitor session during the night, and every number that is a setting is marked as one.

## What this document is

The guide describes how one researcher's coding agents are arranged so that five experiments have a run in progress at all times, and it lists the pieces another team needs to reproduce the arrangement. Machines and tools are named by role only (the operator's laptop, an always-on machine, the private infrastructure repository, the experiment hub). The specific hosts and tools are private, and the design can be copied without them.

A worked example of the problem the arrangement solves: a lane runs a qualification stage for two minutes, and its operator then spends twenty minutes on analysis, the next plan and the pre-run review. The lane has a live run for two minutes in twenty-two, so it counts toward the five for about a tenth of that period.

Terms used below, with the meaning they have in this repository:

| Term | Meaning |
|---|---|
| Lane | One experiment's line of work from plan to post-mortem, owned by one operator session. |
| Stage | One step of a study: a scripted stage with zero model calls, a one-call interface probe, a qualification, or a main stage. |
| Run | One execution of a stage, or of a chain of stages, by a worker on a server. |
| Gate | A pass condition written before the run and checked on a stage's results. A failed gate blocks the next stage. |
| Claim | A reservation with an expiry. A server claim reserves one server for one experiment. A task claim reserves one task for one agent. |
| Pre-run review | The written assessment of a plan that is committed before launch. |
| Post-mortem | The written account after a run: results, quality, failures, causes and the next run. |
| Experiment hub | The service that workers report to. It publishes the state of every experiment and run. |
| Duty cycle | The fraction of time a lane has a live run. |

Tonight's settings are collected here. They are choices made for one night and can be changed.

| Setting | Tonight's value |
|---|---|
| Experiments with a live run | 5 |
| Ready queue depth | at least 3 |
| Spare servers, provisioned and unclaimed | 2 |
| Watcher poll interval | about 1 minute |
| Full status table | every 5 minutes |
| Preferred minimum stage length | 30 minutes |
| Builder agents under the pipeline lead | up to 2 |

## Goal and definition

The goal is five experiments with a run in progress at all times. An experiment counts only while a worker is executing a run. A lane that is between stages, waiting for a decision or being written up does not count.

## Why the count drops

The live count drops because each lane was worked in series: run, analyse, decide what to change, write the next plan and its pre-run review, launch. Every step after the run happens with nothing running. Qualification stages lasted one or two minutes, and the work between stages took twenty minutes or more. Two things lengthen the gap further.

- A failed gate adds a repair loop before the next launch.
- A decision that waits on the human adds the time the human takes to answer.

The number of lanes needed is the target divided by the duty cycle. At a duty cycle of about one third (an estimate from tonight, not a measurement), holding five live runs needs about fifteen lanes. The alternative is to raise the duty cycle, which is what most of the rules below do.

## Roles

The arrangement has six roles.

| Role | Count | What it does |
|---|---|---|
| Monitor and reviewer session | 1 | Watches every lane, relays the human's instructions to the other sessions, reviews plans before any paid run, and reports a status table and the running cost every few minutes. It launches nothing itself. |
| Watcher script | 1, under the monitor | Polls the experiment hub's public state about once a minute and prints event lines and a periodic table (next section). |
| Lane operator session | 1 per experiment | Runs on an always-on machine and owns its study from plan to post-mortem. Two lanes tonight were operated by sub-agents of the monitor on the operator's laptop, under the same rules. |
| Results analyst | 1, looping | Reads results while runs are still going and keeps one decision package per lane. Records lessons that apply across lanes. Waits on change instead of polling blindly. |
| Pipeline lead | 1, with up to 2 builder agents | Keeps a ready queue of at least 3 experiments that are fully prepared before any slot opens. |
| Human | 1 | Sets goals, waives or requires review, and gives the few approvals the operator sessions will not accept second-hand. |

### The watcher

The watcher prints one line for each event worth acting on, and a full table every five minutes. The events are:

- a run started, ended or failed;
- a run has had no hub update for several minutes;
- planned runs exist with no worker;
- a claim was created, was released or is about to expire;
- a server is offline;
- the live count is below the target.

The full table lists every experiment with its server and state, the ready-queue depth, the free servers, the state of every operator session, the free memory on the machine that hosts those sessions, and the cumulative cost reported by the runs.

The watcher follows two rules of its own. It keeps its state on disk, so a restart does not announce every past event again. It sums cost from one figure per run and skips summary runs that restate a stage total, so no cost is counted twice.

### The analyst's decision package

The decision package for a lane holds three things: what the partial results show, with denominators; whether the gate will pass and when the run ends; and the next run, already decided for both outcomes. For the failing outcome the package names the most likely cause and the specific change.

## The run queue and what "ready" means

Run requests are issues in the private infrastructure repository, marked with a queue label. A request is in one of four states: waiting, ready, running or blocked.

A request is ready when all four conditions hold.

1. The study's code, its offline tests and a scripted stage with zero model calls exist on the main branch and pass.
2. A pre-run review is on the main branch. It contains the assignment manifest, the call counts, the gates, the model settings, a hard call cap and the pinned commit.
3. The launch commands are exact and take the server as a parameter.
4. The reviewer has read the request.

Review happens when a request becomes ready, while other runs are in progress. Review never happens at launch time.

## Rules that keep the gap short

| Rule | Reason |
|---|---|
| Prepare the successor while the current run is in progress, for both outcomes. | The next launch needs no planning once the result arrives. |
| Chain stages wherever software checks the gate. One launch runs the interface probe, the qualification and the main stage, and stops by itself at a failed gate. | No session has to act between stages that pass. |
| Launch on the gate result. Write the post-mortem in parallel. | The write-up does not delay the next run. |
| Prefer stages that run for 30 minutes or more. | Short stages spend most of their time in setup. |
| Keep 2 spare servers provisioned and unclaimed. | A ready request does not wait for a server to be created. |
| Make the first paid step of any study a one-call interface probe. | A request the interface rejects is found by one call, before the qualification, and a rejected request is not billed. |

## Rules that keep runs honest while moving fast

- One experiment and one run per server. Each has its own claim. Before launch the operator checks the server for an existing claim and an existing worker.
- The plan and the pre-run review are on the main branch before launch, and the run is pinned to that commit.
- Every run has a hard call cap and reports its cost to the hub.
- Gates and thresholds are never lowered after a failure. A model or prompt change is a dated amendment with fresh qualification cases.
- A same-researcher review is recorded as a same-researcher review and is never described as independent.
- Launch secrets reach a worker only in memory, over the launch connection.
- When an instruction changes, runs that have already started finish as launched.

## Model rules for the strongest tier

The checklist holds the rules for the strongest model tier (Opus tonight). Each rule was learned from a failed run.

- Reasoning cannot be turned off, and a reasoning token budget is rejected.
- Sampling parameters are rejected.
- Depth is set by an effort level. Set the level explicitly and record it.
- Reasoning tokens count against the output cap. A small cap truncates the response before the answer.
- Responses carry reasoning blocks before the answer. The adapter must filter them.
- A refusal is its own failure category. Automatic fallback to another model must be off in an experiment.
- A rejected request is not billed. The one-call probe therefore comes first.

One consequence for study design: an arm on the strongest tier cannot be request-identical to arms on weaker tiers. The write-up must say so.

## Failures seen and the fix for each

The table lists each failure from tonight.

| What happened | How it was detected | What changed |
|---|---|---|
| An always-on machine ran out of memory because an unrelated service was crash-looping. The service manager then killed every agent session at once, because the sessions shared one unit. | The watcher showed staged lanes that never started, and the machine was then checked. | The offending service was stopped. Sessions were resumed from their saved transcripts with a short briefing. The watcher now reports free memory. Open item: the unit's kill policy should isolate sessions from each other. |
| The operator's laptop filled its disk. | Every shell command failed. | Worktrees are kept sparse, no local environments are created, and old scratch data is cleared. |
| Operator sessions refused instructions relayed by the monitor for claims, spending and model changes, and stopped to ask the human. | The sessions blocked and asked. | The human gives each session one standing instruction that names the monitor. The monitor never routes around a refusal. |
| Infrastructure state existed on two machines after a handover. | A second session reported during the handover that the state had been copied to the always-on machine. Sessions there had since created servers, so the copy on the operator's laptop was stale. | Only one of the two machines may create or destroy servers. |
| Two sessions started the same study. | After the monitor told each session what the others held, one session reported an unfinished draft of a study that the pipeline lead already had. | A session claims a task before building. The monitor tells each session what the others hold. |
| Two experiments shared a server. | The watcher showed a second experiment's runs on a server claimed for another experiment, and the monitor confirmed the worker processes on that server. | The one-run-per-server rule was sent through the shared inbox. The watcher lists servers that host more than one experiment. |
| A qualification "failed" with every call rejected at zero cost. The cause was an interface error, and the model never produced a result. | The failure category showed that every call was rejected, and the cost was zero. | Operators read the failure category before reading the verdict. The probe runs first. |
| A diagnostic reported "qualification false" by design and was misread as a failure. | The monitor later read the run's closing comment on its queue request, which reported that the diagnostic met its acceptance. | The monitor checks whether a run is a diagnostic or a gate before reporting it. |
| The cost total counted one study twice, because its summary run restated its stage total. | A stage's cost summed from the hub was twice the figure in that stage's own report. | The watcher skips summary runs that restate a stage total. |
| A prompt was ambiguous about a boundary case that the scorer treated one way. | The analyst regenerated the cases offline before the next qualification. | One clause was added to the rule as a dated instrument repair, and the scripted stage was rerun at the new version before the qualification. |
| A pilot would have exhausted its spending reservation partway through and broken its paired arms. | The analyst read the budget code during the qualification. | The lane's operator committed a new design version with a larger reservation, a longer stage timeout and a call cap, then ran a fresh qualification chained into the pilot. |
| The watcher crashed on its own bug. | The watcher printed its own error line before restarting. | The watcher restarts itself and announces the error. |

## What the human sees

The human receives a table every few minutes and a note when something changes.

| Output | Content |
|---|---|
| Status table | One row per experiment: its server, whether it is running, between runs or blocked, and what it is running or waiting on. |
| Summary figures | The live count against the target, the ready-queue depth, the free servers and the running cost. |
| Immediate note | Sent when a lane passes or fails a gate, or when a session blocks. |

## Reproduction checklist

The minimum pieces are listed in a suggested setup order. The operator's description gives the pieces; the order is this document's suggestion, chosen so that each piece exists before the piece that reads from it.

1. An experiment hub with public state. Workers report runs and cost to it, and anyone can read it.
2. A claims mechanism: exclusive, expiring reservations of one server for one experiment.
3. A run queue with labels: issues in the infrastructure repository with the states waiting, ready, running and blocked.
4. Servers: one per experiment that will run, plus spares that stay provisioned and unclaimed (2 tonight).
5. A watcher that polls the hub, prints event lines and a periodic table, and keeps its state on disk.
6. A monitor session that reads the watcher's output, reviews requests as they become ready and reports to the human.
7. Operator sessions on an always-on machine, one per experiment, with a way to send each of them a message. The human gives each session a standing instruction that names the monitor.
8. A results analyst that keeps one decision package per lane.
9. A pipeline lead, with builder agents, that keeps the ready queue filled (at least 3 tonight).

With the pieces in place, size the number of lanes from the duty cycle: lanes needed equals the target divided by the fraction of time a lane has a live run. Then apply the gap rules to raise that fraction.

## Related files in this repository

- [AGENTS.md](../../../../AGENTS.md): the agent protocol, including claims, logs and the required pre-run and post-run review.
- [RUN-REVIEW.md](../../../toolkit/agent-experiments/RUN-REVIEW.md): the pre-run review and post-mortem procedure.
- [READY-CHAIN.md](../pipeline/READY-CHAIN.md): the contract a study follows so that it can be prepared in full and launched as one chain.
