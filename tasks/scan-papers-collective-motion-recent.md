---
id: scan-papers-collective-motion-recent
type: task
title: Catalogue collective motion papers from 2024 onward
kind: scan
status: claimed
priority: p0
owner: dmarz/collective-motion-recent
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

The field moves fast and the seminal scan will skew old. Catalogue 2024 to 2026 work on collective motion, especially data-driven inference of interaction rules, 3D tracking, and learned models of flocking. Include strong preprints and workshop papers.

## Search plan

- arXiv listing searches sorted by date, OpenReview (ICLR, NeurIPS, ICML, CoRL), and forward citations of the seminal papers in the sibling scan task.
- Check the accepted-paper lists of the most recent relevant conferences and workshops.

## Done when

- At least 20 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 4 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

Scan by dmarz/collective-motion-recent on 2026-10-03. Scope: collective motion work from 2024 to 2026 (plus a few late-2023 preprints published in 2024), with emphasis on inference of interaction rules, 3D tracking and learned models.

Tool conditions: OpenAlex returned "Insufficient budget" (free daily IP budget exhausted by the parallel agents) after round 2, so later rounds used arXiv HTML search listings, Crossref (DOI records and bibliographic queries, intermittently 429), WebSearch, and Semantic Scholar citation endpoints (worked for a few calls, then 429). Citation counts in entries are therefore Crossref is-referenced-by-count (2026-10-03), not OpenAlex; arXiv-only papers have `citations: null`.

### Search rounds

| # | Where | Query / action | Results looked at | Relevant | New |
|---|---|---|---|---|---|
| 1 | OpenAlex | title.search "collective motion", year > 2023, sorted by citations | 50 | 14 | 14 |
| 2 | OpenAlex | title.search "flocking", year > 2023, sorted by citations | 50 | 8 | 5 |
| 3 | arXiv listing (by date) | "flocking learning" | 50 of 113 | 14 | 11 |
| 4 | arXiv listing (by date) | "fish schooling" | 50 of 207 | 20 | 15 |
| 5 | arXiv listing (by date) | "collective motion data-driven" | 50 of 206 | 0 | 0 |
| 6 | arXiv listing (by date) | "collective behaviour animal groups", "bird flocks", "insect swarms", "locust marching" | about 150 | 18 | 9 |
| 7 | arXiv listing (by date) | "graph neural network collective dynamics", "Vicsek model", "collective motion review" | 150 | 22 | 10 |
| 8 | WebSearch | inference of interaction rules (Nature-family 2025); reviews of collective motion 2024-25; 3D tracking of jackdaw and starling flocks | 28 | 12 | 7 |
| 9 | Crossref bibliographic (from 2024) | PINN pigeons local rules; collective escape starlings; deep learning fish interaction rules | 18 (two queries hit 429) | 3 | 2 |
| 10 | WebSearch | Cell Rep Phys Sci pigeons; neural basis of flocking (Konstanz); VR fish control law; 3D-MuPPET; symbolic regression of interaction rules | 45 | 10 | 5 |
| 11 | Forward citations (Semantic Scholar) | citing [[sayin-2025-behavioral]], sorted by citations | 71 | 20 | 9 |
| 12 | Forward citations (Semantic Scholar) | citing [[amichay-2024-revealing]] (29) and [[heins-2024-collective]] (70) | 99 | 22 | 6 |
| 13 | Forward citations (Semantic Scholar) | citing Ballerini et al. 2008 (2009 citing works) and Katz et al. 2011 (949), filtered to 2024+, top 60 each by citations | 120 | 30 | 8 |
| 14 | Backward citations | reference lists of [[amichay-2024-revealing]], [[hang-2026-self]], [[salahshour-2025-allocentric]], [[zheng-2024-body]] (read in full text) | about 250 | 0 within 2024+ scope (all older seminal work, left to scan-papers-collective-motion) | 0 |
| 15 | arXiv listing | "murmuration" | 50 of 98 | 0 (number theory and heart sounds) | 0 |
| 16 | arXiv listing | "schooling inference interactions", 2024+ results | 19 | 5 | 1 |

Saturation: rounds 15 and 16 yielded 0/50 and 1/19 (5%) new relevant items. Rounds 11-13 (citation chasing) still yielded new items, so the citation graph rather than keyword search is where remaining recent work sits (see gaps).

### Counts

- 49 new paper entries created by this agent, all tagged collective-motion; 2 already present from the sibling scan and confirmed relevant ([[sayin-2025-behavioral]], [[chate-2024-dynamic]], both by dmarz/collective-motion) and 1 from the MARL scan ([[brambati-2025-learning]]); all three already carry the collective-motion tag.
- By kind: 13 reviews, perspectives or books ([[toner-2024-physics]], [[solon-2024-thirty]], [[lecheval-2026-future]], [[chase-2025-physics]], [[couzin-2025-collective]], [[de-lamo-2026-statistical]], [[volkening-2024-methods]], [[fabregas-2026-mathematical]], [[gompper-2025-motile]], [[cai-2025-reinforcement]], plus tool papers [[papadopoulou-2024-swarmverse]], [[itoh-2024-fish]], [[waldmann-2024-3d]]); the remaining 36 split roughly into empirical animal studies, models and theory, data-driven inference or learned models, and tracking (see Themes; several papers fall in more than one).
- By year (entries created here): 2024: 26, 2025: 14, 2026: 9.
- `python3 scripts/lab.py check` 0 errors 0 warnings; `verify` 49 papers checked, 0 problems.

### Read in full (read_depth: full)

[[amichay-2024-revealing]], [[zheng-2024-body]], [[heins-2024-collective]], [[hang-2026-self]], [[salahshour-2025-allocentric]], [[han-2024-collective]], [[de-lamo-2025-data]], [[couzin-2025-collective]] (short Comment). All others are abstract level.

### Themes found (for the survey writer)

1. Alignment is losing its status as a primitive: locusts do not align ([[sayin-2025-behavioral]]); ring-attractor "allocentric flocking" ([[salahshour-2025-allocentric]]), active inference ([[heins-2024-collective]]), turn-away colloids ([[das-2024-flocking]]), RL with spacing costs ([[brambati-2025-learning]]) and evolved boids ([[reynolds-2026-evoflock]]) all get order without an explicit alignment rule. Counterpoint: [[gao-2024-learning]] recovers a second-order Vicsek law from bird flock data.
2. Selective, perception-based attention: [[zheng-2024-body]], [[xiao-2024-perception]], [[puy-2024-selective]], [[ito-2024-selective]], [[krongauz-2024-vision]], [[mezey-2025-purely]].
3. VR and biohybrid causal tests: [[amichay-2024-revealing]], [[li-2025-reverse]], [[escobedo-2026-closed]].
4. Criticality and information transfer: [[hang-2026-self]], [[puy-2024-signatures]], [[gonzalez-albaladejo-2024-power]], [[zampetaki-2024-dynamical]], [[jadhav-2024-collective]], [[papadopoulou-2026-mechanistic]].
5. Inference and learned models: [[han-2024-collective]], [[gao-2024-learning]], [[hem-2025-learning]], [[de-lamo-2025-data]], [[kim-2025-commanding]], [[wu-2024-cbil]], [[li-2025-collective]], [[mcgraw-2024-parallel]], [[boffi-2024-model]].
6. 3D tracking and formations: [[waldmann-2024-3d]], [[phurtivilai-2026-trackfish3d]], [[itoh-2024-fish]], [[ko-2025-beyond]].

### Notable gaps

- No OpenReview / ICLR / NeurIPS / ICML / CoRL accepted-paper list was searched (OpenReview not reached in this run); ML-venue work on learned flocking and multi-agent trajectory models is under-covered.
- Insect field data beyond midges: mosquito swarms (Gupta et al. 2024 Curr Biol, 10.1016/j.cub.2024.07.043) and malaria-mosquito swarm rules (PLoS Comput Biol 2026, 10.1371/journal.pcbi.1014685) were seen in citation lists but not catalogued (no abstract reachable).
- Several Nature-family 2024-2026 papers seen only as titles in forward-citation lists were not opened: Stednitz et al. 2025 Curr Biol (zebrafish interaction states), Sun et al. 2026 Phys Life Rev review (networked collective dynamics), Marshall and Reina 2024 Anim Behav (aims and methods), Nabeel et al. 2023 Phys Biol (data-driven SDEs, pre-2024), Kawashima et al. 2026 (fish interaction networks), Sathiyakumar 2024 (persistent homology regime detection).
- Wild 3D bird data (jackdaw arrays, starling 3D reconstructions) 2024+ beyond the starling escape paper not found as primary papers.
- Most entries are abstract level; the 15 empirical papers would benefit from full reads before load-bearing use.
- Citation counts are Crossref, not OpenAlex (OpenAlex unavailable).

### Code repos seen (for the code scan task; not catalogued here)

- https://github.com/conorheins/collective_motion_actinf (active-inference collective motion, JAX/Julia) [[heins-2024-collective]]
- https://github.com/ekanso/schooling_extreme (50,000-fish hydrodynamic schooling sims) [[hang-2026-self]]
- https://github.com/DerekZhengEvosil/Body_orientation_change_of_neighbors_leads_to_scale_free_correlation [[zheng-2024-body]]
- https://gitlab.ethz.ch/cmbm-public/toolboxes/cri (Collective Relational Inference, PyTorch) [[han-2024-collective]]
- https://github.com/alexhang212/3D-MuPPET [[waldmann-2024-3d]]
- https://ftc-2024.github.io/ (Fish Tracking Challenge 2024 benchmark) [[itoh-2024-fish]]
- swaRmverse R package (CRAN; repo URL not opened) [[papadopoulou-2024-swarmverse]]
- figshare code for [[amichay-2024-revealing]]: https://doi.org/10.6084/m9.figshare.25398523.v1 ; Code Ocean capsule for [[salahshour-2025-allocentric]] (URL not given on page)

### Suggested follow-up tasks (not opened as task files by this agent; the coordinator commits)

1. scan-papers-collective-motion-mlvenues: OpenReview and proceedings search (ICLR, NeurIPS, ICML, CoRL, AAMAS 2024-2026) for learned flocking, multi-agent trajectory forecasting and interaction-rule discovery.
2. scan-datasets-3d-collective: catalogue 3D-POP, 3D-ZeF, SweetFish, TrackFish3D, starling/jackdaw 3D data and the Dryad rummy-nose tetra U-turn data (10.5061/dryad.9m6d2) as dataset entries.
3. fullread-collective-motion-empirical: full reads of [[sayin-2025-behavioral]] (already full by sibling), [[li-2025-reverse]], [[puy-2024-selective]], [[papadopoulou-2026-mechanistic]], [[ko-2025-beyond]], [[gao-2024-learning]].
4. scan-papers-insect-swarms-recent: mosquito, midge and locust 2024-2026 field work.
5. Rerun forward-citation chasing via OpenAlex (cites:W-id, sorted by date) once the IP budget resets, to replace Crossref counts and pick up items missed by Semantic Scholar.

### Audit (dmarz/collective-motion-recent-audit)

Audit on 2026-10-03. `verify` on the scan's 48 own entries returned 0 BAD lines before and after the audit (cai-2025-reinforcement is by dmarz/marl-emergence and only tagged here). All 48 were cross-checked against OpenAlex single-work records (title, authors, year, venue). None was a phantom and none was deleted. Spot-checks against full text: all 8 read_depth: full entries (amichay-2024, zheng-2024, heins-2024, hang-2026, salahshour-2025, han-2024, de-lamo-2025-data, couzin-2025). Numbers and cite strings were confirmed against the papers, and the full-read claims stand. Six abstract-level entries (ko-2025, gao-2024, montanari-2025, jadhav-2024, xiao-2024, huang-2024) were checked against their abstracts and match.

Fixes:
- [[de-lamo-2025-data]] now says 60-minute recordings for N = 40/50/60 at 50 fps, not 20-minute.
- Every citations field now holds the OpenAlex count with its W-id, replacing the Crossref count. The two exceptions are reynolds-2026 and volkening-2024, which are not in OpenAlex.
- arxiv ids were added to gonzalez-albaladejo-2024, gompper-2025 and fabregas-2026.
- kim-2025 has a note that its arXiv version carries a different title.
- The dangling [[caprini-2023-flocking]] link in das-2024 was removed.

Completeness: three extra rounds were run.
1. OpenCitations forward citations of Vicsek 1995 and Ballerini 2008, filtered to 2024+. This gave 874 citing works, resolved via Crossref and ranked by citations. The Vicsek list came back truncated at 1664 of its citing works.
2. Crossref bibliographic queries in neighbouring vocabularies: reviews, interaction-rule inference, 3D field tracking.
3. WebSearch for insect swarms, drone-based field studies and ML-venue learned interaction rules.

Added 11 entries:
- Reviews: [[amichay-2025-integration]], [[nguyen-2025-where]], [[kline-2025-studying]].
- Insect swarms (closes the scan's noted gap): [[cribellier-2026-complex]], [[gupta-2024-mosquitoes]].
- Birds: [[friman-2024-it]].
- Vision models: [[castro-2024-modeling]].
- Robots and active matter: [[casiulis-2025-geometric]], [[xu-2024-self]].
- Inference methodology: [[martina-perez-2025-inverse]].
- Fish VR: [[escobedo-2026-swimming]].

Found but not added:
- Zhu et al. 2026, "Inferring the rules of social interaction in moving Tibetan antelopes", Behav Ecol Sociobiol, 10.1007/s00265-026-03773-x. Paywalled, not opened.
- Seara et al. 2025, Sociohydrodynamics, PNAS, 10.1073/pnas.2508692122. About human residential dynamics, so off-topic.
- Negi, Winkler and Gompper 2024, PRR 6, 013118 (visual perception + alignment).
- Wang et al. 2024, NJP, 10.1088/1367-2630/ad1b81 (visual-attention neighbour selection).
- Confinement bistability in schooling fish, PRE 110, 034613.
- Burst-and-coast fish school phases, R Soc Open Sci, 10.1098/rsos.240885.
- Motion-salience threshold SPPs, Chaos Solitons Fractals 2025.
- Nambu-Goldstone exponents in the Vicsek model, PRL 133, 258301.
- Xu et al. 2026, spatial correlation functions for living matter, PRR 8, 033179.
- Kawashima/Stednitz items listed in the scan's gaps.
- Hierarchical equivariant GNN forecasting of collective motion, arXiv 2501.00626.
- Locust visual attention, Proc B 2026 (10.1098/rspb.2026.0755).

Still thin:
- OpenReview/ICLR/NeurIPS/ICML proceedings were not searched (OpenAlex list queries were out of budget again during the audit).
- Field 3D bird data remain thin.
- Mammal herds beyond sheep remain thin.
- The forward-citation rounds rank only on Crossref counts and only on a truncated Vicsek citing list.
