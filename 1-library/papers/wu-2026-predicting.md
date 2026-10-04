---
id: wu-2026-predicting
type: paper
title: Predicting the scale limits of social mechanisms in agent societies
authors:
- Zengqing Wu
- Chuan Xiao
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.22884
doi: null
arxiv: '2608.22884'
cite: Wu, Z., & Xiao, C. (2026). Predicting the scale limits of social mechanisms in agent societies. arXiv preprint arXiv:2608.22884.
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Asks whether a social mechanism that works in a small LLM-agent group (reciprocity, consensus, punishment, gossip) still operates when thousands of agents interact, and proposes an audit that predicts this before running large simulations. The audit asks how often the mechanism can act, whether agents use the information it supplies, and whether the measurement itself creates apparent scale effects. Controlled experiments show a single structural term can decide whether reciprocity, consensus or punishment survives scaling; for gossip, the population at which it fails is set by the reach and lifetime of messages. LLM agents also respond to how social information is expressed (counts vs percentages change scale behaviour). Predictions made before execution held on third-party code and a second model family, and one failed prediction marked the boundary of the finding.

## Contribution

A pre-registration-style method for scale extrapolation in LLM societies; complements [[flint-2026-group]] and [[de-marzo-2024-ai]] (size thresholds) and [[zhou-2025-pimmur]] (validity of LLM social simulations).

## Key results

- Claimed: one structural term predicts survival of reciprocity, consensus and punishment under scaling.
- Claimed: gossip failure population set by message reach and lifetime.
- Claimed: number format (counts vs percentages) changes scale behaviour.
- Claimed: prospective predictions held on third-party code and a second model family.

## Methods and models

Controlled LLM-society experiments at multiple population sizes; audit criteria; external validation. Models not checked.

## Limitations and open questions

Abstract-level read; the "structural term" is not specified in the abstract.

## Relevance to us

Practical guidance for designing scalable LLM swarm experiments on a hackathon budget: test the audit before paying for large runs. Related: [[yang-2024-oasis]], [[ricco-2026-consensus]].
