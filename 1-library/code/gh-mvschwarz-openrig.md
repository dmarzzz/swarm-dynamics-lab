---
id: gh-mvschwarz-openrig
type: code
title: "OpenRig: YAML-defined persistent teams of Claude Code and Codex agents with roles, shared context, a message queue and a tmux TUI"
repo: mvschwarz/openrig
url: https://github.com/mvschwarz/openrig
authors: ["mvschwarz (Feral Machine)"]
year: 2026
language: TypeScript
license: "Apache-2.0"
stars: 4631
last_commit: 2026-10-03
topics: [llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

OpenRig ("a harness wraps a model, a rig wraps your harnesses") is an open-source orchestration layer that turns a pile of Claude Code and Codex terminal sessions into a persistent, named team. A rig is defined in YAML (seats with role, runtime, model), booted with `rig up`, and shown as a graph, a seat table (runtime, model, context, state) and per-seat detail in a tmux-based TUI. Humans talk to a lead agent (`rig send "dev-owner@rig" '...'`), which coordinates specialists across teams and surfaces decisions; work is tracked in a queue (`rig queue list`). Starter rigs ship as owner/checker pairs (two Codex, two Claude, or mixed). Requires Node 22/24 and tmux on macOS or Linux; setup writes provider hooks and workspace trust settings, and asks once whether agents may run `rig` commands without permission prompts. It is the system behind the author's "AI civilization" experiments described in [[x-feralmachine-2105506490736091586]]. 4,631 stars, created 2026-04-01, actively pushed (last push 2026-10-03); npm package `@openrig/cli`.

## What it can do for us

Reference topology for a persistent-population agent collective: long-lived agents with accumulated context, work routed by expertise, hierarchical lead/specialist/tier structure, a shared queue as the coordination substrate. If we want a testbed for coordination failure modes in long-running heterogeneous teams (Claude plus Codex in one rig), this is the most-used open tool of that shape we have seen. The seat table (context size, state per agent) is also a ready-made trace source for population-level measurement.

## Run notes

Not run. Read the README on main via the GitHub API. Install per README: `npm install -g @openrig/cli && rig setup --dry-run`, then `rig up first-project --cwd .` and `rig tui --shared` inside a repository with an authenticated `claude` or `codex` CLI.

## Limitations

Coding-agent specific and tied to vendor CLIs (Claude Code, Codex, "Pi"); a Hermes adapter is only on the roadmap per the author. Setup modifies trust settings and installs executable hooks on the host, which the README flags. No benchmarks or published evaluation of team performance versus a single agent. Rapid release cadence (docs admitted to lag the code in the week of access).
