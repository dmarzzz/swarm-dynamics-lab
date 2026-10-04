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

## Notes from dmarz/sd-coordination

This lane catalogued the same source independently (added_by dmarz/sd-coordination, accessed 2026-10-03). Its distinct content:

- Frontmatter `cite` in this lane's version: Trokhymovych, M., Baeza-Yates, R., Flammini, A., Saez-Trumper, D., & Menczer, F. (2026). Adversarial Creation and Detection of AI-Generated Social Bot Content. arXiv:2606.07219.
- Frontmatter `relevance` in this lane's version: 3
- Frontmatter `citations` in this lane's version: 0 (Semantic Scholar, 2026-10-03)

### Summary

Detectors for AI-generated text often fail in the wild for lack of ground truth. The authors model malicious impersonation of real social media users: they pair real human messages with AI-generated messages written to imitate those users, building a multilingual, cross-platform dataset. Training on this adversarial data yields accurate detection of AI-generated text and outperforms existing content-based bot detectors on real-world, out-of-distribution data.

### Contribution

A training-data recipe for content-level detection of LLM bot text that transfers to real data better than existing classifiers.

### Key results

- Significantly outperforms existing content-based bot detectors on real out-of-distribution data (abstract; numbers not there).

### Methods and models

Adversarial pairing of human posts with LLM imitations of the same users; classifier training; multilingual, cross-platform evaluation.

### Limitations and open questions

Abstract only. Content-level, per-message or per-account; does not use coordination.

### Relevance to us

The content channel to combine with coordination signals. [[yang-2023-anatomy]] found that content classifiers failed on a real ChatGPT botnet while coordination patterns caught it; this paper claims progress on the content side.
