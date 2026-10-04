# Development result: repair helps the primary, not the weak checker

**Not freshly qualified. No v8 native OCR or held-out calls were run.** We replayed the same20 previously used train40–59 receipts (19 scorable,1 unknown) from v7. Repeated replays are not additional independent samples. Development choices were informed by these cases, so gains require fresh qualification.

[Original prospective plan](PLAN.md) · [current amendment](AMENDMENT-01.md) · [setup](SETUP.md) · [failed prototype post-mortem](reviews/development-01-post.md).

| Worker / policy | Original correct / wrong / refer | Corrected spatial contract |
|---|---|---|
| RapidOCR original image |11 /0 /8|13 /0 /6|
| Tesseract PSM6 |1 /0 /18|2 /2 /15|
| RapidOCR enhanced image |9 /2 /8|11 /1 /7|
| Targeted R0→T1 fallback |not the v7 policy|13 /1 /5|
| Always require R0/T1 agreement |not the v7 policy|2 /0 /17|

All policies referred the unknown-reference receipt. The primary's corrected contract recovers two legitimate totals without an observed wrong acceptance on these development cases. It does not establish safety or unseen-data performance. Tesseract fallback adds one wrong acceptance and no correct completion; it must not be deployed as an improvement.

## What was fixed

The old parser required an entire reconstructed line to be a clean label-plus-number. A small word's bounding box could determine the row grouping and separate a legitimate amount from its label. The prototype instead forms an anchor-centered row and requires one exact, unambiguous numeric field to the right of a recognized total label. It preserves exclusions and records supporting observation/region hashes.

The first prototype was too permissive: it accepted `SUB.TOTAL`, and it accepted a generic total quantity despite an unreadable explicit GRAND TOTAL. We retained [replay01](results/development-01.json), added regressions, then blocked dotted subtotals and unresolved final-total fields before [replay02](results/development-02.json). The rejected [parser snapshot](archive/fields-v1.py) exactly matches replay01's recorded hash. Both versions reproduce their saved candidates, policies and summaries in the [same-author replay audit](results/replay-audit.json).

Wrong OCR digits remain wrong. We did not correct13,450 into73,450 or933,000 into33,000 using labels. The checker therefore still fails a sensible competence floor. A lower threshold would hide the problem, not fix it.

## Next design

Keep the strong RapidOCR primary and corrected field contract as candidates for fresh qualification. Replace Tesseract's proposed checker role with a separately qualified EasyOCR candidate, as specified in AMENDMENT-01. No superiority or independence is assumed from its name. Its normalization adapter is implemented and unit-tested without loading weights; exact package/runtime/model hashes remain to be pinned before native admission.

The main comparison is primary alone versus targeted fallback versus always-check agreement, with identical-decision always-fallback as a computation control. Fallback addresses primary abstention only. It cannot catch a confidently wrong primary; a later prospective error-detection cohort must test that separate question. No minority is selected using gold, and weak dissent gets no automatic veto.

The Q0 floor is deliberately stronger than v7: each selected reader must reach at least50% correct on scorable receipts and at most one wrong acceptance, with >=16 scorable, complete accounting and no execution errors. Fresh Q0 uses train60–79; one reserved repair uses80–99; test50–99 stays sealed. Failure means stop, not engine shopping on the same qualification set.

Eighteen offline tests pass, covering association boundaries, dotted/hyphenated subtotal, unresolved grand total, conflicting/multiple amounts, wrong digits, fallback semantics and malformed adapter output. These are software checks, not EasyOCR competence evidence. Read-only replay reused existing OCR durations for cost accounting and made0 new calls; it does not measure v8 runtime or establish a matched-compute benefit.
