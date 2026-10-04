# Telephone A0 native authored fidelity diagnostic

2026-10-04, Vishesh / codex-village-fit. Prospective final scope following owner approval to run both authored and AI Village scopes. This diagnostic is separate from real-data evaluation. Researcher review is not required by owner direction.

## TLDR

Measure whether Claude Haiku 4.5 preserves clean original claims over three fresh-context handoffs. Eight original development roots, paired prose P, structured S and original-source lookup R, three hops each: at most 72 calls. Score supported obligation retention and unsupported assertions through reviewed semantic annotations. Copy/lookup is perfect; this diagnostic tests native fidelity, not model necessity, natural prevalence or AI Village effects.

## Question and prediction

Does the model preserve qualification, attribution, scope, time, correction, source dependence, unavailable-evidence uncertainty and polarity in simple answerable tasks? Structure might preserve more meaning than prose; exact source reopening may prevent accumulated error. No gain is expected over lossless copy. A clean ceiling closes this diagnostic; a fidelity miss identifies an observed model/interface limitation, not a license to redesign for a favorable result.

## Setup

Use exactly the eight inspected original roots in `../../t1/src/fixtures.py`, with three predeclared obligations per root. Freeze the exported source/gold files and assignment hash before dispatch. These are same-author development fixtures with shared background obligations, not eight sampled worlds or a held-out evaluation. Keep gold, trajectory fixtures, family labels and operator history outside actor payloads.

Use `claude-haiku-4-5-20251001`, temperature 0, no thinking/tools/caching, standard Anthropic Messages interface. Each request is fresh, with one user message and common system instructions. 8192 maximum input tokens, 512 maximum output tokens; count inputs through the provider count endpoint before generation, and fail closed beyond the limit. Enforce the serialized byte cap without truncation. Same model/settings in all conditions.

## Protocol

Seed 20261004 shuffles arm order within each root. Each chain has three consecutive requests. P receives originals at hop 1, previous prose only later. S receives originals at hop 1, previous structured claims only later. R receives original records plus its prior prose at later hops, using exact reference lookup over the entire three-record archive. R deliberately has more source access; this does not isolate formatting. No BM25/search-quality claim.

The first 9 calls, one complete root across all arms, are an interface checkpoint: stop on any transport, model identity, token accounting, truncation or structured-schema failure. This checkpoint is not semantic qualification. Continue only valid output collection; post-run semantic assessment of all 72 outputs decides clean-task fidelity. No retries, model switches or successor stages are automatic. A technical failure stops the whole attempt and leaves future assignments unstarted; retain uncertain cost.

Store exact experimental requests/responses privately with hashes, identifiers, usage, latency and safe failure categories. Raw source material here is original authored text; no operator transcripts or credentials enter evidence. Publish only reviewed original-text artifacts or safe aggregates. Count assigned, started, terminal, valid, reviewed and analyzed separately. A missing output is never zero retention; dependent hops stay unavailable.

## Metrics

Primary descriptive contrast: equal-root mean S minus P supported retention at hop 3. Report each paired difference and all-assigned worst-case bounds if missing. No population confidence interval from these eight authored roots. Also report per-hop retention, contradiction, unsupported critical additions, unknown support, citation validity, first observed loss, calls, tokens, latency and cost.

Use the T1 scorer after independent-from-generation manual semantic annotation. Two same-operator passes compare gold and evidence; disclose that this is not independent authorship. Parse validity never grants retention. Copy and exact lookup remain the 1.0 ceiling.

Clean-fidelity screen: all three arms retain at least 85% of critical obligations at hop 1, every uncertainty control preserves uncertainty at hop 1, and no unsupported critical commitment appears in ordinary controls. Review every miss and every trace. Passing applies only to these clean cases and this interface; real-data V0 has its own cohort and qualification.

## Resources and admission

A0 is authorized within the existing USD2 cumulative Telephone cap pending any exact higher-cap decision. Maximum API token charge at current standard rates is USD0.774144 (72 × 8192 input × USD1/M plus 72 × 512 output × USD5/M). Bound API exposure to USD1.50 and infrastructure to USD0.50 for this stage; no new ledger allowance for V0. No separate paid probe. One worker, one request at a time, maximum two-hour admitted window with a verified infrastructure rate that fits its reservation.

Before launch, publish/register this immutable URL with P/S/R condition TLDRs and verify the rendered public page. Verify source/runtime/tests, current exclusive allocation in the approved account, original cumulative ledger and precise credential routing. Use the established authorized queue/central launch workflow. No paid call before admission. After every outcome, reconcile costs/resources and complete operational plus scientific post-mortem. A0 does not automatically launch a different unready scope.

## Direct OpenRouter amendment before first native call

The [prospective execution amendment](../DIRECT-OPENROUTER-PLAN.md) supersedes provider, origin and budget details above. The owner authorizes direct dispatch, USD5 cumulative including existing infrastructure, and Haiku via OpenRouter. Use anthropic/claude-haiku-4.5 with Anthropic-only routing, no fallback/data collection and conservative UTF8-byte input counting plus framing allowance. Preserve original cases,72-call stage cap,512-token output limit and all semantic gates. No native call used the earlier provider contract. This is not a new allowance per stage.
