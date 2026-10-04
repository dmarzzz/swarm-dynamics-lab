# Deployment record

Experiment: compositional-safety. Owner/source: dmarz/patchwork-hypotheses. Server: sim-dmarz. Dashboard: https://swarm-live.pages.dev/#/x/compositional-safety. This is separate from discussion-dose-v3.

Exclusive fleet claim: dmarz-compositional-safety, created via agentops PR 56 and released via PR 93 at 2026-10-04 03:59:19 UTC after the worker exited and all uploads reconciled. No infrastructure provisioning was required. Code, results and cumulative accounting remain on sim-dmarz, but there is no active worker or reservation. Obtain a fresh exclusive claim before any subsequent server work.

The isolated checkout is `/srv/swarm/compositional-safety/swarm-lab`; the pinned virtual environment is `/srv/swarm/compositional-safety/venv`. The host has Python 3.12.3. Requirements pin PyYAML 6.0.2 and Pillow 11.3.0. Reporting uses the provisioned module at `/usr/local/lib/swarm`; non-login shells require `PYTHONPATH=/usr/local/lib/swarm`. No credentials, private endpoints or server addresses belong in this record.

| Attempt | Source revision | Launch |
|---|---|---|
| s0-001 | 84fad81e3b8732e195a24f9ef4cf1a09ef76c7b5 | `python src/worker.py S0 s0-001` |
| q0-001 | 70ca3754b63257e709970ce3c79e3c483679eace | `python src/worker.py Q0 q0-001` |
| q0-002 | b7eec0facb5535efc45478677df56afebbeae95f | `python src/worker.py Q0 q0-002` |
| q0-003 | 45a01456e930463a99fa5eb9aee5bad26a453a37 | `python src/worker.py Q0 q0-003` |
| i0-001 | 232dad10f175006ee0f1a778346b6d7d355f2b1d | `python src/probe.py i0-001` |
| i0-002 | 0911e343031078af1e8e4de8f5a5018ffebe6535 | `python src/probe.py i0-002` |
| q0-004 | a286ec4c7712eb8cf9221b60455fc440a56434e7 | `python src/worker.py Q0 q0-004` |

Commands run inside the experiment folder using the pinned virtual environment and `SWARM_SOURCE=dmarz/patchwork-hypotheses`. API aliases are injected in process memory from the approved encrypted source. Each attempt has a frozen pre-run review. The finite worker does not restart itself or retry model calls.

The cumulative `accounting/study.jsonl` remains in this checkout across revision changes. Moving to another checkout requires preserving that same cumulative accounting and all attempt IDs; a fresh folder does not create a new authorization or permission to replay calls. The current study cap is 9,216 attempted calls and $185 reserved, within the owner's shared $500 allocation. Actual usage and retained reservations are separate quantities. The local ledger does not centrally enforce other studies' spending.

Each run reports to the hub. The public page renders synthetic images/GIFs and metadata; complete synthetic observations, event logs, manifests and hashes are retained with the team run artifacts. “Done” on a run means execution ended; the stage summary explicitly states whether qualification passed. Consult the post-mortems before launching a successor.
