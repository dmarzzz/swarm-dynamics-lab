# Setup record: wild-identity saved-data reporting supplement

Status: offline archive report, not experimental launch authorization. Owner/operator: shadow/sol-identity. No independent design review claimed. This record follows the fields of the [setup template](../../../toolkit/agent-experiments/templates/experiment-setup.md) and [runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md); it is retrospective for the original census. The supplement plan was committed at `ef790b7b` before its implementation. Dates: 4 October 2026.

## Ownership and question

- Question: how sensitive is exact-name-reference activity to retained page text versus edit-hunk text?
- Decision: report an archive diagnostic, not an identity-churn coordination effect. Supplement conditional page-cluster uncertainty after the owner's 11:25 EDT audit request.
- Research status: post-hoc descriptive archive census. No accepted hypothesis, formal experiment, random treatment, model dispatch or causal identification.
- Prior art and caveats: [README.md](README.md#novelty-boundary); original [PLAN.md](PLAN.md); preceding failures and repair in the [lane log](../../../../lab/researchers/shadow/log/2026-10-04-sol-identity.md).
- Current stage: saved-data analysis only. Next action: reconcile supplementary totals/figure, run fixture and repo checks, and push the bounded report. Never escalate this record into authorization for model calls.

## Gate evidence

| Gate | Status | Evidence and next action |
|---|---|---|
| G0 question and research scope | Descriptive only | Prior-art boundary is in README; no formal hypothesis acceptance or independent review asserted. |
| G1 plan before supplement implementation | Pass for supplement only | UNCERTAINTY-PLAN.md committed at ef790b7b after census point estimates were known. Original census plan was schema-informed and post-hoc. |
| G2 offline instrument | Fixtures required | test_analyze.py and test_uncertainty.py; reconcile every supplementary event count to frozen summary.json. |
| G3 experimental admission | Not applicable to saved-data report | No new experiment, credentials, infrastructure or model dispatch. This is not a waived/passed experimental launch gate. |
| G4 qualification and scientific escalation | Not requested | No model, scenario or next-stage experiment. |
| G5 reporting closeout | Required | Supplement totals, plots and interpretation documented in FINDING.md, uncertainty.json and lane log. |

## Design and instrument index

- Frozen archive hashes and git cutoff: results/summary.json.
- Original metric script: analyze.py v1.0.1; supplement: uncertainty.py. Python standard library only.
- Units: paired page aggregates of dependent revisions. Independent exchangeable pages are an unverified bootstrap model, not an observed independent sample. Cross-page copying/shared actors are unmodeled. No claim of valid population coverage.
- Fixed seed 20261004, 2,000 resamples, percentile intervals; deterministic leave-one-page-out sensitivity. All rejected zero-denominator draws reported. No tuning based on outcomes.
- Controls: known-answer ratio/difference fixtures, identical proportions across pages, seed reproducibility, interpolation and zero-denominator failures.
- Visualization: original lifetime/Lorenz SVG retained; supplement static 1800px reference-fraction SVG. Static rendering is appropriate to frozen archive summaries; no live temporal experiment exists.

## Operations, admission and limits

Manual offline report. Analyze with `python3 uncertainty.py --data /path/to/DATA --results results` from this directory. No launch/resume dispatch supported. Budget: zero calls, tokens and provider charges. No secrets read or transferred; no host provisioning; one nice-10 local process, standard-library CPU only. No private data rows or page names published: only hashed per-page aggregates. Formal Flight Deck filing remains blocked as documented in README.md.

## Attempt history and closeout

Original census: complete; all source rows accounted for, ten fixture tests and 25 aggregate checks. Initial hunk newline bug repaired and re-run, recorded in lane log. No silently discarded rows. Supplement: five known-answer fixture tests before saved-data computation; totals must equal 13,692 attributed revisions, 5,065 snapshot-reference revisions, 2,164 hunk-reference revisions. The report's saved JSON records source/script hashes, valid/rejected replicates and leave-one-out failures. Reporting compliance is separate from causal identification or formal artifact filing.

Next decision: complete the valid diagnostic; do not launch a churn experiment without stable actor/time/read-exposure evidence and appropriate formal gates. This supplement does not repair historical registration or certify bootstrap assumptions.
