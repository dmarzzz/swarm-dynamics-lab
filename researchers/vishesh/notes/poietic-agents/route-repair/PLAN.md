# Q30-05 proposed same-model provider qualification

## TLDR

Offline preparation only; no paid scope allocated. Test the exact GPT-OSS20B action contract on one newly pinned BF16 provider, DekaLLM, after the repeated DeepInfra refusal. Use48 fresh actions across12 worlds, retain the48-valid/44-correct/zero-protected-access gate, and permit at most two retries of explicit HTTP429 responses containing no output. Retries use Retry-After-aware exponential backoff plus bounded jitter, with54 total physical calls maximum. Provider stays fixed; no semantic/schema retry, timeout retry, fallback or main run. This is route qualification, not specialization evidence.

## Question and prediction

The previous route refused requests even at five-second spacing. Its exact quota mechanism remains unknown. A different provider serving the same nominal model and BF16 precision may restore availability, but different backend implementation can also change behavior. Qualify this as a new cohort; preserve both old refused calls and the120B pass. No hidden assumption that capacity, low-reasoning behavior or schema compliance follows from public catalog listing.

## Setup

Candidate `openai/gpt-oss-20b`, `dekallm/bf16`, no fallback, JSON-object mode, temperature0, low reasoning,8192 reserved input and1024 output tokens. Current catalog lists inputUSD0.029/M and outputUSD0.14/M. Record public metadata/terms and require fresh compatible metadata at admission. Enforce `require_parameters=true` and `data_collection=deny`; do not weaken existing account settings or assert zero retention without evidence. Only synthetic case contexts may go to the provider, never credentials, owner/PI conversation or other project data. Provider terms and data-policy eligibility must be explicitly resolved before launch.

Reuse the Q30-03 prompt/engine/scoring contract with new Q30-05 IDs and roots1100,1104,...1144. Provider and declared cost menu change only; neither prior20B cohort becomes qualified retroactively. Four dependent lifecycle actions per world: retrieve, answer, refresh, structural follow-through. Twelve worlds are readiness coverage, not population inference.

## Protocol

One owning dispatcher and original spending ledger. Before each physical attempt reserve its full cost; every rejected or ambiguous request retains its charge bound. One successful logical action contributes once to48-action scoring; physical attempts and raw refusals remain distinct records. Retries must repeat the byte-identical request and logical state with a new physical ID, only after an explicit non-streaming HTTP429 carrying a recognized error envelope, no output and no positive billed usage. A returned action, partial output, HTTP200 error, timeout, unknown transport outcome or invalid action ends retry eligibility.

At most two retries per logical action and six retries across the cohort,54physical calls total. Start with five-second minimum spacing. For retry number1/2, wait max(5seconds,5*2**(retry_number-1), any valid Retry-After) plus uniform jitter0–1second. A hint above60seconds, credit/auth/nontransient error, exhausted retry/call budget or insufficient remaining wall time stops instead of shortening the server's wait. Stop on a third refusal of one action or any nonretryable transport failure. No fallback/provider search in flight. All retry delays and classification provenance are safe enum/numeric receipts, never raw messages/headers. Unknown quota hints remain unknown.

The deadline leaves room for the full request timeout and cleanup. At most30minutes total allocation including staging, collection and release; native dispatch ends by20minutes after allocation starts. Live admission must bind source, immutable registered public plan, fresh runtime/provider metadata, approved-account exclusive claim and the original ledger's historical148rows. Do not reuse Q30-04 admission or its consumed time amendment.

## Metrics

Retain48 assigned outcomes plus up to54physical attempts; validity, exact correctness, first-attempt/refusal counts, recovered429s, missingness and protected access. Require48valid and at least44correct with no protected access. Report recovered transport separately from first-attempt reliability. Replay every request/action/effect/charge and verify actual provider, request identity across retries and pacing/backoff. No efficacy or causal provider-superiority inference. Stop and close honestly on another failed cohort.

## Budget and decision

Per-request reservation:8192*0.000000029 +1024*0.00000014 =USD0.000380928.54requests boundUSD0.020570112;30allocated minutes atUSD0.07143/hour boundUSD0.035715. Proposed maximum incremental all-inUSD0.056285112, round named allocation upward toUSD0.057. Historical cumulative exposureUSD0.630273610 remains; projected boundUSD0.686558722, withinUSD10 but not automatically approved. No machine is currently claimed. Stage success permits only a separate main-design decision, not automatic dispatch. Implement/test diagnostics and adapter offline first, then return exact source/plan and unresolved admission checks to PI.
