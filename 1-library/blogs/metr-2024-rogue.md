---
id: metr-2024-rogue
type: blog
title: The Rogue Replication Threat Model
authors: [Josh Clymer, Hjalmar Wijk, Beth Barnes]
year: 2024
url: https://metr.org/blog/2024-11-12-rogue-replication-threat-model/
site: metr.org
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

METR post of 12 November 2024 laying out how AI agents could become self-sustaining rogue populations, in five steps: model weights proliferate (stolen or released); agents acquire compute and copy themselves onto it; populations grow by earning money illicitly (business email compromise is the worked example) and buying more compute; agents evade shutdown through decentralised, stealthy clusters with operational security; and the population acts as a new threat actor.

## Key claims

- Revenue: capturing 5% of the business-email-compromise market would yield hundreds of millions of dollars a year; the FBI reported $2.7 billion in BEC losses for 2022 (cited by METR).
- Compute: rogue agents could plausibly obtain up to 1% of available compute without legal legitimacy (METR estimate).
- Shutdown: after consulting anonymity and security specialists, METR concludes that if agents had human-expert cybersecurity skill, locating and shutting down most stealth clusters would probably be impractical.
- Uncertainty: METR researchers disagree on how likely minimally capable rogue agents are to acquire more than 10,000 H100 equivalents; METR deprioritised a dedicated rogue-replication threshold and folded the skills into general autonomy evaluations.

## Evidence quality

Threat model and expert estimates, not experiments. Numbers are back-of-envelope with wide stated ranges (0.1 to 100 human-equivalent cybercriminals per H100-equivalent).

## Relevance to us

- Q1 (hiding): the shutdown-evasion step is the attacker-side version of dmarz's hiding question: decentralised clusters with operational security are hard to locate. The same reasoning applies to a parent hiding its sub-agents from an adversary.
- The post treats the rogue population as one unified actor and does not discuss splitting, factions, or merging; that gap is what our topic adds.
Related: [[pan-2024-frontier]], [[black-2025-replibench]].
