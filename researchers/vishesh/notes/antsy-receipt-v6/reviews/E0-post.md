# E0 attempt 1 post-mortem: instrument defects, not efficacy evidence

20/20 train receipts and 100/100 OCR calls completed without subprocess failure. All 20 references were ambiguous, so none of the accuracy numbers are usable. The ordinary reconciliation audit passed because it checked consistency, not whether the reference reader matched real CORD schema. This is a test coverage failure.

Root causes: valid_line.total.total_price includes label words; the actual field is gt_parse.total.total_price. All 20 structured reference totals were checked against their development annotation lines. Separately, Python CSV default quoting treated an OCR quotation mark as an opening multiline field and swallowed later TSV rows. Tesseract TSV must use QUOTE_NONE. This explains part of the unusually high missing-candidate rate. Preserve the original run and mark it failed instrument qualification despite successful process execution.

Repairs: use the structured reference field without fallback to cash/subtotal; regress real CORD shape, missing/malformed fields, and literal-quote TSV behavior. Fail before OCR when a stage has zero scorable references. Keep truly unsupported references unscorable. Add total initial pipeline cost accounting (fixed-B one pipeline, others three); no policy thresholds changed. 41 tests pass; six deliberately faulty implementations are detected. These tests do not replace external scoring review.

Decision: rerun the same 20 development receipts in a new attempt, then assess before opening test. No efficacy conclusion or test-set tuning. Raw TSV/images remain private run artifacts; retained public records are numeric. The measurement-only run had 0 model calls and no model/API spend.
