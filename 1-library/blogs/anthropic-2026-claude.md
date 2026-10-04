---
id: anthropic-2026-claude
type: blog
title: "Claude discovers a novel enzyme system with CRISPR-like repeats"
authors: [Anthropic]
year: 2026
url: https://www.anthropic.com/news/claude-discovers-novel-enzyme-system
site: anthropic.com
topics: [llm-agent-swarms]
added_by: shadow/sol-w1
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Anthropic announces a new life-sciences research group and wet lab, and its first result: about 950 parallel Claude agents, given one high-level prompt, searched a large DNA sequence database for new reverse transcriptase (RT) systems for 21 hours using about 210 million tokens. The agents gathered over 200,000 RTs, picked out about 3,500 new candidate systems, and narrowed them to the 20 most compelling, each written up as a human-readable report. One agent noticed a tandem repeat array next to an RT gene in jumbo phages that previous work had not described; humans named the system array-associated reverse transcriptase (ART): an RT, an adjacent accessory gene of unknown function, and a long array of evenly spaced repeats resembling a CRISPR array. First lab experiments (done by human scientists) show the array is expressed as distinct short RNAs. Function is still unknown. Human involvement is described as the initial prompt plus lab work; a harness of their own sometimes coordinates many parallel Claude sessions.

## Key claims

- Scale of the agent campaign: ~950 agents, 21 hours, ~210M tokens; funnel 200,000+ RTs to ~3,500 candidates to 20 reports (stated by Anthropic).
- An agent independently flagged the repeat array, counted repeats and spacing, compared with known RT systems and checked the literature before filing a report.
- ART arrays are transcribed into discrete short RNAs (first experiments, details in the preprint).
- Hypothesis volume is now large enough that the hypotheses themselves are studied, to learn which proposals humans judge worth testing and feed that taste back into instructions.
- Feng Zhang (MIT/Broad), after reviewing the preprint, called the RNA-repeat arrays "genuinely intriguing".

## Evidence quality

Vendor announcement accompanied by a technical preprint (https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf, not read for this entry). The biological claim is at the "new candidate system with initial expression data" stage; function is unvalidated. The agent-campaign numbers are self-reported with no description of the coordination harness, the failure rate of the 3,500 candidates, or how duplicates across agents were handled. The batch item that surfaced it (@techwithjoe_io, status 2103126249921036726) gives slightly different numbers (215M tokens, 3,564 candidates, 19 dossiers) and attributes caveats to Hacker News; those figures are not in this post and are not used here.

## Relevance to us

A rare public, quantified example of a large homogeneous LLM agent swarm (hundreds of copies, one prompt, shared search space) producing a verifiable discovery. Useful as a scale and design reference for llm-agent-swarms: it is a broad-parallel search with a funnel of self-critique and human review rather than an interacting society. It also frames hypothesis triage as the bottleneck when a swarm generates thousands of candidates, which bears on any swarm-aggregation design.
