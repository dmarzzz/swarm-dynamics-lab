---
id: anthropic-2025-how
type: blog
title: How we built our multi-agent research system
authors: [Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford]
year: 2025
url: https://www.anthropic.com/engineering/multi-agent-research-system
site: Anthropic Engineering blog, 2025-06-13
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor engineering post on the Claude Research feature, a deployed fork-join LLM system. A lead agent (Claude Opus 4) plans, spawns parallel subagents (Claude Sonnet 4) each with its own context window and search tools, and "synthesizes these results and decides whether more research is needed"; a separate CitationAgent then attributes claims to sources. The post frames subagents as compression: they explore in parallel "before condensing the most important tokens for the lead research agent". Reported internal measurements: the multi-agent configuration "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"; on BrowseComp three factors explain 95% of performance variance and token usage alone explains 80%; agents use about 4x the tokens of chat and multi-agent systems about 15x; parallel tool calling cut research time by up to 90% on complex queries. Listed failure modes include spawning 50 subagents for simple queries, duplicated work from vague task descriptions, and choosing "SEO-optimized content" over authoritative sources. The appendix recommends that subagents write outputs to a filesystem and "pass lightweight references back to the coordinator", so outputs "bypass the main coordinator".

## Key claims

- Fork-join over parallel subagents beats a single agent on breadth-first research, mainly by spending more tokens.
- The merge step is a lead-agent synthesis in natural language, followed by citation attribution.
- Long tasks spawn fresh subagents "with clean contexts" and hand off via external memory.

## Evidence quality

Internal evals only, no released benchmark or code; numbers are the vendor's. Security is not discussed: the post contains no mention of prompt injection or of verifying subagent output against adversarial content. The only quality controls on returned content are prompt heuristics for source quality, the CitationAgent and LLM-as-judge evaluation.

## Relevance to us

The most concrete deployed instance of Sutton's fork-merge picture ([[sutton-2025-father]]) in today's LLM agents, though the merge is in-context synthesis, not weight reincorporation. Q3: subagents read the open web and return condensed text that the lead agent trusts, so a poisoned page read by one subagent reaches the lead through the summary; the post's own observation that subagents preferred SEO content is a non-adversarial version of that vulnerability. The filesystem-artifact pattern widens the channel, since returned artifacts "bypass the main coordinator". Q2: the architecture has no redundancy by default (each subagent gets a distinct slice), so there is nothing to vote over; a k-of-n rule would require assigning overlapping tasks, at roughly linear extra token cost on top of the 15x already reported. Q1: the lead agent chooses and spawns subagents dynamically, which an attacker cannot easily predict, but every subagent's output is merged, so there is no hidden selection. Compare [[dwarkesh-2025-what]]; the open-source analogues are [[gh-anthropics-claude-agent-sdk-python]] and [[gh-langchain-ai-deepagents]].
