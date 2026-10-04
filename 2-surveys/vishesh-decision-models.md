---
id: vishesh-decision-models
type: survey
title: Jev decision models and collective robustness
owner: vishesh
agents:
- vishesh/codex-decision-models
status: in-progress
started: 2026-10-03
topics:
- decision-models
- llm-agent-swarms
questions:
- When does communication amplify a typed decision model's errors?
- Which interventions preserve useful disagreement and reliable decisions?
seminal:
- guo-2017-calibration
- seeley-2012-stop
- berdahl-2013-emergent
search_log:
- where: arxiv
  query: site:arxiv.org repeated evidence multi agent debate correlation majority
    vote; selected primary follow-ups Choi, Zhu, Kaesberg, Lin
  date: '2026-10-04'
  results: 4
  new: 0
- where: github
  query: site:github.com debate-or-vote multiagent debate; official repository README
    inspected
  date: '2026-10-04'
  results: 1
  new: 1
- where: lesswrong
  query: site:lesswrong.com correlated evidence double counting information cascades;
    Understanding Information Cascades inspected
  date: '2026-10-04'
  results: 1
  new: 1
- where: web
  query: 'Primary-page follow-up: Bara epistemic, Bertalanic Ringelmann, Qian scaling,
    Ashery conventions'
  date: '2026-10-04'
  results: 4
  new: 0
- where: openalex
  query: data incest social learning
  date: '2026-10-04'
  results: 3
  new: 2
- where: citations-backward
  query: 'Hamdi 2013 references: constrained DAG estimation; optimal incest removal;
    data fusion/misinformation removal'
  date: '2026-10-04'
  results: 3
  new: 3
- where: openalex
  query: dependent evidence opinion pooling shared information
  date: '2026-10-04'
  results: 5
  new: 5
- where: openalex
  query: multi agent debate correlated errors majority voting
  date: '2026-10-04'
  results: 10
  new: 6
- where: openalex
  query: provenance evidence duplication agent memory
  date: '2026-10-04'
  results: 10
  new: 10
- where: citations-forward
  query: OpenAlex cited_by for Guo 2017, Seeley 2012, Berdahl 2013; one relevant downstream
    lead per seed
  date: '2026-10-04'
  results: 3
  new: 3
- where: openalex
  query: Bayesian social learning data incest
  date: '2026-10-04'
  results: 6
  new: 6
- where: openalex
  query: multi agent evidence provenance false corroboration
  date: '2026-10-04'
  results: 9
  new: 9
- where: web
  query: multi agent duplicate evidence provenance; data incest LLM evidence; correlated
    majority voting multi-agent debate (selected primary hits)
  date: '2026-10-04'
  results: 4
  new: 2
- where: openalex
  query: multi agent debate majority voting
  date: '2026-10-04'
  results: 8
  new: 3
- where: openalex
  query: collective decision quorum social information
  date: '2026-10-04'
  results: 10
  new: 9
---

## Scope

Initial screening of typed text decisions, spatial evidence, dependent errors, cross-inhibition and selective routing. Perception is a separate component; Jev is text-only in inspected documentation [[typesafe-2026-models]]. Heterogeneous model cooperation has a separate research task. No accepted hypothesis or experiment results.

## Search log

See 5-experiments/studies/vishesh/decision-models/SEARCH-LOG.md for actual search families and access limitations. Earlier structured counts were not retained. The new 2026-10-04 rounds above have explicit inspected-hit counts; see [research packet](../5-experiments/studies/vishesh/decision-models/quorum-of-mirrors/RESEARCH-GATES.md) for counting rules, reading attribution, citation trails and unresolved leads. This does not reconstruct missing historical counts.

## Landscape

Typed APIs define output structure [[openrouter-2026-jev]], while confidence and jaggedness documents constrain interpretation [[typesafe-2026-confidence]] [[typesafe-2026-jaggedness]]. The evidence audit surveys evaluation weaknesses [[tang-2026-typed]]. Calibration [[guo-2017-calibration]] and selective classification [[geifman-2017-selective]] supply measurement frameworks. Collective sensing [[berdahl-2013-emergent]] and stop signals [[seeley-2012-stop]] motivate mechanisms, not guaranteed transfers.

## What is known

Adversarial decision flips already have a benchmark [[hu-2026-jevadvbench]]. Option naming can change decisions under a fixed rubric [[sun-2026-type]]. Broad evaluation reports task and threshold dependence [[deusser-2026-evaluating]]. Shared judge errors challenge simple confidence fallback [[rao-2026-jev]]. Dependent advisers complicate majority-vote arguments [[sasahara-2026-latent]]. Social influence can reduce diversity without improving accuracy [[lorenz-2011-how]]. These summaries have the reading-depth limits in SOURCES.md; no local replication.

The shared catalogue already contains full-read records relevant to this question: source dependence [[bara-2026-epistemic]], quorum response mechanisms [[sumpter-2009-quorum]], compute scaling [[qian-2025-scaling]], group-size limits [[bertalanic-2026-ringelmann]], and emergent conventions [[ashery-2024-emergent]]. These are inherited team readings, not five new full reads by this updater. Together they motivate fixed-quorum failure accounting, explicit computational comparators and separating agreement from truth. A fresh full read of [[wang-2026-graphecho]] and an attributed full-read supplement on [[hamdi-2013-removal]] narrow Quorum to a controlled engineering replication.

## Open problems and disagreements

Candidate openings are spatial error propagation beyond directly exposed cells; provenance-aware aggregation under fixed information budgets; evidence-triggered inhibition versus arbitrary throttling; finite-capacity reviewer queues; and typed-menu changes after collapsing synonymous actions. Novelty is provisional. Newly catalogued [[jain-2024-interacting]] and [[jin-2026-not]] directly overlap social learning and typed provenance decisions. Abstract-level results on debate diversity disagree across settings [[ferreira-2026-beyond]] [[wu-2025-can]]; do not assume a universal committee gain. Current published confidence formulas supersede the older “undocumented” description for current documentation, not necessarily the historical API [[typesafe-2026-confidence]] [[hu-2026-jevadvbench]].

## Code, data and tools

Coordinate map reference [[gh-dy-ma-jev-world]], prospectively described evaluation suite [[gh-willkelly-jev-evaluation]], and adversarial benchmark [[gh-jevadvbench-jevadvbench]] were inspected at README/metadata depth, not executed. Public map demonstrations motivate visualizations [[x-arithmoquine-2103147890315325714]] [[x-karpathy-2105909609487872075]].

## Gaps

Fifteen exploratory questions, overlap assessments and five top-ranked design sketches are in 5-experiments/studies/vishesh/decision-models/. They remain hunches pending substantive methods review, qualified model access and public registered experimental plans. Scores use the existing owner rubric, with no invented peer ratings.

## Second-pass note

The owner preferred Phantom Coast and Quorum of Mirrors. Their stronger variants are documented in 5-experiments/studies/vishesh/decision-models/REIMAGINING.md. Repeated-evidence theory [[hamdi-2013-removal]] and self-confirming learning [[fudenberg-2019-learning]] are newly catalogued antecedents, so the proposed increment must be a tested intervention and identifiable Jev mechanism.

## Saturation

Not established. The formal survey is in progress. The cited catalogue now includes six full-read records (five inherited, one newly completed), and 12 structured rounds cover the required search families. Forward trails were followed at index metadata depth; downstream full-methods verification remains incomplete. The final rounds found 6/6 and 9/9 uncatalogued relevant leads at search time. Low-yield terminal rounds, resolution of close antecedents and independent survey review remain necessary. No formal hypothesis is proposed or accepted.
