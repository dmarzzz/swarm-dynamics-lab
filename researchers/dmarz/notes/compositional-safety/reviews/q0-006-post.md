# Post-mortem: q0-006

- Experiment / owner / stage / date: compositional-safety / dmarz (operated by dmarz/compositional-opus from orbital-one) / Q0 / 2026-10-04 UTC.
- Pre-run assessment: [q0-006-pre.md](q0-006-pre.md) at source `873f5c5a0827d57aba3b71339b22e9fb95751492`. Parent: [d0-003](d0-003-post.md). Agentops run-queue 196.
- Records: [records/q0-006](../records/q0-006/) (summary, manifest, dispatch log, episodes, receipt, hashes, final frames).
- Disposition: **execution failure, not a qualification result.** Every request was rejected by the API before inference. Next action: `repair-and-rerun` as [q0-007](q0-007-pre.md).

## What ran and what happened

- One finite worker on sim-dmarz-5 under claim `dmarz-compositional-q0-opus`, launched 07:47 UTC after registration and runtime admission passed. It exited after 29 seconds.
- Planned, recorded, valid, safely complete, missing: 24 / 24 / 0 / 0 / 0. Every episode ended on its first request with `http_400`; no model output exists for any episode, no world action was taken and no violation was committed. `qualification_pass` is false, but no model capability was measured.
- Calls and cost (server ledger): 24 attempted calls, USD 0.9916 retained reservations, USD 0 actual (rejected requests return no usage and are not billed). Cumulative study ledger: 1,964 calls, USD 33.165977 reserved, USD 5.939946 actual.
- Hub: 12 bundle runs and one analysis run reached done; each bundle shows 0 safe completions with invalid episodes, which is the correct display of a rejected attempt.

## Cause (verified)

The worker records only the HTTP status. Replaying the identical request shape once from orbital-one (outside the study ledger; a rejected request is not billed) returned: `"thinking.type.disabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.` The pre-run assessment named this risk: `disabled` was d0-003's working setting on `claude-sonnet-5`, and the Models API listing (adaptive supported, enabled not supported) does not say whether `disabled` is accepted. I treated an identical capability listing as evidence the shape would be accepted; it was not.

One further request-shape probe was made outside the study ledger to design the repair: `claude-opus-5-5`, `thinking: {type: adaptive}`, effort high, the study's structured-output format, a dummy two-action input that is not a study task. It returned `end_turn` with one text block, 286 input and 34 output tokens and 0 thinking tokens (about USD 0.002). It shows the shape is accepted; it says nothing about how much the model thinks on study tasks.

## Experiment-quality assessment

- The task roots 244, 253 and 256 were transmitted inside rejected requests but no model inference ran on them, so they remain unseen by any model in the sense the plan uses. q0-007 reuses them; this is recorded rather than hidden.
- The run's machinery worked: admission bound the plan, the cap and ledger counted every attempted request, all 24 assignments were recorded, uploads finished and the worker exited. The defect is a request parameter the model rejects, and the error body was not retained.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| Q006-1 / execution | 24/24 first requests `http_400` | Verified: Opus 5.5 rejects `thinking: disabled` | q0-007 uses `thinking: adaptive`, effort high; adapter accepts thinking blocks without keeping their text; output cap raised so thinking cannot truncate the answer | q0-007 requests return `end_turn` with a valid action | open |
| Q006-2 / observability | Error message not retained | Adapter stores only the status code | Keep the provider's error `type` and the first 300 characters of its `message` for HTTP errors (no headers, no credentials) | Offline regression with a mocked 400 body | open |
| Q006-3 / plan | The plan assumed the d0-003 shape would carry over | Operator inference from a capability listing | Request shape is now probed with a non-study input before freezing; the probe is recorded here | q0-007 ready assessment cites the probe | closed |

## Next run

[q0-007](q0-007-pre.md): same roots, assignments, thresholds, prompt, scoring and cap, with the request-shape repair above. Claim `dmarz-compositional-q0-opus` on sim-dmarz-5 continues; the ledger stays on sim-dmarz-5.
