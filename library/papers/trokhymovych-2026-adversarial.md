---
id: trokhymovych-2026-adversarial
type: paper
title: Adversarial Creation and Detection of AI-Generated Social Bot Content
authors:
- Mykola Trokhymovych
- Ricardo Baeza-Yates
- Alessandro Flammini
- Diego Saez-Trumper
- Filippo Menczer
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.07219
doi: null
arxiv: '2606.07219'
cite: Trokhymovych, M., Baeza-Yates, R., Flammini, A., Saez-Trumper, D., & Menczer, F. (2026). Adversarial Creation and Detection of AI-Generated Social Bot Content. arXiv preprint arXiv:2606.07219.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Argues that AI-text detectors fail in the wild mainly for lack of ground truth, and builds it adversarially: an LLM impersonates real social media users, producing paired human and AI messages across languages and platforms. Detectors trained on this paired data detect AI-generated text accurately and significantly outperform existing content-based bot detection on real out-of-distribution data.

## Contribution

A data-generation recipe (impersonation pairs) for training content detectors that transfer to real bot text.

## Key results

- Multilingual, cross-platform dataset of paired human and AI-generated messages (abstract).
- Training on adversarial pairs significantly outperforms existing content-based bot detectors on real-world out-of-distribution data (abstract; numbers not recorded).

## Methods and models

LLM impersonation of real users to create matched pairs; supervised detectors. Abstract-level read.

## Limitations and open questions

Content-only; an operator using a different model or fine-tune may shift the distribution. Preprint.

## Relevance to us

Counterpoint to the 'content is dead' view in [[katyal-2026-account]]: content detection may still work when trained on the right pairs. Same group as [[yang-2023-anatomy]], which found off-the-shelf detectors failed on the fox8 botnet.
