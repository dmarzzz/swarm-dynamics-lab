# 5-experiments/toolkit: shared methods and harnesses

The shared tooling of phase 5 of [Swarm Dynamics Lab](../../README.md). This folder holds the runbooks,
templates and harnesses that every study follows. It does not replace the source catalogue, the survey gate,
the hypothesis review or the experiment registration in [AGENTS.md](../../AGENTS.md).

## What this is

The toolkit is the reusable part of the experiment work: how to set a study up, how to review a run and how
to scope a claim. It supports any approved project.

## What is in here

| Path | What it holds |
|---|---|
| [`agent-experiments/`](agent-experiments/README.md) | Design guidance, source-linked methodology, protocol and manifest templates, schemas and a validated offline teaching harness. Start with its [integration guide](agent-experiments/INTEGRATION.md). The [setup runbook](agent-experiments/EXPERIMENT-SETUP.md) is required reading before a new study. |
| [`avalon-swarm/`](avalon-swarm/README.md) | A prototype for trust, deceptive claims, coordination and recovery in populations of 100 to 2,000 scripted agents. It holds no results from LLM agents. |

## How to add to it

Add a runbook, template or harness here when more than one study needs it. Code for a single study stays in
that study's own `src/` folder.

## Where it goes next

The studies that use the toolkit are in [`../studies/`](../studies/README.md).
