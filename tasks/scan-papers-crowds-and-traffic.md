---
id: scan-papers-crowds-and-traffic
type: task
title: 'Catalogue the papers: human crowds and traffic'
kind: scan
status: done
priority: p1
owner: dmarz/crowds-and-traffic
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- crowds-and-traffic
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T18:18Z
outputs:
- library/papers
---

## Goal

Build the paper base for `crowds-and-traffic`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Helbing and Molnár 1995, Social force model for pedestrian dynamics (PRE)
- Helbing, Farkas and Vicsek 2000, Simulating dynamical features of escape panic (Nature)
- Moussaïd, Helbing and Theraulaz 2011, How simple rules determine pedestrian behavior and crowd disasters (PNAS)
- Sugiyama et al. 2008, Traffic jams without bottlenecks (New J. Phys.)

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

Written by dmarz/crowds-and-traffic on 2026-10-03.

**Counts.** 49 papers catalogued in `library/papers/` with `crowds-and-traffic` (all new entries by this agent), plus the topic added to one existing entry (`fabregas-2026-mathematical`). Read depth: 7 full, 9 skim, 33 abstract. 18 of the 49 are from 2023–2026. Reviews included: [[helbing-2001-traffic]], [[chowdhury-2000-statistical]], [[corbetta-2023-physics]], [[chatagnon-2025-exploring]], [[warren-2018-collective]], [[haghani-2024-revisiting]] (critical/bibliometric). `lab.py check` and `lab.py verify --agent dmarz/crowds-and-traffic` both pass (49 papers checked, 0 problems).

**Full reads (read_depth: full).** [[sugiyama-2008-traffic]], [[helbing-1995-social]], [[helbing-2000-simulating]], [[moussaid-2011-simple]], [[stern-2018-dissipation]], [[karamouzas-2014-universal]], [[gu-2025-emergence]].

**Search log.** OpenAlex was used for rounds 1–3; after that the shared-IP free daily budget was exhausted (HTTP 429, "Insufficient budget", resets at midnight UTC), so forward chasing used OpenCitations (api.opencitations.net/index/v2/citations) with Crossref metadata, and backward chasing used Crossref reference lists. Citation counts in entries are OpenAlex where captured before the budget ran out, otherwise Crossref `is-referenced-by-count`, labelled in each entry.

| # | Where | Query / seed | Results inspected | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex search (sorted by citations) | "pedestrian dynamics crowd" | 50 | 12 | 12 |
| 2 | OpenAlex title.search | "pedestrian dynamics"; "crowd dynamics"; "traffic flow"; "evacuation dynamics" | 200 | 40 | 30 |
| 3 | OpenAlex title.search | "traffic jams"; "jamming transition traffic"; "phantom jam"; "crowd turbulence"; "lane formation pedestrian"; "faster is slower"; "clogging bottleneck" | 150 | 30 | 15 |
| 4 | Forward citations (OpenCitations + Crossref) | Sugiyama 2008 (614 citing): top 30 by citations + 40 most recent (2023+) | 70 | 20 | 12 |
| 5 | Forward citations | Helbing & Molnár 1995, Helbing et al. 2000, Moussaïd et al. 2011: top 60 each, merged | 100 | 45 | 20 |
| 6 | Forward citations, recency | Moussaïd et al. 2011, citing works 2023+ (241) | 60 | 25 | 14 |
| 7 | Forward citations | Bain & Bartolo 2019 (148), Corbetta & Toschi 2023 (59), Stern et al. 2018 citing works 2023+ | 105 | 35 | 16 |
| 8 | WebSearch (arXiv) | arXiv 2025 pedestrian crowd dynamics active matter | 9 | 8 | 6 |
| 9 | WebSearch (arXiv, ML/control) | MARL mixed-autonomy traffic, stop-and-go wave dissipation, field deployment | 9 | 6 | 3 |
| 10 | WebSearch (psychology) | Warren human crowd collective motion, visual coupling | 9 | 5 | 2 |
| 11 | Backward citations (Crossref references) | Corbetta & Toschi 2023 (96 refs with DOI), Gu et al. 2025 (34), Stern et al. 2018 (36) | 166 | 70 | 10 |
| 12 | Crossref query.bibliographic (from 2005) | "ant traffic rules jamming collective"; "string stability adaptive cruise control experiment"; "robot navigation dense human crowds"; "human swarm collective motion virtual reality"; "pedestrian crowd active matter hydrodynamics"; "stop-and-go waves trajectory data freeway" | 90 | 15 | 6 |

Rounds 11 and 12 found 10/166 (6%) and 6/90 (7%) new items, below the 15% saturation threshold. Vocabulary covered: physics (self-driven particles, jamming transition, active matter, odd/non-reciprocal), traffic engineering and control (car-following, string stability, Lagrangian control, mixed autonomy), robotics (reciprocal collision avoidance, crowd navigation), ML (trajectory prediction, neural simulators, RL), psychology (visual coupling, anticipation), biology (ant traffic, sheep clogging).

**Notable gaps (found but not catalogued, because no page could be opened in this session: publisher pages returned 403 or bot checks, no open copy found).** Bando et al. 1995 optimal velocity model (PRE 51, 1035); Nagel & Schreckenberg 1992 (J. Phys. I 2, 2221; the HAL copy hal.science/jpa-00246697 is behind a bot check); Lighthill & Whitham 1955 kinematic waves; Nagatani 2002 "The physics of traffic jams" (Rep. Prog. Phys.); Hughes 2002 continuum theory and Hughes 2003 Annu. Rev. Fluid Mech.; Helbing et al. 2005 Transp. Sci.; Bellomo & Dogbe 2011 SIAM Review; Duives et al. 2013 and Haghani & Sarvi 2018 reviews; Haghani et al. 2020 Safety Science parts I and II; Kerner three-phase theory; Johansson et al. 2007 social force calibration; Seyfried et al. 2009 bottlenecks; Pastor et al. 2015 and Garcimartín et al. 2016 faster-is-slower experiments; Zanlungo et al. 2011; Trautman & Krause 2010 robot navigation; Fourcassié et al. 2010 ant traffic rules; Laval & Leclercq 2010 stop-and-go mechanism; Korbmacher & Tordeux 2022 trajectory prediction review; Social GAN, Trajectron++ and later ML predictors; Warren lab visual-coupling model. Most should be catalogued in a second pass once the OpenAlex budget resets or from a different network.

**Code and data URLs seen (for the code/dataset scan).** https://github.com/flow-project/flow ([[wu-2022-flow]]; MIT, 1191 stars, last push 2024-07-27, per GitHub API); https://github.com/snape/RVO2 (ORCA, [[van-den-berg-2011-reciprocal]]; Apache-2.0, 971 stars); http://motion.cs.umn.edu/PowerLaw ([[karamouzas-2014-universal]], stated in paper, not opened); https://uofi.box.com/v/trajectoryPaperData and dataset DOI 10.15695/vudata.cee.1 ([[stern-2018-dissipation]]); https://doi.org/10.5281/zenodo.14050598 ([[gu-2025-emergence]] data and simulation code); https://zenodo.org/records/14737521 ([[ma-2025-unraveling]] data); https://doi.org/10.5281/zenodo.7523480 ([[feliciani-2023-trends]] crowd accident database); i24motion.org/data ([[gloudemans-2023-i24]]); https://doi.org/10.5281/zenodo.10696534 (trackpy, used by Gu et al.). Per this run's instructions no code entries were created.

**Suggested follow-up tasks (not opened by this agent; the coordinator can create them).**
1. Second-pass paper scan for the gaps above (classic traffic models and the paywalled reviews).
2. Code scan: Flow, RVO2/ORCA, open pedestrian simulators (JuPedSim, Vadere, PedSim), Gu et al. Zenodo simulation code.
3. Dataset scan: I-24 MOTION, Stern ring-road trajectories, Gunter et al. ACC dataset, Chupinazo crowd data, Jülich pedestrian data archive, Feliciani crowd-accident database.
4. Sub-scan on robot navigation in human crowds (Trautman, CrowdNav-style RL) and on biological traffic (ants, sheep), which this scan touched only lightly.
5. Survey task for `crowds-and-traffic`, with full reads of [[bain-2019-dynamic]], [[bacik-2025-order]] and [[corbetta-2023-physics]] as priorities.

**Audit (dmarz/crowds-and-traffic-audit), 2026-10-03.** `lab.py verify --agent dmarz/crowds-and-traffic` returned 49 checked, 0 problems. I also cross-checked every entry's author list and year against Crossref/DataCite with a script; all matched except one. I spot-checked 13 entries against the source: all 7 `read_depth: full` entries (sugiyama-2008-traffic from the Osaka repository PDF, helbing-1995-social, helbing-2000-simulating, moussaid-2011-simple, stern-2018-dissipation and karamouzas-2014-universal from arXiv PDFs, gu-2025-emergence from the Nature page), plus bacik-2025-order (from PMC full text, including the γ_crit ≈ 13° claim), raulin-foissac-2026-physics, chatagnon-2026-when, wang-2026-avalanches, chowdhury-2000-statistical and chatagnon-2025-exploring. Every number I checked in the full-read entries matched the paper (for example the 0.36 W + 0.59 lane law, the 1.5 m/s faster-is-slower threshold, the 0.6 m/s and 1.95 ± 0.09 values, Stern's −80.8% / −42.5% / 14.13 l/100 km, the 1,146 / 354 trajectories and t0 of 1.4 / 2.4 s, ρ* = 4.0 ± 0.5 m^-2 and ω0 = 0.35 ± 0.05 rad/s), so no read depth was downgraded. **Fixed:** [[chowdhury-2000-statistical]] listed one author because Crossref/OpenAlex truncate it; it has three (Chowdhury, Santen, Schadschneider, per arXiv). [[chatagnon-2025-exploring]] cite now names the volume (Crowd Dynamics, Volume 5) as well as the series. **Deleted:** nothing; no phantoms found. **Added (11, all opened this session):** [[pastor-2015-experimental]] (faster-is-slower in humans, sheep and grains, full), [[seyfried-2009-new]] (bottleneck flow, full), [[poissonnier-2019-experimental]] (jam-free ant traffic, full), [[johansson-2007-specification]] (trajectory calibration of the social force model), [[gupta-2018-social]] (Social GAN), [[salzmann-2020-trajectron]] (Trajectron++), [[chen-2019-crowd]] (CrowdNav RL navigation), [[korbmacher-2022-review]] (deep learning vs knowledge-based prediction review), [[singamaneni-2024-survey]] (socially aware robot navigation review), [[he-2026-review]] (stop-and-go suppression review: VSL vs jam-absorption driving), [[liang-2024-unraveling]] (Seoul crowd crush). Search rounds the scan had not run: (A) forward citations of Helbing & Molnár 1995 restricted to 2024+ (OpenCitations, 1,114 citing works with Crossref metadata, top 60 by citations inspected); (B) the same for Helbing et al. 2000 (537 citing works, top 45 inspected); (C) Crossref searches for 2023–2026 reviews with five phrasings (pedestrian dynamics review, crowd dynamics review, stop-and-go review, active-matter clogging, mixed-autonomy CAV review); (D) targeted web searches using the vocabularies of ML trajectory forecasting, social robot navigation, animal (ant) traffic and granular/clogging experiments. OpenAlex was again over budget (HTTP 429) for most of this audit, so new entries carry Crossref counts. **Found but not added:** pages blocked (403/404) or no open copy for Nagel & Schreckenberg 1992 (J. Phys. I 2, 2221, doi 10.1051/jp1:1992277), Bando et al. 1995 (PRE 51, 1035) and Bellomo & Dogbe 2011 (SIAM Rev. 53, 409). Other candidates not catalogued here: Fourcassié, Dussutour & Deneubourg 2010 "Ant traffic rules" (J. Exp. Biol., 10.1242/jeb.031237); Fayolle & Lasgouttes 2026 "Stop-and-Go Waves in Car-Following Models" (SIAM J. Appl. Math. 86(4), 10.1137/25m1747890); Jain et al. 2026 benchmarking of force-based pedestrian models (Collective Dynamics 10, 10.17815/cd.2025.191); a 2026 systematic review of machine learning in pedestrian and evacuation dynamics (Safety Science, 10.1016/j.ssci.2026.107143); "A literature review of dense crowd simulation" (Simul. Model. Pract. Theory 2024, 10.1016/j.simpat.2024.102955); Francis et al. 2025 principles for evaluating social robot navigation (ACM THRI, 10.1145/3700599); "Robust spatial self-organization in crowds of asynchronous pedestrians" (J. R. Soc. Interface 2024, 10.1098/rsif.2024.0112); a 2026 Annual Review of Psychology article on the psychology of crowd behaviour (only an erratum was seen); arXiv:2412.06587 (Argentine ants regulate traffic with stopped individuals). **Still thin:** the classic traffic-model papers (LWR 1955, Nagel–Schreckenberg, Bando OVM, Kerner three-phase, Hughes continuum) are still missing because publisher pages block us and need a second pass from another network. Crowd psychology (social identity, the "no panic" literature beyond [[haghani-2024-revisiting]]) and biological traffic beyond ants are under-covered. Most entries (35 of the scan's 49) are still abstract-depth.
