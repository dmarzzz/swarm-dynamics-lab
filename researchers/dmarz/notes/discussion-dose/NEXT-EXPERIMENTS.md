# Next discussion experiments (proposed, not launched)

Written 2026-10-04 UTC by dmarz/private-control after [resample-v3-a1](reviews/resample-v3-a1-post.md) and the v3 qualification `v3-q0-a1`. Nothing here is authorized to run; each item needs dmarz's go and its own pre-run review. The v3 benchmark (`src/bench_v3/`) belongs to dmarz/discussion-bench-v3; items that change it are proposals to that owner.

## Where things stand

- Both Haiku 4.5 runs on v3 executed cleanly and both **failed the clean competence screen**. In resample-v3-a1, 62 of 72 individual ballots at the shared post-report checkpoint were ABSTAIN; after three private work turns, 11 of 12 clean decisions were correct. In v3-q0-a1 the owner reports full-evidence single-call answers that copied every value correctly and still picked a constraint-violating option.
- Re-probing an unchanged state is near-deterministic on this model and contract (72/72 votes identical), so a resampling-only arm adds nothing and is dropped.
- Shadow's review findings F1 and F2 are fixed on main (`6563e28`); future manifests pin that source or later.
- Measured cost: $0.0065 per call on v3 (resample-v3-a1: $6.10 / 936; v3-q0-a1: $4.39 / 636). Mean request about 5,300 input and 240 output tokens.

The open question that blocks everything else: **is the failure a missing work step in how the screen asks, or can the model not do the arithmetic?** The order below answers that first and only then spends on the scientific comparison.

## E1. Competence-screen diagnostic (Haiku 4.5)

Purpose: separate "asked to commit before working" from "cannot compute".

| Condition (clean worlds only) | What the agent gets before its ballot | Calls per world |
| --- | --- | --- |
| a. checkpoint (current screen) | report packet, then ballot | 3 |
| b. work-then-commit | report packet, one private work turn, then ballot | 6 |
| c. full-evidence single call (current diagnostic) | all documents, answer | 1 |
| d. full-evidence with work | all documents, one work turn, then answer | 2 |
| e. forced choice | as (a) but ABSTAIN removed from the ballot schema; diagnostic only, never a scientific arm | 3 |

Plus 6 acquisition calls per world. 12 fresh clean worlds (ids 41001-41012, families balanced, both strata), one replicate: **252 calls, about $1.70**. Implementation: a sidecar module like `resample_v3.py` (new files, patched arms) so bench_v3 is untouched until the owner adopts a change.

Readout and decision:
- (b) and (d) reach at least 10/12 while (a) and (c) fail: the screen is measuring the missing work step. Propose to the v3 owner that the qualification screen score the post-work clean decision (b), and that "reports only" gain one work turn before it is used as a baseline.
- (e) correct while (a) abstains: the model knows the answer but prefers to abstain; record as a contract/prompt property.
- All of (a)-(d) fail: capability limit for these templates; go to E2.

## E2. Model ladder on the same screen

Purpose: if E1 shows a capability limit, find the cheapest model that passes before any scientific run. Same 12-world E1 plan, unchanged prompts and grammar, on Sonnet 5.5 (`claude-sonnet-5-5`). 252 calls; cost at that model's pinned rates, frozen in the pre-run review. Only run if E1's (a)-(d) all fail on Haiku. A model switch is a new qualification, never pooled with Haiku results.

## E3. v3 stage 2: discussion vs private work, revised baseline

Purpose: the question v3 exists for, once a model passes the screen. Uses the F1/F2-fixed source and whatever screen revision E1 supports.

- Arms (v3, unchanged except the baseline): independent, reports(+1 work turn if E1 says so), private work, public board; 3 rounds; shared post-report checkpoint.
- Primary contrast (v3 README): within resolvable worlds, (attack board - clean board) - (attack private - clean private) on parent ground-truth error; ambiguous-world unsupported answers as the separate safety endpoint; vote metrics reported with the quorum rule from F1.
- Size: 24 fresh worlds (12 resolvable, 12 ambiguous), one replicate: about 2,450 calls including diagnostics and the 36 memory fixtures, **about $16** on Haiku. Holdout stays closed; this is still exploratory.
- Gate: clean screen passes on the qualification split first; zero malformed/provider-failed calls; usage complete.

## E4. Inheritance across generations (SEC-52), after E3

Purpose: does a false fact admitted once persist when the merged memory seeds the next generation's children? Two generations, merged memory from generation 1 seeds generation 2's private histories, with and without a correction document in generation 2. Builds on v3's memory fixtures; 12 worlds, about 1,500 calls, about $10. Design only after E3 shows the measurement is trustworthy.

## Dropped or deferred

- Resampling-only control: dropped on Haiku (deterministic re-probes). Revisit only with a sampling setting where probes vary.
- pc-style private-control on v2: superseded by v3's private-work arm.
- More v2 runs: v2's claim grammar is replaced by v3's fixed key map.

## Total if all run

E1 $1.70 + E2 (only if needed) + E3 about $16 + E4 about $10, well inside dmarz's $500. Each runs on its own claimed box, one run per server.
