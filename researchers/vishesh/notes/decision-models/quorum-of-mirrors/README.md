# Quorum of Mirrors: when nine reports are only three observations

**Does a group get better evidence when more agents agree—or can it just repeat the same source more loudly?** Quorum of Mirrors tests whether preserving source ancestry helps a group make better decisions when reports overlap.

Imagine an incident desk receives nine reports: seven copy one inspection saying “safe,” while two independent inspections say “unsafe.” Counting reports says safe, 7–2. Counting independent observations says unsafe, 2–1. Adding judges does not add inspections. This is an illustrative use case; the actual inputs are synthetic binary sensor reports with explicitly declared reliability.

The practical decision is whether to invest in **more judgments, better source tracking, or a simple deduplication rule**.

## What has actually run

The repaired **Q1 context screen completed all 16 calls with valid responses, but got 0/8 full-lineage decisions right** (required: at least 7/8). Every choice matched report majority even when copies should count once. Partial-lineage cases were interface checks, not accuracy tests. The [Q1 repair report](reviews/Q1-02-post.md) distinguishes the fixed output-token bug from this valid negative result. The larger committee experiment remains unrun; trustworthy source deduplication in code remains the practical baseline.

The earlier reader screen, **S0**, completed. One model reads each packet with full source IDs and explicit deduplication instructions. There are eight bit triples at two reliability settings, each requested twice: 16 configurations, 32 calls. No agents talk to each other in S0; the swarm comparison is still pending.

| Method | Correct exact-MAP choices on saved inputs | Evidence type |
|---|---:|---|
| Native reader, with source instructions | 29/32 | Observed model calls |
| Count every report | 24/32 | Retrospective deterministic calculation |
| Count each known source once | 32/32 | Retrospective deterministic calculation |

“Correct” means choosing the more likely hidden state given the evidence, not matching a sampled hidden truth. The two computed references are not randomized model arms. The screen passed its predeclared competence thresholds, but all three non-correct responses occurred in the eight calls where report majority and source majority conflict: **5/8 correct there, versus 24/24 elsewhere**. That diagnostic split is retrospective.

## What these results are useful for

For this simple grammar with complete, trustworthy source IDs, an exact deduplication rule already solves the task without model calls. The evidence supports using that rule as an engineering baseline before paying for a committee. It also identifies conflicting copied evidence as a useful stress case for qualification.

We have not established that source-aware instructions improve a model, that discussion helps, or that a swarm beats one solver. Missing or unreliable ancestry, semantic paraphrases, common-cause errors and real incident decisions remain untested. The model’s raw choice scores are not calibrated truth probabilities. These repeated finite patterns cannot establish general reliability.

**Explore the evidence:** [all 16 saved cases](analysis/iteration-3/cases.html) (download/open the HTML for interaction), [auditable comparison data](analysis/iteration-3/comparisons.json), [results and plan evaluation](RESULTS.md). The explorer shows all nine reports, their three visible roots, both voting rules and both actual model responses; it invents no swarm dialogue.

## What the next iteration changes

The Q1 failure cannot tell us whether the model followed copied reports or misleading prior choices: both pointed to the same wrong answer. Its self-review wording was also ambiguous. The new [D1 plan](d1/PLAN.md) separates those factors and makes the reports primary in every instruction.

First, eight clean three-source questions check basic capability. If that passes, 160 calls compare raw versus deduplicated reports with no prior choice, correct/wrong self choices, and correct/wrong peer choices. The practical question is whether normalizing sources in code improves model decisions, and whether prior choices undermine that improvement. These are fixed synthetic patterns with two repetitions, not independent real-world trials or an interacting swarm.

**Status: offline preparation complete; material design decision pending; no new machine or model calls.** [The review and runnable handoff](d1/RUNBOOK.md) explain the evidence, gates and commands. Researcher review remains waived. The maximum 168 new calls reserve $0.225792 within the existing cumulative $1 API budget; no replenishment. Historical Q1/M1/C1 plans remain available but are not the next launch path.

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-quorum-mirrors; source `be37f8b4` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — A native reader can make the evidence-based MAP choice on the small S0 fixture screen; source-aware swarm efficacy is untested. Basis: S0 passed its narrow reader screen. The repaired Q1 produced 16 valid responses but 0/8 correct full-lineage choices; all choices aligned with report majority. Finite scripted fixtures do not establish causal peer influence or swarm efficacy.
- **sample_size_summary:** S0: 16 fixed configurations, 32 valid calls, 29 MAP-correct. Q1-01: 1 contract-failed, 15 unstarted. Repaired Q1-02: 16/16 valid fixed-context fixtures, 0/8 graded MAP-correct; eight partial cases ungraded. No independent worlds or M1/C1.
<!-- experiment-evidence:end -->

## Reproduce and inspect

From this directory, `python3 reassess_s0.py` regenerates the retrospective data and explorer using only saved inputs; `python3 -m unittest discover -p 'test_*.py'` checks the instruments. Neither command calls a model or accesses credentials.

- [Iteration 3 analysis plan](ITERATION-3.md), written before its implementation, explicitly retrospective.
- [Original QM-2 plan](PLAN.md), historical design; current S1 amendments and gates are in S1-PLAN.md and SETUP.md.
- [S0 prospective plan](reviews/S0-02-pre.md), [post-mortem](reviews/S0-02-post.md), [zero-call failed attempt](reviews/S0-01-post.md).
- [Review history](REVIEW.md), [required setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.
