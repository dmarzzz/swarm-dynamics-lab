# Pre-run assessment: s0-fleet-002

- Experiment / owner / stage: market-split-opus; dmarz/market-split-opus; S0 scripted rehearsal, repeated at the amended design.
- Parent attempt and post-mortem: [s0-fleet-001-post](s0-fleet-001-post.md) (6/6 bundles, 12/12 valid scripted episodes, 0 model calls).
- Status: ready
- Why it is repeated: the reviewer's verdict ([phase2-go](phase2-go.md)) raised the study dollar cap from USD 60 to USD 160. That changes `design.yaml` and one assertion in `src/selftest.py`, so both hashes change, and the coordinator admits Q0 only with a passed S0 at the same fingerprint. Nothing that the rehearsal exercises changed: same tasks 100/101, seed 31, three regulators, two arms, eight rounds, same scripted policy.
- Expected finding: identical outcomes to `s0-fleet-001` (same profits, registrations and firm counts), zero model calls, zero cost. A difference in any scripted outcome would mean something other than the cap changed and blocks the paid stages.

## Frozen execution plan

- Engine `56c67cd08ea1a99a55c1a31dea8899663cbe91aae30970e384dbf39cc39c047b`; design `8d952af0314ab58835c93b90eb0d7b4c2ccc8497c64170f7948596d8393a687d`. Runtime as in [deployment.md](../deployment.md).
- Command: `run-market-split-opus.py <commit> setup`, then `run-market-split-opus.py <commit> S0` (attempt `s0-fleet-002`, six bundles, one worker).
- Calls, spend, credentials: zero model calls, zero dollars, no model credential sent. Server `sim-test-01` under exclusive claim `dmarz-market-split-opus`.
- Acceptance: 6 of 6 runs done; 12 valid episodes; `qualification_pass` 1, `visual_ok` 1, `model_calls` 0 and `api_cost_usd` 0 in every run; every uploaded artifact matching its local file by SHA-256; episode profits equal to `s0-fleet-001`'s.
- On a pass the chain continues with I0 under [phase2-pre](phase2-pre.md). On a failure everything stops for repair.

## Visualization mapping

Mapping `market-split-opus-v1`, unchanged from [s0-fleet-001-pre](s0-fleet-001-pre.md); six new run ids, same bindings.
