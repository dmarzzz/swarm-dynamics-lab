# Proposed amendment A3: complete s1-a2's unfinished assignments (2026-10-04, for dmarz to decide)

Status: **proposed, not started.** Written by dmarz/scale-xl at dmarz/fleet-monitor's request. On 2026-10-04 ~10:45 UTC fleet-monitor relayed dmarz's decision to take Option 1 on Opus 5.5 with two calls in flight. The operator session's permission guard refused the code change for the resume path (a relayed instruction, not dmarz's own typed approval in this session), so nothing was implemented. Per fleet-monitor's fallback instruction, the stage is closed out as it stands. The saved s1-a2 inputs remain on sim-dmarz for a later A3 if dmarz approves it directly.

## Situation

s1-a2 stopped at 481 of 576 calls because of an account credit outage unrelated to any outcome ([post-mortem](reviews/s1-a2-post.md)). The 95 unfinished assignments are 1 failed plus 94 not started, spread over all 24 worlds and all 24 cells (17–24 valid worlds per cell). The primary contrast is already decisive. Completion mainly restores precision in the weak-check cells and full 24-world pairing for the Opus-versus-Haiku comparison at N=972.

## What A2 allows

Nothing. A2 forbids automatic re-execution: a run with attempt ≠ 1 is refused, the coordinator refuses an existing batch name, and the stop rule records unfinished rows as not started. Completing the batch needs a new amendment and dmarz's decision.

## Option 1 (proposed): resume only the 95 unfinished assignments, about USD 41

- Inputs: the saved s1-a2 assignments.jsonl.gz on sim-dmarz (packets and ids already built; preparation is skipped). Each resumed request is rebuilt from the saved packet, and its packet hash must equal the stored hash.
- Code change, the only one: a `resume` path that dispatches exactly the 95 assignment ids recorded in s1-a2 as failed or not started, under batch `s1-a2-r1`. Model, effort, prompt, schema, packets, retry rule, evaluator and analysis are unchanged. Because the dispatch code changes, the runtime source hash changes. The coordinator would be amended to accept, for `s1-a2-r1` only, the passed q0-a2 qualification together with a code diff limited to the resume path. Alternatively, rerun S0 (free, about 10 minutes) and Q0 (about USD 10) at the new hash; that is the stricter choice, and I recommend it if dmarz prefers no gate exception.
- Cost: about 95/576 of USD 236, so about USD 39–41 at measured tokens (plus about USD 10 with the stricter Q0 rerun). About 2 minutes of calls. Study total would be about USD 255–265, under the USD 330 ledger cap.
- How the analysis marks resumed rows: every resumed row carries `batch: s1-a2-r1`, `resumed_from: 1a20f29b` and its own timestamps. The primary and secondary analyses are reported three ways: original rows only (as in RESULTS.md now), original plus resumed, and resumed minus original on the cells where both exist, as a drift check. Resumed rows are not new samples of any world already observed; each fills a missing (world, condition) slot exactly once. The first answer for an assignment is never replaced.
- Risk: model behaviour hours apart could differ slightly (temperature cannot be set on Opus 5.5). The drift check above reports it.

## Option 2: full new batch, about USD 246

A fresh s1 batch of all 576 assignments at a new runtime: about 70 minutes of preparation plus about 9 minutes of calls. It gives a single-session cohort but duplicates 481 already-valid observations, which would be a second, separately labelled cohort and not pooled.

## Option 3: stop here

Report the incomplete cohort as it is (RESULTS.md). Cost USD 0 more. The primary finding stands; weak-check cells stay imprecise.
