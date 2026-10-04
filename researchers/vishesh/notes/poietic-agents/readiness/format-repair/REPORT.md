# Formatting repair, provider diagnosis and Haiku substitution cost

2026-10-04. Offline implementation and non-billable checks after D0-01. No model requests, allocation, model substitution, retries or changes to historical scores. The original ledger remains40 calls / USD0.482269482 API exposure; total exposure including prior infrastructure remains USD0.568560890.

## What is fixed and verified

The chat response policy `single-json-fence-v1` accepts a bare JSON object or exactly one complete lowercase `json` fence. It records whether normalization occurred and hashes both original and parsed content; original provider bytes remain retained. It does not infer missing fields, extract an action from prose, unwrap nested actions or repair syntax. Duplicate keys and nonfinite numbers fail. Existing model-route, billing, action-field, engine and protected-access checks still apply. The old `strict-json-v1` behavior remains available; frozen native runs are unchanged.

All121 offline tests pass, including fake-provider loopback handlers for both relay entry points and complete fake-worker rehearsals. Tests cover safe and unsafe formatting, all development lifecycle actions, protected endpoints, known billing after action rejection, strict historical behavior, full-reserve429 failures, HTTP200 provider-error envelopes, no retries and metadata containing secret-shaped strings. Saved-data replay of both returned D0 answers executes the expected fetch under the repaired instrument. Haiku's historical native score remains invalid; this replay is inspected development evidence, not a new qualification pass. [Replay receipt](saved-data-replay.json), [validation](validation.json).

## What the429 establishes

The third D0 dispatch was Qwen's answer request. The relay received HTTP429 and retained only a generic provider marker. The old logger discarded Retry-After, rate-limit headers and typed metadata. The responsible layer and exact limiting policy therefore cannot be recovered from those retained traces. There was no returned answer, so no semantic error can be diagnosed.

Current public catalog reads match the pinned Haiku and Qwen routes and tariffs and show both routes active. A non-billable authenticated key-status read succeeded and shows the configured per-key credit limit is not exhausted. This is current status only: it does not reveal account-wide balance, historical capacity, upstream quota or successful present inference. [Catalog receipt](catalog-check.json), [redacted key-status receipt](key-status.json).

OpenRouter documents429 from either its platform or the upstream provider, with rate-limit headers and typed provider metadata distinguishing cases when present. The repaired relays now retain bounded numeric retry/rate information and recognized error, provider and credit-limit categories. Raw headers, free-form messages, account identifiers and unknown metadata are excluded. HTTP200 bodies containing a provider error are now classified as transport failures rather than malformed agent answers. Worker records retain those safe fields. Unknown billing remains fully reserved; there is still no automatic retry or provider/model fallback. [Error documentation](https://openrouter.ai/docs/api_reference/errors-and-debugging), [limit documentation](https://openrouter.ai/docs/api_reference/limits).

The plausible explanation is temporary rate/capacity rejection, but the exact source is unresolved. Model substitution can avoid a model-specific bottleneck; it does not guarantee relief from account/platform limits.

## Qwen-to-Haiku cost

Verified pinned-route rates per million tokens:

| Model and provider | Input | Output |
|---|---:|---:|
| Qwen3-8B / Alibaba | USD0.117 | USD0.455 |
| Haiku4.5 / Anthropic | USD1.00 | USD5.00 |

Sources: [Qwen route catalog](https://openrouter.ai/api/v1/models/qwen/qwen3-8b/endpoints), [Haiku pricing](https://openrouter.ai/anthropic/claude-haiku-4.5), current catalog receipt above. Formula per call: input tokens × input tariff + output tokens × output tariff. Prices are unchanged from the completed diagnostic.

Haiku is8.55× the input rate and10.99× the output rate. At the one successful Qwen fetch's554input/16output token counts, it would cost USD0.000634 versus USD0.000072098, about8.79×. This holds token counts equal; different tokenization and generated lengths make it a counterfactual, not a measured all-task prediction.

| Replaced Qwen calls | Equal tokens from that one fetch: Qwen → Haiku | Added cost | Maximum-envelope added cost |
|---|---:|---:|---:|
|12, diagnostic role | USD0.000865 → USD0.007608 | USD0.006743 | USD0.142651 |
|48, qualification role | USD0.003461 → USD0.030432 | USD0.026971 | USD0.570606 |
|1000 | USD0.072098 → USD0.634000 | USD0.561902 | USD11.887616 |

The maximum-envelope column assumes every call uses the existing8192input/1024output ceiling: USD0.001424384 Qwen versus USD0.013312 Haiku per call. It is a conservative reservation, not an expected bill. For a more output-heavy1000input/100output example,1000calls cost USD0.1625 with Qwen or USD1.50 with Haiku. No cache discount, tax, credit-purchase fee or new infrastructure cost is assumed. [Full reproducible arithmetic](cost-analysis.json).

Keeping the current three-role diagnostic shape, replacing its12Qwen calls raises the complete36-call maximum API reserve from USD0.180965376 to USD0.323616768. That fits the remaining USD1.017730518 API allowance and USD1.431439110 total allowance, before any separately admitted infrastructure cost.

If we mechanically retain all144 qualification calls with48calls in the substituted role, the complete qualification maximum becomes USD1.294467072. Added to existing exposure, that would exceed the current USD1.50 API subcap by USD0.276736554. A reduced, justified call/token envelope or an explicitly approved subcap change would be needed before admitting that worst-case scope. Qualifying two effectively identical Haiku configurations may be redundant; any collapse into one model cohort is a separate design decision, not an assumed saving here.

Replacing Qwen removes the cheaper generative-model contrast. The swarm could still differentiate tools, skills, data services and finite-choice Jev roles, but it would not demonstrate Haiku-to-Qwen model-cost savings. The model selection has not been changed. Current disposition: offline repair complete; next paid scope and any substitution await a concrete owner decision and fresh admission.
