# Post-mortem: s1-001

Experiment sybil-scale-sonnet / dmarz/scale-sonnet / exploratory S1 / 2026-10-04. Parent [q0-001-post](q0-001-post.md); [pre-run review](s1-001-pre.md). Run `sybil-scale-sonnet/afd8d5b9`; revision `f18f66da9de3fe82eebebc0f8113710cca3ab1c1`; runtime `a1a619f7e39bb608ba48871766e8d1366d923db2df0cb00524dd5a65faffb230`. Model `claude-sonnet-4-6`. Host sim-dmarz-3, claim `dmarz-sybil-scale-sonnet`. **Disposition: complete-valid-result.** No S2 advancement.

## What ran and what happened

2,400 planned, started, terminal, graded and analyzed; zero failures, missing outcomes, duplicates or retries; every one of 100 cells has 24 worlds. Launched 05:40:14Z; collection took 1,467 s and the worker exited about 06:05Z. S1 used 18,298,688 input and 91,680 output tokens, **USD 56.271264**. With Q0 (USD 1.983438) the study ledger shows 2,464 calls, all with reported usage, **USD 58.254702** actual against USD 204.840948 conservative reservation and a USD 240 cap. Expected cost before launch was about USD 50.

Primary contrast (coverage, visible, strong checks, 972 identities, proportional minus fixed): **+52.8 pp** (descriptive paired-world 95% interval +38.9 to +66.7), against +51.4 pp for the Haiku cohort. Sonnet is more accurate than Haiku in 73 of 100 cells (mean +4.7 pp), mostly where admitted packets contain fabrications. Attacker seat shares are identical across models, as expected, since admission precedes the model call. Full tables in [RESULTS.md](../RESULTS.md).

## Verification and visualization review

`publish` then `verify` passed for S0, Q0 and S1: all required artifacts present with matching checksums, four 1800x1200 images per run, 33-frame replay decoded, evaluator and analysis recomputation on the server match. Locally, `build_report.py` under Python 3.12 with pinned requirements recomputed all 2,400 packet hashes, evaluations and scripted baselines and matched the frozen analysis exactly. The Haiku records, fetched the same way, reproduced the committed Haiku results table byte for byte, and the decompressed assignment files of both cohorts are identical, so the world pairing holds. Figures were regenerated locally but not filed as Flight Deck artifacts in this close-out (the shared manifest was unparseable at the time); they remain on the hub run page.

The mapping v1 replay samples completion order, not simulated time; early prefixes have unequal cell counts. The generic S1 `qualification_passed` hub metric carries over from the original runtime; Q0 is the qualification and it passed.

## Experiment-quality assessment

The replication answers a narrow question well: does the population-scaling result depend on the synthesizer model? It does not: the primary contrast is within 1.4 points of Haiku's. A model change cannot affect admission, so the study cannot speak to admission policy design. The cross-model table is descriptive over 100 cells without multiplicity correction. Sonnet's higher abstention (1,598 vs 1,390 of 7,200 rare fields) and fewer wrong non-null answers (2,210 vs 2,756) are measured; the mechanism (discounting repeated reports) is inferred. All Haiku-study limits carry over.

## Failure and repair ledger

| Kind | Evidence | Cause / repair | Acceptance | Status |
|---|---|---|---|---|
| Reporting | First `verify` after Q0 refused `wrong_contact_image` | Artifact order on the hub; `publish` re-uploads final frame first, same bytes | `verify` passes | closed |
| Process | S1 launched 05:40Z before the owner's review waiver was written into SETUP.md G0 | Operating session relayed the waiver after launch; recorded at close-out with the exact words | G0 row records the waiver honestly | closed |
| Operations | orbital-one OOM at 06:07Z killed the operating session | Unrelated crawler crash loop; workers on the fleet were not affected; close-out done after resume | run complete, records intact | closed |

## Next run

No rerun. Successor options, not launched here: the fixed-attacker-resource identity-splitting design in [next-experiments-2026-10-04](../../next-experiments-2026-10-04/README.md) (proposal 3), or a different model family for synthesis. The claim `dmarz-sybil-scale-sonnet` is released with this close-out.
