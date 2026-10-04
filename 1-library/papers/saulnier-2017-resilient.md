---
id: saulnier-2017-resilient
type: paper
title: "Resilient Flocking for Mobile Robot Teams"
authors: ["Kelsey Saulnier", "David Saldaña", "Amanda Prorok", "George J. Pappas", "Vijay Kumar"]
year: 2017
venue: "IEEE Robotics and Automation Letters"
url: https://api.openalex.org/works/doi:10.1109/lra.2017.2655142
doi: "10.1109/lra.2017.2655142"
arxiv: null
cite: "Saulnier, K., Saldaña, D., Prorok, A., Pappas, G. J., & Kumar, V. (2017). Resilient Flocking for Mobile Robot Teams. IEEE Robotics and Automation Letters, 2(2), 1039-1046."
topics: [sybil-resistance, collective-motion, swarm-robotics, sync-consensus]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "200 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A control policy that lets a mobile robot team reach resilient consensus on direction of motion despite non-cooperative (defective or malicious) robots. Robots actively manage connectivity using a metric of communication-graph robustness so the network stays above the critical resilience threshold needed by W-MSR style consensus, guaranteeing convergence within the range of cooperative robots' initial headings. Demonstrated in simulation with holonomic robots.

## Contribution

Couples motion control with graph robustness maintenance, making the topology assumption of resilient consensus an actively controlled quantity rather than a hope.

## Key results

- Consensus value stays within the convex hull of cooperative robots' initial values as long as connectivity management keeps the network above the robustness threshold (abstract).
- Simulation results for resilient flocking with holonomic robots.

## Methods and models

Robustness-aware connectivity control plus W-MSR heading consensus. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Robustness is measured on the perceived graph; [[mallmann-trenn-2021-crowd]] shows spoofed nodes inflate perceived robustness, so this controller can be fooled by a Sybil attacker without an identity check.

## Relevance to us

A flocking baseline for adversarial collective motion experiments, and a concrete example of the 'false sense of resilience' failure that Sybils cause. Related: [[saldana-2017-resilient]], [[leblanc-2013-resilient]].
