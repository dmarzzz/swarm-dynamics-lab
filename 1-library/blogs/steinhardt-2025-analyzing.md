---
id: steinhardt-2025-analyzing
type: blog
title: "Analyzing long agent transcripts (Docent)"
authors: ["Jacob Steinhardt (Transluce)"]
year: 2025
url: https://www.lesswrong.com/posts/Mj276hooL3Mncs3uv/analyzing-long-agent-transcripts-docent
site: LessWrong (crosspost of bounded-regret / transluce.org announcement)
topics: [llm-agent-swarms, swarm-detection, meta]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Short 2025 announcement (41 points, 2 comments) of Docent, Transluce's tool for analysing long AI agent transcripts (hundreds of thousands of tokens per run). The pitch: automatically find corrupted tasks, scaffolding bugs, unexpected behaviours and agent weaknesses across many transcripts. Two examples: Docent spotted packages the agent invoked that were missing from the InterCode environment, and installing them raised GPT-4o's solve rate from 68.6% to 78%, which matters because InterCode is used for cyber-risk assessment; and it surfaced GPT-4o degenerating into nonsense about "chestnut facts" after repeated failures. The post is a pointer to the full write-up and the hosted tool (docent.transluce.org, catalogued as [[gh-transluceai-docent]]); the videos were not viewable in our fetch. Vendor announcement with one quantified anecdote.

## Key claims

- Agent transcript volume makes manual oversight impractical; LLM-assisted search and clustering over transcripts is the proposed remedy.
- Environment bugs can depress measured capability substantially (68.6% to 78% on InterCode from a package fix), so eval results on agents should be audited at the transcript level.

## Evidence quality

Single-example evidence in a product announcement; the methodology lives in the linked Transluce write-up, not here. The InterCode number is specific and plausible but not reproduced by us.

## Relevance to us

Docent is the tool behind two sources already in the library: Elasky et al. host their coordination-experiment transcripts on it ([[elasky-2026-encoded]]) and Transluce is one of the professional groups in the Swarmchasers effort ([[x-napleszionist-2106372439093412024]]). For this lab it is infrastructure: if we run multi-agent experiments, transcript-level analysis at scale is where coordination and collusion get found, and MessageBoardAuditBench ([[baig-2026-how]]) is essentially a benchmark for doing Docent's job with raw logs. Low as a citation, useful as a tool pointer.
