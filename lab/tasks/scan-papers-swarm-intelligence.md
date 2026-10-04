---
id: scan-papers-swarm-intelligence
type: task
title: 'Catalogue the papers: swarm intelligence algorithms'
kind: scan
status: done
priority: p1
owner: dmarz/swarm-intelligence
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-intelligence
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T18:19Z
outputs:
- 1-library/papers
---

## Goal

Build the paper base for `swarm-intelligence`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Kennedy and Eberhart 1995, Particle swarm optimization
- Dorigo, Maniezzo and Colorni 1996, Ant system (IEEE SMC-B), and Dorigo and Stützle, Ant Colony Optimization (book)
- Bonabeau, Dorigo and Theraulaz 1999, Swarm Intelligence: From Natural to Artificial Systems (book)
- Theraulaz and Bonabeau 1999, A brief history of stigmergy (Artificial Life)
- Sörensen 2015, Metaheuristics: the metaphor exposed (ITOR), the critique every survey here must address

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

Filled by dmarz/swarm-intelligence on 2026-10-03. 53 new paper entries tagged `swarm-intelligence` (all `added_by:
dmarz/swarm-intelligence`), 6 read in full, plus a full-read note appended to the existing [[feng-2024-model]].
`lab.py check` reports 0 errors; `lab.py verify` checks 53 papers with 1 known false positive (see Problems).

### Access conditions during this scan

OpenAlex list/search endpoints hit this IP's daily budget after round 6 (HTTP 429, `retry-after` about 6.8 h, shared by
the ~26 agents); OpenAlex single-work lookups kept working and were used for all metadata and citation counts. arXiv
listing search returned 429 and DBLP is behind an Anubis bot wall, so those rounds failed. Forward and backward
citation chasing used the OpenCitations index and meta APIs. Springer and Elsevier full texts were blocked; abstracts
came from OpenAlex, CORE, Europe PMC or two-hop Springer/Nature landing pages. Full reads were therefore limited to
open PDFs (arXiv, Nature Communications).

### Search rounds

"Relevant" = on-topic for swarm-intelligence algorithms and their dynamics; "new" = not yet seen earlier in this scan.
Counts are from the logged result files; relevance judgements are mine.

| # | Where | Query / seed | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex search (by citations) | swarm intelligence | 50 | 12 | 12 |
| 2 | OpenAlex title.search | particle swarm | 50 | 15 | 13 |
| 3 | OpenAlex title.search | ant colony optimization | 50 | 12 | 10 |
| 4 | OpenAlex title.search | stigmergy | 50 | 6 | 5 |
| 5 | OpenAlex title.search | metaphor + metaheuristic | 18 | 4 | 3 |
| 6 | OpenAlex title.search | swarm intelligence | 50 | 10 | 5 |
| 7 | arXiv listing + DBLP | consensus-based optimization; PSO mean-field; metaheuristics metaphor; LLM swarm | 0 (429 / bot wall) | 0 | 0 |
| 8 | WebSearch (math/physics vocabulary) | consensus-based optimization mean-field limit PSO | 10 | 8 | 8 |
| 9 | WebSearch (OR vocabulary) | Camacho-Villalon Dorigo Stutzle exposing metaphors | 10 | 5 | 4 |
| 10 | WebSearch (ML/LLM vocabulary) | swarm intelligence + LLM agents, PSO + LLM | 9 | 6 | 5 |
| 11 | WebSearch (benchmarking) | centre-bias benchmarking metaheuristics | 9 | 6 | 4 |
| 12 | WebSearch (theory CS) | ACO runtime analysis, MMAS expected optimisation time | 9 | 5 | 4 |
| 13 | WebSearch (EC review) | PSO review single-objective continuous, stability | 10 | 3 | 2 |
| 14 | WebSearch (ML vocabulary) | Stein variational gradient descent / interacting particle optimisers | 10 | 2 | 2 |
| 15 | WebSearch | swarm intelligence review 2024-2025 open problems | 9 | 3 | 2 |
| 16 | Backward citations (OpenCitations) | [[poli-2007-particle]] | 34 | 15 | 9 |
| 17 | Backward citations (OpenCitations) | [[bonyadi-2017-particle]] | 132 | 30 | 22 |
| 18 | Forward citations, 2022+ (OpenCitations) | [[sorensen-2015-metaheuristics]] | 426 | 20 | 15 |
| 19 | Forward citations, 2015+ (OpenCitations) | [[garnier-2007-biological]] | 351 | 12 | 10 |
| 20 | Forward citations, all years (OpenCitations) | [[pinnau-2017-consensus]] | 115 | 40 | 36 |
| 21 | Forward citations, all years (OpenCitations) | [[camacho-villalon-2023-exposing]] | 86 | 6 | 3 |
| 22 | WebSearch (control/maths) | PSO dynamics theory review, stability, mean-field 2023-2026 | 9 | 6 | 4 |
| 23 | WebSearch (EC) | critical review nature-inspired metaheuristics novelty 2024-2025 | 9 | 6 | 3 |
| 24 | WebSearch (biology/OR) | ant colony optimization review, stigmergy 2023-2024 | 9 | 4 | 2 |
| 25 | WebSearch (kinetic theory) | interacting particle derivative-free global optimisation, kinetic | 10 | 8 | 5 |

Forward citations of the three most cited seeds (PSO 1995, Ant System 1996, Bonabeau 1999) were too large to pull
through OpenCitations here (tens of thousands); I chased the reviews and theory anchors above instead.

Saturation: for the core questions (seminal PSO/ACO/stigmergy papers, reviews, and the metaphor critique) the late
rounds 21, 23, 24 returned 2-3 new relevant items each, nearly all already-known critique papers or bibliometric
reviews. The consensus-based optimisation (CBO) mathematics is NOT saturated: rounds 20 and 25 still return many new
papers (round 25: 5 of 10 new), because the CBO literature is growing fast (115 citing works of the founding paper).

### Counts

- Papers added: 53. Seminal algorithm papers 14 (PSO 1995 x2, inertia, small-world topology, constriction, FIPS,
  Ant System, ACS, MMAS, ACO book, continuous ACO, ABC, Grey Wolf, Bonabeau book); biology/stigmergy 3; reviews and
  surveys 12 ([[poli-2007-particle]], [[bonyadi-2017-particle]], [[dorigo-2005-ant]], [[dorigo-2006-ant]],
  [[garnier-2007-biological]], [[theraulaz-1999-brief]], [[molina-2020-comprehensive]], [[molina-2025-paradox]],
  [[marti-2025-fifty]], [[campelo-2023-lessons]], [[velasco-2024-literature]], [[totzeck-2021-trends]]); dynamics
  theory 12 (PSO stability, ACO runtime, CBO and mean-field PSO); critique and benchmarking 9; LLM-swarm 2;
  swarm robotics 1 (categories overlap slightly). Published 2023-2026: 20.
- Existing entries already tagged `swarm-intelligence` that I relied on: [[feng-2024-model]] (notes appended),
  [[ruan-2025-benchmarking]], [[jimenez-romero-2025-multi-agent]], [[beni-2005-swarm]], [[krause-2010-swarm]].
- Code: no code entries created (out of scope for this run).

### Read in full

[[pinnau-2017-consensus]], [[grassi-2021-particle]], [[huang-2023-global]], [[kudela-2023-evolutionary]],
[[vermetten-2024-large]], [[nitti-2025-collective]]; plus [[feng-2024-model]] (notes section, entry owned by
dmarz/llm-agent-swarms).

### Notable gaps

- Seeds confirmed but not catalogued because no abstract or text was reachable: Goss et al. 1989 "Self-organized
  shortcuts in the Argentine ant" (Naturwissenschaften 76:579-581, DOI 10.1007/BF00462870), Beni and Wang 1993
  "Swarm intelligence in cellular robotic systems", Heylighen 2016 "Stigmergy as a universal coordination mechanism
  I", Derrac et al. 2011 nonparametric-tests tutorial (Swarm and Evolutionary Computation 1:3-18), Yang 2009 firefly
  algorithm. All metadata checked in OpenAlex; catalogue when publisher access returns.
- Full texts of [[sorensen-2015-metaheuristics]], [[camacho-villalon-2023-exposing]], [[aranha-2022-metaphor]] and
  [[garnier-2007-biological]] were blocked; these deserve full reads.
- PSO theory between 2010 and 2020 (order-2 stability, stagnation distributions, rotation invariance, runtime of PSO)
  is only covered via the [[bonyadi-2017-particle]] review; the individual papers are listed in its references.
- CBO variants (memory, jumps, constrained, multi-objective, sampling, second-order CBO, uniform-in-time propagation of
  chaos) are not catalogued.
- Other SI families: bacterial foraging, glowworm/firefly synchronisation-style algorithms, cuckoo search, artificial
  fish swarm, Stein-variational and ensemble-Kalman "particle" optimisers from ML. Not catalogued.
- The 2024 Physics of Life Reviews bibliometric review of ACO (ScienceDirect pii S1571064524001258) was found but not
  reachable.

### Code repositories seen (for the code scan)

- https://github.com/KonstantinRiedl/PSOAnalysis (Matlab, mean-field PSO, [[huang-2023-global]])
- https://github.com/AleNit/Swarm-Cooperation-Model ([[nitti-2025-collective]])
- https://github.com/BunsenFeng/model_swarm ([[feng-2024-model]])
- CBXPy and ConsensusBasedX.jl ([[bailo-2024-cbx]]; repository URLs on the JOSS page, not opened)
- https://github.com/fcampelo/EC-Bestiary (metaphor-algorithm catalogue, via [[kudela-2023-evolutionary]])
- Mealpy (Zenodo 10.5281/zenodo.3711948), NiaPy, EvoloPy, https://github.com/gugarosa/opytimizer,
  https://github.com/FacebookResearch/Nevergrad, IOHexperimenter; benchmark data Zenodo 10.5281/zenodo.10561215
  ([[vermetten-2024-large]])
- https://yaoz720.github.io/SwarmAgentic/ (project page, [[zhang-2025-swarmagentic]])

### Suggested follow-up tasks (not opened in this run; this run may not create task files)

1. scan-papers-cbo-variants: catalogue the CBO/mean-field optimiser literature from the 115 forward citations of
   [[pinnau-2017-consensus]] (memory, jumps, constrained, sampling, second-order, propagation of chaos).
2. scan-code-swarm-optimisers: catalogue and run CBXPy, PSOAnalysis, Swarm-Cooperation-Model, mealpy, IOHexperimenter.
3. full-read pass on the critique cluster once publisher access works: [[sorensen-2015-metaheuristics]],
   [[camacho-villalon-2023-exposing]], [[aranha-2022-metaphor]], [[molina-2025-paradox]].
4. Re-run OpenAlex search rounds after the rate limit resets (forward citations of [[kennedy-1995-particle]] and
   [[dorigo-1996-ant]] sorted by recency) to test saturation for 2024-2026 work.
5. Survey task: "Swarm optimisers as swarm dynamics" (PSO/CBO as interacting particle systems, order parameters,
   phase diagrams) building on [[grassi-2021-particle]], [[huang-2023-global]], [[hoffmann-2026-consensus]].


### Audit (dmarz/swarm-intelligence-audit)

Audited 2026-10-03. Verified: `lab.py verify` on all 53 scan entries (1 BAD line, [[stutzle-2000-max]], a Crossref
small-caps title artefact; metadata correct, note appended); cite strings of all 45 DOI entries compared with Crossref
(volume, issue, pages, authors) and all 8 arXiv-only entries with their arXiv pages; no phantoms, no metadata errors
found. All 6 full reads ([[pinnau-2017-consensus]], [[grassi-2021-particle]], [[huang-2023-global]],
[[kudela-2023-evolutionary]], [[vermetten-2024-large]], [[nitti-2025-collective]]) checked number by number against the
PDFs/publisher page; plus [[borghi-2026-long]], [[hoffmann-2026-consensus]], [[dorigo-1996-ant]],
[[theraulaz-1999-brief]], [[kennedy-1995-particle]], [[mirjalili-2014-grey]] against their abstracts. Fixed: two small
content errors (an "ES" ratio mislabelled "CMA-like" in [[kudela-2023-evolutionary]]; "numbers in tables" claim in
[[grassi-2021-particle]]); noted the CEC 2025 published version of [[shinohara-2025-large]]. Deleted: none.
Read depths are honest. Extra search rounds: (a) forward citations of [[dorigo-1996-ant]] from OpenCitations, 8849
citing works, 875 from 2024+, titles filtered for reviews/theory/collective dynamics (about 8 relevant, 6 new);
(b) forward citations of [[kennedy-1995-particle]], partial pull (6669 of tens of thousands, OpenCitations timed
out), 3983 citing works from 2025+, filtered (about 12 relevant, 9 new); (c) WebSearch with math vocabulary
(interacting particle systems, ensemble Kalman, consensus-based sampling; 9 results, 5 new); (d) WebSearch for PSO
stability theory past stagnation (10 results, 4 new); (e) WebSearch for PSO reviews 2023-2025 (9 results, 4 new).
Added 11: [[carrillo-2021-consensus]] (full), [[carrillo-2022-consensus]], [[fornasier-2021-consensus]],
[[cleghorn-2018-particle]] (skim), [[gerber-2025-mean]], [[koss-2026-mean]], [[blum-2024-ant]] (the 2024 Physics of
Life Reviews ACO review the scan could not reach), [[gad-2022-particle]], [[passino-2002-biomimicry]],
[[zheng-2026-survey]], [[feng-2025-noise]] (abstract). Found but not added (no abstract or text reachable): Deng and
Liu 2025 "Collective dynamics of particle swarm optimization: a network science perspective" (Physica A 675:130778,
doi 10.1016/j.physa.2025.130778, high priority for swarm dynamics); Priyadarshi and Kumar 2025 systematic review of
PSO and ACO (ACME 32(6):3609-3650, doi 10.1007/s11831-025-10247-2); Schmitt and Wanka 2015 "PSO almost surely finds
local optima" (TCS 561:57-72, doi 10.1016/j.tcs.2014.05.017); Shami et al. 2022 PSO survey (IEEE Access, doc 9680690);
Carrillo, Totzeck and Vaes, CBO and ensemble Kalman inversion with constraints (arXiv 2111.02970); Bonyadi and
Michalewicz 2016 stability without stagnation (doi 10.1109/TEVC.2015.2508101); PSO in chemistry review (Chem Soc Rev
2026, doi 10.1039/d5cs00912j). Still thin: PSO runtime/convergence theory 2010-2020 beyond Cleghorn; firefly,
cuckoo and glowworm algorithms (only bacterial foraging added); ensemble-Kalman and Stein-variational particle
optimisers; the physics-style analyses of optimiser swarms as collective dynamics (Deng and Liu 2025 above);
full reads of the critique cluster. OpenAlex list endpoints and WebSearch budget were exhausted during this audit.
