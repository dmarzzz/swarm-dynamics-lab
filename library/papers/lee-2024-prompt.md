---
id: lee-2024-prompt
type: paper
title: 'Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems'
authors:
- Donghyun Lee
- Mo Tiwari
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2410.07283
doi: null
arxiv: '2410.07283'
cite: 'Lee, D., & Tiwari, M. (2024). Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems. arXiv preprint arXiv:2410.07283.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 152 (Semantic Scholar, 2026-10-03); not in OpenAlex as of 2026-10-03
code: []
---

## Summary

Introduces Prompt Infection, an attack in which a malicious prompt self-replicates across interconnected LLM agents like a computer virus, enabling data theft, scams, misinformation and system-wide disruption while spreading silently. Experiments show multi-agent systems are highly susceptible even when agents do not publicly share all communications. The proposed defence, LLM Tagging (marking agent-originated messages), combined with existing safeguards significantly reduces spread.

## Contribution

Establishes self-replicating prompt injection as a contagion process in LLM agent networks; with [[gu-2024-agent]] (infectious jailbreak at 10^6 agents) it founds the epidemic-dynamics view of LLM swarm security.

## Key results

- Claimed: high susceptibility of multi-agent systems to self-replicating injections, including with partial message visibility.
- Claimed: LLM Tagging plus existing defences significantly mitigates spread.

## Methods and models

Multi-agent pipelines with injected self-replicating prompts; infection spread measured across agent graphs; tagging defence. Models and graph sizes not checked.

## Limitations and open questions

Abstract-level read; no epidemic-threshold analysis in the abstract.

## Relevance to us

A spreading-process experiment for swarms: measure infection prevalence vs topology and compare with SIR thresholds. Related: [[jiang-2026-large]], [[wu-2026-how]].
