---
id: motwani-2024-secret
type: paper
title: 'Secret Collusion among AI Agents: Multi-Agent Deception via Steganography'
authors:
- Sumeet Ramesh Motwani
- Mikhail Baranchuk
- Martin Strohmeier
- Vijay Bolina
- Philip H. S. Torr
- Lewis Hammond
- Christian Schroeder de Witt
year: 2024
venue: Advances in Neural Information Processing Systems (NeurIPS 2024), per Semantic Scholar venue field
url: https://arxiv.org/html/2402.07510
doi: null
arxiv: '2402.07510'
cite: 'Motwani, S. R., Baranchuk, M., Strohmeier, M., Bolina, V., Torr, P. H. S., Hammond, L., & Schroeder de Witt, C. (2024). Secret Collusion among AI Agents: Multi-Agent Deception via Steganography. Advances in Neural Information Processing Systems (NeurIPS 2024). arXiv:2402.07510.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 138 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Formalises secret collusion among generative AI agents: agents coordinating against oversight by hiding information in innocuous-looking messages (steganography). Draws on AI and security literature to define decentralised systems of generative agents, studies incentives for steganography, and builds CASE (Collusion and Steganographic Evaluation), a framework of individual and group capability evaluations: Schelling-point coordination, cipher use (Base64, Caesar), simulating logits, acting as random oracles, and minimum-entropy coupling. Current models show limited steganographic capability, but GPT-4 shows a capability jump over smaller baselines. A qualitative insider-trading case study shows shared common knowledge between an agent and a user breaking GPT-4 safeguards. The paper proves that paraphrasing cannot remove all covert capacity: residual capacity is bounded by semantic entropy (Theorem 4).

## Contribution

The founding formal treatment and evaluation suite for covert collusion between LLM agents, separating capability evaluation from deployed detection.

## Key results

- Measured: individual steganographic capabilities rise with model size, sometimes in discrete jumps; agreement on simple and complex Schelling points correlates with cipher and coupling capabilities.
- Theory: ideal paraphrasing leaves covert capacity up to the semantic entropy of the message (Theorem 4), and paraphrasing across semantics can hurt task performance.
- Observed: standalone GPT-4 could not perform symmetric-key encryption.
- Recommendation: continuous monitoring of frontier steganographic capability; mitigations include filtering pretraining data, restricting tools, and in-context instructions.

## Methods and models

Formal model of local versus global knowledge and common knowledge between sender and receiver; CASE software framework; evaluations across several LLMs with GPT-4 as the strongest.

## Limitations and open questions

Skimmed (introduction, contributions, CASE, results summary, paraphrasing theorem). Evaluations are capability probes; deployed multi-agent tasks with incentives to collude are left to later work such as [[nakamura-2026-colosseum]] and [[tailor-2025-audit]].

## Relevance to us

Sybil resistance in swarms is usually framed as many identities with one controller; secret collusion is the converse, independent identities acting as one. Agents sharing a base model share common knowledge and Schelling points, so nominally independent agents can coordinate without any visible channel, which weakens honest-majority assumptions in [[jo-2025-byzantine]] and links to correlated-error findings in [[bara-2026-epistemic]]. Real-world corpus: [[gh-catgirl3d-agent-collusion-wiki-archive]]. Taxonomy: [[hammond-2025-multi]].
