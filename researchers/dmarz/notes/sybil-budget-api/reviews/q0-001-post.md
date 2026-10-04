# Post-mortem: q0-001

Experiment sybil-budget-api / owner dmarz / API clean qualification / 2026-10-04. Parent: verified fleet S0; [committed Q0 preassessment](q0-001-pre.md). Run `sybil-budget-api/7b177592`, attempt 1. **Disposition: complete valid qualification; advance to S1.** The owner waived independent review; this is the operator's own engineering assessment. S1 is ready but has not been launched at this record. Formal S2 remains disabled.

## Execution and reconciliation

The run used revision `996a4af01ebfff3071b88c60914472b171798053` and frozen runtime `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`, identical to the qualified fleet S0 runtime. Host `sim-dmarz-4`, exclusive claim `dmarz-sybil-followups`. Model `claude-haiku-4-5-20251001`, two concurrent calls, no retries.

All 16 assignments were started, terminal, graded and analyzed. There were zero invalid, not-started or duplicate records. Each size, N=324 and N=972, returned 8/8 exact clean packets, with 100% field correctness and 100% required missing-fact abstention. Across both sizes, all 24 unobserved specialist fields correctly returned null. All structural outputs were valid. The clean competence gate passed at both sizes; security effectiveness remains unmeasured until S1.

Actual spend was **$0.322988**, from 319,968 input tokens and 604 output tokens. All 16 calls reported usage. The persistent study ledger records $1.018967 in conservative nonrefundable reservations; this is distinct from actual cost. Preparation and collection took 11.80 seconds, plus rendering. There were no reporting errors. At the verification snapshot, both follow-ups together had spent $0.366548, all 52 shared reservations were settled, none remained held, and the joint $60 guard was intact. Those shared figures are a point-in-time snapshot, not permission to ignore subsequent commitments. The finite budget-study worker had exited.

## Reproduction and visual verification

Five raw artifacts were fetched into the ignored local data directory. Using the matching pinned Python environment and unchanged frozen source, the final views and replay were regenerated from saved observations without model calls. The reporting verifier confirmed every assignment/episode ID, packet hash, verification count, graph metric, model evaluation, scripted baseline and complete analysis. All 16 records remain in the denominator.

Ten durable hub artifacts were verified. Initial/final images are 1920×1440; all 17 replay frames decoded. Seventeen frames is correct for 16 observed completion steps plus the initial state under the up-to-25-frame renderer. Local final-image inspection confirmed 8/8 exact packets at both sizes, all qualification metrics at 100%, and the cost rounding to $0.3230. The root operator also verified public GIF playback, observing the cursor advance from 0/16 to 16/16 and the correct final metrics. Public playback is therefore checked, not merely inferred from image decoding.

The Q0 visualization is a competence summary and measured call-completion replay. It does not imply conversations among the simulated identities, nor does clean success establish resistance to attackers. Small public evidence is retained in [q0-verification-summary.json](../q0-verification-summary.json).

## Quality and next action

There is no open qualification or reporting defect. Clean full-evidence and missing-specialist fixtures discriminate factual competence from hallucinating absent information, using worlds disjoint from S1. The model passed the predeclared thresholds without prompt changes or repeated attempts. No scientific conditions were selected or tuned from this qualification.

The already committed S1 assessment is ready: 2,880 calls across 120 cells and 24 fresh paired worlds, no retries, persistent study cap and the shared actual-plus-unsettled guard. Root refreshes the exclusive claim and shared budget immediately before launch. Only valid scientific outputs will determine the frontier; null or adverse effects require reporting rather than favorable-result reruns. Holdout 10000–19999 remains untouched. Next action: **advance to S1**, preserving this qualification and its artifacts.
