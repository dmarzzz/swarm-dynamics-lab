# Transport diagnostic a1 post-mortem and prospective a2 repair

2026-10-04 UTC. Parent attempt anthropic-transport-q0-a1 returned HTTP 400; public artifacts were acknowledged. Assigned 1, attempted 1, valid model answer 0. The ledger retains the entire $0.220480 maximum charge because billed usage is unknown; no new ledger or refund is assumed. The 16-task Q-A batch has not started.

## TLDR

Repair the shared Anthropic workspace routing configuration, then repeat one exact-JSON transport diagnostic under a new ID before the reviewed N=1 qualification batch. Compare the response with {"ok":true}, verify pinned route, usage, elapsed time, cost and artifacts. This remains engineering qualification only; both diagnostic attempts and Q-A/Q-B share the original $20 authority.

## Question and prediction

Will the dedicated Swarm Lab key plus its established Swarm Lab workspace routing header eliminate the transport rejection? A read-only model lookup without that header returned HTTP 400 with an allowlisted workspace error category; the same lookup with the explicitly configured Swarm Lab workspace returned HTTP 200 and the pinned model ID. This verifies the routing diagnosis without a second inference call. Predict a2 returns valid complete JSON and ordinary usage; any failure remains recorded and blocks batch dispatch.

## Setup

Same frozen engine, evaluator, budget and native Anthropic provider as the preceding amendment; pinned claude-haiku-4-5-20251001, $1/M input and $5/M output, standard tier. The only configuration repair is the required workspace routing metadata. The private mapping was migrated from the established Swarm Lab Theseus launcher after verifying its exact Keychain selector matches service swarm-lab-anthropic/account vishesh, then verified by the read-only model lookup. No other provider key was read or sent; no identifier or credential is published. The reusable credential policy requires one dedicated API key, separate allowlisted routing metadata, exact project binding and no environment fallback.

Current allocation research-01 under vishesh-swarm-size-anthropic-q1; refresh the claim before dispatch. Keep the same /srv/swarm/optimal-swarm-size-q1-authority/budget.sqlite ledger and original a1 artifacts. Native credentials stay in process memory, core dumps disabled, verified encrypted SSH stdin; all secret diagnostics remain suppressed.

## Protocol

Publish this amendment and register its immutable URL before a2. Attempt ID anthropic-transport-q0-a2 and new output directory; maximum one model request, 60 seconds, 4096 output tokens and $0.220480 pre-dispatch hold. Total maximum diagnostic exposure including the retained a1 hold is $0.440960. Strict JSON, served model/provider, usage and end_turn checks remain unchanged. No retries or fallback inside an attempt.

If and only if a2 passes and reporting is complete, run the already reviewed Q-A design: 16 N=1 assignments, 600 seconds/episode with 60 reserved for integration, at most 19 calls/episode, $2/episode, original $20 total across diagnostics and all stages. Keep the full assigned denominator and stop-on-fatal/publication behavior. Read q1-pre.md and anthropic-amendment.md for task design and interpretation limits. Q-B/core stay closed until their own qualification/design gates. The new runtime configuration and public-plan receipt get a2 filenames; historical a1 configuration/receipt remain intact.

## Metrics

Transport diagnostic validity, complete ordinary usage, settled/held microdollars and publication status. Q-A retains verified on-time success, quality, wall latency and cost. Distinguish infrastructure failure from model competence; neither the a1 HTTP error nor the successful read-only lookup is a task performance result. Assigned diagnostic calls and retained holds stay visible in total spend.

## Visualization mapping

Use the actual recorded service interval, event trace and downloadable replay/static table for each diagnostic and Q-A condition. The HTTP failure retains its own terminal artifact. Do not convert it into an apparent successful or synthetic model trajectory. Public condition TLDRs identify the stage and exploratory limits.
