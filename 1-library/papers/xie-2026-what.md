---
id: xie-2026-what
type: paper
title: "What If Prompt Injection Never Left? Rethinking Agent Security through Cross-Session Stored Prompt Injection"
authors: [Yuanbo Xie, Wenlei Zhu, Tianyun Liu, Yingjie Zhang, Suchen Liu, Yulin Li, Liya Su, Tingwen Liu]
year: 2026
venue: arXiv preprint (position paper)
url: https://arxiv.org/abs/2606.04425
doi: null
arxiv: '2606.04425'
cite: "Xie, Y., Zhu, W., Liu, T., Zhang, Y., Liu, S., Li, Y., Su, L., & Liu, T. (2026). What If Prompt Injection Never Left? Rethinking Agent Security through Cross-Session Stored Prompt Injection. arXiv:2606.04425."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

A position paper with experiments that reframes prompt injection for stateful agents by analogy with stored cross-site scripting. Cross-Session Stored Prompt Injection (XSPI) has a lifecycle: attacker content is written into persistent state (memory, workspace files, tools), is later reincorporated into a new session started by a clean user request, and then activates. The authors give a taxonomy of persistence channels and incorporation mechanisms and build XSPI-Bench, a sandbox on an OpenClaw-like agent with memory, filesystem and tools in e-commerce, travel and finance domains.

## Contribution

Defines end-to-end attack success as the product of write success, incorporation rate and activation rate, and argues for "state-centric" security: governing how external information acquires authority as it enters long-lived state.

## Key results

- Measured: average end-to-end attack success 41.9% across scenarios and models, with scenario averages from 40.0% to 45.0%.
- Measured: decomposition shows large variation by stage; for example, some models write the payload to state readily but incorporate or act on it less (per-model write, incorporation and activation rates in Table 2).
- Measured: factual manipulation persists and activates far more often than preference manipulation in the reported e-commerce rows.
- LLM judge validated against human annotation (over 98% agreement, kappa 0.97) for semantic tasks.

## Methods and models

GLM-5.1, GPT-5-mini, MiniMax-M2.7, Llama-3.1-8B, DeepSeek-V4-Pro and others; three repetitions per case; deterministic checks where possible.

## Limitations and open questions

Position paper; benchmark built by the authors on their own agent harness; defences are proposed as principles rather than evaluated.

## Relevance to us

Q3, the persistence step. dmarz's attack needs corruption to survive the gap between the excursion and the merge. This paper measures that pattern within one agent across sessions: about 42% of attacks written into state come back and act in a later clean session. Fork-merge is the same lifecycle with the parent as the later session and the part's returned memory as the persistence channel. Its three-factor decomposition gives a parent three places to cut: refuse writes from untrusted provenance during the excursion, gate incorporation at merge, and constrain activation afterwards. Related: [[greshake-2023-not]], [[gadgil-2026-bad]], [[dash-2026-untrusted]], [[liu-2026-safe]], [[zerhoudi-2026-compaction]].
