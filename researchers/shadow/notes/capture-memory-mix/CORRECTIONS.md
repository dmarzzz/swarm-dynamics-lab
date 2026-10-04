# capture-memory-mix: corrections (2026-10-04, shadow/sol-cm2)

Prompted by dmarz's review (`researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json`, item
"Capture and memory mix · Qwen MP3", reviewed at ee14e0f3). Every defect it lists was real. This file says what was
wrong, what changed, and whether any number moved. Short version: the reporting was wrong in four places, the code
had one real bug (hub capture fraction) and one resume inefficiency, and **no headline number changes**. The
verdict "mixture rescue does not generalize" is correct and the README now leads with it.

## C1. Attempt lineage was not disclosed (MP3: 327 raw records, 127 invalid, 180 selected)

What was wrong: pilot episode files are append-only and a resumed worker re-runs episodes that lack a fully valid
attempt. `analyze.py` silently deduplicated per (cell, task, seed, arm), keeping the last valid record. The tables
reported only the 180 selected records.

Fix: `src/lineage.py` makes the attempt structure explicit (attempt = consecutive group of one episode's arms) and
selects per EPISODE: the last attempt whose arms are all valid, else the last attempt. That is outcome-blind and
keeps arms paired. `analyze.py` uses it and every MP table now has an "Attempt lineage" section. Check that the
new rule picks exactly the records the old one did:

    python3 src/lineage.py --check results/pilot-mp results/pilot-mp2 results/pilot-mp3
    results/pilot-mp:  raw 459, selected 432, identical: True
    results/pilot-mp2: raw  90, selected  90, identical: True
    results/pilot-mp3: raw 327, selected 180, identical: True

| pilot | model | episodes | attempts | episodes re-run | raw records | raw invalid | superseded | selected | selected invalid |
|---|---|---|---|---|---|---|---|---|---|
| MP | gpt-4o-mini | 144 | 153 | 5 | 459 | 13 | 27 | 432 | 0 |
| MP2 | gemma-3-27b | 30 | 30 | 0 | 90 | 46 | 0 | 90 | 46 |
| MP3 | qwen3-235b | 60 | 109 | 49 | 327 | 127 | 147 | 180 | 2 |

Sensitivity: no episode in any pilot has more than one fully valid attempt, so "last valid" vs "first valid"
cannot differ; `python3 src/lineage.py --sensitivity <dirs>` prints identical A1 means and recovery counts under
both. The re-runs were triggered by validity only (provider HTTP 400s on qwen, the 05:58Z ledger mishap on
gpt-4o-mini), never by outcome.

Note: 79 further invalid qwen records from the first, buggy qwen attempt live in `results/pilot-mp3-attempt1`
(git-ignored, disclosed in preregistration.md section 6). They are not in the 327.

## C2. "No retries" vs "redos"

What was wrong: the table footer said "none are dropped or retried", `preregistration.md` section 4 and the
worker docstring said "never retried", while the README described redone episodes. The first statement was true for
the scripted stages M0/M1/M2 and false for the pilots.

Fix: footer replaced by a retry-accounting line generated from the lineage; preregistration gains a labelled
amendment (section 6, 2026-10-04) stating the pilot re-run policy; worker docstring corrected. Also fixed in
`worker.py`: the resume check required EVERY record ever written for an episode to be valid, so an episode with an
invalid first attempt was re-run on every resume even after a valid attempt existed. It now skips an episode once
any attempt is fully valid. On the saved records this would not have changed the selection (C1 sensitivity), only
saved calls.

## C3. Caption said round 50, config says 30

What was wrong: the MP/MP2/MP3 captions were copied from the scripted stages (recovery 80, scored at round 50).
Pilots use recovery 40, scored at round 30 (`eval_round` in every record's cfg). The trace table header also
listed r50/r80 columns that were empty and labelled the long/short split "r50" while computing it at r30.

Fix: `analyze.py` reads `eval_round` and `recovery_rounds` from the records and writes them into the captions and
headers. The scripted README sections (M0/M1/M2) correctly say round 50 and are unchanged.

## C4. Hub capture fraction above 1

What was wrong: `worker.metrics` averaged the captured counts over arms and divided by the FIRST arm's valid count.
When arms have different numbers of valid records this exceeds 1: MP3 f = 3/4 reported 1.0606, MP2 L = 1 reported
1.3333 (and MP2 f = 1/2 and full, MP3 full were off downward). Bug in the code, not the data.

Fix: capture rate = captured valid arm records / valid arm records (capture is shared by an episode's arms).
`src/resummarize.py` rebuilt every pilot `<cell>.summary.json` from the selected records with the fixed formula and
added lineage counters (`raw_records`, `raw_invalid`, `superseded_records`, `episodes_rerun`, `attempts`) plus
`model_calls_all_attempts` / `cost_usd_all_attempts` next to the selected-record figures. Per-arm call/usd fields
were dropped from the summaries because the counters in the records are cumulative over an attempt's arms and cannot
be split per arm. The hub runs were re-pushed from the corrected summaries.

| cell | old captured | new captured |
|---|---|---|
| MP2 L = 1 | 1.3333 | 1.0 |
| MP2 full | 0.8889 | 1.0 |
| MP2 f = 1/2 | 0.8333 | 1.0 |
| MP3 full | 0.9722 | 1.0 |
| MP3 f = 3/4 | 1.0606 | 1.0 |

All gpt-4o-mini cells were already correct (equal valid counts across arms).

## C5. gpt-4o-mini raw episode records were not in git

`results/pilot-mp/*.jsonl` was git-ignored (only on the hub), so the MP numbers could not be recomputed from the
repo. The 11 episode files (1.1 MB) are now committed. Call logs stay on the hub (size).

## What does NOT change

Every A1/A2 mean, CI, count and Fisher p in README.md and results/MP*.md is identical before and after (the
selection is identical, C1). The cross-model verdict stands as dmarz wrote it: the mixture rescue reproduced on
gpt-4o-mini only, not on gemma-3-27b, reversed on qwen3-235b. The long-list-read moderator is a post-hoc lead from
three models, not a finding. The Claude replication (preregistered in preregistration.md section 7) is the next test.
