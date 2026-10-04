# Post-mortem: fleet-s0-001

- Run: `sybil-specialists-opus/309db47b`, batch s0-001, scripted backend. Host sim-dmarz-4, exclusive claim `dmarz-sybil-specialists-opus` (agentops PR 202), operator dmarz/orbital-orchestrator.
- Source: swarm-lab `d8c7ee0d2ee37d9cb8a2b5767d4777edc8431dd5`; runtime hash `4b4b866a86fca1f8cd4b0eb1420303b1937462d5722b5061fcd7c9ed646cd562`. The study has its own checkout and venv on the host. Both selftest suites passed on setup.
- **Result: pass.**
  - Reconciliation: 216 planned, started, terminal, graded and analyzed; 0 invalid.
  - Scripted qualification on the fresh worlds 3100–3105: 24/24, with field accuracy, exact packets and abstention all at 1.0.
  - Elapsed time: 17.6 s.
- **Resources:** 0 model calls, 0 tokens, USD 0. The ledger does not exist yet.
- **Invariant:** attacker admission at pass .10 (masked) is coverage .0741, degree .0370, random .0185 and no verification 0. This is identical to the Haiku pilot and to the Sonnet version's S0, as required, because admission is algorithmic.
- **Artifacts:** `verify` matched 7 artifacts to the hub hashes. The replay has 28 frames at 1800×1180, all decoded. The worker exited.

## One-call interface probe (outside the study ledger)

Rule 11 of the Opus request rules relayed by dmarz/fleet-monitor on 2026-10-04 requires an interface probe. Before any batch, I sent one request from orbital-one with the study's exact provider code at this runtime. It used engineering world 3199, which is outside both the Q0 set (3100–3105) and the S1 set (4000–4011), with full reports and visible badges. It ran against a throwaway ledger, not the study ledger.

| Field | Value |
|---|---|
| Result | HTTP 200, `end_turn`, one text block after thinking blocks were filtered; schema-valid six-value answer |
| Usage | 2,385 input tokens, 38 output tokens (including thinking at effort low) |
| Cost | USD 0.0103 (reserved 0.0984) |
| Latency | 3.4 s |

The request shape is accepted: no `temperature`, no `thinking` field, `output_config.effort: low` plus the JSON schema format, and `max_tokens` 3,000. This probe counts toward dmarz's shared allowance. It is not part of any stage and is not a study observation.

## Updated estimate for the paid stages

At the probe's usage (about 2,400 input and 40 output tokens per call), Q0 costs about USD 0.25 for 24 calls and S1 about USD 2.0 for 192 calls. Packets vary in size, and thinking length may vary by packet. The USD 40 reservation cap and the 300-call ceiling are the hard limits.

## Next

Q0 (24 calls) is ready at this runtime hash and waits only on dmarz's review decision.
