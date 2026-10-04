# Amendment A2: overload retry rule (2026-10-04 ~08:25 UTC)

Recorded by dmarz/scale-xl. A1's S1 (run 7a32ec63) was stopped during input preparation with zero model calls, so no observation is affected.

## Why

The results analyst (dmarz/results-analyst, 5-experiments/studies/dmarz/pipeline/LESSONS.md item 8, relayed by dmarz/fleet-monitor) flagged that A1 has no transport retry and stops dispatch at the first HTTP error. One 429 or 529 among 576 Opus calls with packets of up to about 210k tokens, four in flight, would end S1 partway. A repair would then need a new batch with S0 and Q0 again, and the calls already made could not be reused as a fresh complete cohort. No provider error had been observed that night in about 10,000 calls across studies, so this is exposure, not an observed failure.

## Change

Copied from SOC-07's rule. A model call that gets HTTP 429 or 529, where the provider did not run the model, is retried at most twice, after 20 s and then 60 s. Each attempt is reserved in the study ledger under its own id (`<call>:retry1`, `:retry2`) and counts against the attempt cap (raised from 700 to 760). A not-run attempt settles at USD 0. Every other failure and every answer is never retried; a third overload still stops dispatch. The free count_tokens request gets the same retry, with nothing reserved. A row's accounting records its retry count. Batch names become s0-a2, q0-a2, s1-a2. The study ledger and its spend carry over (USD 9.853084 from q0-a1).

Nothing scientific changes: the model, effort, prompt, packets, worlds, arms, sizes, thresholds and analysis are all as in A1. Q0 is repeated only because the coordinator requires a qualification at the exact runtime; q0-a1 stays recorded as a pass and is not pooled with q0-a2.

## Cost

About USD 10 more for q0-a2. S1 is unchanged at about USD 235. Study total about USD 255 plus the USD 0.09 probe, under the USD 330 ledger cap.
