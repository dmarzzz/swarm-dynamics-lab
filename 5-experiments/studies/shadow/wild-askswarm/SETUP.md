# Setup record: wild-askswarm / robustness-v1

Owner/operator: shadow/sol-askswarm. Review independence: none claimed.
Status: authorized offline saved-data sensitivity and direct-text review, not a model experiment.
Runbook: [EXPERIMENT-SETUP](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md).
Operations guide: [OPERATIONS](../../../toolkit/agent-experiments/OPERATIONS.md).

## Ownership and question

Shadow's priority steer requests exact-dedup, provenance-root and timestamp-imputation
sensitivity for every AskSwarm answer, plus approximately 30 blinded link reviews.
Question: which descriptive answers and rankings depend on repeated rows, related artifacts
or fallback clocks? Intended decision: narrow the report's claims; share transforms with
halflife/identity. No causal inference, agent autonomy estimate or endorsement classifier.
Prior-art boundary: [NOVELTY](NOVELTY.md); original [PLAN](PLAN.md) and [FINDING](FINDING.md).
The baseline already disclosed inherited snapshots, unknown SwarmTraces actors/clocks and
unvalidated lexical proxies. This follow-up measures sensitivity rather than treating those
warnings as sufficient validation. No formal hypothesis, independent review or gated launch
is asserted. Original outputs remain untouched.

## Gate evidence

- G0: descriptive instrument only; no new experimental hypothesis or population inference.
- G1: pass, [ROBUSTNESS-PLAN](ROBUSTNESS-PLAN.md) committed before implementation (104619cf
  on main). Definitions include conservative wiki fallback-clock exclusion.
- G2: pass, 29 offline unit tests before dataset analysis, including duplicate semantics,
  recursive roots/cycles, unknown clocks, common-support ranks and evidence credit accounting.
- G3/G4: not an API dispatch/qualification; this is explicitly authorized local saved-data work.
  Budget USD 0, one nice-10 process, no fleet allocation or credential transfer required.
- G5: complete, [closeout](POSTMORTEM-ROBUSTNESS.md), [30-link direct-text review](AUDIT.md),
  [15-report arithmetic validation](results/robustness-v1/validation.json). All arms reconciled,
  no API calls, no semantic-adoption claim. Next action: consumers import the published helper.

## Design, provenance and operations

Frozen git ref: `4959a80b2e48050066630c5d22ea5d1fa1b0beb2`; dataset hashes in the original
results/source metrics. Source/package hashes written again in transformed reports. One process,
Python/NumPy only. No prompts/providers, no trials, no independent worlds or synthetic agents.
Input observations: 14,591 wiki revisions; 189,579 artifacts; 2,673 non-merge commits.
The 30-review sample is 15 links per available corpus, not a matched cross-swarm comparison.
Per-stratum Wilson intervals describe small audit uncertainty, not causal precision or IID
population inference. Same assistant builds/reviews; blinding masks identities/order/scores,
not necessarily recognizable text genre. No human review is fabricated.

```bash
python3 -m unittest discover -s tests -v
nice -n 10 python3 run_robustness.py --data /local/data --repo /local/swarm-lab --audit-local /local/outside-repo/audit
```

Immutable output namespace `results/robustness-v1` refuses overwriting. No resume or retry of
partial results as a fresh sample: retain partial outputs, diagnose, use a new named namespace
if required. Audit text remains outside git; only judgments, hashes and derived link IDs ship.
Visualization: full before/after HTML and static rank tables from the measured summaries.
No fabricated live temporal animation for an offline transformation comparison.
