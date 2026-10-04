# Antsy v8: can a second reader earn its place?

## TLDR

Before asking two agents to verify receipts, establish that each can read totals competently. This fresh qualification compares RapidOCR and EasyOCR on 20 real receipt images. Each must reach at least 50% correct totals with at most one wrong acceptance; all 40 calls must finish validly. This is a small competence screen, not evidence that two agents beat one. A failed screen stops the sequence.

## Question and prediction

Does replacing the weak Tesseract checker with EasyOCR produce a competent second perception path for targeted receipt-total verification? The primary parser repaired two concrete errors on used data. Its apparent gain may not generalize. We predict neither a pass nor independence from engine identity: fresh evidence decides whether a comparison is worth running.

## Setup

Twenty CORD-v2 training receipts, indices60–79 at revision7f0115a4b758a71d6473b8d085751692da2fef98. Original-image RapidOCR3.9.2 and EasyOCR1.7.2 (CRAFT/Latin gen2; English+Indonesian; CPU). The engines share pixels and the conservative field parser; differences are not independent evidence sources. Exact package/model fingerprints are frozen by the operator before inference. No receipt annotations, peer outputs or case labels enter either worker. Test50–99 remains unopened.

## Protocol

Fresh subprocess for each reader and receipt, P then C; one thread, 45-second call limit. EasyOCR quantization is disabled for recognizer and explicitly for detector because its1.7.2 Reader stores the detector flag as a tuple. Import/weight checks do not make OCR calls. No uncounted warm-up, retry, alternate engine or automatic next stage. At most40 OCR calls, zero hosted-model calls and zero new billable infrastructure. Use an existing idle exclusive approved-team allocation through orbital-one. Stop on an execution error; retain partial and unstarted counts. Preserve all historical Antsy spending rather than creating a new allowance.

Qualification requires20 complete paired receipts,40 valid journaled calls,at least16 scorable references, and each reader >=50% correct with <=1 wrong acceptance. No threshold relaxation. See [pre-run assessment](reviews/Q0-pre.md), [original design](PLAN.md), [amendment](AMENDMENT-01.md) and [previous post-mortem](reviews/development-02-post.md). Reviewer sign-off is not required by owner directive; no independent validation is claimed.

## Metrics

Correct, wrong, referred and unknown-reference outcomes per reader; all assigned/started/terminal/unstarted counts; paired same-wrong and shared-missing counts; checker rescue of primary abstentions versus correction of confidently wrong primaries. Five fixed policy diagnostics include the primary singleton, checker singleton, targeted fallback, always fallback and agreement. Policy costs reuse measured cold-process durations; they are not randomized end-to-end workflow latency. Fallback cannot repair a confidently wrong primary by construction. No effective-population-size claim.

Live progress counts receipts and valid calls. Final plots and GIF show the actual cumulative outcome history, with no raw receipt images or text. Results and the post-mortem will distinguish execution completion from qualification. S1 requires a matching qualified instrument and a separate admission.
