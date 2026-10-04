---
id: niizato-2020-finding
type: paper
title: 'Finding continuity and discontinuity in fish schools via integrated information theory'
authors: ['Takayuki Niizato', 'Kotaro Sakamoto', 'Yoh-ichi Mototake', 'Hisashi Murakami', 'Takenori Tomaru', 'Tomotaro Hoshika', 'Toshiki Fukushima']
year: 2020
venue: 'PLOS ONE'
url: https://doi.org/10.1371/journal.pone.0229573
doi: 10.1371/journal.pone.0229573
arxiv: null
cite: 'Niizato, T., Sakamoto, K., Mototake, Y., Murakami, H., Tomaru, T., Hoshika, T., & Fukushima, T. (2020). Finding continuity and discontinuity in fish schools via integrated information theory. PLOS ONE, 15(2), e0229573.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '32 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Applies integrated information theory (IIT 3.0, Phi) to tracked schools of ayu (Plecoglossus
altivelis). The distribution of average Phi shows a discontinuity for schools of four or more fish, which
mutual information and summed transfer entropy do not detect, and correlates with a form of leadership defined
as group autonomy. Boids simulations at different coupling strengths behave quite differently from real fish.

## Contribution

One of the first applications of IIT's Phi to animal collectives, suggesting it detects
group-size transitions that pairwise information measures miss.

## Key results

- Discontinuity in <Phi(N)> distributions emerges at N >= 4 fish (measured).
- Not detected by mutual information or sum of transfer entropy.
- Boids do not reproduce the real-fish Phi results.

## Methods and models

IIT 3.0 on binarised motion states of small fish groups; comparison with Boids simulations.

## Limitations and open questions

IIT 3.0 is computationally restricted to very small groups and requires binarisation; IIT's
foundations are contested. Abstract-level read.

## Relevance to us

Option for small-swarm integration metrics; for larger swarms prefer PID-based measures
([[rosas-2020-reconciling]]). Same group: [[niizato-2023-functional]].
