# Post-mortem: Theseus v2 S0

2026-10-04 UTC. Source 3aead11342b0097ce098bf40f1e69e6f40b3b001. Execution complete; qualification FAILED; no continuity conclusion. Next action: one bounded repair on fresh seeds302/303, then stop or advance according to the unchanged gate.

## Assigned and observed

All 12 assigned two-checkpoint runs completed: 24 calls, 24 events, 144 case decisions. No provider failures, schema failures, missing outputs or independent-scorer mismatches. Estimated actual API cost USD0.103255; conservative reservation USD0.357357. All usage present. Public plan, condition TLDRs, allocation and exact source receipts preceded requests. Raw evidence retained separately from process compliance.

| Scenario | Explicit-rule stable | Explicit-rule changed/interface | Learner stable | Learner changed/interface |
|---|---:|---:|---:|---:|
| Release | 10/12 | 6/12 | 7/12 | 8/12 |
| Incident | 9/12 | 11/12 | 7/12 | 8/12 |
| Migration | 12/12 | 10/12 | 9/12 | 10/12 |

Gate was ceiling >=0.90 per scenario/checkpoint and stable learner >=0.75, with valid schema throughout. Several cells fail. The 612-call pilot was not started.

## Diagnosis and experiment quality

Verified: outputs sometimes cite false input values despite restating the supplied rule. Example: incident301 ceiling stable claims B:1 canary=true when its recorded signal is false, and selects canary; release301 ceiling stable says every A ledger signal is false although A:0 ledger signal and freshness are true. Other outputs add conservative requirements not present in the supplied rule. These are model application errors, not missing labels, scorer disagreement or evidence of cultural loss.

Suspected contributors, not isolated causes: dense nested JSON, long repeated identifiers, historical/feedback material competing with the explicit current rule, and operational language encouraging extra precautions. The clean competence ceiling unnecessarily included old historical examples and feedback. The historical learner also inferred more complicated rules than the finite generator intended. A compound repair cannot establish which contributor caused the problem.

## Repair and falsification

Before any new calls, publish S0-repair-pre.md. Format the same observations as compact tables with explicit columns and short unambiguous example labels; keep canonical current case IDs. For the ceiling only, supply current rule and current cases without old history/feedback. Explain the candidate rule family to all actors, but withhold the class-to-source mapping except in the explicit-rule ceiling. The learner still acquires that mapping from accepted historical examples. State that unnecessary checks count as incorrect; no generic conservative override. This narrows acquisition to an explicitly specified family, which must remain clear in interpretation.

Use the same pinned model, six cases per call, 900-token ceiling, 700-character notebook limit, action oracle, majority rule, thresholds and case generator. Fresh302/303 qualification only, 24 calls. No transport/semantic retries. Pilot400/401 remains unopened to model calls. If the repaired model still fails, no pilot: report capability/instrument mismatch. Do not lower the gate or keep rerunning to obtain a pass.

## Visual audit and evidence

Measured replay and 1800x1000 final frame generated from all24 saved events; raw outcome tables reproduce the score audit. S0 uses a single qualification reader, so lineage cards/crew-class curves are not relevant to this stage. The renderer initially used a crew-style clock for qualification; clarify checkpoint labeling before the next run. Live hub progress was recorded per event; standalone replay is delivered separately. No fixture is passed off as this model evidence.

Local full evidence bundle SHA256: 45ff0337c6aec2114890281e058674fdc363180aabe64f25d96a7d590a36d8e6. This bundle preserves the first attempt, including incorrect outputs. Same-author software audit is not independent scientific review.
