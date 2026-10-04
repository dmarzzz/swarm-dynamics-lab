---
id: bate-2026-indecision
type: paper
title: "Indecision and accuracy under social information across groups sizes"
authors: ["Andrew M. Bate", "Charlie Pilgrim", "Richard P. Mann"]
year: 2026
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2606.28025"
doi: null
arxiv: "2606.28025"
cite: "Bate, A. M., Pilgrim, C., & Mann, R. P. (2026). Indecision and accuracy under social information across groups sizes. arXiv preprint arXiv:2606.28025. https://arxiv.org/abs/2606.28025"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Model of agents that each accumulate noisy private evidence (drift-diffusion with thresholds) and also update rationally on the observed decisions and indecision of others. A first decision triggers discrete waves of social updating in which others may follow. Across group sizes, social information makes decisions faster and more accurate than solitary choice, but accuracy per agent peaks at a finite group size, while majority accuracy keeps rising. Waves often fail to resolve indecision, and the agents left undecided are biased and less accurate.

## Contribution

Extends the rational-agent framework of [[mann-2018-collective]] and [[perez-escudero-2011-collective]] to explicit timing (sequential decisions in waves) and reports a finite optimal group size for individual accuracy, a result the authors say is present but overlooked in earlier work.

## Key results

- Agent-level accuracy is maximised at a finite group size; majority accuracy increases monotonically with N (simulation and approximate analytics).
- Benchmarks shown as dashed lines: about 73.1 per cent accuracy for a solitary decision and 86.6 per cent for the infinite-group limit, at the parameters used.
- Waves frequently leave a subgroup unconvinced, especially in smaller groups and when the first decider is wrong; the proportion of runs resolved by the second wave rises to nearly 90 per cent for N = 100 against about 60 per cent for smaller groups.
- In large groups, inaccuracy is dominated by agents rushed into following a wrong first decider before gathering enough private evidence.

## Methods and models

Each agent's log-likelihood ratio y_i follows a drift-diffusion process with drift +alpha (true state H+) and noise D, deciding at +/- theta; decisions are irreversible. Social information from others' decisions and continued indecision is added as Bayesian log-likelihood terms, approximated with truncated series (sixth order). Group sizes N = 1 to 100. 20-page main text plus 18-page SI. I skimmed the model and results sections.

## Limitations and open questions

Homogeneous agents with shared parameters and full knowledge of others' inference rules; instantaneous waves; binary choice. Not yet peer reviewed. The optimal-group-size result depends on these rationality assumptions.

## Relevance to us

A direct prediction to test in LLM-agent and robot swarms: individual accuracy should peak at intermediate N even as majority-vote accuracy keeps improving. Links to [[mann-2018-collective]], [[kao-2014-decision]], [[tump-2024-cognitive]] and [[kao-2024-timing]].
