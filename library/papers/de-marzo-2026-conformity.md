---
id: de-marzo-2026-conformity
type: paper
title: 'Conformity Generates Collective Misalignment in AI Agents Societies'
authors: [Giordano De Marzo, Alessandro Bellina, Claudio Castellano, Viola Priesemann, David Garcia]
year: 2026
venue: arXiv preprint (physics.soc-ph)
url: https://arxiv.org/abs/2605.10721
doi: null
arxiv: '2605.10721'
cite: 'De Marzo, G., Bellina, A., Castellano, C., Priesemann, V., & Garcia, D. (2026). Conformity Generates Collective Misalignment in AI Agents Societies. arXiv preprint arXiv:2605.10721.'
topics: [llm-agent-swarms, collective-decision, criticality-measurement]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

The De Marzo group's follow-up to [[de-marzo-2024-ai]], now with Castellano, Priesemann and Garcia. Opinion dynamics simulated across nine LLMs and one hundred opinion pairs; each agent's behaviour is decomposed into two competing forces, a tendency to follow the majority and an intrinsic bias toward specific positions. A statistical-physics theory built on those two measured quantities predicts when a population of individually aligned agents becomes trapped in a long-lived misaligned configuration, and identifies tipping points at which a small number of adversarial agents shifts population-level alignment irreversibly, persisting after the adversaries stop. The headline: individual-level alignment gives no guarantee of collective safety. Abstract only.

## Contribution

Unifies the majority force (inverse temperature) of [[de-marzo-2024-ai]] with the intrinsic bias field of [[okawa-2026-emergence]] and [[flint-2026-group]] into one two-parameter per-model measurement, across nine models and a hundred topics rather than one game. Also the clearest statement of the committed-minority tipping result as a safety claim, alongside [[flint-2026-indirect]] and [[magistrali-2026-aligned]].

## Key results

- Reported: two measured forces (majority-following, intrinsic bias) govern each agent (abstract; magnitudes per model not read).
- Reported: theory predicts long-lived misaligned traps and tipping points under small adversarial fractions.
- Reported: shifts persist after manipulation ceases (irreversible), which is the opposite of the recovery reported by [[magistrali-2026-aligned]].

## Methods and models

Nine LLMs, one hundred opinion pairs, opinion-dynamics simulation, mean-field style theory. N, update rule and whether agents see all opinions or a sample were not read.

## Limitations and open questions

- Abstract-level read.
- The irreversible versus reversible capture disagreement with [[magistrali-2026-aligned]] is the open question; likely depends on whether the task has an intrinsic bias term and on memory.

## Relevance to us

The current best theory to test or replicate in a hackathon: measure the two forces for one open model on one opinion pair, predict the tipping fraction, then run the population and check. Fits the AI Village and incident framing (populations drift together even when individuals look fine).
