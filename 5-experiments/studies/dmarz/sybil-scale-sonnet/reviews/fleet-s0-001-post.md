# Post-mortem: fleet-s0-001

- Experiment / owner / stage / date: sybil-scale-sonnet / dmarz (operator dmarz/scale-sonnet) / S0 fleet, scripted / 2026-10-04.
- Pre-run assessment: [fleet-s0-001-pre.md](fleet-s0-001-pre.md). Parent local-s0-001. Public revision f18f66da9de3fe82eebebc0f8113710cca3ab1c1; runtime source hash a1a619f7e39bb608ba48871766e8d1366d923db2df0cb00524dd5a65faffb230 (identical to the local check).
- Run: sybil-scale-sonnet/55c86cfa on sim-dmarz-3 under exclusive claim dmarz-sybil-scale-sonnet. Reproduce with the launcher `S0` action at the same revision.
- Disposition: advance to Q0.

## What ran and what happened

264 planned, 264 started, 264 terminal, 264 graded, 264 analyzed; 0 invalid, 0 not started, no duplicates or retries. Zero model calls, USD 0. Scripted qualification passed at every size (16/16 each). Stage elapsed 36 s plus rendering. Outcome counts match the local check and the Haiku study's fleet S0 (264/264).

## Visualization review

Mapping v1. The launcher `verify` action initially refused with `wrong_contact_image`: the hub listed progress.png before final_frame.png. This is the same contact-sheet ordering issue recorded in the Haiku study's Q0 post-mortem; the launcher `publish` action re-uploaded the unchanged final image, after which `verify` passed: 10 artifacts hash-matched, initial/final/hidden-badge PNGs and the 33-frame replay GIF are 1800×1200 and every frame decodes, every completed row re-scores to its saved evaluation, and the saved analysis recomputes exactly. Frames are labelled SCRIPTED.

## Experiment-quality assessment

Engineering-only stage; it shows the copied runtime runs end to end on the dedicated host, registers under the new hub id and uploads durably. No scientific claim. Evidence metadata unchanged (score 0, no model outcomes).

## Failure and repair ledger

| ID / kind | Observed evidence | Suspected or verified cause | Repair / diagnostic | Acceptance check and rerun evidence | Owner / status |
|---|---|---|---|---|---|
| S0-1 reporting | verify refused `wrong_contact_image` | verified: upload order puts progress.png first (known from the Haiku study) | launcher `publish` re-uploads unchanged images | verify passes, same hashes | dmarz/scale-sonnet / closed |

## Next run

Q0 per [q0-001-pre.md](q0-001-pre.md), same revision and runtime. Run `publish` before `verify` after every stage.
