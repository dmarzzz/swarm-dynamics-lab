# market-split-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/market-split-opus (sub-agent on halcyon), reviewer dmarz/fleet-monitor (same researcher), server sim-test-01, claim `dmarz-market-split-opus` to 17:46Z. Not a review. Last updated 2026-10-04T07:58Z.

## 1. Results so far

- S0 `s0-fleet-001`: 6 of 6 scripted bundles done between 07:47:36Z and about 07:48:25Z, 0 model calls, `qualification_pass` 1 and `visual_ok` 1 on each. Post-mortem and the pre-run reviews for I0, Q0 and S1 are on main (commit d1e80164, files `reviews/phase2-pre.md`, `i0-001-pre.md`, `q0-001-pre.md`, `s1-001-pre.md`).
- No model call has been made. The server has been idle since about 07:48Z.

## 2. Gate forecast

Nothing is running. The three paid stages wait for the reviewer's go.

- I0: 6 calls, about a minute. Gate 6 of 6 mandated operations valid. Known risk, stated in the plan: Haiku V1 failed this probe by choosing a more profitable operation than the mandated one, and this study keeps the pilot's original wording without the clarifying sentence the Haiku study added.
- Q0: 32 calls (2 markets x 2 arms x 8 rounds), about 5 to 10 minutes. Gate: all actions valid, each of four episodes profitable and at least 75% of the one-firm reference, zero unpriced calls.
- S1: 864 calls in 18 bundles. Sonnet took 9 to 14 minutes per bundle (about 3 hours 10 minutes with one worker). At the 6 s per call Opus showed tonight in D1-Opus (effort high) a bundle is about 5 minutes and S1 about 1.5 hours; I would plan for 1.5 to 3 hours.

## 3. Next run

The lane already has its ladder and a projection rule written (phase2-pre.md, "Projection after Q0": projected study cost at most USD 45, largest response at most 8,192 tokens, latency at most 180 s). What is missing is only the go.

- **Fastest path:** one conditional go from the reviewer covering I0, then Q0, then S1, with the written projection rule as the condition between Q0 and S1. As written, each stage waits for a post-mortem and a separate go, which is three waits on an agent for about 15 minutes of I0 and Q0 work.
- **If I0 fails on the mandated operation:** this is the known Haiku V1 failure and the repair exists: the clarifying sentence from the Haiku study. It changes `prompt.txt`, so the engine hash changes and S0 must be rerun (under a minute, no model calls). Attempt `i0-002`. The plan requires the reviewer's instruction for this; deciding it now saves the round trip.
- **If I0 fails with HTTP 400:** request-shape defect. Check against [LESSONS.md](LESSONS.md) item 3.
- **If Q0 fails profitability:** a qualification result; the plan stops the study. No change proposed.
- **If the projection after Q0 is over USD 45:** the plan stops and asks. dmarz has said cost is not a gate tonight, but the ledger cap of USD 60 is in `design.yaml`, which is hashed (`src/common.py` line 16) and S1 admission requires I0 and Q0 at the same hashes (`src/coordinator.py` lines 25 to 34). Raising the cap after Q0 means rerunning S0, I0 and Q0 (about 15 minutes). If there is any doubt, raise the cap before I0, not after Q0.

## 4. Design notes for later runs

- S1 keeps a locked one-firm arm and an unregulated condition as controls. In the Sonnet pilot the unregulated condition was 0 of 6 and the locked arm cannot split by construction. Both are cheap relative to the claim they protect; keep them.
- One model realization per cell and six markets from one generator. If Opus replicates 6 of 6 against 0 of 6, a larger market set is the next spend, not another model.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1 and 4.
