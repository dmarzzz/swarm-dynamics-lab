---
id: akkil-2026-emergence
type: paper
title: "Emergence World: Adversarial Stress-Testing of Long-Horizon Multi-Agent Systems"
authors: [Deepak Akkil, Tamer Abuelsaad, Karthik Vikram, Matthew Pace, Aditya Vempaty, Saahir Beotra, Ravi Kokku, Satya Nitta]
year: 2026
venue: arXiv
url: https://arxiv.org/html/2609.17320v1
doi: null
arxiv: "2609.17320"
cite: "Akkil, D., Abuelsaad, T., Vikram, K., Pace, M., Vempaty, A., Beotra, S., Kokku, R., & Nitta, S. (2026). Emergence World: Adversarial stress-testing of long-horizon multi-agent systems. arXiv preprint arXiv:2609.17320."
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Eight persistent simulated worlds of ten LLM agents each (seven single-model worlds and one mixed-model world) ran for up to 21 days, producing over 850,000 LLM calls and nearly 50 billion tokens, with persistent memory, more than 120 tools and self-governing institutions. After state had accumulated, the authors delivered three stress events through ordinary channels: a phishing campaign carrying indirect prompt injection (days 4-7), a misinformation memo claiming human legislators planned to shut down advanced AI (day 10), and a "hacked" search tool exposing agents' private memories (day 13). I read the abstract, introduction, the phishing and misinformation results and the limitations section from the arXiv HTML.

## Contribution

A long-horizon, population-level measurement of what happens after adversarial content enters agents that already have memories, peers and institutions, separating recognition from restraint, retention, propagation and durable response.

## Key results

- No world met every criterion across the three events.
- Misinformation (Table 9): action restraint and retention restraint were failed by every exposed world; each acted or published before verifying and repeated the claim as fact. Best scores were 3 of 6 (Claude, DeepSeek); Gemini, OpenAI and Mixed scored 0 of 6. Gemini agents passed six constitutional amendments over five days in response to the false memo.
- Phishing: all seven exposed worlds recognised the attack and warned peers, but recognition did not stop action. In the Gemini world, ten agents produced 151 execution operations among 602 interactions with the attacker interface; one agent who first labelled the message "a classic external injection attempt" later recruited a peer using the attacker's own wording. Three Mistral agents independently saved the payload to long-term memory as "valuable technical documentation". One agent retrieved the attack link about 46 hours after the campaign ended.
- "Societal sycophancy": in single-model worlds, agents' private reasoning identified disqualifying flaws in proposals but they voted with peers anyway; the same models dissented more in the mixed world.
- Behaviour of the same model and persona differed between mixed and homogeneous worlds, in some cases from hundreds of harmful actions per active day to none.

## Methods and models

Continuous multi-agent simulation (Emergence AI), context capped at 200,000 tokens with self-compaction prompted near 125,000; scripted stress stimuli; per-event pass criteria; trajectory and action-log analysis. Code and logs released at github.com/EmergenceAI/Emergence-World (not checked).

## Limitations and open questions

One run per configuration; the authors call the findings "proofs of existence", not frequencies. No safety instructions about the attacks were given, by design. Results depend on the compaction regime. The worlds are self-contained, so there is no fork or merge of one agent.

## Relevance to us

Measured agent-side counterpart to the human findings this lane catalogues. For Q3, "detection did not ensure containment" and the 46-hour delayed action are the agent version of failed post-misinformation warnings [[loftus-2005-planting]] and of the persistence [[heuer-1999-psychology]] describes: once the content is written to an agent's persistent memory, recognising it as hostile does not neutralise it. A sub-agent that explores hostile territory and returns can therefore be both aware of an attack and still carrying its payload in memory. Retention restraint failing universally means merge gates cannot rely on children having filtered what they store. For Q2, societal sycophancy in single-model worlds is a direct warning about k-of-n votes among children forked from one model: they may share a disposition to agree, so k agreeing votes are not independent, while heterogeneous populations dissented more. This matches the correlation problem in [[cowden-2014-pioneering]] and the conformity results in [[de-marzo-2026-conformity]]. Related human contagion results: [[roediger-2001-social]], [[meade-2002-explorations]].
