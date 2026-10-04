# Post-mortem: fleet S0 s0-001

- Experiment / owner / stage / date: sybil-newcomer-sonnet / dmarz / fleet S0 (scripted) / 2026-10-04.
- Pre-run assessment: [fleet-s0-001-pre](fleet-s0-001-pre.md); parent [s0-local-001](s0-local-001-post.md). Revision 5ad4d2526eec267b8fda1acdb9f579495ef06cd0, source hash `a0fa76922ed6000bb07bca6c9d9bbae312b566f4e4cd7271e147c87f75833ed4` (same as local S0).
- Run ID: `sybil-newcomer-sonnet/b8f340a9`, batch s0-001, host sim-dmarz-5 under claim dmarz-sybil-newcomer-sonnet. Launcher printed the immutable plan URL at that revision with README sha256 `7eeb4c0d7467dbd975d97af667df2cf95b72c0d33b4196ac32bd374471dc9ae0` (sections and bytes matched).
- Disposition: advance (engineering). Q0 remains blocked on review or owner waiver.

## What ran and what happened

- 198 planned → 198 started → 198 terminal → 198 graded → 198 analyzed; 0 invalid, 0 not started.
- 0 model calls, $0; 10.1 s elapsed. Host setup ran the 8 selftests at the pinned revision and passed.
- Scripted qualification passed in all three shapes; counts equal the local S0.

## Visualization review

- Mapping v1. Delivered initial, live progress, final (1800×1200) and an 8-frame replay GIF; checksums of all eleven uploaded artifacts match the host's saved files; every GIF frame decodes.
- The launcher's `verify` first failed with `wrong_contact_image` because the hub listed `progress.png` before `final_frame.png`. Running `publish` (re-upload in mapping order, as the parent study's workflow does) fixed the order; `verify` then passed. Reporting only, no rerun.

## Experiment-quality assessment

Engineering stage only. It confirms the exact public revision, launcher, claim and plan checks, host environment and hub/artifact path. No scientific claim; evidence_confidence stays 0.

## Failure and repair ledger

| ID / kind | Observed evidence | Suspected or verified cause | Repair / diagnostic | Acceptance check and rerun evidence | Owner / status |
|---|---|---|---|---|---|
| R1 reporting | verify: wrong_contact_image | hub lists artifacts by upload order; worker's last live progress upload came after the final frame | launcher `publish` | verify passed on the same run | dmarz/newcomer-sonnet / closed |

## Next run

Q0 `q0-001` per [q0-001-pre](q0-001-pre.md), at a revision with the same source hash. Blocked until dmarz waives cross-researcher review for this study or another researcher files a review (task `review-sybil-newcomer-sonnet`). After S1 and Q0 complete, run `publish` before `verify`.
