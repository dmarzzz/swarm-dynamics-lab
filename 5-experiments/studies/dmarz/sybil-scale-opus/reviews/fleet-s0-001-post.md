# Post-mortem: fleet-s0-001, p0-001 and q0-001

Experiment sybil-scale-opus, owner dmarz (operator dmarz/orchestrator-2 for dmarz/scale-opus). Revision `80d70b7a9ec6ad489a0e36a3acfd704d488dada2`, source hash `621c867c6ff495da807988b90807ed7c82642c6112bc91c74271618572d0c96a`, host sim-dmarz-13, exclusive claim `dmarz-sybil-scale-opus` (agentops #267). Review: owner waiver (SETUP.md G0), not an independent review.

## Results (measured)

- Fleet S0 `sybil-scale-opus/f6e8f67e`: 264/264 valid, 0 model calls, USD 0; published.
- P0 one-call probe: valid, exact packet, all six skills correct, returned model `claude-opus-5-5`.
- Q0 `sybil-scale-opus/07d6ee3a`: 64/64 valid, qualification passed at every size; USD 3.094784. Study ledger after Q0: 65 calls, actual USD 3.128748, reserved USD 13.476368; no retries.

## Quality and failures

None. Q0 passing says Opus 5.5 at effort low reads the packet format at every size; it implies nothing about S1.

## Next run

S1 launched immediately on the software gate: `sybil-scale-opus/79bb3882`, 2,400 calls paired by world with the Haiku (`sybil-scale-api/56defc84`) and Sonnet (`sybil-scale-sonnet/afd8d5b9`) cohorts. Expected about USD 115 from Q0 per-call usage.
