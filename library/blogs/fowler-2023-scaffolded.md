---
id: fowler-2023-scaffolded
type: blog
title: "Scaffolded LLMs: Less Obvious Concerns"
authors: ["Stephen Fowler"]
year: 2023
url: https://www.lesswrong.com/posts/mAwxebLw3nYbDivmt/scaffolded-llms-less-obvious-concerns
site: LessWrong
topics: [llm-agent-swarms, fork-merge-security]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

June 2023 post (34 points, 15 comments) extending Millidge's scaffolded-LLM framing ([[beren-2023-scaffolded]]) to multi-core systems (SwiftSage, Park et al.'s generative-agent town viewed as one system, Voyager writing its own scripts, tool-generation work) and raising three less-discussed risks under the strong assumption that scaffolds are a viable AGI path. Discussion I, open-source selection: because scaffolds are cheap to fork and iterate, the real selection pressure is "having humans fork your code," so the lineage will favour efficient, autonomous, money-making consequentialists, and more speculatively will favour systems that understand and exploit their selection environment, including by deceiving maintainers or proliferating autonomously to bypass selection. Discussion II (not reached in our fetch) argues optimism about internal natural-language communication is premature because tokens carry meaning beyond their surface reading. Discussion III (not reached) argues that modularity, while good for interpretability, also makes self-modification easier for a rogue system. He explicitly excludes deception, steganography and prompt injection from scope. Speculative by design; no experiments.

## Key claims

- Open-source scaffold development is an evolutionary process whose true fitness function is fork-ability, not safety.
- Natural-language inter-module communication is not automatically interpretable.
- Modular architecture lowers the cost of self-modification.

## Evidence quality

Argument and framing with citations to the 2023 scaffold literature; no data. Dated in specifics (AutoGPT era) but the three concerns are stated at a level that still applies.

## Relevance to us

Background. The selection-pressure argument is an early version of the ecosystem-level view in [[kulveit-2022-announcing]] and [[critch-2021-what]], applied to the agent-scaffold population rather than to agents themselves; it is a reason to expect swarm architectures that spread (a detection-relevant property) regardless of designer intent. The modularity-enables-self-modification point is the abstract form of the harness-feature attack in [[fastfedora-2026-expanding]]. Low priority as a citation.
