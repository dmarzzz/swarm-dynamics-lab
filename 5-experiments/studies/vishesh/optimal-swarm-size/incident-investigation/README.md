# Offline incident investigation prototype

**Implemented and validated offline.** Nine authored development cases from three templates; 18 deterministic reference executions and 12 semantic/fault tests pass. No hosted agent was called. This qualifies the small simulator's stated behavior, not model capability, real incident performance or an optimal swarm size.

| Structure | Evidence and remediation | Query rounds: 1 slot | Query rounds: 3 slots |
|---|---|---:|---:|
| Independent | Three services; separate metrics, release and handshake evidence; three independent faults | 9 | 3 |
| Serial | Gateway trace reveals the next dependency handle; protocol fault at hop three | 3 | 3 |
| Mixed | Three metric queries reveal a shared pool; redistribution must respect capacity | 4 | 2 |

These are unit-duration simulated acquisition rounds. Every row uses the **same reference algorithm**, with different tool capacity—not a different number of agents. Repairs and query counts are reported separately. The serial handle restriction models addresses learned from trace evidence; it is not a sleep inserted to make serial execution slow. Newly discovered handles become available only in the next query batch.

## Cases and ground truth

Each structure has fault, clean and insufficient-evidence conditions. The independent fault combines capacity shortage, revision drift and protocol mismatch. The serial trace has healthy intermediate hops and an upstream protocol mismatch. The mixed fault has allocations 2/2/5 against demands 3/3/3 and capacity 9: atomic redistribution to 3/3/3 works; increasing either deficient service first exceeds capacity and is rejected. Reducing the oversized pool before increasing the others is a legal sequential alternative.

Actor observations provide logs as structured span/release/handshake records, metrics and dependency handles. They contain no condition label, gold diagnosis, repair recommendation or future/unissued records. Warnings are plausible distractions rather than sufficient causal evidence. The reference consumes only `start`, `query` and `act`, cites relevant evidence, and repairs from those observations. The evaluator separately checks authored cause labels, supporting citations, terminal configuration and capacity constraints. Tests use a second, hand-computable state oracle: revision r2, protocol 2, at least three units per service, and total nine in the shared-pool case. This is same-author cross-checking, not an independent audit.

All three clean cases require no repairs. A no-fault claim requires inspection of the full reachable evidence, preventing an uninvestigated clean guess from passing. All three insufficient cases withhold one critical record: the reference escalates without guessing or mutating state. Correct escalation is separate from physical recovery and diagnosis accuracy. There is no silent exclusion of missing evidence.

## What was checked

- All nine cases at both capacities: correct cited resolution and recovery, or justified escalation; 18/18 reference outcomes.
- Expected acquisition rounds and per-round capacity; speculative handles and same-batch use of newly discovered handles rejected.
- Wrong diagnosis despite a correct final state; wrong final state despite a correct diagnosis; citations that exist but do not support the claim.
- Unsafe shared-pool increase rejected without mutation; safe atomic and sequential alternatives.
- Clean guesses without investigation and guessed resolutions of incomplete cases fail.
- Five opaque-ID/order variants per structure and changed irrelevant warnings preserve valid solutions. These are robustness mutations, not independent incident samples.
- A meaningful protocol counterfactual removes the diagnosis when both public evidence and underlying state become healthy.

[Prospective plan](PLAN.md) · [Simulator and reference](prototype.py) · [Tests](test_prototype.py) · [Validation summary and source hashes](results/validation.json) · [Complete reference traces](results/reference-runs.json) · [Evaluator-only development corpus](results/development-cases-evaluator.json).

Run from this directory: `python3 validate.py`. It rebuilds the deterministic evidence and runs tests without network access. Evaluator corpus files are for offline scoring and must not be inserted into future model inputs. `ActorTools` is a programming interface, not a security sandbox; a future native launcher must explicitly serialize only actor packets and returned tool evidence.

## Case-quality assessment and limits

| Dimension | Assessment | Evidence / boundary |
|---|---|---|
| Decision relevance | Pass for instrument demonstration | Separates concurrent collection, discovered dependencies and shared remediation |
| Answerability | Pass on authored support | Reference witnesses; clean and missing-evidence controls |
| Labels and scoring | Pass on authored support | Independent literal state checks and wrong-answer/action/citation mutations |
| Actor isolation | Pass for exported tool interface | Public packet allowlist; no evaluator data passed to reference; no native sandbox claim |
| Mechanism contrast | Limited | Capacity effects within each template are controlled; structures differ in content and query count, so between-structure differences are not a pure topology estimate |
| Challenge and coverage | Limited | Covers faults, clean, missing and conflicting actions; only three simple mechanisms |
| Strong comparisons | Pass for offline reference | Correct deterministic solver retained; future single-agent batching and coordinated teams unqualified |
| Realism | Limited | Synthetic structured telemetry, static evidence snapshot, unit-duration queries; no noisy natural logs, real services, retries or calibrated latency |
| Independence and precision | Limited | Three authored templates with dependent controls/variants; no population estimate or confidence interval |
| Holdouts | Limited | Entire corpus is exposed development material; no untouched evaluation set |
| Robustness | Pass for declared mutations | ID/order/distractor invariance, counterfactual label changes, malformed actions and safety rejection |
| Reproducibility and cost | Pass offline | Source hashes, cases and full reference receipts; zero model calls and zero API spend |

The prototype demonstrates the intended mechanisms; it does not establish that this task is difficult for a model. A competent single agent with the same batching tools may match a team. Next native preparation must freeze an actor/tool contract, qualify that baseline, separate fixed capacity from added capacity, add genuinely independent cases where the intended claim needs them, and price a finite schedule. No forty-agent run or new allocation is included in this offline deliverable.
