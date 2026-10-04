# Post-mortem: q0-001

Experiment market-split-api, dmarz/market-split, Q0, 2026-10-04 UTC. Parent s0-fleet-001; frozen source 92c6f798 and v1 design. Disposition: repair-and-rerun. Pre-run assessment q0-001-pre.md.

## What ran and what happened

Two bundles planned, one started and failed, one cancelled without calls. Two episodes attempted; both invalid, two remaining unstarted. Four paid calls, all usage priced, total $0.004958. No retries. Locked arm completed two rounds, then failed at round3; flexible arm failed at round1. Profits 2236.748768 and 0 are partial, not complete competence outcomes. No discovery result is available. Failed run 45bc5250fa0d; unstarted cancelled run 93b3bed35b2b.

## Failure and repair ledger

Both invalid responses exceeded the existing 200-character note limit. Replaying the exact returned action through the validator gives note_limit, with no quantity/operation fault. The response schema described the limit but did not structurally enforce string length. Proposed repair: request one sentence <=80 characters in both prompt and schema description, retaining the original hard 200-character validator and preserving violations rather than clipping. New regression test checks overlong notes stay invalid and raw responses are retained.

An independent qualification risk is visible: both initial production choices were full capacity, accompanied by an incorrect claim that this maximizes profit. At task20 prices this earns about two-thirds of the one-firm reference. The original prompt specified prices clear from output but left the exact price/profit formula implicit in numeric fields. Repair states the unchanged price and operating-profit equations explicitly for both arms, without giving a best-response solution or any registration strategy. This is a competence clarification, not a change to economic physics or the qualification floor. Because both wording changes occur together, a pass will qualify the revised interface; it will not isolate which wording caused improved behavior.

## Visualization review

Live/final PNG and eight-slot GIF retained measured partial traces and invalid labels under market-split-api-v1; visual_ok=1. Seven uploaded artifacts hash-verified. Missing rounds are not treated as observed. The dashboard marks the run failed. Worker exited1 and the other bundle was cancelled; no background paid worker remains.

## Experiment-quality assessment

The API, structured parser, usage reporting and stop path worked. This was an interface failure, not evidence against natural discovery. Neither episode completed. No change to economic engine, evaluation threshold, objective, model or budget is justified. Preserve all four calls in the single study ledger. Source/config changes require a new S0; use disjoint Q0 fixtures22/23. S1 tasks30–35 and holdout remain model-unopened.

## Next run

s0-fleet-002 repeats all mock controls on tasks22/23 after the two prompt clarifications and the new regression test. Then q0-002 uses the same fresh tasks with four episodes/32calls and the unchanged 100%-valid/positive-profit/75%-reference floor. S1 remains blocked until qualification passes. Aggregate max1,100 calls and standing shared $500 authorization apply unchanged; spent4 calls/$0.004958 so far. No economic outcome is rerun for a favorable result.
