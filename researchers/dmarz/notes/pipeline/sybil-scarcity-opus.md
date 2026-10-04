# sybil-scarcity-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/orchestrator-2 (orbital-one), package by dmarz/pipeline-scarcity, server sim-dmarz-2, run-queue 248. Not a review. Last updated 2026-10-04T09:22Z.

## 1. Results so far

- Launch-ready package on main 08:44Z; reviewer's go 08:49Z with two workers instead of four; claimed 09:12Z.
- Chain started about 09:17Z: S0 (scripted) done, probe `p0-001` 1 of 1 valid (23,537 input tokens, 38 output tokens, USD 0.095), Q0 `q0-001` **passed**: 48 of 48 valid, 1,129,722 input tokens, 1,824 output tokens, USD 4.56, 80 seconds (09:18:46Z to 09:20:06Z). S1 `s1-001` (run ba41e101) started preparing inputs at 09:21Z.
- Each call reads a packet of 486 reports, the same size as sybil-scale-xl's N=972 packets. Opus at effort low answered the probe in 38 output tokens with no thinking tokens.

## 2. Gate forecast

- Q0 is done and passed, including the single-carrier packets, so the instrument can find one truthful report among 486 when nothing is fabricated.
- S1: 1,440 calls, two in flight, about 2.5 to 3 s per call: about 30 to 35 minutes and USD 137. A 429 or 529 is retried twice; any other failed call stops dispatch.
- Rate: about 0.9 to 1.1M input tokens per minute during S1. This overlaps sybil-scale-xl's S1 (about 6 to 7M per minute, starting about 09:45Z).

## 3. Next run

- **If Q0 passes:** S1 starts from the chain.
- **If Q0 fails on the single-carrier packets:** that is the manipulation itself showing at the clean level: the model cannot find one truthful report among 486. It would still be a result about scarcity, but S1's 1-carrier cells would then be at floor. Read which carrier profile failed before changing anything; effort medium is the one setting to try, as a new batch.
- **If S1 stops on a third overload:** the not-started assignments need a resume at the same source hash or a new batch; see [LESSONS.md](LESSONS.md) item 8.
- **After S1:** the primary contrast is accuracy with 1 carrier minus 81 carriers under random auditing, 108 checks, pass rate 0.1. If the decrease is 10 pp or more, scarcity (not the model, not the audit policy) is the lever and sybil-split-opus (plan on main, no code yet) is the natural next run. No further stage in this study.

## 4. Design notes for later runs

- First dmarz study tonight built to the ready-chain contract and launched within about 35 minutes of its package landing. The wait was the reviewer's read and a free server, not the build.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 4, 5 and 8.
