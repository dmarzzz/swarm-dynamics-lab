---
id: kuznetsov-2026-width
type: paper
title: "Width, Memory, and Delay: A Resource Accounting for the Limits of Flat Multi-Agent Systems"
authors:
- "Oleksandr Kuznetsov"
- "Emanuele Frontoni"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.00028
doi: null
arxiv: "2608.00028"
cite: "Kuznetsov, O., & Frontoni, E. (2026). Width, Memory, and Delay: A Resource Accounting for the Limits of Flat Multi-Agent Systems. arXiv preprint arXiv:2608.00028."
topics:
- llm-agent-swarms
- sync-consensus
- swarm-robotics
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

Asks whether adding agents can by itself overcome performance limits in multi-agent systems (robot swarms or LLM collectives), or whether deeper organisation is needed. Responding to a preprint claiming that flat homogeneous systems face a population-independent "causal floor" on error removable only by hierarchy, the authors build a disturbance-rejection testbed with an exactly computable optimum and replace that claim with a three-resource model: population width N, per-agent internal-model memory d, and prediction across the observation delay tau. A flat homogeneous swarm whose agents carry a matched internal model of the disturbance matches or beats a designed two-loop hierarchy at equal per-agent memory, so temporal depth can be dynamical (recurrent memory) rather than architectural. The resources are not interchangeable; the paper charts exchange rates and hard non-exchange boundaries on a width x memory map, and shows a residual floor set by delay and the environment's unpredictability over that horizon.

## Contribution

A control-theoretic accounting of what "more agents" can and cannot buy, framed generally enough to inform LLM agent scaling debates ([[kim-2025-towards]], [[bertalanic-2026-ringelmann]], [[qian-2025-scaling]]).

## Key results

- Claimed (abstract): flat swarms with matched internal models match or beat a two-loop hierarchy at equal per-agent memory.
- Claimed: width, memory and delay-prediction are not mutually interchangeable, including under an equal total-state budget.
- Claimed: a delay-set residual floor, verified against the optimal controller.

## Methods and models

Linear disturbance-rejection testbed with a computable optimum; comparisons of flat vs hierarchical organisations; online learning of the disturbance spectrum vs oracle knowledge; robustness checks with a mild bounded nonlinearity and a spatially extended plant.

## Limitations and open questions

- Abstract-level read. The testbed is a linear control problem, not an LLM system; transfer to LLM collectives is by analogy.

## Relevance to us

A useful theoretical lens for the hackathon's scaling questions: report memory and delay alongside N. Flagged as a gap by the original scan. Related: [[fortuna-2026-multi-agent]], [[tran-2026-single]].
