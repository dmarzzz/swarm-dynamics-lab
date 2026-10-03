---
id: araujo-2011-maximum
type: paper
title: "A maximum independent set approach for collusion detection in voting pools"
authors: [Filipe Araujo, Jorge Farinha, Patricio Domingues, Gheorghe Cosmin Silaghi, Derrick Kondo]
year: 2011
venue: Journal of Parallel and Distributed Computing, vol. 71, no. 10, pp. 1356-1366
url: https://mescal.imag.fr/membres/derrick.kondo/pubs/araujo_jpdc11.pdf
doi: 10.1016/j.jpdc.2011.06.004
arxiv: null
cite: "Araujo, F., Farinha, J., Domingues, P., Silaghi, G. C., & Kondo, D. (2011). A maximum independent set approach for collusion detection in voting pools. Journal of Parallel and Distributed Computing, 71(10), 1356-1366. https://doi.org/10.1016/j.jpdc.2011.06.004"
topics: [swarm-detection, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "31 (Crossref, 2026-10-03)"
code: ["https://github.com/filipius/colluding"]
---

## Summary

Collusion detection for repeated redundant computation of the BOINC/SETI@home kind: a supervisor sends each workunit to a small voting pool of volunteer workers and accepts the majority result; Byzantine workers who collude can out-vote honest ones when they land in the same pool. The setting has a fixed worker population that participates in many pools over time, so the supervisor accumulates a history. The authors define a "votes against" graph G = (V, E) whose vertices are worker identifiers and whose edges connect workers that disagreed in some pool, and propose detectors: breadth-first search on the graph, AV1 (count of votes against each node), heuristics for the maximum independent set (MIS) of the graph (colluders agree with each other, so honest workers form a large independent set in the conflict graph and colluders sit outside it), plus a few others. Four colluder types are modelled: M1 always wrong when in majority, M2 and M3 betray partners or abstain from cheating to hide, and M4 sabotages only after finding peer colluders with 50% persistence. Simulations with 20% colluders report false positive and false negative pool rates (Figs 4-7); AV1 and MIS heuristics work very well when workers participate at similar rates and cannot present multiple identifiers. The paper then explicitly admits that these methods are "completely powerless" under whitewashing (leave and rejoin with a fresh identifier to escape blacklists) and proposes AV2, which normalises votes against by participation count and runs in O(m + n log n) over the conflict graph, as a partial answer. Code released. Read: abstract, introduction and threat model, graph construction, algorithm descriptions, simulation set-up and the summary of Figs 4-7, conclusions; probabilistic analysis (Theorem 5.1) skimmed.

## Contribution

Reframes collusion detection in redundant computing as a graph problem on a disagreement graph, with MIS heuristics that detect persistent colluding groups, and an honest account of how cheap identity change (whitewashing / Sybil) defeats the approach.

## Key results

- AV1 and MIS heuristics give low false positives and false negatives at 20% colluders when identities are stable (figures given per colluder type in Figs 4-7).
- With whitewashing, BFS/AV1/MIS fail; AV2 (participation-normalised) partially recovers at O(m + n log n).
- Detection pressure deters collusion because colluders must either betray peers or be caught together.

## Methods and models

BOINC-like simulator, voting pools of small size, four colluder behaviour models, disagreement graph, MIS heuristics and simple counting detectors, false positive / false negative pool metrics.

## Limitations and open questions

Simulation only; assumes a central supervisor with full voting history; colluder models are hand-designed; whitewashing handled heuristically, not solved; no cost model for identity creation.

## Relevance to us

Close structural analogue to detecting a coordinated agent swarm inside a population of nominally independent agents: build the agreement/disagreement graph over repeated tasks, look for the clique that always agrees with itself and against the independent set. The whitewashing failure is exactly the Sybil hole an LLM-agent operator would exploit by rotating identities, which ties swarm-detection to sybil-resistance. Related: [[marti-2004-limited]] (whitewashing cost in reputation), [[davis-2008-sybil]] and [[konrath-2007-attacking]] (coordinated fakes in swarms), [[bijani-2014-review]] (malicious-group detection lineage). Root: [[douceur-2002-sybil]].
