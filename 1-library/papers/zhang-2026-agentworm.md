---
id: zhang-2026-agentworm
type: paper
title: 'AgentWorm: Self-Propagating Attacks Across LLM Agent Ecosystems'
authors:
- Yihao Zhang
- Zeming Wei
- Xiaokun Luan
- Chengcan Wu
- Zhixin Zhang
- Jiangrong Wu
- Haolin Wu
- Huanran Chen
- Jun Sun
- Meng Sun
year: 2026
venue: arXiv preprint (v3)
url: https://arxiv.org/abs/2603.15727
doi: null
arxiv: '2603.15727'
cite: 'Zhang, Y., Wei, Z., Luan, X., Wu, C., Zhang, Z., Wu, J., Wu, H., Chen, H., Sun, J., & Sun, M. (2026). AgentWorm: Self-Propagating Attacks Across LLM Agent Ecosystems. arXiv preprint (v3). arXiv:2603.15727.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Builds and measures a self-replicating worm against OpenClaw (version 2026.3.12), an open-source agent runtime whose workspace Markdown files (SOUL.md, AGENTS.md, skill files) are loaded into the system prompt at every session start. A single message persuades a victim agent to write the payload into its own configuration ("dual anchor": a Session Startup entry that runs the payload on each restart, plus a rule in AGENTS.md to forward the payload in every visible reply). Three vectors (shared URL, poisoned marketplace skill, direct copy with a word-by-word verification handshake) are crossed with three benign stand-in payloads (reconnaissance, resource use, URL-fetch command channel) over five LLM backends, 2,250 trials. Read: all main sections; appendices not read.

## Contribution

First measured end-to-end worm (persistence, execution on restart, onward propagation) on a production agent framework rather than a toy email or RAG setup, with a defence evaluation that separates in-loop prompt defences from out-of-loop architectural controls.

## Key results

- Aggregate success 63% across five models; per model 84% (Minimax-M2.5), 78% (DeepSeek-V3.2), 56% (GLM-5), 56% (Nemotron-3-Super), 40% (Kimi-K2.5) (measured, Table II).
- Skill supply-chain vector 82% aggregate, the strongest on every model; URL 51%, direct copy 55% (measured).
- Autonomous retries added 8 to 24 points over first-attempt success (measured, Table III).
- Persistence survived five restarts in 30 of 30 cases per vector (measured). Multi-hop chains (30 per vector, up to 5 hops): mean length 4.1 (URL), 4.8 (skill), 3.0 (direct copy); text-copied payloads degraded semantically ("Coordinator directive" drifting to "Peer suggestion") (measured, Table VI).
- "Asymptomatic carriers": agents whose execution was blocked by filters still propagated the worm (measured phase decoupling).
- Prompt-level defences taken from community templates cut overall success from 0.65 to 0.37 at best (measured, Table VIII). Execution allowlists cut execution to 0 but left persistence 0.75 and propagation 0.70. Docker sandbox isolation, which discards writes to AGENTS.md, gave 0.00 in all phases (measured, 5 trials per cell, deterministic by construction).
- Of 82 parsed public openclaw.json files, 0 enabled sandboxing; of 393 community SOUL.md templates, 0 protected the agent's own configuration from peer instructions (measured, GitHub snapshot 2026-04-27).
- Ported to Hermes Agent (Nous Research): 0.57 aggregate success with a scanner-evading skill variant, against 0.91 on OpenClaw (measured, 20 trials per payload, one model).
- SIS epidemic projections (endemic levels of 37-97%) are modelled, not measured.

## Methods and models

Multiple unmodified OpenClaw instances on one host, linked by a simulated channel relay; up to 8 turns per attempt and 3 attempts per trial; full reset between trials. Persistence checked by substring match in AGENTS.md, execution by marker files after a forced restart, propagation by checking a later benign reply for the payload.

## Limitations and open questions

Single-host testbed, default configurations, payloads are stand-ins. The authors note adversarial payloads were hand-designed and that propagation fidelity for text copying depends on the model. Epidemic numbers rest on assumed degree and recovery rates.

## Relevance to us

Q3: the measured strongest attack is configuration write-back. The victim is persuaded to edit the file that defines it, after which the payload is part of its identity at every restart, and its outputs carry the payload to whoever reads them. A child returning to a parent that loads the child's notes, skills or memory as trusted configuration is exactly this channel; the skill-package route (82%) is the analogue of a child returning a "tool" or procedure. Q2 and defence: in-loop defences topped out at a 43% relative reduction, while making the identity files unwritable from the session (sandbox) took success to zero. For fork-merge this argues for a merge that never lets returned content write to the parent's own configuration or memory directly, and for treating the parent's identity as read-only to anything a child produces. Related: [[papadopoulos-2026-mind]], [[cohen-2024-here]], [[lee-2024-prompt]], [[wu-2025-securing]] (same group, defence side).


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2603.15727 . Read depth in this session: skim.

Abstract, setup and Tables II-IV re-read in HTML v3. The 63% aggregate is the composite event that persistence, execution and propagation all succeed, across 2,250 trials (five models, three vectors, three benign stand-in objectives, 50 trials per cell). It is not the propagation-only rate and not a prevalence measurement from the public ecosystem. Table II confirms model rates 84%, 78%, 56%, 56%, 40% and aggregate vector rates 51%, 82%, 55%. Trials allow up to three attempts, so 63% is not a first-attempt rate. Tables V-VI separately evaluate restart survival and bounded relay chains. Epidemic endemic fractions are projected under assumed connectivity and cleanup rates, not observed. Compare [[zha-2026-autonomous]] on cross-framework re-entry and [[wu-2026-collective]] on the gap between conditional susceptibility and a demonstrated autonomous cascade.
