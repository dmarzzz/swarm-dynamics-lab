# Revisions to the Swarm of Theseus film

## v3, 2026-10-05

Same narration as v2, to the sample. One line of the picture changed: the status under the wall during the closing.

v2's line read "status checked 2026-10-05 00:23 utc // fifty-seat qualification (gpt-6 sol) passed // full fifty-member
turnover run in progress, no result yet". The hub recorded that run's execution as closed at 00:33 UTC, ten minutes
later, with its scientific review still to come. The line was dated and true when written, and out of date before the
film reached the site.

v3's line names only what is settled: "fifty-seat qualification (gpt-6 sol) passed 2026-10-04 // the fifty-member
turnover study reports separately // its outcome is not shown here". It does not need to change when that study
publishes. The film still gives no outcome for it.

Checked: the audio track of v3 is identical to v2's (decoded and compared sample for sample), and the status line was
read back from the encoded file at 226 s. Use v3; v2 is kept as filed.

## v2, 2026-10-05

vishesh reviewed the films on the results site for accuracy on 2026-10-05 at 00:03 UTC and sent notes. v1 stays filed as
`artifacts/theseus-film/theseus-film-v1.mp4`; v2 supersedes it and is 3 min 57 s (v1 was 3 min 44 s).

| Where in v1 | What the review found | What v2 does |
|---|---|---|
| 03:29 to 03:37, closing | "Its qualification failed ... that turnover run has not happened yet" was true on 2026-10-04 and is now out of date. | Says the earlier follow-up failed its qualification and that a later qualification, with GPT-6 Sol and a fifty-seat roster, passed. Says the fifty-member turnover study is separate from this pilot and sends the viewer to its dated results. A dated status line is on screen under the wall. The film does not report that study's outcome. |
| Whole film | The pilot's numbers can be read as being about the newer fifty-seat study. | A second line under the title stays on screen for the whole film: historical pilot, rule supplied to the founders, crews of three, 6 paired synthetic worlds x 6 conditions = 36 dependent runs. The opening sentence calls it an early pilot. |
| 03:13 to 03:20 | "a question added nothing measurable on top of notes" was wider than the measure. | "On that measure, no added benefit from the question was established", after naming the measure: the last two steps, crews of three, six worlds, one model. |
| 02:57 to 03:03, observatory | The narration said observatory crews with notes "got every case right" while the picture lit all six steps. Those crews made errors in steps 0 to 3 (4, 3, 4, 3 and 2, 2, 4, 3 right out of 4) and were right on every case only in steps 4 and 5. | The sentence now says "in those last two steps", and steps 0 to 3 stay dimmed while the observatory columns are picked out. |
| End card | No sign that the film had been revised. | Adds "version 2, 2026-10-05" and why. |

The results at 02:36 to 02:50 (100%, 100%, 92%, 52%, 90%) matched the study's records in the review and are unchanged.

### What was checked

- `make_film.py` still refuses to build unless the study's records support each narrated fact. v2 adds checks for the
  observatory sentence at the step level, for the "no added benefit" sentence (notes and notes plus question score the
  same on steps 4 and 5), and for the passed fifty-seat qualification (`execution-diagnostic/sol50/scale50/Q50-POST-MORTEM.md`).
- The fifty-member run (`swarm-of-theseus-s50-main`) was read from the public hub at 2026-10-05 00:23 UTC: started,
  still logging conditions, no finished result. That is the status line's date.
- The finished file's whole audio track was transcribed by Whisper (large-v3-turbo) and compared with `script.json`:
  619 scripted words, every difference a spelling or number form ("36" for "thirty-six", "Reid" for "reed"). The last
  7.0 s, over the end card, are silent.
- Frames were read back from the encoded file at 4 s, 222 s, 229 s and 235 s.

### What was not checked

- Nobody has listened to the narration by ear, in v1 or v2. The check above is a machine transcription.
- The picture and the narration were not compared frame by frame outside the five changed segments. The other 24
  narration clips are the v1 recordings, unchanged.
- The status line will go out of date when the fifty-member run finishes. It carries its own date for that reason.
  To change it, edit `STATUS` and `REVISED` in `make_film.py` after rereading the study's records. (It did, the same
  hour: see v3 above.)

### How it was rebuilt

Five narration clips were spoken again (W1, R4, C2, C4 and the new C5) with the same voice and speed. The picture was
recorded again from the page, because the timeline follows the clip lengths. `record_stream.mjs` is new: it pipes frames
straight into the encoder. The shared recorder writes every frame to disk first, about 5 GB for this film, and the
disk on the build machine could not hold that.
