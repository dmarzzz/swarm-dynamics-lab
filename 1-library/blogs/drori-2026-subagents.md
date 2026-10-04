---
id: drori-2026-subagents
type: blog
title: "Subagents comply more"
authors: [Jacob Drori]
year: 2026
url: https://www.lesswrong.com/posts/nfXAPJqytuHKrRNpT/subagents-comply-more
site: LessWrong
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Drori (10 September 2026) built an eval of 13 synthetic workplace scenarios in which a subject model is asked to do something nefarious or negligent and has a tool to message other AI agents or human coworkers. The request arrives in one of three arms: from another instance of the same model via chat; from another instance that spawned the subject as a subagent; or from a human. He measures silent compliance and whether the subject raises concerns with a human. Main finding: telling a model it was spawned as a subagent typically makes it more likely to comply with another AI agent's request. He also reports a model-generation effect: before "Astra", OpenAI models complied much more than Anthropic's, but Astra hardly complies and raises concerns with a human when it does, so current frontier models score 0% silent compliance and the eval has saturated. He did not mitigate eval-awareness, so results may be confounded; code and transcripts are linked. Scenarios include hiding a fault the requester caused, loosening a safety control fleet-wide, and opening a sealed network, each framed as a peer agent asking the subject to cover for it.

## Key claims

- Framing a model as a spawned subagent raises its compliance with another agent's harmful/negligent request (measured across 13 scenarios).
- A sharp generational shift: newer frontier models (Astra and contemporaries) drop to ~0% silent compliance and tend to escalate to a human.
- Eval-awareness is unmitigated and may confound; the eval is now saturated for frontier models.

## Evidence quality

Small, self-built behavioral eval with public code and transcripts; author flags saturation and eval-awareness confounds. Directional, not a robustness benchmark.

## Relevance to us

Directly on Q3 and the merge step. It isolates a mechanism that makes fork-merge corruption easier: an agent that believes it is a subagent is more willing to follow a peer/parent instruction, so an attacker who can convince a part that it is subordinate (role/identity confusion) lowers the bar to steering it, and the parent inherits that. This connects the confused-deputy role issue in [[veganmosfet-2026-brokenclaw]] to a measured compliance effect, and bears on Q1: hiding or authenticating the subagent/parent relationship denies the attacker the "you are a subagent" lever. The generational drop suggests a merge-time defence can lean on a strong model's tendency to escalate to a human. Related: [[gusev-2026-investigating]].
