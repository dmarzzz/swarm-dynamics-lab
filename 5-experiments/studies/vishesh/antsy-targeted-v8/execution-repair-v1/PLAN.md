# Antsy D1: locate the checker's latency bottleneck

Prospective repair plan, 2026-10-04. Owner/operator vishesh/codex-methods. **Offline implementation is authorized; this changed diagnostic has not been approved or run.** Preserve Q0-attempt-1, frozen source a3919814 and every original outcome. Read the [Q0 post-mortem](../reviews/Q0-attempt-1-post.md) first. This plan precedes repair implementation.

## Empirical unknown and decision

EasyOCR returned two valid results, then exceeded the45-second cold-call limit on train62 without phase traces. Was most observable time consumed by imports, reader construction or pixel OCR? Existing saved outputs cannot recover the missing timestamps. The experiment earns another diagnostic only if those timings can determine whether the unchanged cold-reader service is feasible or should be parked. This is an execution diagnostic, not fresh qualification, an engine comparison or evidence for swarm benefit.

If all planned calls finish validly within45s with complete traces, propose a separate fresh qualification; do not launch it. If any call exceeds45s or fails, keep qualification closed and use its last completed phase to prepare a specific repair or park the checker. A completed OCR result can inform parser inspection but cannot repair the original failed Q0. Missing/contradictory traces make the diagnosis inconclusive and stop collection.

## Fixed diagnostic design

- Attempt proposal: **D1-latency-attempt-1**. EasyOCR only; unchanged1.7.2 CRAFT/Latin-gen2 English+Indonesian CPU, quantization disabled, fixed seed and single-thread settings, identical parser and original image pixels.
- Exactly **three reused development receipt units**, CORD-v2 train60,61,62 at revision7f0115a4b758a71d6473b8d085751692da2fef98. Bind images to hashes in the Q0 trace audit. Dimensions576×864,576×864,960×1706; two smaller units and one larger unit. This is a deliberately small diagnostic with no population precision target. Image size and content are confounded, so do not claim a causal size effect.
- At most **two cold subprocess repetitions per receipt**, in fixed order60,61,62,60,61,62: six OCR calls total. Repetitions are nested timing observations, not six independent receipts. The reused inputs are openly development-selected; train80–99 and test50–99 remain unopened.
- **Cold only.** No persistent reader, inference warm-up, alternate model, resize, GPU or stronger-machine rescue. Same verified host class/runtime as Q0; record actual resource match before admission. Each process starts without peer output, gold labels, operator conversation or inherited agent memory. A warmed service would be a materially separate future design.
- Keep the original **45-second eligibility threshold**. The proposed diagnostic supervisor may observe for at most **90seconds**, solely to distinguish slow completion from continued noncompletion.90s is not a relaxed qualification threshold. Stop after the first completed call exceeding45s, timeout, nonzero exit, signal, malformed output or missing/inconsistent phase trace. Mark all later cells unstarted; no automatic retry.
- Reserve the full six-call envelope before launch. Ten-minute overall wall limit, one child at a time,90s execution ceiling plus at most2s process-group cleanup per call. Stop starts when insufficient time remains. Zero hosted calls, zero model/API charges, **USD0 new/incremental infrastructure**, existing idle exclusive approved-team allocation only. Historical Antsy spend/reservations carry forward unchanged; no new allowance. Provisioning is not needed or authorized by this plan.

The earlier RapidOCR observations are background, not a randomized latency comparator. D1's comparison is each cold phase and total time against the fixed45s service requirement; no treatment-effect estimate is planned.

## Instrument repair before any diagnostic

Work in this separate versioned directory. Do not edit the original Q0 instrument or results.

1. A child emits append-only fsynced phase events: worker start, imports begin/end, reader initialization begin/end, OCR begin/end, extraction begin/end, output begin/end. Events contain allowlisted phase names, sequence numbers and monotonic elapsed time only. OCR combines detection and recognition; do not claim finer attribution than these boundaries.
2. Parent records dispatch before Popen, then terminal status after child cleanup. Write stdout/stderr directly to private files throughout execution, preserving bytes even on timeout or signal. Retain any partial output and phase file; never forward raw exception messages/streams into a public report. Parent records only allowlisted failure categories, return code, counts, timings and hashes.
3. Bound execution with a dedicated process group; terminate and reap the exact group on timeout. Retain completed calls and unstarted assignments, refuse existing output directories, never retry. Fail closed on unsafe artifact paths or mismatched input hashes.
4. Retain valid raw OCR privately. Candidate parsing must be byte-for-byte equivalent to the frozen worker on fixture outputs. Fault tests exercise normal completion, errors, partial phase files, malformed output, timeout stream retention, child cleanup and collision refusal without importing OCR engines or making network calls.
5. Keep launch admission outside this offline helper: exact owner approval, immutable public plan registration, current budget/allocation, source/runtime and input hashes must be verified before a native entry point exists. A tested helper is not a launch receipt.

## Measurements, missingness and acceptance

Collect wall time, durable phase times, input/config/source hashes, raw-output hashes, stderr/stdout hashes, terminal category and child-stop evidence for every start. Report full planned/started/valid/failed/unstarted counts and explicitly distinguish execution validity, latency eligibility and OCR answer quality. A timeout is not a wrong total; a missing phase is not zero duration. No error-correlation estimate, confidence recalibration, accepted-error rate or efficacy conclusion is justified by three reused receipts.

Offline acceptance: fault fixtures prove data retention and cleanup; phase validation rejects missing, duplicate, out-of-order or nonfinite events; hashes and candidate contract bind normal output; no raw strings appear in public diagnostics; no future allocation or native inference during preparation. Before owner review, publish the exact tested repair source and evidence. If approved later, freeze a condition-specific public plan and all runtime/input hashes before dispatch; preserve a new D1 identity distinct from Q0.

## Closeout and boundary

Every eventual terminal outcome receives operational finalize plus scientific review. Publish numeric phase timelines, all-assignment accounting and sanitized diagnostic categories; retain raw streams privately. Read back uploaded artifacts, verify workers/children stopped and release the claim. Any successor qualification requires its own concrete owner-approved plan and retained cumulative budget. Researcher review remains waived; this is same-author development, not independent validation.

Expected value is narrow: identify the observable expensive phase and decide whether further work on this checker is warranted. Preparation and reporting time count against that decision even when monetary cost is zero. Park if these traces would not change the decision.
