---
id: {{id}}
type: experiment
title: TODO
owner: {{researcher}}
agents: [{{agent}}]
hypothesis: TODO
status: planned
created: {{date}}
code: []  # library ids of external code used
---

Before implementation, follow the [experiment setup runbook](../../tooling/agent-experiments/EXPERIMENT-SETUP.md)
and copy the [setup record](../../tooling/agent-experiments/templates/experiment-setup.md) to this study's
`SETUP.md`. Fix its copied links and record current gate evidence. Preserve research-review gates;
a generated template is not permission to run.

## TLDR

TODO question, treatment, comparator, success metric and limitations in plain language.

## Question and prediction

TODO testable question, prospective prediction if any, primary contrast and claim boundary.

## Evidence metadata

- **evidence_confidence:** unassessed — name the claim and rationale using the [0–4 rubric](https://github.com/dmarzzz/swarm-lab/blob/main/experiments/EVIDENCE-METADATA.md); do not reuse an agent confidence value.
- **sample_size_summary:** observed independent units and completed/assigned outcomes; label planned units separately.

Add this study and its supporting paths to `experiments/evidence-metadata.json`, then run `python3 scripts/experiment_evidence.py --write`. Keep frozen registration and run configurations unchanged.

## Setup

TODO environment, versions, hardware, seeds. Put code in this folder under src/ and outputs under results/.

## Protocol

TODO exact steps and parameter sweeps, written before running.

## Metrics

TODO what you measure and how, decided before running.

## Results

## Analysis
