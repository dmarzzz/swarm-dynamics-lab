# Anthropic qualification amendment — prospective

2026-10-04 UTC, written before adapter implementation or paid calls. User explicitly selected the shared Anthropic setup already used by other experiments. The original OpenRouter proposal is superseded for optimal swarm size only. Existing $20 total authorization remains unchanged, including diagnostic, Q-A, Q-B and failed/ambiguous requests. Formal dmarz offline package review 2f5281f applies to the retained engine/evaluator/budget; new adapter checks and a bounded transport diagnostic are required before the Q-A batch.

## TLDR

Qualify the shared Anthropic transport with one minimal JSON call, then run the already reviewed 16-task N=1 engineering screen if the diagnostic passes. Compare requested/served model, usage accounting and exact diagnostic JSON; subsequently measure verified task success, quality, latency and cost. Both stages share one immutable $20 ledger. This is synthetic engineering qualification, not an optimal-swarm-size result or approval for Q-B/core.

## Question and prediction

Can the approved shared Anthropic credential access pinned claude-haiku-4-5-20251001, produce a complete JSON response and expose valid usage fields through the bounded process adapter? Expected minimal answer is {"ok":true}. Failure retains exposure and blocks Q-A until diagnosed. Passing the transport check is not task competence.

## Setup

Native endpoint https://api.anthropic.com/v1/messages, version 2023-06-01, pinned model claude-haiku-4-5-20251001; standard service tier, no tools, cache directives, thinking, geographical premium routing or fallback. Shared credential is consumed from the existing approved Keychain setup through an encrypted SSH stdin relay, never printed or written to public source. Process environment names SWARM_MODEL_API_KEY and optional SWARM_MODEL_WORKSPACE_ID match the other experiments.

Official model reference fetched 2026-10-04: https://platform.claude.com/docs/en/models/haiku-4-5/overview lists 200K context, $1/M input and $5/M output. Messages usage reference: https://platform.claude.com/docs/en/api/messages/create. Reserve the full 200000 input-token context plus 4096 output tokens: $0.220480 per call. Requests disable cache creation by omission; if cache usage unexpectedly appears, retain the full hold and stop rather than use an unreviewed discount/rate. A successful response with ordinary usage settles at the pinned rates, rounded upward to microdollars. Any unknown charge keeps its hold. This is conservative accounting at verified published rates, not a provider-side dollar limit.

## Protocol

First run one transport diagnostic, maximum one call, 60-second deadline, 4096 output-token ceiling, $0.220480 worst-case hold. It is charged to the same canonical optimal-swarm-size-q1 ledger as the later batch. Register an immutable plan and condition-specific TLDR before it. Require exact {"ok":true}, served model match, native provider match, end_turn and valid nonnegative integer input/output usage. No retries or fallback. Save trace, output and reporting artifacts.

After the diagnostic passes, freeze its receipt in the runtime configuration, refresh the Q-A public registration to this amended source/plan, verify the current exclusive machine claim and execute the existing 16 N=1 assignments. Q-A remains 600 seconds/episode, 60 seconds reserved for integration, $2/episode, 19 maximum calls/episode and $20 total shared across all stages/failures. No task generator, evaluator, actor prompt, assignment split or scoring change is included. Native Messages moves the system message to the top-level system field and requests JSON in the existing prompt; JSON schema failures follow existing malformed-plan/answer rules. The final artifact parser remains strict, with no removal of markdown fences or other undocumented repair.

## Metrics

Transport: exact diagnostic JSON, requested/served route match, valid usage, elapsed wall time, charged/held microdollars and publication receipt. Q-A retains the full 16-row denominator and reviewed metrics in q1-pre.md; missing and failed outputs are not dropped. Nonzero cache fields, missing usage, authentication or route failure stop batch admission. New provider fixtures cover request transformation, usage/rate math, cache rejection, HTTP safety and reservations. Run the entire suite on the intended server's Python 3.12 before dispatch. The one canonical ledger is never recreated to reset spending.

## Visualization mapping

Preserve actual monotonic service intervals and raw trace; one diagnostic call uses the same measured replay and public progress. Known synthetic rendering tests remain explicitly separate. No simulated spatial motion. Downloadable replay and static table remain the supported fallback. Prior reporting diagnostic already verified child imports, acknowledgments, byte identity, public status and timeout handling; repeat run-specific public admission on this allocation.

## Admission requirements

Published source and source/config hashes, dmarz review reference, adapter regression evidence, passing public-plan preflight, current exclusive allocation and the named shared credential. Server allocation and deployment receipts are written outside the source checkout before dispatch. New adapter re-review is requested as an engineering amendment; no prior review is relabeled as having examined this code. No model calls have occurred at the time this amendment is written.
