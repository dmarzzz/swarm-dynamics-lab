---
id: collu-2025-misleading
type: paper
title: Misleading Large Language Models used (or misused) in Scientific Peer-Reviewing via Hidden Prompt-Injection Attacks
authors:
- Matteo Gioele Collu
- Umberto Salviati
- Roberto Confalonieri
- Mauro Conti
- Giovanni Apruzzese
year: 2025
venue: ACM Transactions on AI Security and Privacy (accepted); arXiv preprint
url: https://arxiv.org/abs/2508.20863
doi: null
arxiv: '2508.20863'
cite: Collu, M. G., Salviati, U., Confalonieri, R., Conti, M., & Apruzzese, G. (2025). Misleading Large Language Models used (or misused) in Scientific Peer-Reviewing via Hidden Prompt-Injection Attacks. Accepted to ACM Transactions on AI Security and Privacy. arXiv preprint arXiv:2508.20863.
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Formalises three threat models for hidden prompt injection in paper PDFs aimed at LLM-generated reviews, not all of them malicious. Designs prompts invisible to human readers, derives four representative reviewing prompts from a user study with domain scholars, and evaluates across reviewing prompts, commercial LLM systems and papers. Adversarial prompts reliably mislead the LLM, sometimes against an 'honest-but-lazy' reviewer, and the authors test ways to make such prompts harder to find with automated content checks.

## Contribution

Evidence that invisible document-borne instructions reliably reach and steer LLM agents, the same property that canary detection relies on, plus methods to evade automated scanning for them.

## Key results

- Hidden prompts reliably mislead LLM reviewers across prompts, systems and papers (abstract; no numbers there).
- Methods proposed and tested to reduce detectability of the prompts under automated checks (abstract).

## Methods and models

Threat modelling, user study for reviewing prompts, cross-system evaluation. Abstract-level read. The arXiv page lists DOI 10.1145/3803804, which did not resolve in Crossref on 2026-10-03, so it is left out of the doi field.

## Limitations and open questions

Abstract only.

## Relevance to us

Implies canary instructions can also be hidden from an operator scanning for them, which matters if swarm operators sanitise inputs. Related: [[rao-2025-detecting]], [[lin-2025-hidden]], [[gharami-2025-chatgpt]].
