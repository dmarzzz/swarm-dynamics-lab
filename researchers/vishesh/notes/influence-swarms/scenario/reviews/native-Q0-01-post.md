# Native Q0-01 post-mortem

Execution retained all nine assigned terminal outcomes, all invalid. Six API calls, USD 0.021259, no missing usage, no reporting errors. The first team report and independent generalist report in each case failed the citation contract, so downstream decisions did not execute. These are interface failures, not nine bad purchasing decisions.

Observed defect: the schema specified a single free-text citation string, while the task naturally required multiple records. All first-case findings returned comma-separated IDs in that string, rejected by the validator. The records also contain incorrect cost arithmetic; partial finance reports inferred unsupported totals. Original requests/replies and failed hub run are preserved.

Repair: findings carry citation arrays, IDs are constrained by the structured-output enum to supplied records, and a source-only worksheet computes weighted automation, software and human-handling totals from visible quotes/pilots/workload. It does not supply feasibility or a recommended choice and applies to every arm where the same inputs are present. Keep the final model choice unchanged. Use a fresh buyer profile for the amended qualification. Source/config changes prohibit using Q0-01 as qualification for S1.

Next native Q1-01 is a bounded diagnostic under the same exclusive claim and same unreplenished USD 1.40 subquota. Existing reservation consumed USD 0.089651 conservatively; actual usage was lower and is not refunded. Independent case review and production realism remain unproven.
