---
id: abedini-2026-dont
type: paper
title: "Don't Trust Stubborn Neighbors: A Security Framework for Agentic Networks"
authors: [Samira Abedini, Sina Mavali, Lea Schönherr, Martin Pawelczyk, Rebekka Burkholz]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2603.15809
doi: null
arxiv: '2603.15809'
cite: "Abedini, S., Mavali, S., Schönherr, L., Pawelczyk, M., & Burkholz, R. (2026). Don't Trust Stubborn Neighbors: A Security Framework for Agentic Networks. arXiv preprint arXiv:2603.15809."
topics: [llm-agent-swarms, sync-consensus, sybil-resistance]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Models LLM multi-agent opinion dynamics with the Friedkin-Johnsen model and checks the fit empirically on 4 to 8 agents (Gemini-3-Flash, GPT-5 mini, GPT-OSS-120B, MiniMax-M2.5, Qwen3-235B, Ministral-3-14B) on CommonsenseQA and ToolBench. A single stubborn, persuasive adversary reaches about 65% attack success when it sits at a star hub, 33% in a fully connected graph and 24% at a star leaf. A trust-adaptive defence that down-weights peers by their track record cuts attack success while keeping cooperative accuracy.

## Contribution

Gives a closed-form account (stubbornness, persuasiveness, susceptibility) of how one confident agent can drag a whole LLM network to a false answer, and shows that the FJ model fits measured LLM-MAS dynamics.

## Key results

- One fully stubborn agent can in theory dominate the equilibrium opinion (proved).
- Attack success about 65% (star hub), 33% (full), 24% (star leaf) (measured).
- Defences: more benign agents, more benign stubbornness (which slows consensus), or trust-adaptive weighting from warm-up questions; the last reduces attack success with little accuracy loss (measured).

## Methods and models

Friedkin-Johnsen dynamics with innate opinion anchoring; experiments over star and complete topologies, 100 examples per task; trust warm-up of 10 questions. Skimmed via the HTML.

## Limitations and open questions

The adversary is stubborn by construction; the paper does not test whether a false belief persists after the adversary is removed or corrected. Trust weights rely on ground-truth scoring during warm-up.

## Relevance to us

V4: a planted agent that confidently mislabels a real resource as a honeypot is exactly a "stubborn neighbour", and topology (hub vs leaf) should set how far the false alarm spreads. The trust-adaptive defence is the swarm-level mirror of [[chen-2026-trust]]. Related: [[yan-2026-when]], [[zhong-2025-disentangling]], [[gans-2026-when]].
