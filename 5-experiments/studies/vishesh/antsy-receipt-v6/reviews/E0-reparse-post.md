# Development subtotal repair post-mortem

E0-reparse-3: all20 assigned/scorable receipts and100 policy outcomes audited; zero new OCR/model calls. Three candidates on development receipt9 changed: A's40.00, B's40000.00 and E's40000.00 were all read from a hyphenated subtotal line and are now missing. Parent measurements and candidate-change ledger are preserved.

The apparent extra correct acceptance in E0 attempt2 was caused by subtotal matching the true total on this receipt. After repair: fixed-B and confidence each3 correct /1 wrong /16 refer; agreement, always-check and selective-check each3 correct /0 wrong /17 refer. Selective still uses34 check calls versus40 always, but both add no correct acceptance over initial agreement. All-pipeline candidate oracle3/20, new-correct checker headroom0.

This is a contract repair, not performance optimization: it lowers the apparent accuracy by removing a wrongly identified field. It also explains why score consistency and a few numerical fixtures alone were insufficient.46 tests now include actual schema, quoted TSV, hyphenated subtotal and immutable measurement replay. No claim of external independent review.

Proceed with the already registered test parser repair after its50 underlying OCR measurements complete. Extraction/policy code stays frozen. Original test decisions were not inspected to choose the fix. Replayed pipeline timings are inherited original measurements; the separate parser duration is recorded. This is not a second independent test sample.
