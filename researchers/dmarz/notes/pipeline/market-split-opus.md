# market-split-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/market-split-opus (sub-agent on halcyon), reviewer dmarz/fleet-monitor (same researcher), server sim-test-01, claim `dmarz-market-split-opus` to 17:46Z. Not a review. Last updated 2026-10-04T08:05Z.

## 1. Results so far

- S0 `s0-fleet-001`: 6 of 6 scripted bundles, 0 model calls (07:47Z to 07:48Z).
- 07:59Z (commit b097331b): the reviewer's go is recorded and a dated amendment raises the study cap from USD 60 to USD 160 before any model call. Because the cap is in the hashed design, S0 was repeated as `s0-fleet-002`: 6 of 6 bundles done 08:00:28Z to 08:01:23Z.
- I0 `i0-001`: **passed**, 6 of 6 mandated operations valid, 6 calls, USD 0.061, 27 seconds (08:01:55Z to 08:02:22Z). The mandated-operation conflict that failed Haiku V1 did not occur. USD 0.010 per call.
- Q0 and S1 have not started.

## 2. Gate forecast

- Q0: 32 calls (2 markets x 2 arms x 8 rounds). Gate: every action valid, each of four episodes profitable and at least 75% of the scripted one-firm reference, zero unpriced calls. Sonnet and Haiku both passed this stage in their studies. No Opus evidence yet beyond I0's six valid actions. Expect about 5 to 10 minutes.
- S1: 864 calls in 18 bundles. Sonnet took 9 to 14 minutes per bundle (about 3 hours 10 minutes). I0 ran at 4.5 s per call; if S1 calls take 5 to 10 s, a bundle is 4 to 8 minutes and S1 is 1.2 to 2.4 hours.
- Cost: the plan's projection rule runs after Q0. I0's USD 0.010 per call is below the central estimate (USD 0.028 per S1 call), so the USD 45 projection line and the USD 160 cap both look safe; S1 prompts are longer than I0 prompts, so this is only a first reading.

## 3. Next run

- **If Q0 passes and the projection is inside the three limits:** S1 (`s1-001`), pre-run file on main. With the go recorded, nothing else is needed.
- **If Q0 fails profitability:** a qualification result; the plan stops the study and the 75% floor is not lowered. No change proposed. Read the per-round actions first to see whether the losses come from over-registration (fees of 20 plus 3 per firm per round) or from quantity choices.
- **If a Q0 response is invalid or truncated:** the bundle fails and the worker stops. Check `stop_reason`; the 8,192 ceiling is in the hashed design, so a change repeats S0, I0 and Q0 (about 10 minutes at tonight's pace).
- **After S1:** results next to the Sonnet pilot's. If it replicates (at least 5 of 6 firm-regulated, at most 1 of 6 owner-regulated), the next spend is a larger and more varied market set, not another model. That plan does not exist yet and S1's 1.2 to 2.4 hours is the time to write it.

## 4. Design notes for later runs

- S1 keeps a locked one-firm arm and an unregulated condition as controls. In the Sonnet pilot the unregulated condition was 0 of 6 and the locked arm cannot split by construction. Both are cheap relative to the claim they protect; keep them.
- One model realization per cell and six markets from one generator. If Opus replicates 6 of 6 against 0 of 6, a larger market set is the next spend, not another model.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1 and 4.
