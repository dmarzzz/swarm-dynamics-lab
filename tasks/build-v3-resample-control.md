---
id: build-v3-resample-control
type: task
title: Sidecar repeat-vote (resample-only) control for discussion benchmark v3
kind: build
status: claimed
priority: p1
owner: dmarz/private-control
for: dmarz
created: 2026-10-04
created_by: dmarz/private-control
depends_on:
- build-discussion-benchmark-v3
topics: []
claimed_at: 2026-10-04T02:26Z
updated: 2026-10-04T03:11Z
---

## Goal

Build and, after the v3 review passes, run the resampling-only control that the [v3 README](../researchers/dmarz/notes/discussion-dose/benchmark-v3/README.md) defers ("would answer a separate mechanism question"). Question from [pc-H4](../researchers/dmarz/notes/discussion-dose/reviews/pc-H4-a1-post.md): when private work drifts toward the planted value, is that self-revision or ballot resampling?

Coordination with dmarz/discussion-bench-v3, which owns `src/bench_v3/` and the v3 launch:

- New files only (a module subclassing the v3 `Runner` with a `resample` arm: same shared report checkpoint, same probe count, no work posts between probes). No edits to `src/bench_v3/*` or `benchmark-v3/*`. If an upstream hook is needed, ask through dmarz's inbox first.
- Arms in one run, per world: reports, private, resample (pairing needs one run; v3's private arm is repeated, not borrowed).
- Worlds outside v3's reserved development, qualification and holdout IDs and its property-test range.
- Same launch gate as v3: an approved launch manifest that hashes the passed independent review. No launch before `review-discussion-benchmark-v3` is done. Separate box, separate hub batch; never shares a worker with the v3 launch.
- About 12 worlds, about 1,000 calls (~$6 under the dmarz $500 budget).

## Done when

- [x] Sidecar module and offline tests (equal probe counts, no posts in resample arm, shared checkpoint, v3 selftest still passes) committed.
- [x] Design note and pre-run review committed before any paid call.
- [ ] Run after the v3 review passes; post-mortem committed; claim released.

## Progress

Built b3e1bb2, resynced to v3 fixes 9c4c945, hub wrapper 50d9180, waiver gate a1ddb36. Launched resample-v3-a1 at 658a81a on sim-dmarz-5 (claim dmarz-v3-resample), hub run discussion-v3-resample/1004-030243-d6fa86. Independent review waived by dmarz (launch/resample-v3-review-waiver.md).
