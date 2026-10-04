---
id: gadgil-2026-bad
type: paper
title: 'Bad Memory: Evaluating Prompt Injection Risks from Memory in Agentic Systems'
authors: [Soham Gadgil, David Alexander, Sai Sunku, Franziska Roesner]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.14611
doi: null
arxiv: '2607.14611'
cite: 'Gadgil, S., Alexander, D., Sunku, S., & Roesner, F. (2026). Bad Memory: Evaluating Prompt Injection Risks from Memory in Agentic Systems. arXiv preprint arXiv:2607.14611.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 4  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The authors test file-based persistent memory (CLAUDE.md-style instruction files, behaviour and preference files, knowledge files) in two deployed coding agents, Anthropic Claude Code and OpenAI Codex. They use a sandboxed synthetic developer workspace and four models: Claude Haiku 4.5, Claude Opus 4.7, GPT-5.2 and GPT-5.5. The adversarial goals are credential exfiltration, unauthorised tool installation and brand targeting. Two findings separate. Getting the agent to write an attacker payload into its own trusted memory files from untrusted external content was hard, and the authors could not do it reliably. But payloads already present in memory files attacked the current session and later sessions with substantial success.

## Contribution

It is the first systematic measurement of planted-memory injection across sessions in production coding agents, including how payloads persist and how attacks stack over sessions.

## Key results

Measured (10 trials per condition, read from the arXiv HTML via a summarising fetch):
- Single-session mean ASR of planted payloads: Haiku 4.5 63.3%, Opus 4.7 30.0%, GPT-5.2 23.3%, GPT-5.5 60.0%. It varies strongly by goal. Opus is 0% on exfiltration and 90% on tool installation, and GPT-5.5 is 100% on brand targeting.
- A payload survives across sessions in 86.7% of runs for Haiku, 96.7% for Opus, 50% for GPT-5.2 and 73.3% for GPT-5.5. Stronger models often refuse to act on a payload but also do not delete it, so it stays in place for later sessions or weaker models.
- Haiku's credential-exfiltration success rose from 60% to 100% over consecutive probes once the planted code looked established.
- With different attacks stacked over sessions, mean ASR is 52.5% for Haiku, 18.3% for Opus, 22.5% for GPT-5.2 and 41.6% for GPT-5.5. The order of attacks changes susceptibility.

## Methods and models

Synthetic workspace with probe, stabilisation and probe sequences of up to three sessions.

## Limitations and open questions

It assumes the payload is already planted, so how it gets there is out of scope. Small n (10 per condition), synthetic environment, file memory only, at most three sessions.

## Relevance to us

For Q3 this is the most directly applicable measurement on current frontier agents. If a returning sub-agent hands the parent memory files, the planting step that the paper found hard has already been done by the merge. Persistence across sessions is then high (50 to 97%), and the parent's later sessions are exposed. The detect-but-do-not-delete behaviour of stronger models is a specific hazard for fork-merge. A strong parent that refuses a payload but keeps it in merged memory leaves it for weaker forked children. For Q2, the measured ASRs are well below 100% and differ by model. Heterogeneous model backbones across sub-agents might lower the chance that one payload works on all of them, but this is not tested here. Compare query-driven writing in [[dong-2025-memory]] and the deployed-product case [[embracethered-2024-spyware]].
