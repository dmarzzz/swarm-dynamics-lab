# Pre-run assessment: q0-a1

- Experiment / owner / stage: sybil-scale-xl A1 / dmarz (operator dmarz/scale-xl) / Q0, claude-opus-5-5, effort low.
- Parent: s0-a1 must pass at the same source hash (the coordinator enforces this).
- Status: ready after s0-a1 passes, the claim on sim-dmarz is still exclusive, and the study ledger is empty. dmarz chose the trimmed Opus design and its cost range (AMENDMENT-A1.md).
- Design: 4 clean worlds (5000–5003) × `sample` and `common_only` packets × visible × 3 sizes = 24 calls. Per-size thresholds unchanged: 100% structural validity, ≥95% field accuracy, ≥90% exact packets, 100% abstention on missing facts.
- Plan: 4 in flight, 300 s timeout, no retries, first failure stops dispatch. Each call is preceded by a free count_tokens request that sets its reservation. Expected spend USD 7–12 including output.
- Risks: first use of Opus with this request shape. A thinking-related failure (max_tokens stop, refusal or a non-text block) stops the stage. That is a design repair with its own attempt, not a retry.
- Records to keep for S1: input tokens per size measured by Opus, output and thinking tokens per call, latency at N=8,748.
- Visualization: qualification view per size (mapping v1).
