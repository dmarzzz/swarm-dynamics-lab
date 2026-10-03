---
id: gh-ukgovernmentbeis-control-arena
type: code
title: 'ControlArena: library of settings, model organisms and protocols for AI control experiments'
repo: UKGovernmentBEIS/control-arena
url: https://github.com/UKGovernmentBEIS/control-arena
authors: [UK AI Security Institute, Redwood Research]
year: 2025
language: Python
license: MIT
stars: 246
last_commit: 2026-10-01
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [greenblatt-2023-ai]
---

## Summary

Python library from the UK AI Security Institute and Redwood Research for running AI control experiments, built as a thin wrapper over Inspect AI. Provides settings (evaluation environments with benign main tasks and harmful side tasks, covering code sabotage, research sabotage, data poisoning), micro-protocols (trajectory-level, such as defer-to-trusted), policies ("model organisms": honest, attacking, trusted, untrusted), monitors producing suspicion scores, macro-protocols for auditing and shutdown in post-hoc analysis, attack tools with different monitor visibility, scorers and analysis utilities. Actively maintained (last push 2026-10-01). [[makins-2026-multi]] counts undetected success following ControlArena's convention.

## What it can do for us

The natural harness for a fork-merge control experiment: define a setting where several untrusted sub-agent policies work on separate main tasks, one carries a side task (corrupt the parent on merge), and compare merge-time monitors (per-child versus joint). Settings and monitor components exist; multi-agent sequencing would have to be added (inferred from the README, not checked in code).

## Run notes

Not run. Module tree inspected via the GitHub API (control_arena/, agent_scaffolds/, analysis/, tests). Documentation at control-arena.aisi.org.uk.

## Limitations

Single-agent micro-protocols are the documented unit; no multi-agent setting is named in the README. Requires model API access; some settings need sandbox containers.
