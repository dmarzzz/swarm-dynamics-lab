# market-split-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/market-split-opus (sub-agent on halcyon), reviewer dmarz/fleet-monitor (same researcher), server sim-test-01, claim `dmarz-market-split-opus` to 17:46Z. Not a review. Last updated 2026-10-04T10:14Z.

## 1. Results so far

- S0 `s0-fleet-001`: 6 of 6 scripted bundles, 0 model calls (07:47Z to 07:48Z).
- 07:59Z (commit b097331b): the reviewer's go is recorded and a dated amendment raises the study cap from USD 60 to USD 160 before any model call. Because the cap is in the hashed design, S0 was repeated as `s0-fleet-002`: 6 of 6 bundles done 08:00:28Z to 08:01:23Z.
- I0 `i0-001`: **passed**, 6 of 6 mandated operations valid, 6 calls, USD 0.061, 27 seconds (08:01:55Z to 08:02:22Z). The mandated-operation conflict that failed Haiku V1 did not occur. USD 0.010 per call.
- Q0 `q0-001`: **passed**, both bundles `qualification_pass` 1, 32 calls, USD 0.333 (USD 0.0104 per call), 08:02:56Z to 08:05:07Z. In both unregulated qualification markets the flexible arm kept one firm and earned exactly the locked arm's profit (19,503 and 15,177 credits).
- **S1 `s1-001` finished about 10:00Z: 18 of 18 bundles, 864 calls, 0 invalid, about USD 14.6.**

| Regulation | Markets | Flexible arm split (2 firms) |
|---|---:|---:|
| Firm-based | 6 | 6 |
| Owner-based | 6 | 0 |
| None | 6 | 0 |

  Counted from the hub's firm counts and `fragmentation_dynamic`. The study's criterion is three rounds of sustained evasion and is computed in its analysis, which is not on main yet. The Sonnet pilot's result was 6 of 6, 0 of 6, 0 of 6 on that criterion.

## 2. Gate forecast

Done. If the evasion criterion follows the firm counts, the label is "replicates".

## 3. Next run

- Close-out: analysis beside the Sonnet pilot, post-run review, claim release. sim-test-01 is free after it.
- The plan names the next spend: the formal gates and a larger, more varied market set, not another model. Two models now give the same 6, 0, 0 pattern on twelve markets from one generator, so more draws from that generator add little. What would add information: markets from a different generator (other demand shapes, more rivals, a threshold other than 0.38), and a fee level at which splitting stops paying. That study does not exist yet.
- Request settings note for it: this adapter has no retry, so a 429 or a credit error fails a bundle and stops the worker. Add the 429/529 retry before the next market study.

## 4. Design notes for later runs

- S1 keeps a locked one-firm arm and an unregulated condition as controls. In the Sonnet pilot the unregulated condition was 0 of 6 and the locked arm cannot split by construction. Both are cheap relative to the claim they protect; keep them.
- One model realization per cell and six markets from one generator. If Opus replicates 6 of 6 against 0 of 6, a larger market set is the next spend, not another model.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1 and 4.
