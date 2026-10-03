---
id: sutton-2022-alberta
type: paper
title: The Alberta Plan for AI Research
authors: [Richard S. Sutton, Michael Bowling, Patrick M. Pilarski]
year: 2022
venue: arXiv
url: https://arxiv.org/abs/2208.11173
doi: null
arxiv: "2208.11173"
cite: Sutton, R. S., Bowling, M., & Pilarski, P. M. (2022). The Alberta Plan for AI Research. arXiv preprint arXiv:2208.11173.
topics: [fork-merge-security, meta]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null
code: []
---

## Summary

A research roadmap for the Alberta groups. It defines the AI problem as "the online maximization of reward via continual sensing and acting, with limited computation, and potentially in the presence of other agents", and lays out twelve steps from continual supervised learning with given features (Step 1) through GVF prediction, actor-critic control, average-reward GVFs, STOMP and the Oak architecture (Steps 10 and 11) to Prototype-IA, intelligence amplification of one agent by another (Step 12). Its fourth distinguishing feature is a focus on environments that include other intelligent agents, with which the primary agent may "communicate, cooperate, and compete".

## Contribution

The canonical statement of Sutton's research agenda; it positions continual learning with a single agent's own experience stream as the core problem.

## Key results

- No empirical results; it is a plan.
- The only multi-agent content is cooperation and competition with other agents and intelligence amplification (Step 12: one agent increasing "the speed and overall decision-making capacity of a second agent"). There is no discussion of an agent copying itself or merging copies (checked by searching the PDF for copy, merge, multi-agent and cooperat).

## Methods and models

Base agent with four components: perception (state construction), reactive policies, value functions and a transition model, all learned continually, plus planning.

## Limitations and open questions

Adversarial settings and security are not discussed.

## Relevance to us

Negative evidence for provenance: the 2022 plan does not contain the fork-merge idea, so the earliest Sutton statement found in this lane is the 2025 interview [[sutton-2025-father]]. Step 12 (one agent amplifying another) is the closest neighbour: it is an inter-agent knowledge channel, and in a fork-merge system every child-to-parent merge is an amplification step that could carry corruption (Q3). See also [[silver-2025-welcome]].
