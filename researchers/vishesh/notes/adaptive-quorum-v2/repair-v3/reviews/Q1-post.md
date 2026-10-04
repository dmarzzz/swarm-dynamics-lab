# Q1 post-mortem

Execution complete, qualification failed: 22/22 cases completed, zero invalid; 16/16 core, 5/6 boundary. All four labels scored 4/4. 66 physical calls, 198 logical predicate evaluations. The failed case `edge-2` has retention one day for every provider: target NONE, model chose A. Atomic receipts identify retention interpretation as the defect. It is not a threshold-accuracy or infrastructure failure. [All outcomes](../results/Q1/results.jsonl).

Next architecture amendment: model eligibility is intersected with a deterministic hard-constraint guard on the **observed** typed row. The guard has no hidden fixture access. It can block a falsely admitted provider but cannot repair false source data, certify provider policies or force a model to admit an eligible one. Log every model-versus-observed eligibility discrepancy and block. This is explicit defense in depth, not evidence that the model learned the constraints. The strongest baseline remains pure symbolic selection, which may make the model superfluous for this toy environment.

Q2 uses disjoint task IDs and changed boundary values, preserves all Q1 records and tests the original one-day bug offline. Qualify before sweep. D0/Q1 visuals use the declared static diagnostic mapping; temporal rendering is tested separately. No budget overrun, holdout access, paid inference or outcome retries occurred.
