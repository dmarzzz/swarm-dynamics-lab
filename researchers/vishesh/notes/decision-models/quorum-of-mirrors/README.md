# Quorum of Mirrors: when nine reports are only three observations

**Does a group get better evidence when more agents agree—or can it just repeat the same source more loudly?** Quorum of Mirrors tests whether preserving source ancestry helps a group make better decisions when reports overlap.

Imagine an incident desk receives nine reports: seven copy one inspection saying “safe,” while two independent inspections say “unsafe.” Counting reports says safe, 7–2. Counting independent observations says unsafe, 2–1. Adding judges does not add inspections. This is an illustrative use case; the actual inputs are synthetic binary sensor reports with explicitly declared reliability.

The practical decision is whether to invest in **more judgments, better source tracking, or a simple deduplication rule**.

## What has actually run

Only the prerequisite reader screen, **S0**, has run. One model reads each packet with full source IDs and explicit deduplication instructions. There are eight bit triples at two reliability settings, each requested twice: 16 configurations, 32 calls. No agents talk to each other in S0; the swarm comparison is still pending.

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

The [current run roadmap](RUN-ROADMAP.md) starts with 16 context checks and a 64-call native copying/instruction screen. If that exposes an interpretable problem, four paired worlds compare peer discussion with judges reviewing their own answers, a pooled solver and deterministic rules. This buys a stronger control at the cost of very weak precision. [Fresh research findings](RESEARCH-GATES.md) narrow the claim to a controlled engineering replication; search saturation and formal survey/hypothesis acceptance remain open. The requested design review arrived with revisions, now addressed in the [review response](REVIEW-RESPONSE.md).

The next 16-call qualification instrument is now implemented and checked: [readiness and remaining steps](NEXT-RUN-READINESS.md), [frozen prospective plan](NEXT-RUN-PLAN.md). All 54 study tests pass; no new native calls or scientific worlds were generated.

**Launch status: operator preparing the next run. Researcher review is not required by owner direction.** Existing spending approval remains valid; no new paid calls were made for this analysis. [SETUP.md](SETUP.md) records the exact gates and next actions. Historical feedback is retained; it is not a pending approval.

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — A native reader can make the evidence-based MAP choice on the small S0 fixture screen; source-aware swarm efficacy is untested. Basis: The small predeclared competence screen passed; 14/16 repeated pairs agreed. Retrospective exact references score report counting 24/32 and root counting 32/32 on the same finite inputs. These are not native comparator arms or evidence of swarm efficacy.
- **sample_size_summary:** S0: 8 bit triples × 2 reliability settings × 2 identical-request samples = 16 configurations, 32/32 valid calls, 29 MAP-correct; not 32 independent worlds. S1 not run.
<!-- experiment-evidence:end -->

## Reproduce and inspect

From this directory, `python3 reassess_s0.py` regenerates the retrospective data and explorer using only saved inputs; `python3 -m unittest discover -p 'test_*.py'` checks the instruments. Neither command calls a model or accesses credentials.

- [Iteration 3 analysis plan](ITERATION-3.md), written before its implementation, explicitly retrospective.
- [Original QM-2 plan](PLAN.md), historical design; current S1 amendments and gates are in S1-PLAN.md and SETUP.md.
- [S0 prospective plan](reviews/S0-02-pre.md), [post-mortem](reviews/S0-02-post.md), [zero-call failed attempt](reviews/S0-01-post.md).
- [Review history](REVIEW.md), [required setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).
