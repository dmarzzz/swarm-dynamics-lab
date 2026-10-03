---
id: scan-papers-swarm-robotics
type: task
title: 'Catalogue the papers: swarm robotics'
kind: scan
status: claimed
priority: p0
owner: dmarz/swarm-robotics
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-robotics
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `swarm-robotics`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Brambilla et al. 2013, Swarm robotics: a review from the swarm engineering perspective (Swarm Intelligence)
- Rubenstein, Cornejo and Nagpal 2014, Programmable self-assembly in a thousand-robot swarm (Science)
- Werfel, Petersen and Nagpal 2014, Designing collective behavior in a termite-inspired robot construction team (Science)
- Vásárhelyi et al. 2018, Optimized flocking of autonomous drones in confined environments (Science Robotics)
- Dorigo, Theraulaz and Trianni, Swarm robotics: past, present, and future (Proc. IEEE, 2021)
- Hamann, Swarm Robotics: A Formal Approach (book)

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

Scan by dmarz/swarm-robotics on 2026-10-03. Academic sources only (papers, reviews, one monograph).

**Search rounds** (results = items screened; new = relevant items not already in the library or earlier rounds)

| # | Where | Query / method | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex | full-text `swarm robotics review`, sorted by citations | 50 | 3 | 3 |
| 2 | OpenAlex | `title.search:swarm robotics`, sorted by citations | 50 | 38 | 35 |
| 3 | OpenAlex | `title.search:swarm robotics`, `publication_year:>2022` | 50 | 15 | 12 |
| 4 | Crossref | bibliographic lookups of seeds and landmark titles (Werfel, Vásárhelyi, Kilobot, particle robotics, mean-field survey, Soria, Mathews, Boudet, Gardi) | 40 | 11 | 9 |
| 5 | Semantic Scholar | forward citations of [[rubenstein-2014-programmable]] (1278 citing; top 50 by citations) | 50 | 20 | 12 |
| 6 | Semantic Scholar | forward citations of [[vasarhelyi-2018-optimized]] (498 citing; top 35 by citations + 40 most-cited from 2024-2026) | 75 | 25 | 12 |
| 7 | Semantic Scholar | forward citations of [[brambilla-2013-swarm]] (1805 citing; top 40 by citations + 40 most-cited from 2024-2026) | 80 | 30 | 10 |
| 8 | Semantic Scholar | search `self-propelled robots collective dynamics` (physics vocabulary) | 30 | 5 | 3 |
| 9 | Crossref + S2 batch | backward references of Dorigo et al. 2021 (Proc. IEEE) and [[ben-zion-2023-morphological]], 22 DOIs resolved | 22 | 14 | 9 |
| 10 | Web (Google-style) | `robot swarm collective behavior Science Robotics 2025 decentralized` | 10 | 4 | 3 |
| 11 | Web / arXiv | `arXiv 2025 robotic active matter swarm self-propelled robots collective motion experiment` | 9 | 6 | 4 |
| 12 | arXiv abs pages | ML vocabulary: GNN decentralised swarm control, deep RL for swarms | 2 | 2 | 1 |
| 13 | Crossref | `robot swarm collective behavior self-organization`, journal articles 2015+ | 30 | 8 | 3 |
| 14 | Crossref | `decentralized flocking aerial robots drones swarm`, journal articles 2014+ | 30 | 6 | 2 |

Rounds 13 and 14 each found at most 10% new items (3/30, 2/30), so the scan is close to saturation for
high-impact work. Two further Semantic Scholar searches (`active matter robots collective motion experiment`,
`kilobot collective decision making`) returned HTTP 429, and the OpenAlex free daily budget for this machine's
IP was exhausted after round 3 (resets at midnight UTC), so OpenAlex forward/backward chasing was replaced by
Semantic Scholar and Crossref.

**Counts.** 59 new paper entries created by this agent, all tagged `swarm-robotics`: 15 reviews, perspectives or
books, 44 primary papers; 21 of the 59 are also tagged `active-matter` (robophysics and microrobot
collectives); 21 are from 2023-2026. Six entries added in parallel by other topic agents already carried the
`swarm-robotics` tag and needed no change ([[huttenrauch-2019-deep]], [[mezey-2025-purely]],
[[chen-2024-persistent]], [[strobel-2024-llm2swarm]], [[reina-2015-design]], [[tolstaya-2020-learning]]).
`lab.py check` reports 0 errors and 0 warnings, and `lab.py verify` checked all 59 against arXiv and Crossref
with 0 problems.

**Read in full (6):** [[vasarhelyi-2018-optimized]], [[ben-zion-2023-morphological]], [[sun-2023-mean]],
[[chvykov-2021-low]], [[baconnier-2022-selective]], [[valentini-2017-best]]. Skimmed: [[viragh-2014-flocking]].
The rest are abstract-level. For those, details not in the abstract are marked "not checked".

**Seeds.** All checked out and are catalogued except Dorigo, Theraulaz and Trianni 2021 (Proc. IEEE 109(7),
1152-1165, DOI 10.1109/jproc.2021.3072740). The metadata is confirmed, but IEEE Xplore blocked access and no
abstract exists, so it was not catalogued (no phantom sources). [[dorigo-2020-reflections]] is catalogued in its
place. Hamann's book is catalogued from the publisher description only.

**Gaps.**
- Reviews found but not catalogued because the publisher pages blocked automated access and no abstract was
  reachable: Bayındır 2016 (Neurocomputing, tasks review), Kolling et al. 2016 (human-swarm interaction survey,
  IEEE THMS), Oh et al. 2017 (pattern-formation review, RAS), Blais & Akhloufi 2023 (RL for swarm robotics),
  Hunt & Hauert 2020 (safety checklist, Nat. Mach. Intell.), Dorigo et al. 2013 (Swarmanoid). Also seen and not
  yet opened: Barca & Şekercioğlu 2012, Navarro & Matía 2012, Senanayake et al. 2016 (search/tracking), Yang &
  Zhang 2020 (Annu. Rev. magnetic microrobot swarms), ACS Nano 2023 micro/nanorobotic swarms review, Nat. Rev.
  Mater. 2025 swarming micromotors review, Coppola et al. 2020 (micro air vehicle swarming survey), An overview
  of swarm coordinated control (IEEE TAI 2024), The 2024/2025 motile active matter roadmaps.
- Primary work seen and not catalogued: Valentini, Hamann & Dorigo 2015 (100-Kilobot decisions, AAAI; no
  abstract reachable), Gauci et al. 2018 consensus without computation, Pickem et al. 2017 Robotarium, Mondada
  et al. 2004 swarm-bot, Schilling et al. 2019/2021 vision-based drone flocking, Karagüzel 2022 collective
  gradient perception with flying robots, Swarmodroid bristle-bots (arXiv 2305.13510), Balázs 2024
  decentralised drone traffic, PRIMAL (MAPF), Duarte et al. 2016 evolved aquatic swarm.
- Thin coverage: underwater and marine swarms beyond [[berlinger-2021-implicit]], human-swarm interaction,
  heterogeneous swarms (Swarmanoid), field deployments, and quantitative replication of flocking phase
  diagrams on robots (Turgut et al. 2011 on leaders and transitions in a robotic flock).
- Code repos were not catalogued (code entries were out of scope for this run). The task's Done-when item on
  code entries is still open.

**Code repositories seen** (for the code-scan task): https://github.com/csviragh/robotsim (drone flocking
simulator, [[vasarhelyi-2018-optimized]], [[viragh-2014-flocking]]); https://github.com/CMA-ES/pycma
(optimiser used there); https://github.com/collmot (drone swarm org cited by Vásárhelyi 2018);
https://github.com/WestlakeAerialRobotics/Human-swarm-interface ([[sun-2023-mean]], Zenodo
10.5281/zenodo.7960508); https://github.com/Pold87/LLM2Swarm ([[strobel-2024-llm2swarm]]);
https://github.com/soft-matter/trackpy (tracking used by [[ben-zion-2023-morphological]]); data/code archives
at Zenodo 10.5281/zenodo.4056700 ([[chvykov-2021-low]]) and 10.5281/zenodo.6653906 ([[baconnier-2022-selective]]).
Swarm simulators worth a code scan: ARGoS, Kilombo/Kilobot simulators, Buzz, the Robotarium, EGO-Swarm planner.

**Suggested follow-up tasks** (not opened, because this run could only write the files it was given):
1. `scan-code-swarm-robotics`: catalogue the repos above plus ARGoS, Kilombo, Robotarium and EGO-Swarm, and link
   them through `code:` fields.
2. `scan-papers-swarm-robotics-reviews-2`: open the uncatalogued reviews listed in Gaps through a browser or
   library access, starting with Dorigo et al. 2021, Bayındır 2016 and Kolling 2016.
3. `scan-papers-robophysics`: a separate pass on robotic active matter (Goldman, Dauchot, Kellay, Bechinger
   labs) seeded from [[janzen-2026-active]] and the motile active matter roadmap.
4. `question-flocking-delay`: reproduce the collision versus delay and communication-range map of
   [[vasarhelyi-2018-optimized]] (Fig. 2) in simulation, and test whether [[chen-2024-persistent]]-style
   adaptive delay changes it.
