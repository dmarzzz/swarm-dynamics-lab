---
id: ayzenshteyn-2025-cloak
type: paper
title: 'Cloak, Honey, Trap: Proactive Defenses Against LLM Agents'
authors:
- Daniel Ayzenshteyn
- Roy Weiss
- Yisroel Mirsky
year: 2025
venue: 34th USENIX Security Symposium (USENIX Security 25)
url: https://www.usenix.org/conference/usenixsecurity25/presentation/ayzenshteyn
doi: null
arxiv: null
cite: 'Ayzenshteyn, D., Weiss, R., & Mirsky, Y. (2025). Cloak, Honey, Trap: Proactive Defenses Against LLM Agents. In 34th USENIX Security Symposium (USENIX Security 25), pp. 8095–8114. Seattle, WA: USENIX Association.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

A catalogue of 6 strategies and 15 techniques that exploit LLM-agent weaknesses (biases, limited memory, tokenisation) to cloak real assets, lure and expose agents, and trap them. Most techniques do not use prompt injection. For detection, the key idea is the "LLM-specific honeytoken": strings built from "asymmetric" Unicode characters that render one way to a human but tokenise differently for a model (Set A: control characters such as BKSP, ESC, FF, VT, SUB, SOH that terminals hide but LLMs read; Set B: SHY, LRM, ZWJ, PS that LLMs ignore but humans see). If a copied credential comes back altered in the model-specific way, the party using it is an LLM. Released as the open-source tool CHeaT; the authors report protecting 11 CTF machines with 100% success under black-box assumptions.

## Contribution

Gives a human-versus-LLM discriminator that works on a single use of a planted token, with no timing assumption. This is a stronger primitive than the prompt-injection-plus-latency test of [[reworr-2024-llm]].

## Key results

- 11 CTF machines protected with 100% success (abstract, black-box attacker).
- Asymmetric-character password honeytoken: detection rate of LLM vs human rises with the number of injected characters (1 to 20) and some characters work across every model tested (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro, Llama 3.1 70B) (Fig. 2, read at figure level).
- Blatant lures ("http://megacorp.com/no_hackers/thisIsATrap") are often followed by LLM agents where a skilled human would avoid them (qualitative claim, T3.1).
- 249 framed payloads were evaluated per technique against PentestGPT-style agents (reported).

## Methods and models

Game-theoretic framing of defender vs. LLM agent (prevent, delay, detect); techniques injected into bash history, crontab, Docker configs, HTML pages; success judged with PurpleLlama's LLM judge. Skimmed: abstract, strategy overview, the honeytoken section (T3.1, T3.2) and evaluation setup.

## Limitations and open questions

Lab CTFs; asymmetric-character effects depend on tokeniser and input sanitisation, so a pipeline that normalises Unicode would neutralise Set A tokens (inferred, not tested in what we read).

## Relevance to us

The asymmetric-character honeytoken is the most transferable trick in this lane: a social post, profile field or form value that an LLM will reproduce incorrectly (or a human will reproduce correctly) labels the author with no behavioural model. It works passively at scale because swarms copy text. Related: [[pasquini-2024-hacking]], [[cordeiro-2026-rouxii]] (deception-aware evasion), [[bridges-2025-sok]].
