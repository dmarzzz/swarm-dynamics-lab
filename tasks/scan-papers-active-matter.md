---
id: scan-papers-active-matter
type: task
title: 'Catalogue the papers: active matter physics'
kind: scan
status: claimed
priority: p1
owner: dmarz/active-matter
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- active-matter
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `active-matter`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Marchetti et al. 2013, Hydrodynamics of soft active matter (Rev. Mod. Phys.)
- Toner and Tu 1995, Long-range order in a two-dimensional dynamical XY model (PRL)
- Cates and Tailleur 2015, Motility-induced phase separation (Annu. Rev. Condens. Matter Phys.)
- Bechinger et al. 2016, Active particles in complex and crowded environments (Rev. Mod. Phys.)

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

Scan by dmarz/active-matter on 2026-10-03. OpenAlex hit its daily credit limit for this IP after four queries
(HTTP 429, retry-after about 7 hours), so citation chasing used the Semantic Scholar Graph API (single calls with
back-off), Crossref for metadata and relevance search, DataCite for arXiv metadata, and WebSearch for discovery.
Citation counts are OpenAlex where captured before the limit, otherwise Semantic Scholar, each labelled with source
and date.

### Search rounds

"Relevant" = on-topic for active matter / swarm dynamics; "new" = not already in the library at the time.

| # | Where | Query or seed | Results inspected | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex search (sorted by citations) | "active matter review" | 50 | 0 | 0 |
| 2 | OpenAlex title.search | "active matter" | 50 | 25 | 25 |
| 3 | OpenAlex title.search | "motility-induced phase separation" | 25 | 22 | 18 |
| 4 | OpenAlex title.search | "self-propelled particles" (then 429 on "active nematic", "active Brownian particles", "active particles") | 25 | 22 | 18 |
| 5 | Semantic Scholar, forward citations by count | Toner & Tu 1995 (1004 citers) | 50 | 35 | 22 |
| 6 | Semantic Scholar, forward citations by count | Marchetti et al. 2013 RMP (3394 citers) | 60 | 40 | 25 |
| 7 | Semantic Scholar, forward citations 2023+ | Marchetti et al. 2013 RMP | 60 | 30 | 25 |
| 8 | Semantic Scholar, forward citations by count and 2023+ | Cates & Tailleur 2015 (1568 citers) | 90 | 55 | 22 |
| 9 | Semantic Scholar, forward citations 2023+ | Toner & Tu 1995 | 45 | 25 | 12 |
| 10 | Semantic Scholar, backward references | Bechinger et al. 2016 (469 refs) | 30 | 12 | 3 |
| 11 | Semantic Scholar, backward references | Cates & Tailleur 2015 (119 refs) | 40 | 15 | 4 |
| 12 | WebSearch | robotic active matter reviews 2024-2025 | 10 | 7 | 5 |
| 13 | Semantic Scholar search, 2022-2026 | "active matter swarm robots collective" | 30 | 18 | 9 |
| 14 | Crossref relevance search | "motility-induced phase separation active Brownian particles" | 25 | 20 | 17 |
| 15 | Crossref relevance search | "flocking active matter Vicsek hydrodynamics" | 25 | 18 | 16 |
| 16 | WebSearch | active matter review 2025 swarm collective motion | 9 | 6 | 1 |
| 17 | WebSearch | active matter robots flocking phase transition 2024-2025 | 10 | 8 | 3 |

Saturation: rounds 16 and 17 gave 1/9 (11%) and 3/10 (30%) new. Reviews and seminal papers are saturated (later rounds
only returned already-catalogued reviews). The long tail is not: Crossref rounds 14-15 still returned many uncatalogued
specialised follow-ups on MIPS and Vicsek variants. Those are mostly incremental; the highest-cited were added.

### Counts

- 62 new paper entries by dmarz/active-matter (all type paper), tagged active-matter. By year: 1995-2010: 9;
  2011-2019: 23; 2020-2022: 10; 2023-2026: 20.
- Roughly 20 are reviews, roadmaps or lecture notes. 167 library papers now carry the active-matter topic, counting
  entries added by other topic agents.
- Notes under "## Notes from dmarz/active-matter" appended to three existing entries after full reads:
  fruchart-2021-non, das-2024-flocking, mahault-2019-quantitative.
- Several seeds and seminal papers had already been created by other agents and were left to them, with active-matter
  already tagged: marchetti-2013-hydrodynamics, toner-1998-flocks, gregoire-2004-onset, chate-2008-collective,
  bricard-2013-emergence, chate-2020-dry, gompper-2025-motile, janzen-2026-active, lavergne-2019-group,
  scholz-2018-rotating, deblais-2018-boundaries, baconnier-2022-selective, chate-2024-dynamic, gu-2025-emergence.
- `lab.py check --agent dmarz/active-matter`: 0 errors, 0 warnings. `lab.py verify`: 62 checked, 1 flagged. The flag is
  toner-1995-long, a false positive: Crossref's title for 10.1103/PhysRevLett.75.4326 embeds MathML markup around "XY",
  and the arXiv version reverses the title order, so neither source matches above 0.85. The DOI and title were checked by
  hand against Crossref.

### Read in full (read_depth: full)

cates-2015-motility, toner-1995-long, fily-2012-athermal, shaebani-2020-computational, chate-2019-dry (the Chaté and
Mahault lecture notes, arXiv:1906.05542), buttinoni-2013-dynamical. The full-read notes on fruchart-2021-non,
das-2024-flocking and mahault-2019-quantitative add three more full reads, but those entries belong to other agents.

### Gaps

- OpenAlex citation chasing was not possible after the first four queries. A rerun once the limit resets should redo
  forward citations sorted by count for Vicsek 1995 and Bechinger 2016, and backward references for Marchetti 2013
  (that Semantic Scholar call returned empty).
- Not catalogued because no page could be opened (publisher 403 and no arXiv or PubMed record found): Toner, Tu &
  Ramaswamy 2005 "Hydrodynamics and phases of flocks" (Ann. Phys.), and the Science Robotics 2024 perspective "Robot
  swarms meet soft matter physics" (10.1126/scirobotics.adn6035), whose record has only a one-line abstract.
- Under-covered subareas: 3D flocks and active matter in 3D; inertial and underdamped active matter (only luo-2025-flocking
  and omar-2021-phase); active solids and odd elasticity beyond veenstra-2025-adaptive and bo-2026-three; active
  glasses and jamming; chemotactic and quorum-sensing MIPS theory (2023+); active nematic defects in cell tissues;
  non-reciprocal field theories seen in citation lists but not catalogued, e.g. "Nonreciprocal Pattern Formation of
  Conserved Fields" (PRX 2024) and "Non-reciprocity across scales in active mixtures" (Nat. Commun. 2023); the Martin et al. 2023 coarse-graining of non-reciprocal flocking (arXiv:2307.08251), opened
  but not catalogued.
- The highest-relevance entries are only read at abstract depth: baconnier-2025-self, veenstra-2025-adaptive,
  ziepke-2025-acoustic, aina-2022-toward, ning-2024-macroscopic. They should be read in full before a survey cites them
  as load-bearing.

### Code repositories seen (for the code scan)

- https://github.com/swarmtronics/ampy (AMPy, Python/OpenCV swarm-kinematics package; dmitriev-2025-swarmodroid)
- https://github.com/swarmtronics/swarmodroid.firmware and https://github.com/swarmtronics/swarmodroid.pcb (open bristle-bot hardware)
- Dedalus spectral PDE solver (used by fruchart-2021-non for the non-reciprocal flocking PDEs). Named in the paper; URL not opened.
- das-2024-flocking says "Data and code are available on this link", but the link did not survive PDF text extraction. Check the arXiv HTML version.

### Suggested follow-up tasks (not created; this run may only write the files it was given)

1. Full reads of baconnier-2025-self, veenstra-2025-adaptive, ning-2024-macroscopic and ziepke-2025-acoustic. They are
   the strongest bridges from active matter to robot swarms.
2. Rerun OpenAlex forward and backward chasing once the rate limit resets (see Gaps).
3. A survey task, "Which active-matter mechanisms produce flocking or clustering in robot swarms without explicit
   communication?" Seeds: fily-2012-athermal, cates-2015-motility, das-2024-flocking, caprini-2023-flocking,
   baconnier-2025-self, deseigne-2010-collective, kumar-2014-flocking, luo-2025-flocking, giraldobarreto-2025-active.
4. A code scan of the swarmtronics repositories and of public Vicsek/ABP simulators. Give priority to GPU-ready
   aarch64-compatible ones.
5. A non-reciprocal active matter scan covering the field-theory papers listed in Gaps.
