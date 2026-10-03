---
id: cai-2025-are
type: paper
title: "Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs"
authors: ["Will Cai", "Tianneng Shi", "Xuandong Zhao", "Dawn Song"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2504.04715
doi: null
arxiv: "2504.04715"
cite: "Cai, W., Shi, T., Zhao, X., & Song, D. (2025). Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs. arXiv:2504.04715."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Formalises model substitution by commercial LLM API providers (for example serving a quantised or smaller model at the advertised price) and evaluates detectors under adversarial conditions. Text-output statistical tests are query-intensive and miss subtle substitutions; log-probability methods are defeated by inference nondeterminism in production. The authors argue software-only verification is unreliable and propose Trusted Execution Environments for provable model integrity at modest overhead.

## Contribution

A negative result for black-box attribution: subtle model swaps are hard to detect from outputs, so attestation is proposed instead.

## Key results

- Statistical tests on text outputs fail against subtle substitutions and need many queries (abstract).
- Log-probability methods are defeated by production inference nondeterminism (abstract).
- TEEs give cryptographic integrity guarantees with modest performance overhead (abstract).

## Methods and models

Systematic evaluation of output-based and logprob-based substitution detectors; TEE prototype.

## Limitations and open questions

Concerns provider honesty, not detection of unknown agents; abstract-only reading.

## Relevance to us

Marks a limit of fingerprint-based attribution: near-identical models (quantised variants) blur together. For swarm detection this caps how finely model-level linking can split operators who use the same base model. Contrast [[zhang-2026-which]], [[bruckner-2026-one]].
