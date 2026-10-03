---
id: trokhymovych-2026-adversarial
type: paper
title: "Adversarial Creation and Detection of AI-Generated Social Bot Content"
authors: ["Mykola Trokhymovych", "Ricardo Baeza-Yates", "Alessandro Flammini", "Diego Saez-Trumper", "Filippo Menczer"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.07219
doi: null
arxiv: "2606.07219"
cite: "Trokhymovych, M., Baeza-Yates, R., Flammini, A., Saez-Trumper, D., & Menczer, F. (2026). Adversarial Creation and Detection of AI-Generated Social Bot Content. arXiv:2606.07219."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Detectors for AI-generated text often fail in the wild for lack of ground truth. The authors model malicious impersonation of real social media users: they pair real human messages with AI-generated messages written to imitate those users, building a multilingual, cross-platform dataset. Training on this adversarial data yields accurate detection of AI-generated text and outperforms existing content-based bot detectors on real-world, out-of-distribution data.

## Contribution

A training-data recipe for content-level detection of LLM bot text that transfers to real data better than existing classifiers.

## Key results

- Significantly outperforms existing content-based bot detectors on real out-of-distribution data (abstract; numbers not there).

## Methods and models

Adversarial pairing of human posts with LLM imitations of the same users; classifier training; multilingual, cross-platform evaluation.

## Limitations and open questions

Abstract only. Content-level, per-message or per-account; does not use coordination.

## Relevance to us

The content channel to combine with coordination signals. [[yang-2023-anatomy]] found that content classifiers failed on a real ChatGPT botnet while coordination patterns caught it; this paper claims progress on the content side.
