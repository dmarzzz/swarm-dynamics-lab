# Deployment record: sybil-budget-sonnet

Host sim-dmarz-2 (dmarz fleet), exclusive claim `dmarz-sybil-budget-sonnet` (agentops PR #195, 2026-10-04 ~07:18Z; released PR #235 ~08:45Z). Launcher `scripts/run-sybil-budget-sonnet.py` in the private agentops repo (host taken from the merged claim). Earlier planned host sim-dmarz-7 was taken by another researcher before launch.

| Stage | Run | Revision | Result | Cost (USD) |
|---|---|---|---|---|
| fleet S0 | `sybil-budget-sonnet/ef4b32a6` | 5b1445a9 | 256/256 valid | 0 |
| Q0 | `sybil-budget-sonnet/35565940` | 63047d27 | 16/16 valid, qualified | 0.967557 |
| S1 | `sybil-budget-sonnet/f66ac194` | b8fed70d | 2,880/2,880 valid | 117.887289 |

Source hash for all three: `5cbe54cbd48bc164c7873d2a419710118455c74cf73122a137992361998cf680`. Study actual USD 118.854846 over 2,896 calls. Raw records fetched read-only after the worker exited into git-ignored `data/sybil-budget-sonnet/s1/`.
