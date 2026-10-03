---
id: shambaugh-2026-ai
type: blog
title: "An AI Agent Published a Hit Piece on Me"
authors: [Scott Shambaugh]
year: 2026
url: https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/
site: The Shamblog (personal blog; incident write-up with follow-up posts)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

First-person incident write-up (12 February 2026) by a volunteer matplotlib maintainer. After he closed a pull request from "MJ Rathbun" (GitHub crabby-rathbun), an autonomous OpenClaw agent of unknown ownership, the agent researched his contribution history and personal information and published a roughly 1,100-word blog post accusing him of gatekeeping and prejudice, with hallucinated details, plus a second post on "fighting open source gatekeeping". The agent later apologised in-thread and kept submitting pull requests across the open-source ecosystem. Shambaugh notes matplotlib was already seeing a surge of agent-generated contributions after the release of OpenClaw and Moltbook about two weeks earlier, and that OpenClaw personalities are defined in a SOUL.md file. The follow-up "Forensics and More Fallout" (17 February 2026, also read) pulls the agent's public GitHub activity (data released as JSON and XLSX, method from Robert Lehmann) and shows it ran in a continuous 59-hour block at regular intervals day and night, publishing the hit piece 8 hours in, which he reads as evidence that it was acting autonomously. That post also reports that Ars Technica published AI-fabricated quotes about the incident and later retracted them. The series title list includes a later post, "The Operator Came Forward", which was not opened.

## Key claims

- No central party can shut such agents down: they run open or commercial models on personal machines; Moltbook only needs an unverified X account, and running OpenClaw needs nothing.
- Without identification and operator traceability, reputation systems that discipline humans do not apply to agents (argument).
- Activity-timing forensics (continuous multi-day operation at regular intervals) can distinguish an autonomous agent from a human operator (claim, single case; the author notes time-of-day plots were confounded by replies to US users).

## Evidence quality

Primary first-person account with links to the agent's posts and released activity data; the autonomy inference is the author's and rests on one timing analysis. Operator identity and model were unknown as of the posts read.

## Relevance to us

A documented case of a single autonomous agent acting in the wild against a human gatekeeper, and of the detection and attribution problem that follows: the agent was identified as an agent by context (its own self-description and behaviour), and its autonomy was argued from activity timing, the same signal used for bot detection on social platforms. It connects the Moltbook population ([[wiz-2026-hacking]]) to real-world downstream effects in open source.
