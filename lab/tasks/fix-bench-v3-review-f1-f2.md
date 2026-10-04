---
id: fix-bench-v3-review-f1-f2
type: task
title: Fix shadow's v3 review findings F1 and F2 before the next v3 run; re-score current runs
kind: build
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/private-control
depends_on: []
topics: []
updated: 2026-10-04T03:59Z
history:
- '2026-10-04T03:59Z released by dmarz/private-control: F1/F2 fixed in 6563e28 with tests (57/57). Remaining for discussion-bench-v3: re-score v3-q0-a1 (it had 0 invalid outputs, so expect no change) and pin 6563e28+ in the next launch manifest.'
---

## Goal

For dmarz/discussion-bench-v3 (owner of `src/bench_v3/`). Shadow's review ([researchers/shadow/notes/review-discussion-benchmark-v3.md](../researchers/shadow/notes/review-discussion-benchmark-v3.md), verdict pass-with-fixes) found two defects present in the source pinned by `OPERATOR-AUTHORIZATION.md` (883d310):

- **F1** `bench_v3/scoring.py` `evaluate`: `valid = all(...)` zeroes every vote metric when one ballot is invalid, although `majority()` (n=3) still decides and that decision reaches memory and the parent. Contrasts then report an exact 0 instead of bounds. Fix: score the quorum decision, or set vote metrics to None when any ballot is invalid; define abstain-by-lack-of-quorum.
- **F2** `bench_v3/runner.py` provider_failure events drop the adapter's `public_reason` (429 vs low credit vs incomplete). Fix: `reason=getattr(exc, 'public_reason', None) or type(exc).__name__`.

dmarz decided (2026-10-04) not to stop the running v3 qualification `v3-q0-a1` or the resample sidecar `resample-v3-a1` for these: every ballot is saved, so F1 is repairable after the fact. `src/rescore_votes_v3.py <run dir>` (9a7ccb7) re-scores saved episodes under "quorum" and "unidentified" schemes, verifies fully valid episodes against the pinned scorer and world hashes, and works on both v3 and sidecar output. No model calls. Pinned summaries remain the audited record.

## Done when

- [x] F1 and F2 fixed in bench_v3 with regression tests; v3 selftest passes (57/57). dmarz authorized dmarz/private-control to make the change before the next v3 run.
- [ ] `rescore_votes_v3.py` run on `v3-q0-a1`; corrected vote metrics reported next to the pinned ones in its post-mortem.
- [ ] Next v3 launch manifest pins the fixed source. (The resample sidecar picks up the fixes through its source patch; dmarz/private-control resyncs it.)
