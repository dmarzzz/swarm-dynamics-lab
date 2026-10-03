---
id: roger-2023-preventing
type: blog
title: Preventing Language Models from hiding their reasoning
authors:
- Fabien Roger
- ryan_greenblatt
year: 2023
url: https://www.alignmentforum.org/posts/9Fdd9N7Escg3tcymb/preventing-language-models-from-hiding-their-reasoning
site: AI Alignment Forum
topics:
- swarm-detection
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

The post studies covert text channels that could conceal reasoning or coordination between models. In experiments with human-designed steganographic encoders, contextual paraphrasing removes most hidden capacity while retaining useful task information imperfectly. It explicitly separates these measured defenses from speculative takeover and collusion scenarios, including cases where a single surviving bit would already be dangerous.

## Key claims

- GPT-3.5 models were fine-tuned on 2,000 sycophancy examples and evaluated on 1,000 new examples; hidden reasoning improved this toy task.
- Capacity and answer quality were evaluated on AlpacaEval and AQUA-RAT; contextual paraphrasing reduced hidden capacity more than generic paraphrasing.
- The tested encoders share schemes or secrets in advance; the post cautions that stronger future models and code channels could defeat these conclusions.

## Evidence quality

Research explanation linked to arXiv 2310.18512, with experimental design and limitations. Experiments test built steganography schemes rather than spontaneous covert collusion in a deployed swarm. Figures were read through their surrounding descriptions, not numerically re-extracted.

## Relevance to us

A useful communication-channel baseline for swarm monitors and merge-time sanitization. Reducing average bitrate is not equivalent to preventing coordinated triggering. Compare [[roger-2023-coup]] for activation-based monitoring.
