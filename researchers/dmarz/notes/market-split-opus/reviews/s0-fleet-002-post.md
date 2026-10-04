# Post-mortem: s0-fleet-002

- Experiment / owner / stage / date: market-split-opus; dmarz/market-split-opus; S0 scripted rehearsal repeated at the amended design; 2026-10-04, about 08:00 UTC.
- Pre-run assessment: [s0-fleet-002-pre](s0-fleet-002-pre.md); parent `s0-fleet-001`. Pinned commit `b097331b874f2dcab2b31a830e54cdc39f9d321d`; engine `56c67cd08ea1a99a55c1a31dea8899663cbe91aae30970e384dbf39cc39c047b`; design `8d952af0314ab58835c93b90eb0d7b4c2ccc8497c64170f7948596d8393a687d`. Scripted mock backend; no model.
- Run ids: `market-split-opus/` `883ea748c13c` (task 100, none), `aee57482d1e8` (100, firm), `236d36498b53` (100, owner), `b9d26e50b9fb` (101, none), `a69ce538c0df` (101, firm), `f7b3f9b3b98e` (101, owner).
- Disposition: advance to I0.

## What ran and what happened

- 6 bundles planned, started and done; 12 of 12 scripted episodes valid; `qualification_pass` 1 and `visual_ok` 1 in every run; 0 model calls, USD 0. 18 of 18 offline tests passed on the server at this commit before the stage.
- Every episode's profit, first registration round and final firm count equals the matching `s0-fleet-001` episode exactly, as expected when only the dollar cap changed.
- 42 of 42 artifacts match their local files by SHA-256 against the hub. Image sizes and the eight replay frames were checked by the verifier. I did not look at a frame from this attempt; one from `s0-fleet-001` was inspected and the outcomes are identical.
- The public plan at `b097331b` was checked by the launcher before the stage (SHA-256 `99e8133f7e3317cf827c7700c1cc657122287a473395874f37953bad0eac22be`, published bytes equal local bytes) and the hub registration now links to that commit.

## Experiment-quality assessment

A software check of the amended design, nothing more. It supplies the passed S0 at the current fingerprint that the coordinator requires before Q0. No failure, no repair.

## Next run

`i0-001`, six calls, under [phase2-pre](phase2-pre.md) and the reviewer's go in [phase2-go](phase2-go.md).
