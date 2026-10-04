# Immune Response — A7 HTTP400 diagnostic

Retrospective owning-agent review,2026-10-04. [Run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-195440-d3cac7). Runtime `d64febc4179eecf136eeb4bd3203c200e58bd29a`; [prospective plan](../DIAGNOSTIC-A7.md), [reconciliation](a7-reconciliation.json), [rubric](a7-quality.json).

## Finding

The failure reproduces as a **schema-invalid/unsupported provider error**. It is specific to the composed controller schema in this three-request diagnostic; ordinary structured output succeeds on the same route and input. Completing the union branches did not fix it. This narrows the cause substantially but does not identify one exact rejected schema rule.

| Condition | Only change from original | Result | Known API cost |
|---|---|---|---|
| Exact A6 controller wire | None; byte serialization/hash matches | HTTP400, schema-invalid/unsupported | Unknown; reservation retained |
| Complete branches | Each anyOf branch typed, required and closed, including reason | HTTP400, same error category | Unknown; reservation retained |
| Flat transport control | Remove anyOf; retain top-level fields | Successful Anthropic Haiku4.5 response | USD0.001441 |

All other request fields, supplied fictional observation and two retained experimental advisor statements were identical. All three requests were inspected. Both parsed error envelopes mention schema-related keywords including anyOf, additionalProperties, required, type and properties. Those are allowlisted indicators, not an exact error quotation or proof that each keyword is defective. Raw error text was deliberately not retained. The original A6 error body is still unavailable; this new exact replay supplies the reproducible classification.

[Anthropic's documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) supports anyOf with limitations and requires closed objects. Therefore it would be incorrect to claim that Anthropic universally rejects anyOf. [OpenRouter's structured-output documentation](https://openrouter.ai/docs/guides/features/structured-outputs) also distinguishes supported model parameters from schema validity. Generic JSON Schema validation is insufficient to establish hosted acceptance. Both rejected variants combine top-level properties with anyOf branches; the diagnostic did not isolate that composition from every other schema feature. No conclusion about which layer (OpenRouter transformation versus upstream validation) rejects it is supported by the retained classification.

## What this rules out and what it does not

A general credential failure or unavailable model is inconsistent with the successful flat control minutes after the rejected variants. The matching-payload comparison supports schema-specific rejection. This is not a randomized replicated provider experiment and does not prove universal behavior across time or routes. It does not justify more agents, a model upgrade or additional budget.

The successful control returned inspect/none/0 with a request to verify the already-current healthy probe. Its answer conforms to both schemas, but no action executed. One valid answer is neither proof of useful repair nor resolution of the earlier advisors' factual errors. The flat schema deliberately admits invalid action combinations, so simply reverting to it would reintroduce A5's interface mismatch.

## Execution, accounting and integrity

A zero-request startup attempt failed importing the worker. The original marker and log were preserved; a fresh-process import test and corrected initialization passed before the same three still-unstarted assignments resumed.29local and remote tests passed, including exhaustive equivalence of the ten admitted actions and bounded error redaction. Only the expected400 continued to the next distinct preassigned condition. No request retry, fourth call or simulator transition occurred.

All3request/usage hashes reconcile, including exact A6 replay bytes. One response, two400errors, no missing assignments. Six hub artifacts were fetched and hashes matched; full transport and relay journal remain in local retained evidence, not falsely described as public raw trace coverage. Known actualUSD0.001441; reservationsUSD0.022768. Cumulative411calls/USD3.352050reserved of originalUSD8. Two new calls lack usage; their reservations remain. No new machine or allowance. Existing shared-machine allocated cost is not separately measured. Worker/relay/tunnel stopped and allocation released after evidence backup. Offline finalize completed; its model_calls0 means no new calls from finalization, not zero native calls.

## Decision

Operational diagnostic complete; scientific qualification remains on hold. Reject the hypothesis that adding complete branch definitions alone fixes the interface. Do not revert to unconstrained action combinations. A next offline repair should use a simple flat enum of legal action identifiers with a deterministic one-to-one decoding to action/service/version, then exhaustively verify equivalence and preserve reason text separately. This removes the problematic schema composition without permitting impossible actions. It changes the response contract and needs a prospective bounded qualification before deployment. Alternatively isolate root composition in a separately specified request-level test if identifying the exact parser rule has practical value. No successor is launched automatically.

The three-row table is the complete visualization: there is no native animation because nothing acted on a simulated service. The full prior qualification gates remain required after hosted transport acceptance. This is an owning assessment, not an independent review.
