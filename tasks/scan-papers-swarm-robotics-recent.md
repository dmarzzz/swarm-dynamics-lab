---
id: scan-papers-swarm-robotics-recent
type: task
title: Catalogue swarm robotics papers from 2024 onward
kind: scan
status: claimed
priority: p0
owner: dmarz/swarm-robotics-recent
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-robotics
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

The field moves fast and the seminal scan will skew old. Catalogue 2024 to 2026 work on swarm robotics, especially drone swarms, learned swarm controllers, and sim-to-real results. Include strong preprints and workshop papers.

## Search plan

- arXiv listing searches sorted by date, OpenReview (ICLR, NeurIPS, ICML, CoRL), and forward citations of the seminal papers in the sibling scan task.
- Check the accepted-paper lists of the most recent relevant conferences and workshops.

## Done when

- At least 20 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 4 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Written by dmarz/swarm-robotics-recent on 2026-10-03. Scope: swarm robotics papers from 2024 to 2026, academic sources first, with emphasis on drone swarms, learned swarm controllers, sim-to-real, and physics-of-robot-swarms results. The seminal and older work belongs to the sibling task `scan-papers-swarm-robotics`.

**Tool availability during the run.** OpenAlex returned 429 for the whole session: the shared free daily budget for this IP was exhausted, with reset at midnight UTC. Citation counts in my entries therefore come from Crossref `is-referenced-by-count` or Semantic Scholar, each labelled with its source and date. DBLP served a bot-check page. The arXiv export API returned 503, then 429. The arXiv HTML search pages, arXiv abs/HTML full texts, Crossref, DataCite, Europe PMC REST and NCBI eutils worked. Semantic Scholar worked for part of the session, then rate-limited. The Science, ScienceDirect, MDPI, PMC and IEEE pages were blocked.

### Search log

| # | Where | Query (abridged) | Results screened | Relevant | New |
|---|---|---|---|---|---|
| 1 | WebSearch | swarm robotics review 2024/2025 drone swarm learned controller | 10 | 6 | 6 |
| 2 | WebSearch | arXiv 2025 decentralized drone swarm RL sim-to-real real-world flight | 9 | 6 | 6 |
| 3 | WebSearch | Science Robotics 2024 swarm robots collective behaviour | 9 | 5 | 5 |
| 4 | OpenAlex | title.search "swarm robotics", year > 2023, sorted by citations | 0 (429, budget exhausted) | 0 | 0 |
| 5 | arXiv listing (HTML search, title, newest first) | "swarm drone" | 93 (about 45 from 2024+) | 10 | 10 |
| 6 | arXiv listing (title, newest first) | "robot swarm", "robot swarms", "swarm robotics", "aerial swarm", "quadrotor swarm" (2024+ only) | about 180 unique | about 45 | about 40 |
| 7 | arXiv search (all fields), 8 queries | swarm RL quadrotor; flocking drones real-world; swarm sim-to-real; GNN swarm control; robot collective motion active matter; kilobot; self-assembly modular swarm; swarm emergent behaviour discovery | 55 unique | 25 | 15 |
| 8 | WebSearch | swarm robotics review 2024/2025 (Swarm Intelligence, Frontiers, perspectives) | 10 | 4 | 3 |
| 9 | WebSearch | LLM robot swarms (LLM2Swarm, SwarmGPT, LLM-powered swarms) | 9 | 5 | 4 |
| 10 | Crossref bibliographic match | 10 arXiv titles to published versions (Sci Robot, Nat Commun, npj Robot, PNAS, RA-L, AAMAS, ICRA) | 40 | 8 | 0 (metadata only) |
| 11 | Semantic Scholar forward citations (backbone of the chase) | citers of Vásárhelyi 2018, Rubenstein 2014, Dorigo 2021, Brambilla 2013, Zhou 2022, Batra 2021; 2024+ only, sorted by citation count | 1,374 citing papers from 2024+; top 120 screened | about 25 | about 15 |
| 12 | Semantic Scholar forward citations, sorted by recency | citers of Zhang 2025 (NMI), Huang 2024 (ICRA), Mezey 2025 (npj Robotics) | 174 | about 20 | 8 |
| 13 | Semantic Scholar keyword search, 2024-2026 | "flocking robots experiment"; "multi-robot RL swarm real robots" (3 further queries hit 429) | 80 | 8 | 4 |
| 14 | WebSearch (OpenReview, CoRL, NeurIPS, ICLR) | swarm robots learning, decentralized multi-robot policy | 10 | 5 | 1 |
| 15 | WebSearch | robot swarm 2025 Science Robotics emergent self-organisation physical robots | 9 | 6 | 4 |
| 16 | Backward references (full reads) | reference lists of Zhang 2025, Choi 2026, Verdoucq 2025, Casiulis 2025, Zhang 2026 | about 300 refs | mostly pre-2024 (sibling scope) | 0 in scope |
| 17 | WebSearch | robot swarm phase transition order parameter 2025/2026 | 9 | 3 | 0 |
| 18 | WebSearch | MARL drone swarm flocking real-world Crazyflie 2025 | 9 | 7 | 5 |
| 19 | WebSearch | swarm robotics 2025 survey, learning-based control, GNN | 9 | 6 | 4 |
| 20 | WebSearch | kilobot or e-puck swarm experiment 2025 | 10 | 0 in scope | 0 |
| 21 | WebSearch | 2026 learned decentralized swarm policy, real robots, emergent | 9 | 6 | 2 |
| 22 | WebSearch | aerial/drone swarm 2025 in Science Robotics, Nature, T-RO | 9 | 7 | 1 |

**Saturation.** The last two rounds found 2/9 (22%) and 1/9 (11%) new relevant items, and round 20 found 0/10. The physics-of-robot-swarms and review strands saturated. The learned aerial-swarm MARL strand is close but not fully saturated: each new query still turns up one or two Crazyflie-scale RL papers.

### Counts

- New library entries created by me: **45 papers** (7 from 2024, 26 from 2025, 12 from 2026). Read depth: 6 full, 3 skim, 36 abstract. All 45 pass `lab.py check` (0 errors, 0 warnings) and `lab.py verify` (45 checked, 0 problems).
- Review and perspective articles found and catalogued: [[abbass-2025-road]], [[refis-2025-network]], [[cazenille-2025-signalling]], [[xu-2026-small]]. Already in the library from sibling agents: [[kegeleirs-2025-towards]], [[garzon-ramos-2024-designing]], [[rahman-2025-llm-powered]], [[cai-2025-reinforcement]]. Reviews found but **not catalogued** because the page could not be opened: Du et al. 2025, "A Survey on Autonomous and Intelligent Swarms of Uncrewed Aerial Vehicles (UAVs)", IEEE T-ITS 26(10), DOI 10.1109/tits.2025.3569500; Xu et al. 2026, "Swarm Robotics Collaborative Architecture Based on Embodied Cognition: A Survey...", IEEE T-ASE, DOI 10.1109/tase.2026.3708974; Alqudsi & Makaraci 2024/2025, review of swarm flying robots, Proc. IMechE C, DOI 10.1177/09544062241275359.
- Existing entries I updated: added the topic `swarm-robotics` to [[jung-2025-kinetic]]. Appended "Notes from dmarz/swarm-robotics-recent" with full-read details and published DOIs to [[casiulis-2025-geometric]] and [[mattson-2025-discovery]].
- Already catalogued by sibling agents and relevant here (not duplicated): [[zhu-2024-self]], [[mezey-2025-purely]], [[strobel-2024-llm2swarm]], [[ji-2026-genswarm]], [[jin-2026-physics]], [[bektas-2025-emergent]], [[nitti-2025-collective]], [[zhao-2024-snail]], [[kim-2025-commanding]], [[arbel-2024-mechanical]], [[zheng-2024-body]], [[batra-2022-decentralized]].

### Full reads (read_depth: full or full-text notes)

1. [[zhang-2025-learning]]: differentiable-physics vision policy, communication-free 6-drone swarm (Nature Machine Intelligence 2025).
2. [[huang-2024-collision]]: end-to-end DRL quadrotor swarm with obstacles, zero-shot to Crazyflie (ICRA 2024).
3. [[choi-2026-communication]]: LiDAR DRL with implicit leader-follower and communication-free 5-UAV navigation.
4. [[verdoucq-2025-flocking]]: phase diagram and criticality of a 10-drone outdoor flock, with intruder responses.
5. [[varadharajan-2024-hierarchies]]: hierarchical vs egalitarian swarms with a Poisson coverage model.
6. [[zhang-2026-asymmetric]]: asymmetric physics (differentiable surrogates) for 512-quadruped swarm learning.
7. [[casiulis-2025-geometric]] (full read recorded as notes; the entry is owned by dmarz/collective-motion-recent-audit).
8. [[mattson-2025-discovery]] (full read recorded as notes; the entry is owned by dmarz/swarm-robotics).

### Code repositories seen (for the code scan task; no code entries were created in this run)

- https://github.com/HenryHuYu/DiffPhysDrone ([[zhang-2025-learning]])
- https://github.com/CAB-Lab-Princeton/LEGO-MARL ([[wang-2025-local]])
- https://github.com/Pold87/LLM2Swarm ([[strobel-2024-llm2swarm]])
- https://github.com/WindyLab/GenSwarm ([[ji-2026-genswarm]])
- https://github.com/AleNit/Swarm-Cooperation-Model ([[nitti-2025-collective]])
- https://github.com/Da-Zhao1997/Snail-inspired-robotic-swarms ([[zhao-2024-snail]])
- https://github.com/MISTLab/Swarm-SLAM (Swarm-SLAM, arXiv:2301.06230; seen in the listing, paper not catalogued)
- Project pages with code or video links: https://sites.google.com/view/obst-avoid-swarm-rl ([[huang-2024-collision]]), https://sites.google.com/view/pursuit-evasion-rl ([[chen-2025-online]]), https://sites.google.com/view/sync-sbc/home ([[raveendra-2026-syncsbc]]), https://sites.google.com/view/swarmdiscovery-with-rsrs/home ([[mattson-2025-discovery]]). Google Drive code for [[zhang-2026-asymmetric]].
- Data: the outdoor 10-drone flocking dataset is at https://doi.org/10.5281/zenodo.17902132 ([[verdoucq-2025-flocking]]). The Done-when item "every paper that ships code has its repo catalogued in library/code/" is **not met** by this run: this run's rules forbid creating code entries, so the list above is handed to the code scan.

### Notable gaps

- OpenAlex citation counts and OpenAlex forward-citation chasing were not possible (budget). Rerun after the midnight-UTC reset to replace Crossref/S2 counts and to cross-check round 11.
- Peer-reviewed conference proceedings were not browsed issue by issue (ICRA 2025/2026, IROS 2025, CoRL 2024/2025, RSS 2025, ANTS 2026, DARS 2024). Coverage of these comes only through arXiv and citation trails. DBLP was blocked.
- Science Robotics issues for 2024-2026 were not browsed directly. Science and ScienceDirect pages were blocked.
- Under-covered sub-areas: magnetic microrobot and nanorobot swarms, underwater and surface robot swarms, heterogeneous air-ground swarms, human-swarm interaction, swarm security and fault tolerance beyond [[shefi-2025-bugs]].
- Paywalled items not catalogued: Deng et al. 2026, "Learning safe and decentralized flight for aerial swarms in dynamic complex environments", Chinese Journal of Aeronautics 39(7) 104113, DOI 10.1016/j.cja.2026.104113. The three reviews listed above are also uncatalogued.

### Suggested follow-up tasks

1. Code scan: catalogue the repositories above in library/code and link them via `code:` (DiffPhysDrone, LEGO-MARL, GenSwarm and LLM2Swarm first).
2. Full reads, if a survey needs them: [[zhang-2025-gcbf]] (GCBF+), [[hou-2025-primitive]], [[zhu-2024-self]] (SoNS, 135 pp.), [[zhao-2026-self]] (aquatic SOC exponents) and [[chiu-2025-learn]].
3. Dataset task: reanalyse the Verdoucq et al. Zenodo flocking data (polarisation susceptibility vs alignment gain) as a candidate hackathon experiment.
4. Rerun OpenAlex after reset, for citation counts on all 45 entries and forward-citation chasing of [[zhang-2025-learning]], [[huang-2024-collision]] and [[vasarhelyi-2018-optimized]].
5. Scan of microrobot, underwater and heterogeneous swarms from 2024 onward, the gap noted above.
6. Retrieve the paywalled reviews (Du 2025 T-ITS; Xu 2026 T-ASE; Alqudsi 2024 Proc IMechE C) and Deng 2026 CJA through a browser session, then catalogue them.
