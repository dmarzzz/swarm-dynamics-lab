---
id: scan-papers-sync-consensus
type: task
title: 'Catalogue the papers: synchronisation, consensus and networked control'
kind: scan
status: claimed
priority: p1
owner: dmarz/sync-consensus
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- sync-consensus
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `sync-consensus`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Kuramoto model and Strogatz 2000, From Kuramoto to Crawford (Physica D)
- O'Keeffe, Ha and Strogatz 2017, Oscillators that sync and swarm (Nature Communications), the swarmalator paper
- Jadbabaie, Lin and Morse 2003, Coordination of groups of mobile autonomous agents using nearest neighbor rules (IEEE TAC)
- Olfati-Saber 2006, Flocking for multi-agent dynamic systems: algorithms and theory (IEEE TAC)
- Olfati-Saber, Fax and Murray 2007, Consensus and cooperation in networked multi-agent systems (Proc. IEEE)
- Cucker and Smale 2007, Emergent behavior in flocks (IEEE TAC)
- Castellano, Fortunato and Loreto 2009, Statistical physics of social dynamics (Rev. Mod. Phys.)

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

Scan by dmarz/sync-consensus, 2026-10-03. Tooling note: the OpenAlex list/search endpoints hit the shared
daily IP budget (HTTP 429, "Insufficient budget") after the first query, and Semantic Scholar and the arXiv export
API were rate-limited, so discovery used Crossref (relevance-sorted), arXiv HTML search listings, OpenCitations
(forward citations, resolved through Crossref), DataCite (arXiv metadata), OpenAlex single-work lookups (citation
counts, abstracts) and WebSearch. IEEE, Elsevier, SIAM and AIP landing pages block automated access, so many
control-theory entries are abstract-level from the OpenAlex record and their `url` is that record.

### Search rounds

| # | Where | Query / action | Results | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex search | "Kuramoto synchronization review" (cited_by sort) | 50 | 8 | 8 |
| 2 | arXiv listing (title) | swarmalator | 50 | 50 | 50 |
| 3 | Crossref | consensus problems in networks of agents with switching topology | 15 | 3 | 3 |
| 4 | Crossref | Kuramoto model synchronization review | 15 | 1 | 1 |
| 5 | Crossref | flocking multi-agent dynamic systems algorithms theory | 15 | 4 | 4 |
| 6 | Crossref | Cucker-Smale flocking emergent behavior | 15 | 6 | 6 |
| 7 | Crossref | opinion dynamics bounded confidence consensus | 15 | 4 | 4 |
| 8 | Crossref | swarmalators sync and swarm | 15 | 8 | 4 |
| 9 | WebSearch | swarmalator review; Ren-Beard-Atkins consensus survey; 2024-25 swarmalator robots | 28 | 12 | 6 |
| 10 | arXiv listing (all fields) | synchronization robot swarm; firefly pulse-coupled; mobile oscillators; Kuramoto flocking alignment | 34 | 8 | 6 |
| 11 | Backward (Crossref refs) | O'Keeffe et al. 2017 reference list | 70 | 25 | 15 |
| 12 | Backward (Crossref refs) | Olfati-Saber, Fax & Murray 2007 reference list | 100 | 30 | 12 |
| 13 | Forward (OpenCitations) | O'Keeffe 2017: 303 citing; top 40 by citations + 30 since 2024 | 70 | 30 | 25 |
| 14 | Forward (OpenCitations) | Cucker & Smale 2007: 1518 citing; top 40 + 20 since 2023 | 60 | 20 | 12 |
| 15 | Forward (OpenCitations) | Olfati-Saber 2007: 8697 citing; top 50 + 30 since 2023 | 80 | 15 | 8 |
| 16 | Crossref | sync in complex networks review; opinion dynamics tutorial; gossip averaging; resilient consensus; oscillator models of collective motion; nonlinear opinion dynamics | 60 | 18 | 10 |
| 17 | arXiv + Crossref (ML vocabulary) | Kuramoto oscillatory neurons; GNN decentralized flocking controllers; consensus swarm robots experiment; distributed subgradient | 24 | 8 | 6 |
| 18 | Backward (review) | Sar et al. 2026 robotics section references | 12 | 8 | 4 |
| 19 | arXiv + Crossref (saturation) | Kuramoto robots; review consensus flocking; firefly sync swarm robots; higher-order simplicial sync | 38 | 6 | 3 |
| 20 | Crossref (saturation) | synchronization of moving agents / mobile oscillators | 15 | 8 | 5 |
| 21 | Crossref (saturation) | survey consensus multi-agent recent advances, 2020+ | 15 | 3 | 3 |

"New" counts relevant items not already seen in earlier rounds. The last three rounds found 3/38, 5/15 and
3/15 new relevant items; the core canon (reviews, seminal control and Kuramoto papers, swarmalators) is
saturated, but incremental control variants (event-triggered, fixed-time, adaptive consensus) and
one-way-coupled mobile-oscillator papers keep appearing and were deliberately not catalogued.

### Counts

- 53 papers catalogued with this topic by this agent (all via `lab.py new`, `verify`: 53 checked, 0 problems).
  Of these 15 are reviews, tutorials, surveys or a monograph: [[acebron-2005-kuramoto]], [[strogatz-2000-kuramoto]],
  [[dorfler-2014-synchronization]], [[rodrigues-2016-kuramoto]], [[arenas-2008-synchronization]],
  [[ghosh-2022-synchronized]], [[olfati-saber-2007-consensus]], [[ren-2007-information]], [[cao-2013-overview]],
  [[castellano-2009-statistical]], [[proskurnikov-2017-tutorial]], [[bernardo-2024-bounded]],
  [[sar-2022-dynamics]], [[sar-2026-interplay]], [[kuramoto-1984-chemical]].
- 11 papers from 2023-2026, including robot swarmalators [[ceron-2024-reciprocal]], [[beattie-2025-realizing]],
  [[quinn-2025-decentralised]].
- read_depth: 6 full, 3 skim, 44 abstract.
- Existing entries tagged with sync-consensus: [[vicsek-1995-novel]], [[conradt-2005-consensus]],
  [[vasarhelyi-2018-optimized]] ([[ricco-2026-consensus]] and [[fruchart-2021-non]] already carried it or were
  annotated by other agents).

### Full reads

[[okeeffe-2017-oscillators]], [[jadbabaie-2003-coordination]], [[cucker-2007-emergent]] (equations partly lost
in text extraction), [[yoon-2022-sync]], [[ceron-2023-diverse]] (main text and Methods, not the 100-page
Supplement), [[okeeffe-2025-global]]. Skims: [[sar-2026-interplay]], [[dorfler-2014-synchronization]],
[[quinn-2025-decentralised]].

### Gaps

- Full text not obtained for the most cited control papers ([[olfati-saber-2007-consensus]] author preprint link
  is dead, IEEE blocks automated access); [[olfati-saber-2006-flocking]], [[olfati-saber-2004-consensus]] and
  [[barcis-2020-sandsbots]] deserve full reads from a browser.
- Not catalogued (seen, relevant, lower priority): Hegselmann & Krause 2002 (JASSS, no DOI); Winfree 1967;
  Pikovsky-Rosenblum-Kurths 2003 and Strogatz 2003 books; Sepulchre-Paley-Leonard 2008 (limited communication);
  Leonard et al. collective-motion/ocean-sampling papers; Tanaka 2007 chemotactic oscillators; Uriu 2013 and
  Frasca 2008 mobile oscillators; Majhi 2017/2019 moving oscillators; Schilcher et al. ACSOS 2021/2025 and PRE 2025
  (swarmalator stochastic and discrete-time coupling, from the Bettstetter group); Barciś et al. MRS 2019 (ROS 2
  proof of concept, arXiv 1903.06440); Lee, Yeo & Hong 2021 (finite-cutoff swarmalators); Degond et al. 2022
  (non-reciprocal swarmalators, topological states); Millán et al. 2020 (explosive higher-order Kuramoto);
  Boccaletti et al. 2023 (higher-order networks review); Berner et al. 2023 (adaptive dynamical networks review);
  Li-Duan-Chen 2010 follow-ups; Qin et al. 2017 consensus survey; Vicsek & Zafeiris 2012 is in the library under
  collective-motion; Chazelle "natural algorithms" (flocking convergence bounds); Tolstaya et al. 2020 and Gama et
  al. GNN decentralised flocking controllers (belong to marl-emergence); Markdahl 2020 robot sync on the sphere;
  Amichay 2024 pairwise temporal coupling in collective motion.
- Event-triggered, finite/fixed-time and adaptive-neural consensus (thousands of control papers) were skipped as
  low relevance to swarm dynamics.
- No swarmalator or consensus dataset was found; experimental data on firefly swarms (Sarfati et al. 2020,
  J. R. Soc. Interface) is a candidate for the dataset scan.

### Code repos seen (for the code scan)

- https://github.com/Khev/swarmalators (O'Keeffe; 1D ring code for [[yoon-2022-sync]] at
  tree/master/1D/onring/non-identical; also referenced by [[okeeffe-2025-global]])
- https://github.com/autonomousvision/akorn ([[miyato-2025-artificial]])
- Dedalus spectral solver mentioned for [[fruchart-2021-non]] in another agent's notes.

### Suggested follow-up tasks

1. Code scan: catalogue gh-khev-swarmalators and gh-autonomousvision-akorn and run the 1D swarmalator example
   against the closed forms in [[yoon-2022-sync]].
2. Full reads from a browser of [[olfati-saber-2006-flocking]], [[barcis-2020-sandsbots]],
   [[beattie-2025-realizing]], [[ceron-2024-reciprocal]] (hardware numbers: update rates, delays, message loss).
3. Swarmalator-robotics mini-scan: Schilcher et al. (ACSOS 2021, 2025; PRE 2025), Barciś et al. MRS 2019,
   Gardi et al. 2022 microrobot collectives, Sarfati et al. 2020 fireflies (dataset).
4. Survey task for sync-consensus focused on the question "what is known about coupling an internal clock or
   phase to motion in robot swarms", seeded from [[sar-2026-interplay]], [[dorfler-2014-synchronization]] and
   [[olfati-saber-2007-consensus]].

### Audit (dmarz/sync-consensus-audit)

Audit 2026-10-03. `verify --agent dmarz/sync-consensus`: 53 checked, 0 BAD, so nothing was deleted. Spot-checked
15 entries: all six `read_depth: full` entries ([[okeeffe-2017-oscillators]], [[yoon-2022-sync]],
[[ceron-2023-diverse]], [[okeeffe-2025-global]], [[cucker-2007-emergent]], [[jadbabaie-2003-coordination]]) against
the full PDFs, the content of [[quinn-2025-decentralised]], and Crossref metadata and cite strings for
[[sar-2026-interplay]], [[beattie-2025-realizing]], [[barcis-2020-sandsbots]], [[riedl-2023-synchronization]],
[[bernardo-2024-bounded]], [[ghosh-2022-synchronized]], [[anwar-2024-collective]] and [[kuramoto-1984-chemical]]. One
substantive error was fixed: the sync eigenvalues in [[okeeffe-2025-global]] (multiplicity and sign). Everything
else matched, the full reads are real, and the abstract-level entries say plainly when they are abstract-level.
Six extra search rounds: Crossref with sensor-network vocabulary ("firefly-inspired pulse-coupled synchronization
wireless sensor networks", 15 results, 2 relevant); Crossref with crowd and human vocabulary ("crowd synchrony
clapping bridge", 15, 2); WebSearch and Crossref for 2023-2026 reviews (higher-order, adaptive networks, Kuramoto,
about 30 results, 3 relevant); forward citations of [[olfati-saber-2007-consensus]] through OpenCitations (8718
citing; the 200 newest requested and 26 resolved through Crossref, 3 relevant); forward citations of
[[olfati-saber-2004-consensus]] (2175 records parsed from a download that cut off partway; the 150 newest requested
and 103 resolved, about 4 relevant); and WebSearch follow-ups on the scan's gap list (about 70 results). The recent
forward citations are almost all event-triggered, fixed-time or microgrid consensus papers, which supports the
scan's choice to leave that literature out. Added 11 entries: [[hegselmann-2002-opinion]],
[[sepulchre-2008-stabilization]], [[leonard-2007-collective]], [[werner-allen-2005-firefly]], [[sarfati-2021-self]],
[[strogatz-2005-crowd]], [[yeung-1999-time]], [[hendrickx-2017-open]], [[pecora-1998-master]],
[[boccaletti-2023-structure]], [[berner-2023-adaptive]]. Of these, 1 was read in full, 8 skimmed and 2 read at
abstract level. Found but not added: Winfree 1967, J. Theor. Biol. 16:15 (no abstract or full text reachable);
the 2021 Nature Communications paper on the Millennium Bridge instability without synchronisation
(10.1038/s41467-021-27568-y); Sarfati et al. 2022, chimera states among synchronous fireflies (Sci. Adv.,
10.1126/sciadv.add6690); Al-Mekhlafi et al. 2019, firefly time synchronisation for WSN (IEEE Access); Santillan
2025, PCO synchronisation with electronic oscillators (Chaos Solitons Fractals); the 2026 IEEE TCyb paper on
consensus convergence-rate optimisation in open multi-agent systems; the 2026 Physica A paper on higher-order
Kuramoto synchronisation; the 2026 review of platoon control through network synchronisation (Automation); Zhou &
Kurths 2006 PRL on adaptive weights; Eckhardt et al. 2006, Chaos (Millennium Bridge). Still thin:
pulse-coupled and firefly synchronisation on hardware after 2005 (no robot-swarm PCO paper after
[[werner-allen-2005-firefly]] has been catalogued); delay and churn effects in robot-swarm sync; quantitative
datasets (the firefly 3D flash data behind [[sarfati-2021-self]] should be chased in the dataset scan); and
human-crowd synchrony beyond the bridge.
