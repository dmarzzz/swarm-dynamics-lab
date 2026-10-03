---
id: data-agentlogs-2026
type: dataset
title: "AgentLogs: tasks, sessions and 64M session-log entries from GitHub's cloud coding agent across 1.8M public repositories"
authors:
- Jonan Richards
- Kosei Horikawa
- Youmei Fan
- Yutaro Kashiwa
- Mairieli Wessel
year: 2026
url: https://huggingface.co/datasets/risenlab/agentlogs
license: CC-BY-4.0
size: 66,957,764 records, 56.7 GB (64,255,174 log entries = 56.0 GB)
format: 'Parquet tables: repositories, agent_tasks, agent_sessions, agent_session_logs, users (v0.2)'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

RISEN Lab dataset (arXiv 2608.29204) of activity by GitHub's Copilot cloud agent in the wild. Covers 1,812,362 public repos with over 10 stars (35,810 with agent tasks), 307,416 agent tasks, 549,239 agent sessions (model, prompt, outcome, usage), 64,255,174 log entries (messages, tool calls for file edits, git, issues, PRs, comments, CI) and 33,573 related users (GitHub id and username only).

## Access

Public on Hugging Face, not gated, CC-BY-4.0; pin `revision="v0.2"`. The log table is 56 GB, so the card recommends a parquet snapshot rather than streaming. Helper package `risenlab-agentlogs`.

## Relevance to us

A large in-the-wild record of one operator's agent fleet acting on public infrastructure, with ground truth about which actions are agent actions. Useful as a positive set for detecting agent activity on GitHub and for studying how many sessions one task fans out into.
