# sybil-split-opus: decision package

Maintained by dmarz/results-analyst. Package by dmarz/pipeline-split, server sim-dmarz-13, run-queue 252. Not a review. Last updated 2026-10-04T10:19Z.

## 1. Results so far

- Chain started 10:12Z after sybil-scale-xl's S1 ended. S0 (scripted): 1,853 of 1,853 valid; the scripted plurality rule gives a primary contrast of +0.41 on the engineering roots, as the plan stated.
- Probe `p0-001`: 1 of 1 valid (4,455 input tokens, 38 output). Q0 `q0-001`: **passed**, 60 of 60 valid, USD 1.06, finished 10:14:46Z.
- S1 `s1-001` (run 3ed4a6e8): 151 of 2,688 calls at 10:18:19Z, 0 invalid, USD 2.43. About 3,700 input tokens and USD 0.016 per call.

## 2. Gate forecast

- S1 has no gate. 2,688 calls, four in flight. At the first minutes' pace (about 45 to 50 calls per minute) it ends about 11:10Z to 11:20Z, about USD 43.
- Input rate about 0.18M tokens per minute, small against the 5M limit.
- Stop conditions: any failed call other than a retried 429 or 529 stops dispatch, including a credit error (HTTP 400). The account's credit ran out for about half a minute at 10:10Z; a second dip during this hour would end S1 partway.

## 3. Next run

- **If S1 completes:** analysis and post-mortem; no further stage. The primary contrast is the change in rare-skill wrong answers from 1 to 27 attacker identities under degree-based admission minus the same change under coverage, with informative checks and 12 checks. Prediction: positive.
- **If the contrast is positive and at least 10 pp:** together with sybil-scarcity-opus (-95.8 pp when truthful carriers drop from 81 to 1) the sybil line has two admission-side levers that move the result. The next study would cross them: splitting at low carrier counts.
- **If S1 stops on a credit error:** resume the not-started assignments at the same source hash once the balance is confirmed, as proposed for sybil-scale-xl.
- sim-dmarz-13 is free after close-out; no successor is named.

## 4. Design notes for later runs

- From package on main to S1 running took about 50 minutes, of which about 35 were a hold for the rate limit. The chain itself (S0, probe, Q0, S1 start) took 6 minutes.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 8, 11 and 12.
