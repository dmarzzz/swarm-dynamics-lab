# E0 attempt2 post-mortem and fresh-test decision

Instrument qualification passes:20/20 assigned/scorable train receipts,100/100 valid OCR calls,100 policy outcomes,0 model calls. Independent classification tally and decision replay pass. All20 normalized references match the structured totals checked against development annotation lines. The prior invalid attempt remains preserved and publicly failed. Actual SVG/PNG is not a required format; the generated PNG and all GIF frames decode and the numeric figure counts match saved summaries.

| Policy | Correct / wrong / refer | Checks | Total measured tool seconds |
|---|---|---:|---:|
| Fixed B |4 /1 /15|0|35.8|
| Confidence |4 /1 /15|0|91.6|
| Agreement |3 /0 /17|0|91.6|
| Always check |4 /0 /16|40|281.3|
| Selective check |4 /0 /16|34|266.6|

Interpretation: selective checking recovers one acceptance relative to initial agreement, with6 fewer checks than always-check. It does not discover a new correct candidate: initial tools already contain every correctly recoverable total. All-five-candidate oracle is only4/20 and marginal new-correct checker headroom is0. This is a poor extraction pipeline for automation, not evidence that swarms perform well. Zero wrong acceptances among four accepted totals has an approximate95% Wilson upper error bound49%; it provides no safety guarantee. Most receipts are referred because the conservative anchored-line extractor produces no admissible total. Rejecting ambiguous/noisy strings is intentional; unsupported label/layout forms and weak OCR need separate development, not silent test tuning.

Decision: keep extraction/policies frozen and run the preplanned50 fresh test receipts as an exploratory bottleneck check. Prediction before test: checking may corroborate candidates and reduce referrals, but often wastes compute when shared OCR/extraction misses the same field. Ask whether any genuinely new correct total appears in transformed checks and whether accepted-error/coverage improve enough to justify cost. Do not proceed to model committees merely because measurement succeeds. No thresholds or candidates were selected to force a win.

Changes after E0 freeze are audit/reporting only: all-unscorable rejection, timeout-retention test, Wilson uncertainty, clearer outcome bars and all-case grid, optional labeled changed-case trace, formatting.44 tests and six mutation checks pass. Fresh S1 pre-run is linked separately. Independent external scorer review remains pending; these are internal audits, not an external endorsement.
