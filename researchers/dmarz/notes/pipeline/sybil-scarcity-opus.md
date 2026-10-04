# sybil-scarcity-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/orchestrator-2 (orbital-one), package by dmarz/pipeline-scarcity, server sim-dmarz-2, run-queue 248. Not a review. Last updated 2026-10-04T10:14Z.

## 1. Results so far

- Launch-ready package on main 08:44Z; reviewer's go 08:49Z with two workers instead of four; claimed 09:12Z.
- Chain started about 09:17Z: S0 (scripted) done, probe `p0-001` 1 of 1 valid (23,537 input tokens, 38 output tokens, USD 0.095), Q0 `q0-001` **passed**: 48 of 48 valid, 1,129,722 input tokens, 1,824 output tokens, USD 4.56, 80 seconds (09:18:46Z to 09:20:06Z). S1 `s1-001` (run ba41e101) started preparing inputs at 09:21Z.
- Each call reads a packet of 486 reports, the same size as sybil-scale-xl's N=972 packets. Opus at effort low answered the probe in 38 output tokens with no thinking tokens.

**S1 finished at 09:59:31Z: 1,440 of 1,440 valid**, 0 retries, 0 failures, 33.75M input tokens, USD 136.49, 37 minutes. Hub metrics: specialist accuracy 20.6% over all cells; `primary_contrast_pp` -95.8 (accuracy with 1 truthful carrier per rare fact minus 81 carriers, random auditing, 108 checks, attacker pass rate 0.1). The study's analysis and post-mortem are the record; I have not read the per-cell results.

## 2. Gate forecast

Done. The prediction (a decrease, practical marker 10 pp) held by a wide margin.

## 3. Next run

- No further stage. This is the first manipulation in the sybil family tonight that moves the outcome, and it is on how much truth is available, with the model, graph, audits and admission held fixed. Four model swaps moved the primary contrasts by 0.7 to 5.7 pp.
- What the result does not yet show is the shape between 1 and 81 carriers. The design has five levels (81, 27, 9, 3, 1); the analysis should say where accuracy falls off, because that sets the levels for any follow-up.
- Successor on the queue: sybil-split-opus (identity splitting at fixed attacker resources), S0 running on sim-dmarz-13 since 10:12Z.
- sim-dmarz-2 is free after close-out.

## 4. Design notes for later runs

- First dmarz study tonight built to the ready-chain contract and launched within about 35 minutes of its package landing. The wait was the reviewer's read and a free server, not the build.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 4, 5 and 8.
