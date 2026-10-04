# Post-mortem: v3o-a2 S1 (stopped attempt)

- Experiment / owner / operator: discussion-v3-opus / dmarz / dmarz/v3-q0-opus (launch); stop and this review by
  dmarz/orchestrator-2 on the same lane.
- Hub run: `discussion-v3-opus/v3o-a2-s1`, status **failed** (set by the operator with an explanatory message).
  Parent stage: `v3o-a2-q0`, passed (clean diagnostic 6/6, clean reports-only 6/6, 636/636 valid, replay-audited;
  [records](../records/v3o-a2-q0/summary.json)). Q0 is not affected by anything below.
- Review: cross-researcher review waived by the owner; none performed.

## Results (measured)

| Item | Value |
|---|---|
| Planned S1 calls | 2,436 on worlds 54101–54124 |
| Call starts / responses / provider failures | 292 / 230 / 61 |
| Failure reason | `provider_credit_balance_low` (HTTP 400) on all 61 |
| Failed calls | consecutive call indices 205–265, about 10:07–10:11 UTC |
| Unresolved | one call (`c000291`) in flight at the stop; whether it was billed is unknown |
| Terminal cases | 50 of 384 |
| Tokens / cost | 1,237,693 input, 92,894 output, **USD 6.808652** (measured from usage on responses) |

The 61 failures are not model or instrument failures. The API account's credit balance ran out for a few minutes
while sybil-scale-xl's main stage was spending about USD 38 a minute in the same workspace; calls after the burst
succeeded (credit restored by reload or top-up; which one is not confirmed here). The runner records a provider
failure and continues, so the cases containing those calls are incomplete and the attempt carried a block of
missing outcomes from its first half hour.

## Decision and stop

2026-10-04 10:14:26 UTC: SIGTERM to the chain process (the launcher's own timeout uses SIGTERM), on fleet-monitor's
recommendation through Dan's channel, option (a). Reason: a roughly 5-hour, roughly USD 90 exploratory stage should
not carry a known hole of 61 failed calls caused by a provider outage; RUN-REVIEW treats this as an execution
failure repaired by a new preserved attempt. The Q0 gate result stands, no gate or scoring rule was changed, and
nothing is relaunched on the same worlds. The journal ends with a `call_start` and no `complete` event, so
`audit` correctly refuses it as interrupted. Loss: about USD 6.81 and 20 minutes.

## Quality and records

Preserved: the full S1 journal, frame, manifest, chain state and chain log on sim-dmarz-9 and copied off-server to
git-ignored `data/` in the operator worktree; [stopped-attempt summary](../records/v3o-a2-s1/stopped-attempt.json),
the frozen [manifest](../records/v3o-a2-s1/manifest.json) and [chain state](../records/v3o-a2-s1/chain-state.json)
are committed. Worlds 54101–54124 are retired in source (`RETIRED_WORLDS`).

Gap found: a SIGTERM leaves the hub run `running` because the chain installs no signal handler; the operator set it
to failed by hand through swarm_report.

## Next run

`v3o-a3`: S1 only, on fresh worlds 54201–54224, admitted by the hash-checked `v3o-a2-q0` summary, identical model
and request configuration, plus a credit halt: after one `provider_credit_balance_low` failure the next dispatch
stops the stage (no retry). [Pre-run review](v3o-a3-pre.md).
