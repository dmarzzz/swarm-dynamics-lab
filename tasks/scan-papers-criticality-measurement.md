---
id: scan-papers-criticality-measurement
type: task
title: 'Catalogue the papers: criticality, information and measurement'
kind: scan
status: claimed
priority: p1
owner: dmarz/criticality-measurement
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- criticality-measurement
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `criticality-measurement`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Mora and Bialek 2011, Are biological systems poised at criticality? (J. Stat. Phys.)
- Bialek et al. 2012, Statistical mechanics for natural flocks of birds (PNAS)
- Muñoz 2018, Colloquium: Criticality and dynamical scaling in living systems (Rev. Mod. Phys.)
- Work on transfer entropy and information flow in collectives (search: 'information transfer' swarm, 'transfer entropy' flock)
- Work on causal emergence and integrated information applied to collectives (search: 'causal emergence' collective)

## Search plan

- Start from the seeds. For each seminal paper, pull its references (backward) and the papers citing it (forward) from Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>/citations?fields=title,year,externalIds,citationCount&limit=100
- Query arXiv (export.arxiv.org/api/query), Semantic Scholar search and OpenAlex (api.openalex.org/works?search=...) with at least 5 different phrasings of the topic, including the terms used by neighbouring fields.
- Look for review articles first: they give the map and their reference lists are dense seeds.
- Prioritise by relevance to the hackathon, then by citation count, then recency. Catalogue the review papers, the seminal papers, and the strongest recent work.

## Done when

- At least 25 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 5 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Scan by dmarz/criticality-measurement, 2026-10-03.

**Counts.** 71 new paper entries created with this topic (all `lab.py verify` clean: 71 checked, 0 problems),
plus 15 existing entries by other agents that carry the topic (14 already tagged; `strandburg-peshkin-2013-visual`
tagged by me): `cavagna-2010-scale`, `bialek-2012-statistical`, `cavagna-2017-dynamic`,
`attanasi-2014-information`, `attanasi-2014-collective`, `gomez-nava-2023-fish`, `tunstrom-2013-collective`,
`verdoucq-2025-flocking`, `romanczuk-2022-phase`, `zheng-2024-body`, `cavagna-2014-bird`, `hang-2026-self`,
`ouellette-2022-physics`, `puy-2024-signatures`, `gonzalez-albaladejo-2024-power`, `strandburg-peshkin-2013-visual`.
By type (new entries): 12 reviews or primers ([[mora-2011-biological]], [[munoz-2018-colloquium]],
[[khaluf-2017-scale]], [[daniels-2016-quantifying]], [[mediano-2022-greater]], [[pilkiewicz-2020-decoding]],
[[tkacik-2016-information]], [[kim-2021-informational]], [[beggs-2012-being]], [[feinerman-2018-physics]],
[[chen-2025-why]], [[hepworth-2022-swarm]]); about 20 empirical animal studies (birds, midges, fish, ants,
bees, macaques); 5 robot or human-swarm experiments; about 20 theory and model papers; about 14
information-measure and method papers (transfer entropy, PID/causal emergence, IIT, JIDT). Skeptical and null-model
papers are included on purpose: [[schwab-2014-zipfs]], [[touboul-2017-power]], [[morrell-2021-latent]],
[[ngampruetikorn-2025-extrinsic]], [[priesemann-2014-spike]], [[klamser-2021-collective]],
[[brown-2020-information]], [[ferretti-2025-out]], [[sattari-2022-modes]]. 35 of the 71 are from 2020 or later,
16 from 2024-2026.

**Full reads (read_depth: full), 6:** [[mora-2011-biological]], [[klamser-2021-collective]],
[[poel-2022-subcritical]], [[rosas-2020-reconciling]], [[crosato-2018-informative]], [[chen-2025-why]]. I also
read [[cavagna-2010-scale]] in full and appended notes to that existing entry.

**Search log.** OpenAlex list/search endpoints ran out of the shared daily budget after round 1 (HTTP 429
"Insufficient budget"); single-work lookups still worked, so citation counts are OpenAlex, but forward and
backward chasing used OpenCitations (COCI) plus Crossref metadata. Semantic Scholar and the arXiv export API
were rate-limited; arXiv listing pages worked intermittently. "New" means not already catalogued (by me or anyone).

| # | Where | Query or seed | Results scanned | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex search | seeds: "criticality living systems", "statistical mechanics natural flocks birds", "scale-free correlations starling flocks" | 90 | 9 | 8 |
| 2 | Crossref bibliographic | "criticality collective behavior animal groups"; "information transfer collective motion transfer entropy" | 80 | 4 | 2 |
| 3 | Crossref title resolution | 42 candidate seminal titles from reviews and memory (all confirmed against Crossref before cataloguing) | 42 | 42 | 40 |
| 4 | Forward citations (OpenCitations + Crossref) | Cavagna 2010 PNAS, by count and by recency | 95 of 951 | 30 | 15 |
| 5 | Forward citations | Munoz 2018, Rosas 2020, Khaluf 2017, Attanasi 2014 Nat Phys, Barnett 2013 | 180 | 45 | 14 |
| 6 | WebSearch | swarm robots criticality susceptibility order-disorder | 9 | 5 | 2 |
| 7 | WebSearch | partial information decomposition synergy collective motion | 9 | 1 | 0 |
| 8 | WebSearch | "causal emergence" flocking/swarm 2023-2025 | 9 | 2 | 0 |
| 9 | WebSearch | multi-agent RL self-organise to criticality / edge of chaos | 9 | 2 | 1 |
| 10 | Europe PMC title search | criticality x collective/swarm/flock; transfer entropy x collective/fish/group | 80 | 9 | 4 |
| 11 | arXiv listing (5 phrasings) | criticality collective motion; transfer entropy swarm; scale-free correlations collective; integrated information collective behavior; maximum entropy flock | 100 | 12 | 4 |
| 12 | Backward references (OpenCitations) | Klamser 2021, Poel 2022, plus reference list of Chen and Prokopenko 2025 | 148 | 40 | 7 |
| 13 | Forward citations, recency | Klamser 2021, Poel 2022, Khaluf 2017 (2023-2026) | 150 | 25 | 10 |
| 14 | WebSearch (3 queries) | "distance to criticality" animal/swarm; transfer entropy leader-follower drones; causal emergence / O-information flocking | 28 | 13 | 4 |
| 15 | Europe PMC, 2022-2026 | (criticality OR scale-free OR susceptibility OR phase transition) x (swarm OR flock OR fish OR collective OR herd OR ants OR bees) in title | 60 | 5 | 1 |
| 16 | arXiv listing, quoted phrases | "criticality hypothesis"; "scale-free correlations" swarm; "information transfer" flock criticality | 23 | 6 | 0 (2 neural-only items not catalogued) |

Saturation: rounds 15 and 16 found 1/60 and 0/23 new catalogued items (new/results under 15%). By new/relevant
the last rounds are around 20%, so the core of the topic is saturated but the 2025-2026 tail is still moving.

**Gaps (still missing or thin).**
- Cavagna, Giardina & Grigera (2018), "The physics of flocking: Correlation as a compass from experiments to
  theory", Physics Reports 728, 1-62 (doi 10.1016/j.physrep.2017.11.003). The central review; I could not open it
  (Elsevier 403, CONICET repository 503), so it is not catalogued. Highest-priority addition.
- Wu, Zheng & Romanczuk (2025) PRR 7, 013300, escape cascades with adaptive networks: no abstract reachable.
- de Lamo, Miguel & Pastor-Satorras (2026), arXiv 2609.37637, "Statistical Physics of Fish Collective Motion"
  (possibly a review, not opened); Cavagna et al. "Dynamical maximum entropy approach to flocking" (arXiv
  1310.3810); Ling et al. 2019 jackdaw turns and information transfer (J R Soc Interface); Baglietto & Albano 2008
  finite-size scaling of Vicsek; Herbert-Read et al. 2015 escape waves; Kelley & Ouellette 2013 and Puckett &
  Ouellette 2014 lab midges; De Palo et al. 2017 critical-like Dictyostelium aggregation.
- Criticality in learning agents is thin: [[hidalgo-2014-information]] and [[chen-2025-why]] only; the EvoSK
  preprint (arXiv 2604.15669, RL agents self-organising to an ergodicity-breaking edge) was seen in search but not
  opened. Nothing found on criticality or information-flow measures in LLM agent collectives beyond
  [[engel-2018-integrated]] (human/computer groups).
- Few studies measure susceptibility by direct perturbation rather than from fluctuations; the exceptions are
  [[chatterjee-2025-maximal]], [[gelblum-2015-ant]], [[lei-2023-exploring]], [[verdoucq-2025-flocking]].
  [[ferretti-2025-out]] shows fluctuation-based estimates are least reliable exactly at the transition.

**Code repos seen (for the code scan).**
- https://github.com/PaPeK/PredatorPrey (predator-prey schooling model of [[klamser-2021-collective]]).
- qianyangchen/isingModelPALoop, Zenodo doi 10.5281/zenodo.13784627 (Ising perception-action loop, [[chen-2025-why]]).
- JIDT, http://code.google.com/p/information-dynamics-toolkit/ as given in [[lizier-2014-jidt]] (current host
  not checked); used by [[crosato-2018-informative]] and [[rosas-2020-reconciling]].

**Suggested follow-up tasks.**
1. Code scan: catalogue the three repos above in `library/code/` and link them from the paper entries.
2. Retrieve and catalogue Cavagna, Giardina & Grigera 2018 (Physics Reports) and the de Lamo et al. 2026 preprint.
3. Full reads of [[sas-2026-improved]] (emergence estimator for large flocks), [[lei-2023-exploring]],
   [[chatterjee-2025-maximal]], [[lin-2025-experimental]] and [[munoz-2018-colloquium]].
4. Survey (prior-art gate): "Is near-criticality a useful design target for robot or agent swarms?", seeded with
   [[klamser-2021-collective]], [[poel-2022-subcritical]], [[lei-2023-exploring]], [[mateo-2017-effect]] and the
   null-model papers above.
5. Experiment idea for a later hypothesis: in a Vicsek or Couzin simulation, sweep alignment across the transition
   and compute side by side xi vs N, chi from fluctuations and from direct perturbation, Fisher information,
   global transfer entropy and Psi, with a shared-external-driver null model.
6. Gap scan on criticality and information-flow measures in MARL and LLM agent collectives.

