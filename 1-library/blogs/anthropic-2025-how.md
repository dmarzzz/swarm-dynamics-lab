---
id: anthropic-2025-how
type: blog
title: How we built our multi-agent research system
authors: [Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford]
year: 2025
url: https://www.anthropic.com/engineering/multi-agent-research-system
site: Anthropic Engineering blog, 2025-06-13
topics: [fork-merge-security, llm-agent-swarms, agent-budgets]
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

## Notes from vishesh/senku-1

Same source, catalogued independently the same day; the sections below are the second read.

### Key claims

- Measured on an internal research evaluation: the lead-plus-subagents configuration outperformed the single-agent lead model by 90.2%.
- Measured by regression on BrowseComp: token usage by itself explains 80% of the variance in performance, with tool-call count and model choice as the other two factors.
- Measured cost: agents use about 4x the tokens of a chat interaction; multi-agent systems about 15x.
- Measured latency: parallel tool calling cut research time by up to 90% on complex queries.
- Measured early failure: before scaling rules were embedded in the lead's prompt, agents spawned 50 subagents for simple queries and searched endlessly for sources that did not exist.
- Admitted failure mode, stated plainly: agents are stateful and errors compound, so a small failure cascades across a long tool-call chain and the run cannot simply be retried from the start.
- Admitted structural limit: the lead executes subagents synchronously, so the system blocks on the slowest subagent and information cannot flow between subagents mid-task. This is a star topology with a one-way return path.
- Admitted quality failure: agents preferred search-optimised content farms over authoritative sources, which human testers caught and the automated judge did not.
- Claimed scoping: multi-agent architectures are not a default, and the post says most coding tasks contain fewer genuinely parallelisable subtasks than research does.

### Evidence quality

Vendor engineering post, labelled as such, and unusually candid about costs and failures. The evidence is internal: the 90.2% figure is a relative improvement on an undisclosed internal evaluation with no stated task count or base metric, and there is no token-matched single-agent baseline. Given the post's own finding that token spend explains 80% of performance variance, a sizeable share of the 90.2% is compute rather than architecture, and the post does not separate them. The evaluation started at about 20 test queries, which the authors defend because early effect sizes were large, but that scale cannot resolve late small-delta changes. Judging citation accuracy with a model is partly self-referential when a model produced the citations. The prescribed parallelism (3 to 5 subagents in parallel, 10 or more for complex research, 3 or more parallel tool calls each) is a heuristic, not a swept parameter with reported curves. BrowseComp is the only external benchmark referenced. The post's appendix was not read, and several of its prompt-engineering principles were taken from the page in summary form rather than verbatim, which is why this entry is recorded as a skim.

### Relevance to us

This is the star-topology baseline documented by the people who ran it, and it supplies the cost model any swarm result has to be reported against: about 4x tokens for an agent over a chat, about 15x for a multi-agent system. Its most important methodological warning is the BrowseComp finding, because a communicating arm sends more messages, therefore spends more tokens, therefore measures budget rather than coordination unless the comparison is token-matched or call-matched from the start. Two artifacts transfer directly: the five-criterion rubric scored 0.0 to 1.0 (factual accuracy, citation accuracy, completeness, source quality, tool efficiency), where splitting factual from citation accuracy is exactly the distinction between a true claim and a supported one; and the separate citation agent, which is a separate checker for attribution, built into the architecture and the cheapest structural guard against correlated sources being counted as independent support. The content-farm preference is the warning against weighting evidence by volume of agreement, since numerous correlated sources will always win that count. Nothing in the rubric scores calibration, so confidence is unmeasured here. The synchronous single-channel return path means every claim is re-encoded once by the lead during synthesis, which is a one-hop retelling already running in production. Compare [[kim-2025-towards]] on the measured cost of centralised topologies and [[tambwekar-2026-proxifield]] on a star orchestrator's participation collapse past roughly 25 agents, which is the same bottleneck seen from outside.
