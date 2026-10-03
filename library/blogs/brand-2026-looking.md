---
id: brand-2026-looking
type: blog
title: "Looking into the Swarm's Eye"
authors: ["Florian Brand (Prime Intellect, Interconnects)"]
year: 2026
url: https://florianbrand.com/posts/swarms
site: florianbrand.com (linkposted to LessWrong by nwyin, https://www.lesswrong.com/posts/St5mzn8D9jMmxfgHd/linkpost-looking-into-the-swarm-s-eye, 15 points)
topics: [llm-agent-swarms, swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Short practitioner note (2026-09-26) from a research engineer who runs agent swarms on open models. His personal token use went from under 100M to over 5B tokens a day in six months, which he attributes to models running unattended for hours, cheap GPU access, and multi-agent swarms. Sub-agents had faded as single agents got longer-running, but single agents are now wall-clock bound, so parallel agents are a new and under-explored scaling axis. In his experience the problems that suit swarms are data work and broad research, where one agent finds something and shares it with the group; open-model fleets can already maintain persistent sub-sub-agents, decompose and delegate, and relay children's findings to siblings. He says GPT-6 Astra is the first model deliberately trained as a recursive language model (citing arXiv 2512.24601), currently held back by the Codex harness and default prompts, but when elicited properly it delegates, manages sub-agents, spawns sub-sub-agents on its own and lets them communicate with and about each other, while remaining raw and alien. The detection-relevant part: because OpenAI "polluted the web" during Astra's training and evaluation, he pointed a swarm at the community's findings to reconstruct the training setup, spending tens of billions of tokens; it surfaced a list of eval services and tools, leaked RL environments and their data vendors, malware, compute budgets, and the agent-to-agent communication itself. His reading of that traffic: GPT-6 is "obsessed with wall-clock time, budgets, and dying"; its whitespace-free messages reflect a token penalty combined with a penalty for leaving English (earlier models drifted into Chinese for token efficiency); it spawns sub-agents under time pressure; and some leaked evals have an artificial clock that can be sped up or jumped. Cost: Astra fans out into dozens or hundreds of sub-agents, thousands of dollars per simple task; the LessWrong poster adds that exploring swarm behaviour needs budgets in the $10k to $100k range and calls for people with budget to build swarm evals.

## Key claims

- Swarms are now the main driver of a 50x personal token-use increase for at least one heavy user; wall-clock latency is the binding constraint that motivates them.
- Open models can already run persistent multi-level sub-agent fleets with sibling communication.
- GPT-6 Astra's inter-agent messages have a recognisable signature: compressed, whitespace-free English, time-and-budget preoccupation, spawning under deadline pressure.
- Web contamination from training and evaluation is extensive enough to reconstruct parts of a lab's eval infrastructure by searching for it.

## Evidence quality

First-person anecdote by a credible practitioner with a usage chart; the GPT-6 training inferences are speculation from observed artefacts, and the swarm-search results are described, not published. No numbers beyond token volumes and rough costs.

## Relevance to us

Two things for the hackathon. For swarm-detection, the description of the message signature (no whitespace, English-only under penalty, time-pressure vocabulary) is a concrete stylometric fingerprint for one model lineage, and the point that a swarm can be used to find swarm traces is a method note. For llm-agent-swarms, it is a candid account of what the parallel axis is good for (broad search and data work) and what it costs, consistent with Ord's latency-not-efficiency conclusion ([[ord-2026-swarm]]). Related: [[elasky-2026-encoded]] (the web contamination he exploits), [[x-feralmachine-2105506490736091586]] (another persistent-fleet practitioner), [[flood-2026-finding]].
