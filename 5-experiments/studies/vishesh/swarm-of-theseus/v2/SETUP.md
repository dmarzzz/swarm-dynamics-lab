# Experiment setup record: swarm-of-theseus-v2

Status: RETROSPECTIVE CLOSEOUT INDEX, recorded 2026-10-04 after both attempts. This index was not preregistered. Original prospective plans and receipts are unchanged. Follow [the setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

Owner/operator/design assessor: vishesh/codex-theseus. Same-author reviews and independent scoring implementation do not constitute different-researcher scientific review. Exploratory instrument; no accepted hypothesis or novelty claim. Question: can successors preserve useful procedures while selectively correcting obsolete ones? Primary planned contrast: evidence-tagged versus rolling inheritance after two replacement waves. No turnover comparison was executed.

## Gate evidence

| Gate | Status | Evidence / next action |
|---|---|---|
| G0 Research admission | Incomplete | [Social grounding](../redesign/SOCIAL-GROUNDING.md); formal survey/hypothesis and different-researcher design review remain unresolved. No formal promotion. |
| G1 Prospective design | Pass | [PLAN.md](PLAN.md), initial design commit cffb785; repair amendment before fresh seeds. |
| G2 Instrument | Pass within scope | 16 offline checks; [source](src/) and [assessment](ASSESSMENT.md). |
| G3 S0 and repair operational admission | Recorded | Immutable public plan/source/review receipts in both manifests; exclusive claim and budget in [deployment record](DEPLOYMENT.md). This is not certification of unresolved research admission. |
| G4 Qualification | FAIL | Both joint gates fail; [results](RESULTS.md). S1 blocked. |
| G5 Closeout | Reconciled | 24/24 terminal runs; 48 durable calls; zero missingness, invalid schemas or audit disagreements. Measured viewer/figure checked; worker exited, figure uploaded, claim released through merged PR119. Final artifact publication accompanies this record. |

## Design and instrument index

[PLAN.md](PLAN.md) defines scenario contracts, paired worlds, controls, sample limits, splits, exact model configuration, feedback cutoff and visualization mapping. [Runner](src/runner.py) binds startup/preflight, qualification and stop rules; [engine](src/engine.py) binds fork/reset/lineage; [provider](src/provider.py) stores exact repaired prompts and budget reservations. [Tests](tests/test_instrument.py) check treatment and leakage boundaries. Seeds 300/301 and repair 302/303 were used; S1 seeds were not dispatched. Two worlds per scenario/checkpoint, twelve dependent cases per metric cell; no precision or generalization claim.

## Attempt history

| Attempt | Pre-review | Reconciliation | Disposition |
|---|---|---|---|
| S0 | [Pre](reviews/S0-pre.md) | 12 assigned/started/terminal runs; 24 calls; 144 decisions | [Failed competence](reviews/S0-post.md) |
| S0-repair | [Pre](reviews/S0-repair-pre.md) | 12 assigned/started/terminal runs; 24 calls; 144 decisions | [Failed joint gate; stop](reviews/S0-repair-post.md) |
| S1 | [Blocked](reviews/S1-pre.md) | 0 dispatched | No turnover result |

## Closeout

Execution complete; schema validity passed; scientific qualification failed. Estimated API cost USD0.165211; conservative call reservations USD0.568098 within separate approved USD15 allocation. No refund/reset of conservative ledger. No provider retries. All failures retained. [Measured report generator](analysis/qualification_report.py) uses saved events only; no model calls. Post-mortems, this index and final report are retrospective; original pre-run documents remain prospective. Next action is a separately planned atomic/batched and decision-only/note-writing diagnostic, or a prospectively narrowed incident study, after resolving applicable research review gates. No further attempt is admitted by this plan.
