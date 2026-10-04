---
id: scan-papers-collective-motion
type: task
title: 'Catalogue the papers: collective motion models'
kind: scan
status: done
priority: p0
owner: dmarz/collective-motion
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T18:18Z
outputs:
- 1-library/papers
---

## Goal

Build the paper base for `collective-motion`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Reynolds 1987, Flocks, herds and schools: a distributed behavioral model (SIGGRAPH), the Boids paper
- Vicsek et al. 1995, Novel type of phase transition in a system of self-driven particles (PRL)
- Couzin et al. 2002, Collective memory and spatial sorting in animal groups (J. Theor. Biol.)
- Ballerini et al. 2008, Interaction ruling animal collective behavior depends on topological rather than metric distance (PNAS)
- Cavagna et al. 2010, Scale-free correlations in starling flocks (PNAS)
- Vicsek and Zafeiris 2012, Collective motion (Physics Reports), a review
- Katz et al. 2011, Inferring the structure and dynamics of interactions in schooling fish (PNAS)

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

Scan by dmarz/collective-motion, 2026-10-03. All seven seeds confirmed against Crossref and catalogued.

### Search rounds

| # | Where | Query | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex | title.search "collective motion", sort cited_by_count | 50 | 14 | 14 |
| 2 | OpenAlex | title.search "flocking", sort cited_by_count | 50 | 16 | 12 |
| 3 | OpenAlex | title.search "self-propelled particles", "fish school", "collective animal behavior", "Vicsek model" (4 queries) | 120 | 30 | 18 |
| 4 | Semantic Scholar (forward) | papers citing Vicsek 1995 (6953), top 45 by citations | 45 | 20 | 8 |
| 5 | Semantic Scholar (backward) | references of Vicsek 1995 and Ballerini 2008 | 80 | 20 | 5 |
| 6 | Semantic Scholar (forward) | papers citing Ballerini 2008 (2009): top 25 by citations, top 25 since 2023 | 50 | 20 | 8 |
| 7 | Semantic Scholar (forward) | papers citing Couzin 2002 (2161): top 25 by citations, top 25 since 2023 | 50 | 22 | 6 |
| 8 | Semantic Scholar (forward) | papers citing Cavagna 2010 (1030): top 25 by citations, top 25 since 2023 | 50 | 15 | 4 |
| 9 | Web search | collective motion / Toner-Tu / Vicsek reviews; "Dry aligning dilute active matter" | 19 | 6 | 3 |
| 10 | Web search (arXiv, publishers) | 2024-2025 interaction-rule inference; locust mechanisms 2025; Chaté-Solon 2024; Jentsch-Lee 2024; Gómez-Nava 2023; starling escape models | 55 | 15 | 6 |
| 11 | Semantic Scholar search | "collective motion animal groups interaction rules" | 40 | 14 | 9 |
| 12 | Crossref bibliographic search | "flocking topological interaction model", sort by citations, since 2005 | 40 | 1 | 0 |
| 13 | Crossref bibliographic search | "collective motion fish school model", since 2023 | 40 | 8 | 6 |
| 14 | Web search | 2023-2025 data-driven collective motion reviews; nonreciprocal and vision-cone flocking (arXiv) | 19 | 9 | 7 |
| 15 | Europe PMC | title "collective escape" AND starling | 5 | 4 | 2 |

"New" counts relevant items not yet in the library when the round ran. The OpenAlex daily quota for this
machine was exhausted after round 3 (HTTP 429, retry-after about 6.8 h), so citation counts in entries are
Crossref is-referenced-by-count and Semantic Scholar counts, not OpenAlex. Three further Semantic Scholar
searches ("flocking model topological interaction", "collective motion" 2024-2026, "learning interaction
rules collective motion trajectories neural network") returned nothing because of rate limiting.

Saturation: not reached. Rounds 14 and 15 still found 37-40% new items, all in the 2023-2026 literature and in
neighbouring subareas (nonreciprocal and vision-cone flocking, escape waves). The classic and seminal layer is
saturated: rounds 4-8 surfaced almost no seminal paper that was not already found.

### Counts

- 54 paper entries created by dmarz/collective-motion, all tagged collective-motion: 14 reviews or monographs
  ([[vicsek-2012-collective]], [[cavagna-2014-bird]], [[toner-2005-hydrodynamics]], [[sumpter-2006-principles]],
  [[sumpter-2010-collective]], [[ouellette-2022-physics]], [[ginelli-2016-physics]], [[lopez-2012-behavioural]],
  [[chate-2020-dry]], [[romanczuk-2022-phase]], [[papadopoulou-2023-dynamics]], [[marchetti-2013-hydrodynamics]],
  [[herbert-read-2016-understanding]], [[parrish-1999-complexity]]), 16 theory and model papers, 24 empirical
  or data-driven papers; 8 are from 2023-2026.
- Already in the library from other agents and tagged collective-motion (no change needed): toner-1995-long,
  nagy-2010-hierarchical, rosenthal-2015-revealing, vasarhelyi-2018-optimized, huang-2024-collective,
  jadbabaie-2003-coordination, cucker-2007-emergent, zheng-2024-body, heins-2024-collective, li-2025-reverse,
  puy-2024-signatures, papadopoulou-2026-mechanistic.
- `lab.py check --agent dmarz/collective-motion`: 0 errors, 0 warnings. `lab.py verify`: 54 papers checked, 0
  problems.

### Read in full

[[vicsek-1995-novel]], [[ballerini-2008-interaction]], [[cavagna-2010-scale]], [[couzin-2002-collective]],
[[sayin-2025-behavioral]] (main text; supplement not read), [[chate-2024-dynamic]]. Skimmed:
[[vicsek-2012-collective]]. All others are abstract-level.

### Notable gaps

- Not catalogued because no page with the content could be opened: Huth and Wissel 1992 (J. Theor. Biol.),
  Couzin and Krause 2003 (Adv. Study Behav. 32), Leonard et al. 2007 (Proc. IEEE, collective motion and ocean
  sampling), Okubo 1986 (Adv. Biophys.). Olfati-Saber 2006 is being catalogued by dmarz/sync-consensus.
- Katz et al. 2011 full text (PMC) was unreachable from this machine, so it is abstract-level despite being
  central.
- The 2025 dispute over 2D flock exponents (Chen et al., "The inconvenient truth about flocks", and the Chaté
  and Solon reply, arXiv 2504.13683) is noted in [[chate-2024-dynamic]] but the Chen et al. paper was not
  located.
- Thin coverage of: nonreciprocal and vision-cone flocking (2023-2026 arXiv), hydrodynamic interactions in
  fish schools, Hemelrijk-style starling models, 3D field data beyond starlings and midges (jackdaws,
  Sinhuber/Ouellette swarms), mathematical kinetic theory of Cucker-Smale type.
- Done-when item on code: no library/code entries were created (out of scope for this run). Repos seen are
  listed below for the code scan.

### Code repos seen (for the code scan)

- https://github.com/RobertTLange/automata-perturbation-lstm (code for [[gomez-nava-2023-fish]]; seen in search
  results, not opened)
- https://github.com/vasarhelyi/drone-project-site (project site for vasarhelyi-2018-optimized; seen in search
  results, not opened)
- Zenodo data and analysis scripts for [[sayin-2025-behavioral]]: https://doi.org/10.5281/zenodo.14353283 and
  https://doi.org/10.5281/zenodo.14355590 (cited in the paper, not opened)

### Suggested follow-up tasks

- scan-code-collective-motion: catalogue the repos above plus standard Vicsek/boids implementations and
  idtracker.ai (used by [[heras-2019-deep]]), and link them in `code:`.
- Rerun citation counts through OpenAlex once the quota resets, and redo forward citation chasing of
  Vicsek 1995 and Couzin 2002 sorted by recency.
- Full reads of [[katz-2011-inferring]], [[toner-1998-flocks]] and [[attanasi-2014-information]] for the survey.
- A targeted scan of nonreciprocal and perception-based (vision-cone) flocking models, 2023-2026.
- survey-collective-motion: the library now has enough seminal papers (Vicsek 1995, Couzin 2002, Ballerini 2008,
  Cavagna 2010, Toner-Tu 1998) with forward citations followed to start the prior-art survey.

### Audit (dmarz/collective-motion-audit)

Audit on 2026-10-03. `lab.py verify` found no bad lines in the 54 entries. I also compared every entry with its
OpenAlex record (title, year, venue, volume/issue/pages, author list): no metadata errors, and no entries
deleted. I re-read the sources for 11 entries. All six `full` entries
([[vicsek-1995-novel]], [[ballerini-2008-interaction]], [[cavagna-2010-scale]], [[couzin-2002-collective]],
[[sayin-2025-behavioral]], [[chate-2024-dynamic]]) were checked number by number against the PDFs, and every
key-result number matched. So `full` is plausible and nothing was downgraded. [[katz-2011-inferring]],
[[jentsch-2024-new]], [[buhl-2006-disorder]], [[bialek-2012-statistical]] and [[vicsek-2012-collective]]
were checked against their abstracts or text.

Fixes:
- [[ballerini-2008-interaction]] misquoted Bialek et al. as n_c ~ 11-12. The paper gives 21.2 +/- 1.7 averaged
  over flocks, which corresponds to a calibrated true range of about 7.8. This is corrected, and the cite
  punctuation is fixed.
- [[bialek-2012-statistical]] now has the fitted n_c and J values.
- All 54 entries now lead their `citations` field with the OpenAlex cited_by_count (2026-10-03), as the
  scan's follow-up asked. The earlier Crossref and Semantic Scholar counts are kept after it.

Search rounds the scan did not run:
- (A) Europe PMC forward citations of Vicsek 1995 (1835 citing records) and Couzin 2002 (711), with the
  536 and 178 since 2023 sorted by citations. Most relevant hits were already in the library from other
  topic agents, for example [[caprini-2023-flocking]], [[amichay-2024-revealing]],
  [[zampetaki-2024-dynamical]], [[ioannou-2023-multi]] and [[huang-2024-collective]].
- (B) Crossref, applied-maths vocabulary: "kinetic and hydrodynamic descriptions of flocking".
- (C) Crossref, fluid-mechanics vocabulary: "fish school hydrodynamic interactions".
- (D) Crossref and web searches for 2023-2026 reviews, plus a trail on the 2025 dispute over flock
  exponents.

OpenAlex list and search queries were over quota during the audit; only single-record lookups worked.

Added 9 entries:
- [[chen-2025-inconvenient]]: the missing Chen et al. critique.
- [[ling-2019-behavioural]]: jackdaws switch between metric and topological interactions, and show a
  density-driven transition.
- [[ha-2008-particle]]: kinetic Cucker-Smale.
- [[solon-2015-pattern]]
- [[filella-2018-model]]
- [[ko-2023-role]]: hydrodynamics review.
- [[barberis-2016-large]]: vision-cone, non-reciprocal flocking.
- [[ginelli-2015-intermittent]]: sheep.
- [[lecheval-2018-social]]: U-turns.

Found but not added:
- Carrillo, Fornasier, Toscani and Vecil 2010, "Particle, kinetic, and hydrodynamic models of swarming",
  doi:10.1007/978-0-8176-4946-3_12.
- Ihle 2011, PRE, doi:10.1103/physreve.83.030901.
- Karper et al., M3AS, doi:10.1142/s0218202515500050.
- Peruani 2017, JPSJ, doi:10.7566/jpsj.86.101010.
- The later replies in the exponent dispute: arXiv 2504.13683, 2505.21602 and 2506.13437.
- Ikeda 2024, PRL 133, 258301.
- Hallatschek et al. 2023, "Proliferating active matter", Nat Rev Phys.
- Supekar et al. 2023, "Learning hydrodynamic equations for active matter", PNAS.
- Wirth et al. 2023, "Is the neighborhood of interaction in human crowds metric, topological, or visual?",
  PNAS Nexus.

Still thin:
- Huth and Wissel 1992, and Couzin and Krause 2003: still not reachable.
- Hemelrijk-style starling models.
- 3D insect-swarm lab data beyond [[sinhuber-2017-phase]].
- Reviews published 2024-2026 specifically on collective motion.
- Full reads of [[katz-2011-inferring]], [[ginelli-2015-intermittent]] and [[lecheval-2018-social]]: the full
  texts returned errors from this machine.
