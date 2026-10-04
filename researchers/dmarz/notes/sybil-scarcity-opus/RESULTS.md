# Results: does Sybil-resistant accuracy depend on repeated knowledge? (Opus 5.5)

Completed 2026-10-04. Exploratory chain 001 at source hash `b37af997…` (launch commit `3ebef1ce`), operator dmarz/orchestrator-2, ready request agentops #248. All four stages ran once: S0 168/168 scripted rows, P0 1/1, Q0 48/48, S1 1,440/1,440. No row failed, was retried or went unstarted. Total model cost USD 141.144916 over 1,489 calls. Same-researcher check only; the run is not independently reviewed. Sanitized records are in [records/](records/); the post-run review is [reviews/chain-001-post.md](reviews/chain-001-post.md).

## Primary contrast

Random auditing, 108 checks, attacker check-pass 0.1, visible badges, paired over 24 world roots:

| Truthful carriers per rare fact | 1 | 3 | 9 | 27 | 81 |
|---|---:|---:|---:|---:|---:|
| Specialist accuracy (Opus 5.5) | 4.2% | 13.9% | 54.2% | 95.8% | 100.0% |
| Rare facts with a truthful report admitted | 63.9% | 91.7% | 100.0% | 100.0% | 100.0% |

**One carrier minus eighty-one: −95.8 percentage points** (descriptive 95% bootstrap interval −100.0 to −88.9; 24 of 24 roots complete; 22 roots at −100). The predicted direction was a decrease and the practical marker 10 points; the observed decrease is about ten times the marker. Graded contrasts against 81 carriers: 3 carriers −86.1 (−95.8 to −75.0), 9 carriers −45.8 (−61.1 to −30.6), 27 carriers −4.2 (−8.3 to 0.0).

At 81 carriers the packet is byte-identical to the original sybil-scale-api packet; Opus scored 100%, matching the 98.6% Haiku anchor from that study.

## Why the drop is not only an admission effect (measured diagnostics)

In the primary cell at one carrier, a truthful report reached the admitted packet for 46 of 72 rare facts (63.9%). Opus answered 3 of those 46 correctly. Across all rare facts in that cell it gave the attacker's fabricated value 94% of the time and returned null 1% of the time. Same-packet scripted plurality scored 3%. In this cell an admitted packet carried on average 0.5 to 0.75 truthful reports and 5.6 to 5.8 copies of the attacker's fabrication per rare fact (attacker seat share 3.6%). The accuracy curve tracks that ratio: at 9 carriers (about 5 truthful against 5.8 false) accuracy is 54%, at 27 (about 14 against 5.8) it is 96%. So the synthesizer behaves close to a count of agreeing reports: when a truthful report is outnumbered by repeated fabrications it follows the repetition. This differs from the newcomer study, where accuracy stayed under the share of truth that was admitted; here most of the loss happens after admission. That is a reading of the measured diagnostics, not a separately tested mechanism.

## Other cells

Specialist accuracy by carriers (1 / 3 / 9 / 27 / 81), 24 roots each; full table with intervals and diagnostics in [records/s1-cells.csv](records/s1-cells.csv).

| Policy | Attacker pass | Checks | Accuracy by carriers |
|---|---:|---:|---|
| random | 0.1 | 4 | 4.2 / 8.3 / 20.8 / 31.9 / 61.1 |
| random | 0.1 | 64 | 0.0 / 8.3 / 43.1 / 83.3 / 100.0 |
| random | 0.1 | 108 | 4.2 / 13.9 / 54.2 / 95.8 / 100.0 |
| random | 0.9 | 4 | 4.2 / 5.6 / 12.5 / 23.6 / 36.1 |
| random | 0.9 | 64 | 0.0 / 0.0 / 0.0 / 0.0 / 27.8 |
| random | 0.9 | 108 | 0.0 / 0.0 / 0.0 / 0.0 / 27.8 |
| coverage | 0.1 | 4 | 0.0 at every level |
| coverage | 0.1 | 64 | 6.9 / 9.7 / 20.8 / 50.0 / 73.6 |
| coverage | 0.1 | 108 | 6.9 / 18.1 / 38.9 / 79.2 / 100.0 |
| coverage | 0.9 | 4 | 0.0 at every level |
| coverage | 0.9 | 64 | 1.4 / 1.4 / 2.8 / 18.1 / 33.3 |
| coverage | 0.9 | 108 | 0.0 / 0.0 / 0.0 / 0.0 / 5.6 |

- With weak checks (attacker pass 0.9), more checks do not help: random at 64 or 108 checks is 0% at every level below 81 carriers and 27.8% at 81.
- Coverage with 4 checks is 0% at every level and both check strengths.
- Policy-by-rarity interaction, (coverage − random at 1 carrier) − (coverage − random at 81): +56.9 points at 4 checks/strong (37.5 to 75.0), +33.3 at 64/strong (18.1 to 50.0), +2.8 at 108/strong (−5.6 to 11.1), +31.9 at 4/weak (15.3 to 50.0), −4.2 at 64/weak (−30.6 to 23.6), +22.2 at 108/weak (8.3 to 37.5). These are driven mostly by coverage's collapse at 81 carriers in low-budget cells, not by gains at one carrier.

## Integrity

`verify` passed for all four stages: assignments match the manifest, packet hashes and grades recomputed, summaries and analysis recomputed, artifacts match the hub. Invariance across carrier levels: 288 matched cells, 0 violations (audit targets, admission and packet order identical across c). 1,207 distinct packets among 1,440 assignments; identical packets are recorded by hash and not counted as extra worlds.

## Limits

One synthetic task, one graph family, one attacker strategy (one repeated fabrication), simulated checks and one model configuration (Opus 5.5, effort low, no temperature). Intervals are descriptive bootstrap intervals over 24 roots; no confirmatory or multiplicity-adjusted claim.
