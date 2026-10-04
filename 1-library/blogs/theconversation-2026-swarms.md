---
id: theconversation-2026-swarms
type: blog
title: "Swarms of AI bots can sway people's beliefs – threatening democracy"
authors: [Filippo Menczer]
year: 2026
url: https://doi.org/10.64628/aai.9w9jwuta3
site: The Conversation (op-ed by a researcher; DOI-registered, published 12 Feb 2026)
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Opinion piece by Filippo Menczer (Indiana University, OSoMe, Botometer) summarising his group's evidence and argument on malicious AI swarms. Evidence recapped: in mid-2023 they found the fox8 botnet, over a thousand crypto-scam accounts posting ChatGPT text, identifiable only because operators left self-revealing refusals ("As an AI language model...") in posts; the bots faked engagement among themselves and with humans, gamed the recommender, and gained followers; Botometer and AI-text detectors could not separate them from humans in the wild. Argument: today's open models plus relaxed moderation and monetised engagement let operators run large numbers of autonomous, adaptive, coordinated agents that produce varied, personalised content, so "copy-paste" detection fails. In a simulation study his team ran, infiltration of a target community was by far the most effective influence tactic, producing "synthetic consensus" via social proof. Mitigations proposed: researcher data access, studying swarm collective behaviour, detection of coordination patterns in timing, network movement and narrative trajectory (agents can look different but shared objectives leave traces), watermarking and labelling AI content, and demonetising inauthentic engagement. Closes by asserting these tactics are already deployed.

## Key claims

- fox8 (2023) shows LLM-driven coordinated botnets exist and evaded Botometer and AI-text detectors (measured, in [[yang-2023-anatomy]] and [[data-fox8-2023]]).
- Infiltration is the most effective swarm tactic in their simulation model (measured in simulation, cited as a PNAS Nexus 2024 study, not opened here).
- Coordination-based detection (timing, network, narrative trajectory) is the main hope, because content varies (claim; method lineage in [[pacheco-2021-uncovering]]).
- "Tactics are already being deployed" beyond fox8 (asserted, no new evidence given in the piece).

## Evidence quality

Opinion piece by the lead researcher, resting on his group's peer-reviewed work: fox8 ([[yang-2023-anatomy]]), the Science policy forum on malicious AI swarms ([[schroeder-2025-how]]), coordinated-network detection ([[pacheco-2021-uncovering]]), and a simulation of inauthentic-account tactics (PNAS Nexus, not yet catalogued). Policy and political statements are opinion. No new data.

## Relevance to us

Short, quotable statement of the swarm-detection problem as the field's best-known group frames it: content-level detection has failed against LLM bots; coordination traces are the remaining signal. Good framing citation for the swarm-detection survey; cite the underlying papers for evidence.
