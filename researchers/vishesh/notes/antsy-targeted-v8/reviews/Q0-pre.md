# Q0-attempt-1 prospective assessment

2026-10-04, vishesh/codex-methods. Owner requested the next run. Same-author assessment; researcher review not required by owner directive. Read development-02-post and Amendment01. This document authorizes preparation, not a bypass of admission.

## TLDR

Test whether RapidOCR and the candidate EasyOCR can each reliably extract receipt totals before comparing targeted verification. Fresh train60–79, 20 paired receipts, 40 OCR calls maximum. Each reader must produce at least 50% correct totals and no more than one wrong acceptance among at least 16 scorable receipts. No execution errors or missing journal outcomes. Failed qualification stops; no S1 or repair is automatically admitted.

## Instrument and resources

Freeze the corrected field parser unchanged. Original pixels only; RapidOCR 3.9.2 with v7 ONNX hashes and requirements. Separate checker environment: EasyOCR 1.7.2, torch 2.6.0 CPU, torchvision 0.21.0 CPU, English+Indonesian, CRAFT and latin_g2, greedy decoding, detail=1, paragraph=False, workers=0, batch_size=1, quantize=False. Pin all resolved package versions and model SHA256 before the first native call. Official model download checksums are verified before deserialization; no download at inference. This is the first native test of the checker, not a passed development test.

One process at a time; fresh worker subprocess and memory per receipt/reader; one inference thread; 45 seconds per call including cold initialization. Fixed P then C order; measured latency is cold pipeline time, not isolated recognition throughput. Stop before another call after any execution error or 25-minute collection limit. Record remaining assignments unstarted. No retries or engine substitutions. The orchestrator verifies native imports before collection but does not call an engine for an uncounted smoke test.

Use an idle, exclusively claimed approved-team host through the private run queue. Zero hosted-model calls and zero new billable infrastructure; inherited Antsy lifetime exposure remains unchanged. Existing free/allocated capacity only; do not provision a chargeable host under this request. If unavailable, queue instead of borrowing capacity. Allocation/current budget receipt and exact source, public-plan/page and runtime hashes are mandatory. A local runner is not permission to dispatch from a laptop.

## Data and scoring

CORD-v2 revision 7f0115a4b758a71d6473b8d085751692da2fef98, train60–79 only. Reject duplicate image hashes and overlap with v4, v6, v7. No test50–99 input is loaded. Pixel-only child process receives image, engine configuration and model directory, never annotation or another reader's answer. Evaluate after both outputs. All 20 assigned cases stay in the denominator; unknown truth is reported separately. No post-Q0 parser tuning or threshold relaxation. Numerical policy comparisons are exploratory diagnostics, not S1 efficacy.

## Visualization mapping

Run antsy-targeted-v8/Q0-attempt-1. Per completed receipt, retain cumulative correct/wrong/refer/unscorable counts for P and C and five fixed policies; x is completed receipts, y is receipt count. A final PNG and animated GIF replay this measured trajectory, beginning with zero observations. Failure states display completed and unstarted counts. Do not expose raw OCR, merchant/customer text or receipt images. No native frame.json schema is assumed; upload progress metrics and PNG/GIF supported by the live site. The post-mortem checks final chart numbers against JSON and records publication/readback status.

## Acceptance and closeout

Before dispatch: all offline tests, immutable plan and this review available publicly, live page verified, exact resolved runtime frozen, exclusive merged claim current and no other worker, cumulative cap receipt, unique attempt lock and empty output directory. On completion: reconcile journal/records, publish qualified=false if any gate fails, upload sanitized artifacts, verify readback, retain private inputs, release only this claim. Failures go to vishesh/codex-methods for diagnosis; the orchestrator must not relax the plan. A successful Q0 still requires separate S1 admission.
