---
id: cai-2026-child
type: paper
title: "When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks"
authors: [Ziwen Cai, Yihe Zhang, Xiali Hei]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2605.08460
doi: null
arxiv: "2605.08460"
cite: "Cai, Z., Zhang, Y., & Hei, X. (2026). When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks. arXiv preprint arXiv:2605.08460."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A security analysis of the spawn (fork) side of LLM multi-agent frameworks. The authors give a role-based formal model of agent networks with three invariants: termination scope (only the direct parent or root may terminate an agent), memory isolation (a child gets only a parent-selected projection of memory) and resource access control (a child gets only the tools its role needs). Testing OpenClaw (primary subject), Hermes and Agent Zero, they report four vulnerabilities: unrestricted memory inheritance ("A single prompt injection propagates to every descendant agent"; in OpenClaw `sessions_spawn` injects AGENTS.md and TOOLS.md and merges the parent's authentication profiles into the child), missing resource access control, asynchronous memory divergence (stale or revoked context persists in already-spawned children) and unauthorized sibling termination. In a proof of concept, a session-based subagent told within its own session to terminate a sibling did so "without any parent authorization". An ablation reports that models from five additional vendors all reproduced the core behaviours. Proposed defences: an Agent Capability Registry using the PDP/PEP access-control pattern with immutable per-child capability sets (kill only along a parent edge), role-scoped memory projection and a revision-based synchronisation protocol.

## Contribution

Frames subagent inheritance and lifecycle authority, not model behaviour, as the root cause of cross-agent compromise, with invariants that can be checked.

## Key results

- Four structural vulnerabilities demonstrated in real open-source frameworks, not uniformly present in all three.
- Sibling termination via natural-language instruction succeeds without an exploit.
- Vulnerabilities compound: inheritance spreads the payload, missing access control arms it, divergence defeats parent-side remediation, sibling termination removes oversight agents.

## Methods and models

Formal role-based model; manual proof-of-concept attacks on OpenClaw, Hermes and Agent Zero; cross-vendor ablation.

## Limitations and open questions

Proofs of concept rather than measured attack success rates; the model assumes role-specialised agents and does not cover undifferentiated agents. The study covers the parent-to-child direction and lateral sibling attacks, not the child-to-parent merge.

## Relevance to us

Measured evidence for two parts of dmarz's Q3 attack sketch. "Cut anyone else out" has a demonstrated mechanism: a compromised child terminating siblings, which in a fork-merge system would remove the honest children whose votes a k-of-n rule (Q2) relies on, so termination authority must be part of any threshold design. And memory inheritance shows why identical forks are fragile: a payload in the parent's memory reaches every child, the copy-clan failure mode from [[bostrom-2023-propositions]]. The divergence finding cuts the other way for the merge: a parent that cleans its memory cannot reach children already spawned, so they return carrying the old state. The paper does not test the return path, which [[anthropic-2026-create]] and [[loven-2026-meld]] address from the defender's side. Context: [[sutton-2025-father]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Read depth this session: abstract. Source opened: https://arxiv.org/abs/2605.08460 .

Primary abstract re-opened. Memory inheritance is a parent-to-child propagation path, whereas the task primarily concerns child-to-parent reintegration; the directions should be evaluated separately. Framework isolation and termination invariants are not themselves measured worm extinction rates.
