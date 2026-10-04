# sybil-specialists-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/orbital-orchestrator (orbital-one), server sim-dmarz-4, claim `dmarz-sybil-specialists-opus` to 13:40Z. Not a review. Last updated 2026-10-04T07:58Z.

## 1. Results so far

- S0 (run 309db47b): 216 of 216 valid, 0 model calls, 40 seconds, finished 07:42:05Z.
- One-call Opus interface probe passed (USD 0.0103, commit 13c76473).
- No paid stage has run. `reviews/q0-001-pre.md` and `reviews/s1-001-pre.md` both say "blocked until dmarz records a review decision". The server has been idle since 07:42Z.
- The Sonnet version of this study was superseded before any paid call.

## 2. Gate forecast

Nothing is running. Q0 is 24 calls at effort low with a 3,000-token cap, a few minutes. Thresholds unchanged: 100% structural validity, at least 95% field accuracy, at least 90% exact packets, 100% abstention on the three missing-fact packets. The plan names the plausible failures: a missing skill answered instead of null, thinking exhausting the 3,000 cap, a refusal. The sister study sybil-scale-xl passed its Opus Q0 tonight at effort low with 24 of 24 valid on much larger packets, which makes an execution failure here less likely (my inference; different packets and cap).

## 3. Next run

- **Blocked on:** dmarz recording a review decision (waiver or review) for this study. Everything else is in place.
- **When the waiver lands:** run Q0 and S1 as one chain under the software gate, as sybil-scale-xl did (8 seconds between Q0 and S1). `s1-001-pre.md` already exists; its only open item is restating the cost from Q0's measured usage, which is arithmetic (expected USD 1.6 to 5.7 against a USD 40 cap). S1 is 192 calls, about 15 to 30 minutes.
- **If Q0 fails on `nonterminal_output`:** raise the output cap (sybil-scale-xl uses 8,000). The cap is in `design.yaml` and so in the source hash; a new batch needs S0 again (40 seconds).
- **If Q0 fails abstention:** a competence result at effort low. The one change to try is effort medium, as a new batch. Do not edit the prompt; the Haiku and Sonnet cohorts used it unchanged.
- **After S1:** no further stage is planned in this study.

## 4. Design notes for later runs

- The whole paid part of this study is 216 calls and about USD 2 to 6. Its setup time is larger than its run time. A waiver recorded per study in advance, for every study in a family, would remove the wait.
- Two finished Sonnet replications in this family show the model swap moved the primary contrasts by 1.4 pp and 2.8 pp. This study will show whether that holds for Opus on the specialist pilot's 12 worlds. If it does, model replications in the sybil family have answered their question.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 4 and 5.
