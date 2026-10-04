# Post-mortem s0-fleet-001

- Owner/stage/date: dmarz / exploratory scripted S0 / 2026-10-04.
- Parent: s0-local-002; pre-run: s0-fleet-001-pre.md.
- Disposition: advance to frozen scripted S1; no paid model run.

## What ran and what happened

Three planned → assigned → completed → verified hub runs, 18/18 valid episodes, two task clusters, no duplicate or missing attempts. Model calls/tokens/API cost: 0/0/$0. Runtime about 12 seconds per hub run. All finance and control outcomes match the corrected local qualification. Source/config hashes and upload receipts are preserved in results/s0-verified.json and each run's summary.json. Server is the exclusively claimed sim-dmarz-market-split.

Runs: market-split/d37a320f (none), market-split/07d3a530 (firm), market-split/803b9107 (owner). The programmed split scores fragmentation under every rule, but effective evasion only under firm regulation. Scripted mean profit lift versus merged: +7202.42 credits with firm regulation; -91 with owner/no regulation. This validates the accounting mechanism and cannot establish natural discovery.

## Visualization review

Mapping market-split-v1. Every hub run has confirmed progress PNG, final PNG and 12-frame GIF, plus raw JSONL, summary and empty visualization-error file. All 18 artifact SHA-256 values match the files on the server, and recovery copies were downloaded locally. The public experiment page shows the plan, condition table and final-frame contact sheet. The firm-regulation run page loads PNGs at 1800×1200 and GIF at 1080×720. Browser screenshots of the same published GIF showed round 1 then round 11: actual playback confirmed. The registration events and HHI gap agree with the saved trace; no missing or interpolated rounds.

## Experiment quality and repair ledger

All 10 self-test groups passed on the actual server before launch with network sockets blocked. Zero accounting, invalid-output or rendering failures occurred. Earlier setup-only failures were first-boot package-manager contention and a skipped reporter-credential task; both were repaired through scoped standard provisioning before any run was queued. No experiment was rerun to obtain favorable results. The discovery primary is now independent of regulator assignment; regulatory success is separate. No API transport, LLM competence or research-gate claim is made.

## Next run

s1-fleet-001: execute the predeclared 432 scripted episodes on dev markets 10–15, both seeds, thresholds and registration fees. Same engine/design, one finite worker, $0 model budget. Verify all traces and artifact hashes, analyze task-cluster differences, stop the worker, release the claim and destroy the temporary host. Formal S2 and model calls remain disabled.
