# Development replay02 post-mortem

## Plan and execution

Replayed the same 100 retained OCR observations from 20 already-used receipts (19 scorable). No new OCR calls, new independent samples, model downloads or fleet allocation. Corrected the two extraction defects diagnosed in replay01; retained that rejected attempt and exact parser source. The replay audit reproduces both reports, candidates and policy outcomes. Eighteen offline tests pass.

## Results and assessment

RapidOCR R0 improves from 11 correct / 0 wrong / 8 referred to 13 / 0 / 6 on reused data. Tesseract T1 reaches only 2 / 2 / 15. Targeted fallback reaches 13 / 1 / 5, so it adds an error without an extra correct result. Reject this checker combination. The primary improvement is a diagnostic finding vulnerable to development-set overfitting, not fresh qualification or a safety estimate.

## Remaining failures and next action

The parser defects have regression tests; the competence failure has not been resolved. Amendment01 proposes EasyOCR as a replacement candidate, with runtime/model staging and native admission still pending. Freeze its development instrument before fresh Q0; preserve strict per-worker thresholds and the unopened evaluation split. Do not claim diversity benefit from different engine names or escalate a failed qualification.

## Visualization and closeout

The results table and per-receipt numeric candidate/policy records support comparison. There is no new time-series animation because this is a deterministic saved-output replay, not a new temporal run; inherited timing is labeled replayed cost. Raw OCR remains private. No new workers or allocations require shutdown. Design/development delivered; native qualification pending.
