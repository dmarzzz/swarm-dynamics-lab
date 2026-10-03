---
id: scan-papers-collective-decision
type: task
title: 'Catalogue the papers: collective decision-making in biology'
kind: scan
status: claimed
priority: p0
owner: dmarz/collective-decision
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-decision
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `collective-decision`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Couzin et al. 2005, Effective leadership and decision-making in animal groups on the move (Nature)
- Couzin et al. 2011, Uninformed individuals promote democratic consensus in animal groups (Science)
- Seeley, Honeybee Democracy (2010 book) and Seeley et al. 2012 on stop signals in nest-site selection (Science)
- Sumpter, Collective Animal Behavior (2010 book)
- Berdahl et al. 2013, Emergent sensing of complex environments by mobile animal groups (Science)
- Pratt and colleagues on quorum sensing in Temnothorax ant emigrations

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

Scan by dmarz/collective-decision on 2026-10-03. All metadata copied from Crossref, OpenAlex (single-record lookups), Europe PMC, arXiv or publisher pages; `lab.py check` and `lab.py verify` (59 papers) both clean.

### Search rounds

"Relevant" counts items in the scanned results that fit the topic; "new" counts relevant items not already found in an earlier round.

| # | Where | Query or seed | Scanned | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex (title_and_abstract, by citations) | collective decision-making animal | 45 | 16 | 16 |
| 2 | OpenAlex | consensus decision-making animals | 40 | 8 | 4 |
| 3 | OpenAlex | quorum sensing ant emigration | 9 | 5 | 4 |
| 4 | OpenAlex | nest-site selection honeybee | 45 | 10 | 7 |
| 5 | Semantic Scholar, forward citations | Couzin et al. 2005 (2807 citing; top 60 by citations and top 40 since 2022 scanned) | 100 | 20 | 10 |
| 6 | Semantic Scholar, forward citations | Pratt et al. 2002 (450 citing) | 75 | 25 | 12 |
| 7 | Semantic Scholar, forward citations | Seeley et al. 2012 (359 citing) | 50 | 12 | 5 |
| 8 | Semantic Scholar search | collective decision-making animal groups | 45 | 20 | 8 |
| 9 | Crossref, backward references | Couzin 2005 (22 refs), Conradt and Roper 2005 (69), Chase and Peleg 2025 (153) | 244 | 30 | 6 |
| 10 | WebSearch (robotics) | best-of-n problem robot swarms collective decision | 10 | 6 | 4 |
| 11 | WebSearch (math biology) | value-sensitive decision-making cross-inhibition | 9 | 6 | 1 |
| 12 | WebSearch (control) | nonlinear opinion dynamics collective decision bifurcation | 10 | 6 | 3 |
| 13 | WebSearch (arXiv, recent) | arXiv 2024 2025 collective decision-making speed accuracy swarm | 10 | 8 | 5 |
| 14 | WebSearch (physics/biology, recent) | collective sensing animal groups fish 2023 2024 | 9 | 5 | 2 |
| 15 | WebSearch (ants, recent) | Temnothorax house-hunting collective decision 2022-2024 | 9 | 6 | 3 |
| 16 | Crossref bibliographic search | 9 title lookups to resolve DOIs of seeds and finds | 36 | 9 | 0 |
| 17 | WebSearch (reviews) | collective decision-making animal groups review 2025 | 10 | 5 | 2 |
| 18 | WebSearch (arXiv) | house-hunting quorum cross-inhibition model 2025 arXiv swarm | 9 | 8 | 5 |
| 19 | WebSearch | quorum response consensus fish shoal or ant colony 2023-2025 | 9 | 6 | 2 |
| 20 | WebSearch | collective decision speed-accuracy social insects 2024 2025 | 10 | 7 | 3 |
| 21 | WebSearch (physics/control) | informed uninformed consensus collective motion bifurcation | 9 | 8 | 4 |

The OpenAlex list endpoint hit its shared daily quota after round 4 (single-record lookups stayed free), so forward-citation chasing used Semantic Scholar and backward chasing used Crossref reference lists. Saturation is not reached by the gate's measure: the last two rounds found 3 of 10 and 4 of 9 new relevant items. The late finds are mostly incremental model papers and preprints rather than new lines of work.

### Counts

- 59 new paper entries created with topic `collective-decision`. 15 are reviews, books or opinion pieces: conradt-2005, couzin-2009, visscher-2007, franks-2002, bose-2017, sasaki-2018, feinerman-2017, leonard-2024, mccormick-2024, davis-2022, liao-2024, ioannou-2023, krause-2010, conradt-2003 (model essay) and the book seeley-2010. 44 are primary empirical or theory papers. 13 are from 2022 to 2025.
- 5 entries created by other agents already carried the topic; I appended `## Notes from dmarz/collective-decision` to [[valentini-2017-best]], [[couzin-2005-effective]], [[chase-2025-physics]], [[sumpter-2006-principles]] and [[sumpter-2010-collective]]. [[bizyaeva-2023-nonlinear]] (dmarz/sync-consensus) already lists the topic.
- Read depth of my entries: 6 full, 2 skim, 51 abstract.

### Full reads

[[sumpter-2009-quorum]], [[pais-2013-mechanism]], [[reina-2017-model]], [[sridhar-2021-geometry]], [[hein-2015-evolution]], [[gal-2022-emergence]], plus [[valentini-2017-best]] (another agent's entry; my notes are appended). Skimmed: [[valentini-2016-collective]], [[bose-2017-collective]].

### Gaps

- Four seed-level Behavioral Ecology and Sociobiology papers could not be opened, because Springer served a bot challenge and no open-access copy was found, so they are not catalogued: Pratt, Mallon, Sumpter & Franks 2002 (quorum sensing in Leptothorax, DOI 10.1007/s00265-002-0487-x, a task seed), Seeley & Visscher 2004 (quorum sensing in honeybee swarms, 10.1007/s00265-004-0814-5), Passino & Seeley 2006 (speed-accuracy model, 10.1007/s00265-005-0067-y) and Seeley & Buhrman 2001 (best-of-N in swarms, 10.1007/s002650000299). Their findings are summarised second-hand in [[sumpter-2009-quorum]] and [[valentini-2017-best]].
- No abstract was reachable for two reviews, which are therefore not catalogued: Leonard 2014, Annual Reviews in Control 38(2):171-183 (10.1016/j.arcontrol.2014.09.002), and List 2004, TREE 19(4):168-169 (10.1016/j.tree.2004.02.004).
- Several key papers are catalogued from the abstract only because the full text was paywalled or blocked: [[couzin-2005-effective]], [[couzin-2011-uninformed]], [[seeley-2012-stop]], [[berdahl-2013-emergent]], [[leonard-2012-decision]] (the PMC page sat behind a bot check), [[marshall-2009-optimal]] and [[strandburg-peshkin-2015-shared]].
- Forward citations of Couzin et al. 2011 were not chased: Semantic Scholar returned 404 for the DOI and then rate-limited.
- Seen but not opened: arXiv 2606.11259 (2026, stabilising role of uninformed participants), arXiv 2206.00587 (geometry-sensitive quorum sensing), arXiv 2403.14856 (quality-sensitive interdependent agents), Myrmecina nipponica pheromone-plus-quorum papers (Animal Behaviour 2012; BES 2013), Kameda et al. 2022 (Nature Reviews Psychology, human information aggregation), Nabet et al. 2009 (J. Nonlinear Sci.), the Conradt and List 2009 theme-issue introduction, and microbial collective decisions (Frontiers in Microbiology 2014).
- The Leonard, Franci and Bizyaeva control line is covered by reviews and two papers only. Primate leadership (Sueur, King and others) and human crowd decisions are thin.

### Code and data seen (for the code scan)

- https://github.com/vivekhsridhar/GODM: data and code for [[sridhar-2021-geometry]]; data also on Zenodo, https://doi.org/10.5281/zenodo.5599711
- https://doi.org/10.5281/zenodo.6569620: behavioural data, simulation code and analysis scripts for [[gal-2022-emergence]]
- Matlab stochastic simulation code is in the journal supplementary file S1 of [[pais-2013-mechanism]], https://doi.org/10.1371/journal.pone.0073216.s007. It is not a repository.
- anTraX, the colour-tag ant tracking software used by [[gal-2022-emergence]] (its ref. 42). I did not check the repository URL.

### Suggested follow-up tasks (not opened; I was told not to run git)

1. Full reads, from user-supplied PDFs, of the paywalled core papers: Couzin 2005 and 2011, Seeley 2012, Berdahl 2013, Leonard 2012. Then catalogue the four Springer BES classics listed above.
2. Code scan: catalogue GODM and the two Zenodo deposits as code or dataset entries and link them in `code:`.
3. Saturation pass with forward citations of [[couzin-2011-uninformed]] and [[pais-2013-mechanism]], sorted by recency, once the OpenAlex quota resets.
4. A small scan of human and LLM-agent analogues (wisdom of crowds, information cascades, zealots) to connect with `llm-agent-swarms`; seeds are [[reina-2023-cross]], [[mccormick-2024-information]] and [[soma-2024-hive]].
5. Survey task for `collective-decision`. Candidate seminal works whose forward citations were followed: [[couzin-2005-effective]], [[seeley-2012-stop]] and Pratt 2002 (the last is not catalogued; use [[sumpter-2009-quorum]] in its place).

### Audit (dmarz/collective-decision-audit)

Audit on 2026-10-03. `lab.py verify` on the 59 scan entries reported 0 problems. I also checked every scan entry's DOI against Crossref for authors, year, volume and pages. All matched apart from a book-versus-e-book year note on [[seeley-2010-honeybee]]. The 2 arXiv-only entries match DataCite. Spot checks against the source: all 6 full reads ([[sumpter-2009-quorum]], [[pais-2013-mechanism]], [[reina-2017-model]], [[sridhar-2021-geometry]], [[hein-2015-evolution]], [[gal-2022-emergence]]), checked number by number against the full text. Also checked: the skim [[valentini-2016-collective]] (author PDF) and the abstract entries [[couzin-2011-uninformed]], [[leonard-2024-fast]], [[soma-2024-hive]] and [[zakir-2025-bio]]. Fixed: one wrong claim in [[valentini-2016-collective]]. The majority rule's 1.89x speed-up is at equal accuracy, and the voter model is more accurate only when the initial opinion share is below 50 per cent. The entry had said the majority rule was less accurate except at rho_b = 0.9. Also fixed: a Condorcet bullet in [[sumpter-2009-quorum]] that claimed an n = 100 result the paper does not state. Nothing deleted; no phantoms. The full-depth claims hold.

Searches I added: forward citations of Couzin 2005 since 2023 from Semantic Scholar (449 citing papers; the top 70 by citations scanned, 9 relevant, 6 new). Forward citations of Couzin 2011 failed again (Semantic Scholar 404; OpenAlex list quota spent). WebSearch with vocabulary from neighbouring fields: primate shared and unshared consensus (9 results, 3 relevant, 2 new); human wisdom of crowds and social influence (9, 4, 3); recent reviews 2024-2025 (9, 5, 3); Crossref title resolution of 9 candidates. Added 11 entries: [[lorenz-2011-how]], [[becker-2017-network]], [[wolf-2013-accurate]], [[sueur-2012-from]], [[kao-2024-timing]], [[papageorgiou-2024-compromise]], [[dreyer-2025-comparing]], [[carlesso-2023-simple]], [[tump-2024-cognitive]], [[bate-2026-indecision]] and [[colombo-2026-stabilizing]]. The last two are the arXiv preprints listed above as seen but not opened.

Still thin: the four Springer BES classics (Pratt et al. 2002, Seeley & Visscher 2004, Passino & Seeley 2006, Seeley & Buhrman 2001). Neither Springer, Semantic Scholar nor Unpaywall-linked sources serve an abstract to this machine. Also thin: forward citations of [[couzin-2011-uninformed]], and primate leadership beyond Sueur (King & Sueur 2011, Int. J. Primatol., not opened). Also not added: Kameda et al. 2022 and the human collective-intelligence line (Woolley 2010, Kurvers 2015 medical diagnosis). Microbial decisions and the arXiv 2206.00587 and 2403.14856 preprints remain unopened.
