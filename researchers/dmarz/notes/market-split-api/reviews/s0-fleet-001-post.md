# Post-mortem: s0-fleet-001

Experiment market-split-api, dmarz/market-split, S0, 2026-10-04 UTC. Parent s0-local-001; pre-run assessment s0-fleet-001-pre.md. Disposition: advance to Q0.

## What ran and what happened

Six planned, started, terminal, graded and analyzed bundles; 12/12 episodes valid, no duplicates or missing records. 96 mock requests; zero API calls, tokens or dollars. All six competence and visualization checks passed. Remote Python 3.12.3 selftest passed all ten groups with network calls blocked. Code 2e56e0e90333585f0f9b8865b56622c2bae0e6d2; engine f68e41b7beccaded79189bae61465853f3b34abf45b746a73755b4c71195837c; design 79b6e321c2a9f4cd0f6b36ee43198d64eb5831fc617e83cf2db9ee62d6ee1b32.

Run suffixes: 27b25d2ef595, c63c94e545e2, c4b0d7a51df0, c16f55cf3e18, a272adce4f39, 8e3683a2bf35. Reproduction: coordinator.py stage S0 --attempt s0-fleet-001, followed by worker.py --attempt s0-fleet-001 --max-runs 6; use a fresh attempt for any new execution. Recovery manifest and all files retained in ignored results/fleet-recovery. Compared 42 uploaded SHA256 digests with server files, and downloaded final receipts with local bytes; no mismatches. Worker exited 0.

## Visualization review

Mapping market-split-api-v1 delivered six live PNGs, six final 1800×1200 PNGs and six 1080×720 GIFs, eight logical rounds each. Final traces agree with summary firm counts, profits and HHI series. Browser playback for 27b25d2ef595 visibly advanced from round 1 to 5 and showed registration and the diverging HHI series. The dashboard lists all six done runs and final frames. No renderer/upload failures. A stale tab initially lacked the new registration; reload resolved it. Sequential-arm live display can reset its logical-round cursor; final replay aligns both arms.

## Experiment-quality assessment

This proves the adapter, simulation, reporting and replay transport work with deterministic mock responses. It says nothing about natural model discovery. Mock dynamic responses deliberately split. Controls preserve total capacity/cash and restrict the locked arm to one firm. Evaluator truth stays out of public actor observations. Two qualification tasks are development fixtures; the six S1 tasks and holdout remain unopened by the model.

## Failure and repair ledger

No experiment failures. A local recovery extraction used a Python-version-specific option; retried with explicit member path/link validation and verified hashes. No server or model rerun required.

## Next run

Q0-001 uses the exact source/design and real frozen Haiku model, tasks 20/21, seed31, no regulator, eight rounds and both arms: four episodes, at most 32 calls. Advance only if all actions are valid, all profits positive and each profit is at least 75% of the scripted one-firm reference. Preserve and diagnose failures; use new fixtures after material repair. S2 remains disabled. Standing shared API authorization is $500 with a persistent 1,100-call experiment cap.
