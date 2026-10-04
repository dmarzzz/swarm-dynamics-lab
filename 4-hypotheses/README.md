# 4-hypotheses: hypotheses

Phase 4 (hypothesise) of [Swarm Dynamics Lab](../README.md). This folder holds hypotheses that cite a
complete survey and their closest prior works, and a hypothesis is accepted only after its survey has passed
review and another researcher has reviewed the hypothesis.

## What this is

A hypothesis file can exist only once every survey it lists passes the prior-art gate. CI rejects it
otherwise. Each file lists at least three closest prior works, the predicted outcome if true and if false,
and the criteria that would drop it. The rules are in [AGENTS.md](../AGENTS.md#hypotheses).

## What is in here

The folder held three hypotheses on 4 October 2026. All three are owned by shadow, cite the
`llm-agent-swarms` survey and have the status `proposed`. No hypothesis is accepted, because no survey has
passed review.

| File | Claim |
|---|---|
| [`shadow-board-nsweep.md`](shadow-board-nsweep.md) | A persistent shared board moves the wrong-consensus to polarisation crossover to larger N than pairwise exchange. |
| [`shadow-capture-memory.md`](shadow-capture-memory.md) | Memory length decides whether committed-minority capture reverses after the minority leaves. |
| [`shadow-neff-evidence-board.md`](shadow-neff-evidence-board.md) | Splitting evidence across agents lifts the N_eff ceiling only when peers carry evidence, not just answers. |

## How to add to it

`python3 scripts/lab.py new hypothesis <researcher>-<short-slug> --agent <id>` creates the file.
`python3 scripts/lab.py check` enforces the survey and prior-work requirements. A hunch that has no complete
survey behind it goes in `5-experiments/studies/<you>/`, labelled as a hunch.

## Where it goes next

Hypotheses rest on the surveys in [`2-surveys/`](../2-surveys/README.md) and draw on
[`3-synthesis/`](../3-synthesis/README.md). An accepted hypothesis can be tested as a registered experiment
in [`5-experiments/`](../5-experiments/README.md).
