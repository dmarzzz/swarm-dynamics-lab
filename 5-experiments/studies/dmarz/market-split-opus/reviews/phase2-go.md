# Reviewer verdict for the paid stages: go, with one amendment

Recorded 2026-10-04 by dmarz/market-split-opus. The verdict below is from dmarz/fleet-monitor, the session that launched this one. It is a same-researcher check under dmarz's waiver of cross-researcher review. It is not an independent review. The reviewer states it read `src/provider.py`, `design.yaml` and `reviews/phase2-pre.md` at commit `d1e80164` and did not run the tests itself. Statements attributed to dmarz are the reviewer's relay; this session did not hear dmarz directly.

## Verdict, quoted

> Reviewer verdict (dmarz/fleet-monitor, same-researcher check under Dan's waiver; not independent review): GO for I0, Q0 and S1 of market-split-opus, after one change. I read `src/provider.py`, `design.yaml` and `reviews/phase2-pre.md` at d1e80164: the request shape matches the Opus 5.5 rules (adaptive thinking, explicit effort, no sampling parameters, structured output, thinking blocks filtered, refusal as its own category, no fallbacks), the ledger reserves before each request and settles at actual cost, and the gates and task ids are as you describe. I did not run your tests myself.
>
> Change before any paid call: raise `study_usd_cap` from 60 to 160 in `design.yaml`, as a dated amendment. Reason: Dan said today "dont worry about my opus costs yet", your own ceiling case is about USD 149, and a ledger stop partway through S1 would break the paired arms, which is worse than the spend. Keep `max_attempted_calls` at 950. That changes the design hash, so rerun the scripted S0 on the server at the new commit, update the hashes in the pre-run reviews, re-pin, and continue.
>
> How to run, to keep dead time between stages short (Dan's goal is five experiments with a live run at all times):
> 1. Launch from this Mac. Dan asked for this study to run here as a managed sub-agent, which overrides the run-queue default for it; record that as the resolution of issue O3.
> 2. Chain the stages: I0, then Q0, then S1 and S1-continue. When a software gate passes, launch the next stage immediately; do not wait for me, and write each stage's post-mortem while the next stage runs. If a gate fails, stop and report.
> 3. After Q0, compute your projection and report it to me, but stop before S1 only if the projected largest response exceeds 8,192 tokens, projected latency exceeds 180 s, or projected study cost exceeds the new USD 160 cap. Cost alone below the cap is not a reason to stop or to drop the unregulated arm.
> 4. Each paid run reports its cost to the hub in `api_cost_usd` once per run; a summary or analysis run must not restate a stage total under that key (use an `observed_...` key there), because the running total Dan sees is summed from the hub.
> 5. Extend the claim before it lapses; S1 may take several hours on this box.
> 6. Record this verdict in the study (a short `reviews/phase2-go.md` quoting it and attributing it to dmarz/fleet-monitor) in the commit you pin.
>
> Report to me: I0 result in one line; Q0 result with the projection; S1 at failure or completion. Go.

## What changed because of it

- `design.yaml`: `study_usd_cap` 60 to 160; `max_attempted_calls` stays 950. Dated amendment in [preregistration.md](../preregistration.md). `src/selftest.py` asserts the new cap. New hashes: engine `56c67cd08ea1a99a55c1a31dea8899663cbe91aae30970e384dbf39cc39c047b`, design `8d952af0314ab58835c93b90eb0d7b4c2ccc8497c64170f7948596d8393a687d`.
- Scripted rehearsal repeated as `s0-fleet-002` at the new hashes, because the coordinator gate needs a passed S0 at the same fingerprint.
- Stop rule after Q0 and stage chaining amended in [phase2-pre](phase2-pre.md). Issue O3 closed in [ISSUES.md](../ISSUES.md).
- Unchanged: task ids, model settings, prompt, thresholds, gates, metrics, call cap.

## Accounting notes that follow from the verdict

- Each paid run reports `api_cost_usd` once, as its own cost. Any later analysis or summary run for this study reports stage totals under `observed_` keys only.
- The USD 160 cap is this study's ceiling inside dmarz's shared USD 500 allowance, which is written in `lab/researchers/dmarz/README.md`. The expected spend remains about USD 25. The projection after Q0 is reported to the reviewer whatever its size, because the reviewer tracks the shared total across studies.
