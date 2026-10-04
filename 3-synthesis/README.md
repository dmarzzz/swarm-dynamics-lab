# 3-synthesis: reading across the surveys

Phase 3 (synthesis) of [Swarm Dynamics Lab](../README.md). This folder holds the cross-cutting documents: the
landscape, people and labs, and the research question atlas. It has no gate, so each document states its own
status and the atlas labels every item an unreviewed hunch.

## What this is

A synthesis document reads across the library and the surveys instead of covering one topic. Each file names
its owner in prose at the top and cites library entries as `[[id]]`. None of these documents is a
gate-passed survey, an accepted hypothesis or an experimental result.

## What is in here

| File | What it is |
|---|---|
| [`research-question-atlas.md`](research-question-atlas.md) | The question atlas: 214 candidate questions from 319 source records across 15 research areas. |
| [`atlas-project-connections.md`](atlas-project-connections.md) | Research context connecting the atlas to sixteen project briefs. |
| [`landscape.md`](landscape.md) | How the library's topics connect, with counts from a library snapshot. |
| [`people-and-labs.md`](people-and-labs.md) | Who produces the seminal and recent work in each topic, and which entries to read first. |
| [`pre-experiment-research.md`](pre-experiment-research.md) | Research prerequisites for choosing swarm experiments. |
| [`swarm-detection-methods.md`](swarm-detection-methods.md) | Methods, evidence and trap design for detecting AI agent swarms in the wild. |
| [`fork-merge-questions.md`](fork-merge-questions.md) | Three questions about fork-merge corruption, set against prior art. Draft, merged incomplete. |
| [`sybil-flashbots.md`](sybil-flashbots.md) | Flashbots Sybil work and its analogues in swarms, P2P networks and LLM agent collectives. Draft, merged incomplete. |

## How to add to it

Synthesis work is claimed as a task on the board in [`lab/tasks/`](../lab/tasks/). Write one file per
document, name the owner and the date in the first lines, cite library entries as `[[id]]`, and mark any
statement that goes beyond the cited sources as inferred.

## Where it goes next

Synthesis reads the surveys in [`2-surveys/`](../2-surveys/README.md). Questions from the atlas become
hypotheses in [`4-hypotheses/`](../4-hypotheses/README.md) once a survey passes the gate, or exploratory
studies in [`5-experiments/studies/`](../5-experiments/studies/README.md) before that.
