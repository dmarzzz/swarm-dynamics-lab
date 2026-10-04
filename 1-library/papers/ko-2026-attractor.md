---
id: ko-2026-attractor
type: paper
title: "Attractor States Emerge in Multi-Turn LLM Conversations"
authors: [Ting-Wen Ko, Jonas Geiping]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.30571
doi: null
arxiv: '2606.30571'
cite: "Ko, T.-W., & Geiping, J. (2026). Attractor States Emerge in Multi-Turn LLM Conversations. arXiv:2606.30571."
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors run open-ended dyadic debates between LLMs on 20 controversial topics, in self-play (a model with itself) and mixed-play (two different models), across 7 models. They track trajectories in representation space, discourse traits (for example meta-commentary, flattery) and stances, and ask whether conversations settle into topic-independent stable regions.

## Contribution

Shows that model-model conversations have model-specific attractor basins and that influence between models is asymmetric: some models pull partners toward their own traits while others are easily moved.

## Key results

- Measured: self-play conversations settle into reproducible, model-specific endpoint regions.
- Measured: in mixed-play, endpoints move along the axis between the two models' self-play basins, i.e. each model pulls the other toward its own basin.
- Measured: influence is asymmetric. Claude Haiku moves little and strongly attracts partners toward its traits such as meta-commentary; GPT-4.1 nano and GPT-4o mini are especially malleable.
- Measured: attractors are not simple stance convergence; self-play does not consistently amplify stance and mixed-play does not always produce compromise.

## Methods and models

Seven LLMs, 20 topics, self-play and mixed-play dyads; trajectory embedding analysis plus trait and stance coding. Skimmed: abstract and conclusion.

## Limitations and open questions

Benign debate, no adversarial optimisation; dyads only; open-ended topics rather than tasks.

## Relevance to us

Q3, mechanism. This extends [[li-2024-measuring]] from "an agent drifts toward its interlocutor's instructions" to "some agents are attractors and others are malleable", measured across current models. For fork-merge that gives a concrete threat model: an adversary in a foreign domain fields a strongly attracting agent, and a sub-agent built on a malleable model drifts toward it over a long exchange without any injection. Defensively it suggests choosing exploring parts from resistant models and measuring the part's representation-space position against the parent's basin before merge. It also bears on Q2: asymmetric influence means honest parts talking to each other can be pulled by one strong deviant, so votes among parts that have conversed are not independent. Related: [[zhang-2024-psysafe]], [[chen-2025-persona]], [[ju-2024-flooding]].
