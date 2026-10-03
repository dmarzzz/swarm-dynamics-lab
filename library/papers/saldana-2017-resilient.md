---
id: saldana-2017-resilient
type: paper
title: "Resilient consensus for time-varying networks of dynamic agents"
authors: ["David Saldaña", "Amanda Prorok", "Shreyas Sundaram", "Mário F. M. Campos", "Vijay Kumar"]
year: 2017
venue: "2017 American Control Conference (ACC)"
url: https://api.openalex.org/works/doi:10.23919/acc.2017.7962962
doi: "10.23919/acc.2017.7962962"
arxiv: null
cite: "Saldaña, D., Prorok, A., Sundaram, S., Campos, M. F. M., & Kumar, V. (2017). Resilient consensus for time-varying networks of dynamic agents. In 2017 American Control Conference (ACC), 252-258."
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "134 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Extends W-MSR style resilient consensus [[leblanc-2013-resilient]] to mobile robots whose communication graph changes over time. When the robustness condition cannot hold at every instant, they show resilience is still guaranteed if the union of graphs over a bounded time window is sufficiently robust, and give a control policy for perimeter surveillance with a robot team, supported by simulations.

## Contribution

Moves resilient consensus from static networks to time-varying mobile teams via a windowed-union robustness condition.

## Key results

- Consensus with resilience to non-cooperating agents holds when the union of communication graphs over a bounded period satisfies (r, s)-robustness (abstract).
- Applied to perimeter surveillance in simulation.

## Methods and models

Resilient consensus with outlier trimming, time-windowed graph unions. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Like all W-MSR descendants it assumes a known bound F on adversaries, which a Sybil attacker breaks by multiplying identities (shown in [[mallmann-trenn-2021-crowd]] and [[strobel-2020-blockchain]]).

## Relevance to us

Relevant because LLM agent swarms also have time-varying interaction graphs; the windowed-union condition is a usable design rule, but it gives no Sybil resistance on its own. Related: [[saulnier-2017-resilient]], [[wardega-2023-byzantine]].
