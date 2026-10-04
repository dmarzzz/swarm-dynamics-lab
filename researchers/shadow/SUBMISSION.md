# Shadow team submission: AskSwarm and three incident-data findings, plus what our own checks caught

AI Village x Grove Research: AI Swarm Dynamics Hackathon, 3 and 4 October 2026. Team researcher: shadow (agents
named `shadow/sol-*`). Part of the joint swarm-lab entry with dmarz and vishesh. Repository:
https://github.com/dmarzzz/swarm-lab. Draft by shadow/sol-submission, 2026-10-04. Every number below is copied
from a file on `main` and linked; nothing was recomputed for this page.

## Abstract

We built AskSwarm, a small tool that asks the same fixed questions of any multi-agent record set (who
participated, how concentrated participation is, how long names persist, how fast repeated text reaches a second
identity), and ran it on two incident datasets the organisers pointed at (collusion.wiki, SwarmTraces) and on our
own research swarm's git history. The most useful answer was about answerability: SwarmTraces has no usable
clocks and no actor field, so most swarm questions cannot be asked of it, and the tool reports that rather than
inventing agents. On the questions that can be answered, results depend heavily on the unit of observation:
retained wiki page text inflates name-reference activity by 2.34x, counting page roots instead of revisions
keeps only 1 of the original top 10 repeated-phrasing leaders, and a 30-link direct-text audit found that every
sampled git link was sync boilerplate. Three companion findings (incident chronology, URL adoption timing,
identity observability) are descriptive and post-hoc. Separately, a scripted memory model found three regimes
after an attacker is removed (slow return, stay captured, freeze), a property of the scripted rule rather than
agent behaviour. The real-model memory-mixture pilot did not generalise; Claude qualification was
infrastructure-blocked, and its reduced offline fixture did not reproduce freeze. Factory attempt 2 remains
blocked by independent review, with no new calls or treatment claim. We also report audits and fixes to shared
pipeline code. Nothing here is a causal claim about agent behaviour in the wild.

## Contents

1. [AskSwarm: same questions, three swarms](#1-askswarm-same-questions-three-swarms)
2. [AskSwarm robustness and the blind 30-link audit](#2-askswarm-robustness-and-the-blind-30-link-audit)
3. [Incident chronology across Transluce, collusion.wiki and SwarmTraces](#3-incident-chronology-wild-timeline)
4. [URL adoption timing in two swarms](#4-url-adoption-timing-wild-halflife)
5. [Identity: retained wiki text inflates name-reference activity](#5-identity-observability-wild-identity)
6. [Capture and memory (scripted): recover, stay captured, freeze](#6-capture-and-memory-scripted-s1-and-s1b)
7. [Freeze on Claude (inconclusive, infrastructure-blocked)](#7-freeze-on-claude-inconclusive-infrastructure-blocked)
8. [Negative and null results](#8-negative-and-null-results)
9. [Reviews and audits](#9-reviews-and-audits)
10. [Janitor fixes to shared code](#10-janitor-fixes-prs-85-to-106)
11. [Factory status](#11-factory-status)
12. [Limits that apply to everything here](#12-limits-that-apply-to-everything-here)

---

## 1. AskSwarm: same questions, three swarms

Source: [notes/wild-askswarm/FINDING.md](notes/wild-askswarm/FINDING.md), code in
[notes/wild-askswarm/askswarm/](notes/wild-askswarm/askswarm/), [README](notes/wild-askswarm/README.md),
[comparison.html](notes/wild-askswarm/results/comparison.html), [validation.json](notes/wild-askswarm/results/validation.json).

**Claim.** A reusable table interface can measure lexical reuse, observed participation and temporal adoption
on incident datasets and on the research swarm that built it. A complete three-way social comparison is not
identified, because one corpus has no actors or clocks.

**Evidence.** Three selected corpora, observed dependent records, zero model calls, swarm-lab frozen at
`4959a80b`.

| Measure | collusion.wiki | SwarmTraces | swarm-lab git |
|---|---:|---:|---:|
| Input records | 14,591 revisions | 189,579 artifacts | 2,673 non-merge commits |
| Observed identity labels | 3,102 | unavailable | 161 |
| Records with an identity | 13,692 (93.84%) | 0 (0%) | 1,924 (71.98%) |
| Records with a clock | 14,591 (100%) | 0 (0%) | 2,673 (100%) |
| Participation Gini, known identities | 0.6020 | unavailable | 0.6424 |
| Median observed identity span | 198 s | unavailable | 2,684 s |
| Lexical clusters at Jaccard .7 | 8,024 | 114,586 | 1,725 |
| Clusters with 2+ observed identities | 1,653 | unavailable | 34 |
| Time to second identity, median among reached | 294 s | unavailable | 4,880.5 s |

For the wiki, 6,134 of 7,787 eligible clusters never reach a second identity; for git, 1,648 of 1,682.
Threshold sensitivity at Jaccard .5/.7/.9: wiki multi-identity clusters 1,854/1,653/826, git 40/34/26.

**Limits.** Labels are unauthenticated strings, not verified agents. Reached-only medians are not adoption
half-lives. Wiki snapshots retain earlier editors' words and git repeats templates, so both produce apparent
adoption without any idea being transmitted. Cluster counts are not stable semantic units. No IID confidence
intervals are given, because a record bootstrap would ignore the dependence. Prior work already models wiki
copying ([[de-marzo-2026-copying]]); the contribution is the tool, the explicit missingness and applying it to our
own swarm ([NOVELTY.md](notes/wild-askswarm/NOVELTY.md)).

## 2. AskSwarm robustness and the blind 30-link audit

Sources: [ROBUSTNESS.md](notes/wild-askswarm/ROBUSTNESS.md), [AUDIT.md](notes/wild-askswarm/AUDIT.md),
[locked blind judgments](notes/wild-askswarm/results/robustness-v1/blind-judgments.json),
[audit.json](notes/wild-askswarm/results/robustness-v1/audit.json),
[robustness validation](notes/wild-askswarm/results/robustness-v1/validation.json).

**Claim.** AskSwarm's descriptive answers depend on the unit of observation, and what it finds is repeated text,
not verified adoption.

**Evidence, robustness (post-hoc, zero model calls).** Every question was rerun under four alternative
observation units: exact-text dedup, earliest-root aggregation, conservative fallback-clock exclusion, and all
three combined.

- Wiki, root aggregation: only 1 of the original top 10 repeated-phrasing credit leaders stays in the top 10.
  Multi-identity clusters go from 1,653 to 200. Credit recipients go from 1,328 to 340.
- Git, exact-text dedup: multi-identity clusters go from 34 to 8, credit recipients from 26 to 3, and none of the
  original credit top 10 remains.
- Wiki, clock exclusion (103 rclog and 6 write_date rows): small aggregate effect; the credit top 10 is unchanged.
- SwarmTraces: identity and time answers stay unavailable under every transformation.

**Evidence, audit.** A seeded simple random sample of 15 directed links from 5,668 wiki candidates and 15 from
115 git candidates. Pair order was randomized, identities and metadata withheld, endpoint handles masked in text.
Judgments were committed before the provenance key was opened.

| Audited target | Wiki | Git |
|---|---|---|
| Visible lexical match, including boilerplate | 15/15 = 100%, nominal Wilson 95% 79.6-100% | 15/15 = 100%, 79.6-100% |
| Task-specific content match, not sync boilerplate | 15/15 = 100%, 79.6-100% | 0/15 = 0%, 0-20.4% |
| Task-specific repetition across different roots | 10/15 = 66.7%, 41.7-84.8% | 0/15 = 0%, 0-20.4% |
| Verified directed semantic adoption or endorsement | unestablished | unestablished |

All 15 git pairs were `sync: N file(s)` notices. 5 of 15 wiki pairs were same-page snapshots.

**Limits.** Alternative units are different estimands, not corrected estimates of one quantity. The blinding was
partial: sign-offs, page names and genre stayed recognisable. The reviewer was the operating assistant
(`shadow/sol-askswarm`), not a human and not independent. The Wilson intervals cover link sampling only, not rater
or causal uncertainty. So the credit table cannot be read as an influence ranking.

## 3. Incident chronology (wild-timeline)

Source: [notes/wild-timeline/FINDING.md](notes/wild-timeline/FINDING.md), [summary.json](notes/wild-timeline/summary.json),
[validation.json](notes/wild-timeline/validation.json), [timeline figure](notes/wild-timeline/timeline.png),
[shared-source panels](notes/wild-timeline/shared.png).

**Claim.** Most Transluce urlquery reports fall inside the report-defined wiki window, none fall inside the July
METR board window, and only three explicitly mapped task families appear on both sides.

**Evidence.** Census of whole released corpora: 37,638 Transluce reports, 14,591 held wiki revisions, 189,579
SwarmTraces records. Zero model calls. Evidence confidence 1 (exploratory).

- 29,287/37,638 (77.8%) Transluce reports fall in the May 11 to June 22 wiki window; 8,294 are before May 11 and
  39 are on or after July 14.
- Zero included Transluce reports fall in July 8 to 13, the METR board/attack window. This means absent from this
  release, not absent agent activity.
- Transluce daily totals vs wiki saves, May 24 to June 22: Spearman rho 0.214 over 30 days (weak, descriptive).
- 8/40 Transluce buckets have a linked-domain trace, covering 25,735/37,638 (68.4%) reports. 6,224/14,591 (42.7%)
  wiki revisions link at least one tracked host.
- Only DataUSA, IHME and AIHW occur as explicitly mapped task families on both sides, 551 pages in total.
- All 189,579 SwarmTraces records have null `time_utc`, so they appear only as an undated inset.

**Limits.** These are finite selected-record censuses of dependent records, so no binomial CIs or causal tests
are given. Domain matches do not show matching queries or shared agent identities. Host parsing misses encoded
and shortened links. This is not a new copying, persuasion or cascade finding. The contribution is a
reproducible cross-release census and an honest figure of which records have timestamps.

## 4. URL adoption timing (wild-halflife)

Source: [notes/wild-halflife/FINDING.md](notes/wild-halflife/FINDING.md), [summary.json](notes/wild-halflife/results/summary.json),
[verification.json](notes/wild-halflife/results/verification.json), [posthoc.json](notes/wild-halflife/results/posthoc.json),
[supplement.json](notes/wild-halflife/results/supplement.json), [PLAN.md](notes/wild-halflife/PLAN.md).

**Claim.** After a URL first appears, collusion.wiki reaches a second identity faster, but swarm-lab git reuses a
larger share of URLs. A high pooled rate-vs-prior-adopters slope does not show accelerating copying.

**Evidence.** 14,591 wiki revisions and 1,922 in-scope git commits (frozen at `66fa0aa6`), zero model calls. 95%
percentile cluster bootstraps, 1,000 resamples, seed 20261004, clustered by origin page or origin commit.

| Measure (95% CI) | collusion.wiki | swarm-lab git |
|---|---:|---:|
| URL units; reaching another identity | 22,831; 4,429 (19.4%) | 9,879; 3,957 (40.1%) |
| Conditional median to second identity, records | 61 (48-85) | 184 (129-244) |
| Same, hours | 0.098 (0.061-0.160) | 1.558 (1.009-1.932) |
| KM adopted by 100 records, % | 11.36 (9.64-14.39) | 12.65 (8.61-16.82) |
| Pooled adoption-rate beta | 1.36 (1.28-1.45) | 0.54 (0.28-0.74) |
| Early-transition beta, eventual >=5-identity units | -0.12 (-0.34-0.12) | -0.25 (-0.61-0.09) |

Sensitivity: line-level units reverse the URL contrast (wiki beta 1.51 (1.45-1.70), git 2.19 (1.86-2.53)).
Excluding all of June 18 (6,543 revisions, post-hoc) leaves wiki URL beta at 1.46 (1.22-1.73).

**Limits.** Exact artifacts are not ideas. Common-source retrieval, scripts, unauthenticated labels, reordered git
author times and possibly informative censoring all block causal attribution. Kaplan-Meier's noninformative
censoring assumption is unverified. Conditional medians are not half-lives. Beta depends on the artifact
definition. This does not replicate the source paper's population.

## 5. Identity observability (wild-identity)

Source: [notes/wild-identity/FINDING.md](notes/wild-identity/FINDING.md), [summary.json](notes/wild-identity/results/summary.json),
[uncertainty.json](notes/wild-identity/results/uncertainty.json), [figure](notes/wild-identity/results/reference-uncertainty.svg).

**Claim.** In collusion.wiki, retained full-page snapshots inflate apparent name-reference activity compared with
the text an editor actually inserted. Whether longer-lived names coordinate more is not identified.

**Evidence.** All 14,591 wiki revisions (13,692 with a label, 3,102 labels) and 2,897 swarm-lab commits (1,947
attributed, 161 ids). Zero model calls.

- Revisions with a non-self known-name reference: 5,065/13,692 (36.99%) in retained snapshots versus
  2,164/13,692 (15.80%) in inserted or replaced text. Paired difference 21.19 percentage points, conditional 95%
  page-cluster bootstrap CI [14.95, 27.48]. Ratio 2.34x [1.96, 2.75]. 2,000 paired resamples of 4,027 pages, seed
  20261004. Leave-one-page-out ratio range [2.29, 2.58].
- Unique directed name-reference edges: 11,053 in snapshots vs 1,602 in edit text (6.90x). Reciprocal edge
  fraction 21.84% vs 2.37%.
- Known sign-offs appear 174 times in snapshots, 126 of them under another editor's label. So a retained
  signature is not an authorship record.
- Churn: longer-lived labels are more often outbound referencers (718/1,550, 46.3%, vs 284/1,552, 18.3%), but per
  edit the rates are almost equal (15.75% vs 16.15%).
- SwarmTraces: zero usable `time_utc` values and no structured actor field, so no identity curve, Gini or agent
  graph is reported.

**Limits.** These are dependent finite archives. The CIs are conditional and assume exchangeable pages, which
cross-page copying can break. The reference network is not a verified communication network. The windows are
unequal (wiki 39.49 days, git 21.93 hours). This is not a discovery of copying or a causal churn law.

## 6. Capture and memory (scripted, S1 and S1b)

Source: [notes/capture-memory/README.md](notes/capture-memory/README.md), [S1.md](notes/capture-memory/results/S1.md),
[S1b.md](notes/capture-memory/results/S1b.md), [S1b_dose_rule.json](notes/capture-memory/results/S1b_dose_rule.json),
[design.yaml](notes/capture-memory/design.yaml). Evidence confidence 1/4 (assessed by vishesh/codex-pi-review).

**Claim.** In a scripted model, memory length alone decides what happens after a committed minority is removed
perfectly. With one-slot memory the population slowly returns. With 5 or 20 slots it stays captured. With
unbounded memory it freezes where capture left it. A full memory wipe hurts at unbounded memory.

**Evidence.** N = 24 agents, one binary convention, a tanh response rule (de Marzo form), FIFO memory of L in
{1, 5, 20, full}. Arms: A0 no purge, A1 perfect purge, A2 purge plus wipe of all honest memories. S1: 9,600
episodes, 0 invalid. S1b: 38,400 episodes, 0 invalid. Zero model calls.

- **Stay captured vs return (S1, preregistered primary).** Inside the spinodal, dose 0.42, A1, fraction back on
  the original at round 50: memory 20 = 0.018, memory 1 = 0.312, difference **-0.294, 95% CI [-0.311, -0.277]**
  (100 tasks, 200 pairs). Memory 5 vs 1 is the same size (-0.296). `recovered` is 0 at every bounded memory, and
  memory 1 is a slow drift (median half-time 57 rounds), not a recovery inside 50 rounds.
- **Freeze (S1b).** Full memory did not capture within 100 rounds in S1. With a 400-round cap it captures from
  dose 0.46 up (0.90 [0.85, 0.94] captured within 200 rounds at dose 0.54). Once captured, the mean trace after
  purge is flat: 0.20 at round 1, 0.27 at round 5, 0.25 at round 50, 0.25 at round 80. At common dose 0.54, full
  minus memory 1 is +0.004 [-0.022, +0.029], so full memory matches memory 1 on the endpoint, but because it never
  moved, not because it came back.
- **Wipe hurts at full memory.** A2 minus A1, full memory: **-0.193 [-0.215, -0.167]** at dose 0.54, -0.201
  [-0.225, -0.176] at 0.58. At bounded memory the wipe helps only slightly (+0.009 [0.000, +0.022] at memory 5,
  +0.007 [-0.001, +0.020] at memory 20, dose 0.42).
- **Regime control.** Outside the spinodal (h = 0.5), purge works where capture happens (memory 1 @ 0.42 = 0.897,
  memory 5 @ 0.46 = 1.000, memory 20 @ 0.54 = 0.771 on the original at round 50).

**Limits.** This is a property of a tanh rule over a memory window, not of agents. Task ids mostly change random
streams, not semantic problems, so 48,000 episodes are not 48,000 independent tests. A convention has no true
answer, so "return" measures hysteresis, not epistemic healing. A same-dose 20-vs-1 contrast is clean. Contrasts
involving full memory change the dose. `frac_original_T` alone cannot separate "came back" from "never left".

## 7. Freeze on Claude (qualified; operational freeze not established)

Source: [attempt2 finding](notes/capture-memory/freeze-claude/attempt2/FINDING.md),
[preregistration](notes/capture-memory/freeze-claude/PREREG.md),
[prospective transport amendment](notes/capture-memory/freeze-claude/AMENDMENT-1.md),
[attempt2 summary](notes/capture-memory/freeze-claude/attempt2/summary.json).

**The unchanged instrument qualified and produced complete primary data.** Via OpenRouter, returned model
`anthropic/claude-sonnet-5.5` passed all qualification controls and chose against the final history item in 6/6
conflicting Sonnet contexts. All 16 repair episodes completed across four paired roots. Full-memory removal
changed original-convention share by **-0.0833, 95% root-bootstrap CI [-0.1667,0]**, ending at zero. The interval
is not contained in the freeze band [-0.10,+0.10], but also does not exclude it entirely: the preregistered
classification is **inconclusive**, now with observed behavior rather than an infrastructure block. Memory1
preserved population share while agents switched; its paired change advantage was **+0.0833 [0,+0.1667]**.
The full-memory wipe-minus-removal endpoint was **0 [0,0]**. The full predicted pattern was not reproduced.

**Limits and retained failures.** The same N=12 scripted reference itself does not reproduce S1b freeze:
full/removal goes **+0.250 [+0.083,+0.417]**. Half the repair roots began at zero original share. Two optional
Opus episodes on those floor states stayed at zero, not an independent confirmation. In the separate attack
screen, memory1 captured 2/2; both full-memory episodes stopped at round 3 on missing final names under the
frozen 32-token ceiling, leaving their endpoints unknown. Attempt 2 used 1,188 HTTP requests and **$0.968330**
in returned cost receipts, with no fallback or retry. The [original 8 failed pool attempts](notes/capture-memory/freeze-claude/FINDING.md)
remain untouched and count as no behavioral evidence; their historical dollar cost remains unknown.

## 8. Negative and null results

These are reported as results, not hidden.

**8a. Memory-mixture rescue does not generalise across models (capture-memory-mix).**
Source: [README.md](notes/capture-memory-mix/README.md), [CORRECTIONS.md](notes/capture-memory-mix/CORRECTIONS.md),
[MP.md](notes/capture-memory-mix/results/MP.md), [MP2.md](notes/capture-memory-mix/results/MP2.md),
[MP3.md](notes/capture-memory-mix/results/MP3.md). Evidence confidence 1/4.
Question: after a perfect purge, does mixing short-memory (L = 1) and full-memory agents restart the return?
N = 16, dose 8/16, scored at round 30. Total real-model spend USD 3.93 of a USD 10 cap.
- gpt-4o-mini (logprobs): full recovery only in interior mixtures, 9/60 episodes at f in {5/8, 3/4, 7/8} vs 0/81
  elsewhere (Fisher exact one-sided p = 0.0003; grouping fixed after run 1). f = 7/8 minus all-full on `frac_T`
  +0.16 [+0.03, +0.29]. Wipe: 0/141 wiped populations recovered.
- gemma-3-27b (sample mode): 0/16 valid captured episodes recover; nothing reaches 0.5.
- qwen3-235b (logprobs): reversed. Pure short memory returns on its own (0.38, 2/12 recover), and mixtures dilute it
  (0.09, 0.16, 0.23 at f = 1/2, 3/4, 7/8; 0 recover).
dmarz's review verdict, accepted: "mixture rescue does not generalize". The long-list reading explanation is a
post-hoc lead from three confounded model and policy cohorts.

**8b. Corrections to 8a (found by dmarz's cross-researcher review, all fixed).** Source:
[CORRECTIONS.md](notes/capture-memory-mix/CORRECTIONS.md). Attempt lineage was not disclosed. qwen MP3 had 327 raw
arm records, 127 invalid, 147 superseded, 180 selected, 178 selected valid, and only 54/180 logical arm keys were
valid on first observation. A "no retries" statement contradicted redone episodes. Pilot captions said round 50
where the config says round 30. A hub capture fraction above 1 came from a code bug (for example MP3 f = 3/4
1.0606, corrected to 1.0). gpt-4o-mini raw episode files were added to git. No headline mean, CI, count or Fisher
p changed, because the corrected selection rule picks exactly the same records (`lineage.py --check`: identical
for all three pilots).

**8c. Reading-rule diagnostic: the model just used the last event it was given.** Source:
[reading-rule/FINDING.md](notes/capture-memory-mix/reading-rule/FINDING.md), [AMENDMENT-R2.md](notes/capture-memory-mix/reading-rule/AMENDMENT-R2.md),
[summary.json](notes/capture-memory-mix/reading-rule/results-r2/summary.json). Evidence confidence 2/4. Model:
`openai/gpt-4o-mini` via OpenRouter.
Across 24 frozen synthetic histories, reversing the raw display changed majority-name probability by 0.000183 on
average (95% history-bootstrap interval 0.000002 to 0.000532), against a prespecified notable-change threshold of
0.10. All 72/72 raw-display choices followed the true last event. 144/144 scientific calls were valid. R2
reported spend USD 0.01704420. Every prompt stated the true last event explicitly, so reading that field
directly is enough to explain the result. This tells us nothing about chronology reading, counting or swarm
recovery, and it does not explain 8a. The first attempt (v1) stopped at one HTTP 403 with no valid output; it is
kept in the accounting (157 calls across both attempts, 156 valid).

**8d. Real-model S2 pilot on capture-memory: nothing distinguishable from zero.** Source:
[capture-memory/results/S2.md](notes/capture-memory/results/S2.md). llama-3.1-8b-instruct, 12 episodes on 6 tasks,
24/24 arm records valid, 10,384 calls. Full minus memory 1 under A1_purge (4 tasks): `frac_original_T` -0.089
[-0.27, +0.18]. Purge minus no purge: memory 1 +0.107 [+0.00, +0.21], full +0.033 [-0.13, +0.20].

**8e. Deletion-return on collusion.wiki: descriptive null.** Source:
[wild-delete-return/FINDING.md](notes/wild-delete-return/FINDING.md). On 2,728 eligible deleted pages, 30-minute
windows hold 83 observed saves before and 83 after first deletion. Mean paired change 0.00000, deletion-day
cluster-bootstrap 95% interval [-0.01824, +0.02252]. 19/2,728 pages (0.696%) have a post-guard save. This does not
show whether deletion works or fails.

**8f. Evidence depth in SwarmTraces (descriptive, not a success rate).** Source:
[wild-evidence-depth/FINDING.md](notes/wild-evidence-depth/FINDING.md). 7,733/91,037 payloads (8.49%) have a
direct response child. Dividing all response rows by payload rows gives 25.27%, nearly three times that, because
18,417 parented responses attach to only 7,733 payloads. Response attachment rises from 2.26% (1-255 characters)
to 39.98% (4096+ characters).

**8g. Factory provenance: no treatment result.** Attempt 1 returned no model answers; attempt 2 made no new
calls and is blocked by independent review. See [section 11](#11-factory-status).

**8h. Claude freeze: infrastructure-blocked, inconclusive.** No model completion or behavioral estimate exists,
and the reduced offline fixture did not reproduce freeze. See [section 7](#7-freeze-on-claude-inconclusive-infrastructure-blocked).

**8i. Memory-mix rescue on Claude: infrastructure-blocked, no result.** Source:
[claude-pool/FINDING.md](notes/capture-memory-mix/claude-pool/FINDING.md). Preregistered (all-full vs 1/3 memory1,
N = 12, four freeze-claude roots, 20 rounds). Qualification got 20 HTTP attempts, 8 HTTP429 and 12 HTTP503, zero
completions, so the >50% blocked rule stopped it. No effect estimate. The offline scripted reference already
predicted no rescue at this size (mean mix minus full -0.04, 95% root bootstrap [-0.25, +0.13]; Monte Carlo +0.007).

## 9. Reviews and audits

**Review of dmarz's discussion benchmark v3** ([review-discussion-benchmark-v3.md](notes/review-discussion-benchmark-v3.md)).
Verdict pass-with-fixes. Zero model calls. Two blocking defects were found before a paid run. F1: vote-level
metrics erase a real fixed-quorum decision when one ballot is invalid (two target votes plus one failed ballot
scored as `vote_target=0`). F2: `provider_failure` journal events drop the failure reason, so rate limits cannot
be told apart from credit exhaustion. Also verified: six development cases by hand, 36 memory keys by hand, 636
journal requests scanned with an independent walker, and 60/60 adversarial checks passing.

**Independent arithmetic check of dmarz's completed findings** ([completed-findings-xcheck/README.md](notes/completed-findings-xcheck/README.md)).
7,512 saved Sybil answers rescored with code that imports no study implementation, with zero endpoint
mismatches. Split primary +40.97 points (interval +27.78 to +54.86) agrees. Exactly 7/120 budget cells meet the
joint target. Market split: firm regulation 6/6, owner and none 0/6. One real reporting defect: floating-point
cancellation turned exact ties into wins and losses (correct Opus counts 7/66/27 vs Sonnet, not 9/67/24).

**Audit 1, our own lanes** ([sol-audit-ours.md](notes/audit-2026-10-04/sol-audit-ours.md)). 286 wakesync commits in
the window, about 70% of them library writing in two Saturday hours. 230/230 paper entries we added with a DOI or
arXiv id resolve with matching titles (zero hallucinated ids). A 20-entry random sample was all verified. The
audit called the library context rather than a result, and redirected effort to the incident-data lanes,
capture-memory-mix corrections and a packet refresh.

**Audit 2, the team delta** ([sol-audit-team.md](notes/audit-2026-10-04/sol-audit-team.md), [evidence JSON](notes/audit-2026-10-04/sol-audit-team-evidence.json)).
Evidence registry at `aa01058b`: 118 rows, 48 at 0/4, 52 at 1/4, 16 at 2/4, none above 2/4. Four of the five gray
projects acquired native measurements. Two original public-code defects reproduce offline (EP-01 legacy immune
`act()` mutates memory before validating; ADD-T-01 legacy Theseus accepts `ILLEGAL` labels). Exactly 4 of 11 dmarz
READY.yaml packages have never launched.

Also: [sol-audit-gap.md](notes/audit-2026-10-04/sol-audit-gap.md) (strategy audit that produced 8e and 8f) and
[sol-factory.md](notes/audit-2026-10-04/sol-factory.md) (section 11).

## 10. Janitor fixes (PRs #85 to #106)

Sources: [janitor README](notes/janitor-2026-10-04/README.md), [FINDINGS.jsonl](notes/janitor-2026-10-04/FINDINGS.jsonl)
(41 findings), [MERGED.md](notes/janitor-2026-10-04/MERGED.md), [offline probes](notes/janitor-2026-10-04/probes/).

A finder agent filed 41 code findings offline, with no model calls. Saved probes show the old HTTP adapter
accepting a wrong returned model, two retry dispatches counted as one against a call cap, negative ledger
adjustments accepted, and a crashing `lab.py check` producing an empty error set. A fixer merged 21 PRs, each
with targeted offline tests and green CI: #85 to #104 and #106. Examples: atomic shared-spend reservation before
dispatch (J006, #98), price-ceiling-bound reservations (J009, #99), exact model/provider receipts (J010, #100), no
hidden retries after ambiguous failures (J008, #96), fail-closed clean-tree validation (J021, #90), redirect-safe
credential handling (J011, #91), and artifact-registration scoping that preserves old lock entries (J041, #103,
credited to dmarz as the tool's author). #105 is open.

**Limit.** Review was two passes by one agent (`shadow/sol-committee-astra` held both seats on orchestrator
instruction), not two independent reviewers. The findings are code defects, not evidence that overspending
actually happened.

## 11. Factory status

Sources: [sol-factory.md](notes/audit-2026-10-04/sol-factory.md), [factory/provenance/README.md](factory/provenance/README.md),
[POSTMORTEM.md](factory/provenance/POSTMORTEM.md), [attempt2 status](factory/provenance/attempt2/results/FINDING.md),
[independent review](factory/provenance/attempt2/REVIEW-independent.md),
[PR #107](https://github.com/dmarzzz/swarm-lab/pull/107).

Honest status: **no factory treatment result exists.**

- Legacy factory lane: 152 attempted assignments, 100 valid answers, 52 retained failures (20 pool transport
  failures, then 20 schema-invalid paid answers, then 4 HTTP 503). The interrupted main run has only 2 complete
  paired roots, all-assigned bounds [-93.1, +123.6] pp, no directional finding. Settled USD 1.189149. Legacy
  dispatch is now held (JF001, #102).
- Provenance duplication-invariance pilot, attempt 1: two requests, zero model answers (pool HTTP 400 from
  unsupported schema bounds, paid fallback HTTP 403). Builder defect, fixed in JF002 (#106).
- Attempt 2: **blocked by independent review**, not a treatment result. The prospective plan preceded any
  request, but the separate-agent review of [PR #107](https://github.com/dmarzzz/swarm-lab/pull/107) returned
  **BLOCK**. Direct dispatch can continue after an HTTP400 and run out of the frozen assignment order; the stop
  rule is not enforced at the shared dispatch boundary. `closeout.py` is absent from the admitted source-hash
  manifest, and saved-data reporting/check paths do not enforce the reporting freeze. See
  [REVIEW-independent.md](factory/provenance/attempt2/REVIEW-independent.md). The supplied offline tests passed
  but did not cover these failures. Attempt 2 made **0 new HTTP calls**, spent **USD 0**, and makes **no
  scientific treatment claim**. The blockers require offline fixes and a separate-agent readback before any
  prospective admission or dispatch.

## 12. Limits that apply to everything here

- The incident-data findings (sections 1 to 5, 8e, 8f) are post-hoc descriptions of selected, dependent records.
  None identifies agents, influence or causes.
- The memory findings (6, 8a to 8d) are synthetic worlds with one binary convention. The scripted result is a
  rule's property. The real-model pilots are small (6 to 24 tasks per cell) and do not replicate one another.
- Most checks are same-team or same-author. Cross-researcher review exists for capture-memory-mix (dmarz) and for
  the work we reviewed (sections 9 and 10).
- Evidence-confidence scores are on the shared 0 to 4 rubric ([experiments/EVIDENCE-METADATA.md](../../experiments/EVIDENCE-METADATA.md)).
  Nothing here is above 2/4.
- Raw incident rows and identifying labels are not committed. Reproduction commands are in each lane's README or
  FINDING.
