---
id: zhong-2025-disentangling
type: paper
title: 'Disentangling the Drivers of LLM Social Conformity: An Uncertainty-Moderated Dual-Process Mechanism'
authors: [Huixin Zhong, Yanan Liu, Qi Cao, Shijin Wang, Zijing Ye, Zimu Wang, Shiyao Zhang]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2508.14918
doi: null
arxiv: '2508.14918'
cite: 'Zhong, H., Liu, Y., Cao, Q., Wang, S., Ye, Z., Wang, Z., & Zhang, S. (2025). Disentangling the Drivers of LLM Social Conformity: An Uncertainty-Moderated Dual-Process Mechanism. arXiv preprint arXiv:2508.14918.'
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Adapts the information-cascade paradigm of [[bikhchandani-1992-theory]] to nine LLMs (GPT-4o, o4-mini, Mistral Small 3.1, Claude 3.7 Sonnet, Gemini 2.5 Flash and Pro, Llama 4 Maverick, DeepSeek-R1, Qwen3-235B). Each decision gets one private signal and one to three public predecessor decisions in medical, legal and investment scenarios with signal accuracies q = 0.667, 0.55 and 0.70. Fitted weights show models underweight all evidence at low-to-medium uncertainty but overweight public signals at high uncertainty (public beta above 1.55 vs private 0.81).

## Contribution

The only paper found that fits Bikhchandani-style private-versus-public signal weights to LLM decisions, giving an empirical handle on when an LLM agent will follow predecessors over its own evidence.

## Key results

- High uncertainty: public-signal weight above 1.55 vs private 0.81, i.e. normative-like amplification of others' choices (measured).
- Medium uncertainty: conservative underweighting of all sources (beta about 0.56 to 0.66) (measured).
- Low uncertainty: private signal dominates (0.85 vs about 0.71 public) (measured).
- Authors argue this makes LLM groups vulnerable to wrong cascades under uncertainty (interpretation; cascade chains were not run end to end).

## Methods and models

Single-shot prompts with private and public cues, 52 trials per task repeated three times, logistic weight estimation. Skimmed via the HTML.

## Limitations and open questions

Public signals are presented as advisors' decisions, not as a live chain of agents, so cascade formation and breaking are inferred from weights rather than observed. No correction or late public information release.

## Relevance to us

V4 (false-alarm cascades): when a resource is ambiguous, a single peer flag may be overweighted relative to the agent's own inspection, which is the condition under which a false alarm should cascade. Suggests V4 should vary how ambiguous the falsely flagged resource is. See also [[cho-2025-herd]] and [[abedini-2026-dont]].
