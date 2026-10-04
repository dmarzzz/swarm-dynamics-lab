# Pre-run assessment: q0-a1

- Experiment / owner / stage: sybil-scale-xl A1 / dmarz (operator dmarz/scale-xl) / Q0, claude-opus-5-5, effort low.
- Parent: s0-a1 must pass at the same source hash (the coordinator enforces this).
- Status: ready after s0-a1 passes, the claim on sim-dmarz is still exclusive, and the study ledger is empty. dmarz chose the trimmed Opus design and its cost range (AMENDMENT-A1.md).
- Design: 4 clean worlds (5000–5003) × `sample` and `common_only` packets × visible × 3 sizes = 24 calls. Per-size thresholds unchanged: 100% structural validity, ≥95% field accuracy, ≥90% exact packets, 100% abstention on missing facts.
- Plan: 4 in flight, 300 s timeout, no retries, first failure stops dispatch. Each call is preceded by a free count_tokens request that sets its reservation. Expected spend USD 7–12 including output.
- Risks: first use of Opus with this request shape. A thinking-related failure (max_tokens stop, refusal or a non-text block) stops the stage. That is a design repair with its own attempt, not a retry.
- Records to keep for S1: input tokens per size measured by Opus, output and thinking tokens per call, latency at N=8,748.
- Visualization: qualification view per size (mapping v1).

## Interface probe (2026-10-04 ~08:10 UTC, before Q0)

One call from orbital-one with the A1 adapter at revision d8653369 and a probe-only ledger (not the study ledger): qualification world 5000, N=972, `sample` packet, visible badges. The answer parsed and matched all six expected values exactly. Usage: 23,536 input tokens (count_tokens gave the same number), 38 output tokens, 2.9 s, USD 0.094904 (reserved 0.25628). Opus therefore uses about 48 tokens per report, against about 36 for Haiku, which is the top of the assumed 1.0–1.35× range. At effort low the thinking output was negligible on this packet.

Revised estimate from this measurement: Q0 ≈ 2.45M input tokens, about USD 10. S1 ≈ 58.7M input tokens, about USD 235, plus under USD 5 of output if output stays near 40 tokens per call. **Total about USD 245 plus the USD 0.09 probe**, inside dmarz's chosen USD 200–270 range and the USD 330 ledger cap. Pinned runtime for S0/Q0/S1: revision d8653369, source hash 0384b4cd….
