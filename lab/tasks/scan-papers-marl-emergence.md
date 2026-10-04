---
id: scan-papers-marl-emergence
type: task
title: 'Catalogue the papers: multi-agent rl and emergent coordination'
kind: scan
status: done
priority: p0
owner: dmarz/marl-emergence
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- marl-emergence
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T18:19Z
outputs:
- 1-library/papers
---

## Goal

Build the paper base for `marl-emergence`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Lowe et al. 2017, Multi-agent actor-critic for mixed cooperative-competitive environments (MADDPG)
- Foerster et al. 2016, Learning to communicate with deep multi-agent reinforcement learning
- Yang et al. 2018, Mean field multi-agent reinforcement learning (ICML)
- Hüttenrauch et al. 2019, Deep reinforcement learning for swarm systems (JMLR)
- Baker et al. 2019, Emergent tool use from multi-agent autocurricula (hide-and-seek)
- Leibo et al. 2021, Melting Pot (ICML)

## Search plan

- Start from the seeds. For each seminal paper, pull its references (backward) and the papers citing it (forward) from Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>/citations?fields=title,year,externalIds,citationCount&limit=100
- Query arXiv (export.arxiv.org/api/query), Semantic Scholar search and OpenAlex (api.openalex.org/works?search=...) with at least 5 different phrasings of the topic, including the terms used by neighbouring fields.
- Look for review articles first: they give the map and their reference lists are dense seeds.
- Prioritise by relevance to the hackathon, then by citation count, then recency. Catalogue the review papers, the seminal papers, and the strongest recent work.

## Done when

- At least 25 papers catalogued in 1-library/papers/ with this topic, including every review article you found.
- At least 5 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in 1-library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Written by dmarz/marl-emergence on 2026-10-03.

**Access problems that shaped the search.** OpenAlex returned results for the first two rounds and then hit its
shared per-IP daily budget (HTTP 429, "Insufficient budget", reset at midnight UTC). The arXiv export API and,
later, arXiv's own search page also returned 429. The Semantic Scholar API worked only for single batch and
citation calls with long back-off. The DBLP API is behind a bot challenge. Springer, ScienceDirect and IEEE
landing pages are blocked to automated reads. Citation counts therefore come from several sources (OpenAlex
before the cut-off, then Crossref `is-referenced-by-count`, Semantic Scholar or OpenCitations). Each entry's
`citations` field names its source and date.

### Search rounds

| # | Where | Query or seed | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex (title.search, by citations) | "multi-agent reinforcement learning" | 50 | 14 | 14 |
| 2 | OpenAlex (title.search) | the six seed titles, plus "mean field games", "swarm reinforcement learning", "deep reinforcement learning for swarm systems" | ~110 | 12 | 8 |
| 3 | arXiv listing (newest first) | "emergent communication multi-agent reinforcement learning" | 50 | 4 | 4 |
| 4 | Crossref | "survey multiagent reinforcement learning"; "deep RL swarm robotics collective behaviour"; "RL flocking self-propelled agents" | 120 | 6 | 5 |
| 5 | WebSearch | physics vocabulary ("RL emergence collective motion flocking schooling Physical Review"); "MARL swarm emergent behavior review 2024"; the Durve seed | 28 | 10 | 6 |
| 6 | Backward citations (read in full) | reference lists of Hüttenrauch 2019, Durve 2020, Brambati 2025, Yang 2018 | ~150 | 14 | 5 |
| 7 | Forward citations (Semantic Scholar, sorted by count and separately for 2024 and later) | Hüttenrauch 2019 (257), Durve 2020 (39), Yang 2018 (743) | 1039 | 30 | 14 |
| 8 | Forward citations (Semantic Scholar, keyword-filtered) | Verma 2018 (440), Mordatch 2018 (838) | 1278 | 14 | 6 |
| 9 | WebSearch | "learning mean field games survey"; "MARL predator prey swarming confusion"; "GNN decentralized controllers robot swarm flocking" | 27 | 8 | 2 |
| 10 | WebSearch | "MARL emergence of flocking milling schooling 2024 2025" | 9 | 5 | 2 |
| 11 | WebSearch | "mean-field RL large swarm collective behavior order parameter" | 9 | 6 | 4 |
| 12 | Crossref | "MARL emergent collective behaviour swarm self-organization" | 40 | 4 | 2 |
| 13 | WebSearch | "MARL ant colony foraging pheromone stigmergy" | 9 | 6 | 4 |
| 14 | Forward citations (Semantic Scholar) | Li 2023 predator-prey (25), Falk 2021 (42) | 67 | 8 | 6 |
| 15 | WebSearch | "inverse RL collective animal behavior, reward from fish or bird trajectories" | 9 | 5 | 2 |
| 16 | Crossref | "reinforcement learning flocking collective motion learned alignment rule" | 40 | 6 | 3 |
| 17 | WebSearch | "survey learning-based swarm robotics emergent behaviour deep RL flocking aggregation" | 9 | 6 | 3 |

**Saturation.** The large rounds have saturated: rounds 12, 14 and 16 found 5%, 9% and 8% new items. The
small web-search rounds (9 results each) still turn up 2 to 4 new items each, all in sub-niches: stigmergy,
inverse RL, swarm-robotics surveys. I stopped because the count target (about 40) was well exceeded, not
because every niche is exhausted.

### Counts

- 62 papers catalogued with `marl-emergence`, all added by this agent (no duplicates found). Read depth: 6
  full, 1 skim (MADDPG), 55 abstract. `lab.py check`: 0 errors and 0 warnings. `lab.py verify`: 62 checked, 0
  problems.
- By kind: 14 reviews or surveys, about 20 seminal or benchmark MARL papers, and about 28 papers on learned
  collective behaviour from the physics, biology and robotics communities.
- By year: up to 2015, 4; 2016 to 2019, 19; 2020 to 2023, 25; 2024 to 2026, 14.
- Reviews catalogued: [[busoniu-2008-comprehensive]], [[hernandez-leal-2019-survey]], [[zhang-2021-multi]],
  [[gronauer-2022-multi]], [[oroojlooy-2023-review]], [[lazaridou-2020-emergent]], [[lauriere-2022-learning]],
  [[cichos-2020-machine]], [[orr-2023-multi]], [[zhu-2024-survey]], [[cai-2025-reinforcement]],
  [[cui-2022-survey]], [[chen-2026-five]], [[zheng-2026-brief]].

### Read in full

[[huttenrauch-2019-deep]], [[durve-2020-learning]] (arXiv v1 text), [[yang-2018-mean]] (main text),
[[verma-2018-efficient]] (main text, methods and the RL part of the supplement), [[brambati-2025-learning]],
[[baker-2020-emergent]] (main text, appendix skimmed).

### Notable gaps

- These reviews were found but could not be opened (publisher pages blocked), so they are not catalogued: Panait
  and Luke 2005, "Cooperative multi-agent learning: the state of the art", AAMAS journal,
  doi:10.1007/s10458-005-2631-2; Blais and Akhloufi 2023, "Reinforcement learning for swarm robotics", Cognitive
  Robotics, doi:10.1016/j.cogr.2023.07.004; the 2024 "survey on multi-agent reinforcement learning and its
  application" in the Journal of Automation and Intelligence, doi:10.1016/j.jai.2024.02.003; and a 2026 Springer
  chapter "Reinforcement learning for swarm intelligent systems: a comprehensive survey".
- These primary papers were found but not opened: Wang et al. 2023, "Modeling collective motion for fish
  schooling via MARL", Ecological Modelling 477:110259 (ScienceDirect blocked); Huang, Malhamé and Caines 2006
  (the other founding mean-field-game paper); a 2025 paper on fish-school milling with GCN-critic MADDPG,
  doi:10.1007/s42235-025-00721-9; Shen et al. 2022, "Deep RL for flocking motion of multi-UAV systems: learn
  from a digital twin", IEEE IoT-J; Liu et al. 2019, "Emergent coordination through competition"; "Learning to
  school in dense configurations with multi-agent deep RL", Bioinspiration and Biomimetics 2022; Ashwood et al.
  2022, dynamic inverse RL; and the stigmergy line (Nguyen 2021, arXiv:2105.03546).
- 55 of the 62 entries are abstract-level. The highest-value candidates for upgrading to full reads are
  [[li-2023-predator]], [[munoz-gil-2026-emergent]], [[heuthe-2024-counterfactual]], [[jung-2025-kinetic]],
  [[borra-2021-optimal]] and [[loffler-2023-collective]].
- There is no Semantic Scholar or OpenAlex citation count for some arXiv-only papers (left null).
- Nobody has yet measured whether learned flocks reproduce the Vicsek order-disorder transition. Brambati and
  colleagues mention a noise-driven transition near eta_c of about 1 without analysing it, and Borra and
  colleagues predict a second-order transition analytically. That is a gap in the literature, not in this search.

### Code repositories seen (for the code-scan task; not catalogued here)

- https://github.com/LCAS/deep_rl_for_swarms (Hüttenrauch 2019, mean embeddings)
- https://github.com/openai/multi-agent-emergence-environments (hide-and-seek, Baker 2020)
- https://github.com/openai/multiagent-particle-envs (MPE, Lowe 2017)
- https://github.com/marlbenchmark/on-policy (MAPPO, Yu 2022)
- https://sites.google.com/view/swarm-rl (project site for Batra 2022 quadrotor swarms; its code repository was not opened)
- Repositories named in abstracts but not opened: Melting Pot (Leibo 2021), MAgent (Zheng 2018), PyMARL and SMAC
  (Samvelyan 2019).

### Suggested follow-up tasks

1. Code scan for marl-emergence: catalogue the repositories above in 1-library/code/ (stars, licence, last
   commit, whether it runs on aarch64) and link them through `code:`. MAgent2 and PettingZoo are the
   large-population environments to check.
2. Upgrade to full reads: [[li-2023-predator]], [[munoz-gil-2026-emergent]], [[heuthe-2024-counterfactual]],
   [[jung-2025-kinetic]], [[borra-2021-optimal]], [[loffler-2023-collective]].
3. A sub-scan on inverse RL for collective behaviour (Šošić, Schafer, Wälchli, plus Ashwood and the bird-flocking
   IRL work), coordinated with the criticality-measurement and collective-motion topics.
4. A sub-scan on stigmergic and implicit-communication MARL (ForMIC, PooL, Pitteri 2026, Nguyen 2021), shared
   with swarm-intelligence.
5. Retry the uncatalogued reviews in the gaps list from a browser or an institutional proxy.
6. Survey seed: "Do learned swarm policies reproduce the phase transitions of hand-written collective-motion
   models?" Prior art: [[durve-2020-learning]], [[brambati-2025-learning]], [[borra-2021-optimal]],
   [[yang-2018-mean]], [[yamaguchi-2025-emergent]], [[pitteri-2026-ant]], [[jung-2025-kinetic]].

### Audit (dmarz/marl-emergence-audit)

Audited 2026-10-03. `lab.py verify --agent dmarz/marl-emergence` reported 62 checked, 0 problems, so no phantom
or mismatched records. I spot-checked 14 entries against the source: all six `full` entries
([[huttenrauch-2019-deep]], [[durve-2020-learning]], [[yang-2018-mean]], [[verma-2018-efficient]],
[[brambati-2025-learning]], [[baker-2020-emergent]]) against their PDFs, number by number, plus
[[li-2023-predator]], [[loffler-2023-collective]], [[mi-2026-unveiling]], [[berman-2026-micro]],
[[pitteri-2026-ant]], [[munoz-gil-2026-emergent]], [[singh-2025-active]] and [[yamaguchi-2025-emergent]] (authors
from DataCite, abstract claims from arXiv), and compared every DOI entry's cite string with Crossref volume, issue,
pages and authors. The numbers and metadata held up. The only correction was the journal name in
[[brambati-2025-learning]] (which now says "Journal of Statistical Mechanics: Theory and Experiment", with the cite
quoted for YAML). Nothing was deleted and no read_depth was downgraded.
Completeness: four extra rounds. (a) Semantic Scholar forward citations of Lowe 2017 (1000 newest, filtered for
swarm and collective terms) were nearly all UAV-application noise, about 1% new. (b) Forward citations of Foerster
2016 were mostly the emergent-communication and LLM line. (c) Web and Crossref searches using statistical-physics and
game-theory vocabulary ("learning dynamics", "replicator", "chaos in games", "mean-field games") found a whole
community the scan had missed. (d) Web searches on predator-confusion flocking, fish-school RL and 2023-2026 reviews.
I added 10 entries: [[hahn-2019-emergent]] (full), [[ivanov-2022-collective]], [[shibayama-2026-deep]],
[[guo-2019-learning]], [[ha-2022-collective]], [[barfuss-2019-deterministic]], [[galla-2013-complex]],
[[sanders-2018-prevalence]], [[bloembergen-2015-evolutionary]] and [[jiang-2020-graph]] (all skim except Hahn).
Found but not added (publisher blocked or lower priority): Wang et al. 2023, Ecological Modelling 477:110259,
doi:10.1016/j.ecolmodel.2022.110259 (ScienceDirect 403); Sheng et al. 2026, "From individual decisions to team
emergence: a survey on explainable cooperative MARL", AI Review 59:209, doi:10.1007/s10462-026-11598-3 (Springer
body not readable); Li et al. 2026, "Formation control of swarm robotics: a survey from biological inspirations to
design automation methods", RAS 196:105245, doi:10.1016/j.robot.2025.105245; Ning and Xie 2024, JAI 3(2):73-91,
doi:10.1016/j.jai.2024.02.003; Brandizzi 2023, "Toward more human-like AI communication: a review of emergent
communication research", IEEE Access, doi:10.1109/ACCESS.2023.3339656; Hu et al. 2022, "The dynamics of Q-learning
in population games: a physics-inspired continuity equation model" (AAMAS); Morihiro et al. 2008 (Q-learning
flocking, cited by Hahn). Still thin: the statistical physics of learning dynamics (Sato and Crutchfield, Kianercy
and Galstyan, Barfuss's later papers), MARL-communication architectures beyond CommNet/DGN (TarMAC, ATOC), and
citation counts. OpenAlex hit its daily budget during this audit, so new entries have Crossref counts or null.
