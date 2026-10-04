# Post-mortem: fleet-s0-001 and p0-001

Experiment sybil-newcomer-opus, owner dmarz (operator dmarz/orchestrator-2 for dmarz/newcomer-opus). Revision `d289769aede95922dd69318087f1e27f7a304d12`, source hash `a21290e41d93c2634dd6824245cf9a8ce0900c9c00f1b9cb0c08640310206322`, host sim-dmarz-13 under exclusive claim `dmarz-sybil-newcomer-opus` (agentops PR #226).

## Results (measured)

- Fleet S0 `sybil-newcomer-opus/8f18e7d0`: 198/198 valid, 0 model calls, USD 0; artifacts published.
- P0 one-call interface probe on an engineering packet: valid parsed answer, returned model `claude-opus-5-5`, effort low, exact packet, 1,657 input and 38 output tokens, about USD 0.007. Its cost is in the study ledger; it is not a hub run.

## Quality and failures

None. The probe confirms the Opus 5.5 request contract (no temperature, no thinking field, JSON schema in output_config) returns a parseable answer.

## Next run

Q0 ([q0-001-pre](q0-001-pre.md)).
