---
id: russell-2025-people
type: paper
title: People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text
authors:
- Jenna Russell
- Marzena Karpinska
- Mohit Iyyer
year: 2025
venue: ACL 2025 (pages 5342-5373 per Semantic Scholar)
url: https://arxiv.org/abs/2501.15654
doi: null
arxiv: '2501.15654'
cite: Russell, J., Karpinska, M., & Iyyer, M. (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), 5342-5373. arXiv:2501.15654.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 62 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Hires annotators to label 300 non-fiction English articles as human or AI-written (GPT-4o, Claude, o1) and explain their decisions. Annotators who frequently use LLMs for writing are accurate without training: the majority vote of five such experts misclassifies only 1 of 300 articles, beating most commercial and open-source detectors even under paraphrasing and humanisation. Experts rely on AI vocabulary but also on formality, originality and clarity.

## Contribution

A positive result for human expert detection of long-form AI text, with a released explained dataset.

## Key results

- Measured (abstract): five-expert majority vote errs on 1 of 300 articles, robust to paraphrasing and humanisation.

## Methods and models

Annotation study with paragraph-length explanations; comparison with automatic detectors. Abstract read only.

## Limitations and open questions

Long-form articles; short social posts are much harder. Expert labour does not scale to platforms. Abstract depth.

## Relevance to us

Expert human review is a viable verification layer for small samples drawn from a suspected swarm cluster, after cheap population-level screening.
