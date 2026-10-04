# Direct-route 429 diagnosis and repair

Prospective operational repair, 2026-10-04, before implementation. The owner requested diagnosis, correction and continuation. This authorizes operational investigation; it does not reset the cumulative budget or authorize a larger scientific cohort.

## Evidence and purpose

[D6](reviews/D6-post.md) ended on its first HTTP429, with no usable retry time, no response and no usage. The error body was deliberately discarded. Neither the missing retry time nor another study's failed call establishes the cause. Account-side access is currently unavailable: the authorized Console session is logged out. Coordinating studies have no confirmed account explanation. Metadata HTTP200 is not inference readiness.

Anthropic's [rate-limit documentation](https://platform.claude.com/docs/en/api/rate-limits), read 2026-10-04, describes request/token and acceleration limits, and monthly tier spend-cap errors that can return429 without Retry-After. The [limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api) requires an eligible admin or organization-scoped credential; the experiment's workspace key is not an appropriate substitute. Do not search for unrelated keys or switch providers.

## Offline repair contract

Add an explicitly opt-in HTTP error classifier for a later source-pinned admitted diagnostic. Read at most8193 bytes, accept only a complete JSON error envelope of at most8192 bytes, inspect provider type/message in memory, and retain only fixed enumerated labels. Unknown, ambiguous, malformed, oversized or unreadable bodies retain unknown cause. Never save the raw body, arbitrary message, URL, exception text or arbitrary headers. Labels describe the provider's reported reason, not independently verified account state. Preserve D6's default no-body behavior and immutable deployed source.

Tests must cover each supported reason, ambiguous explanations, misleading HTTP status, malformed/oversized data, reader exceptions, injected secret-like strings and integration with first-failure stop. Zero automatic retries remains the rule, including a reported Retry-After. No live calls or allocation are needed for these tests.

## Resolution and continuation

First obtain authorized Console evidence for the correct organization/workspace. For a confirmed transient request/token limit, prepare paced serial dispatch respecting the reported reset; coordinate shared throughput without stopping other workers. For spend or billing exhaustion, the account owner must resolve it within their authority. A different key or machine does not repair an organization-wide limit. Ambiguous errors remain unresolved.

After account resolution, the same two frozen D6 contract checks may be proposed as a separately registered recovery attempt: matrix first, typed only after a valid response with usage; no chair, no scientific cohort, zero retries, at most USD0.097280 conservative reservation. These are two contract checks on one inspected case, not independent samples or evidence of behavioral improvement. Before dispatch, bind the opt-in classifier, exact source/requests/validators, immutable public plan and condition TLDRs, fresh exclusive approved-account allocation, runtime tests and original ledger. This document is preparation, not admission or a runnable successor.

Original capUSD8, reservedUSD4.917472, calls247, unreservedUSD3.082528. Missing charges remain unknown. No new ledger, allowance or account-wide limit increase is implied. A successful acquisition permits assessment of a later feasible behavioral plan, not automatic D5 replay. Report execution, process, qualification and scientific status separately and complete closeout even after another failure.

## Offline outcome

Implemented the opt-in classifier in `analysis/acquisition_d6.py`; the historical runner does not enable it.81 tests pass, including six new tests for fixed labels, ambiguity/status checks, secret-text exclusion, bounded/failed reads, no-read default and a one-request stopped session with preserved reservation. No model call, allocation, quota change or account-side correction has occurred. Native diagnosis remains unresolved pending authorized Console access.
