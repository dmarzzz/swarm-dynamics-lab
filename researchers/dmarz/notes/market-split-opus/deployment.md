# Deployment record: market-split-opus

2026-10-04; owner dmarz/market-split-opus. Server `sim-test-01` (existing 2 vCPU test server owned by dmarz), exclusive agentops claim `dmarz-market-split-opus`. One experiment, one worker. No server is created or destroyed by this study. Older checkouts of other studies on the server's disk are left untouched; this study lives under its own directory with its own checkout, virtual environment, ledger and worker log.

Launcher: `scripts/run-market-split-opus.py` in the private agentops repository. Runtime: Python 3.12.3 with PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4 and Pillow 11.3.0 from `requirements.txt`. The hub reporting configuration is already on the server. The model key and workspace id are read from the encrypted agentops store and passed over ssh stdin into the worker's process environment; they are not written to disk, a command line or a log. No credential, address or hub token appears in this repository.

Budget: at most 950 attempted calls and USD 60 for the whole study, enforced before each request by the study ledger. The ledger is created at the first paid stage and is never reset or copied. This study draws on dmarz's shared USD 500 allowance.

Process note: the agentops run-queue document says dmarz's runs are launched from orbital-one. This study is launched from halcyon on the instruction of the reviewer session dmarz/fleet-monitor, which relays dmarz. The conflict is recorded in [ISSUES.md](ISSUES.md) as O3.

Stage receipts are appended below after verification.

## Receipts

2026-10-04 07:46 UTC: claim `dmarz-market-split-opus` merged (private agentops PR 204), exclusive, `sim-test-01`, until 17:46 UTC. Immediately before claiming, agentops main had no active claim naming the server and `ps` on the box showed no worker, container or session of any study.

2026-10-04 07:47 UTC: `setup` at commit `8c27b690b42cf473c65975d58b8ed3d7487730e1`. 18/18 offline tests passed on the server. Runtime Python 3.12.3, PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4, Pillow 11.3.0. Engine `9f520ef8fc17f8c2fcba0ebfbd2555a91fbbf026db55c5c04b9b2fc9a720577d`, design `c0e9af0975b0d6a00a38202cce0af20ea152cd060673225f04f3f6ef6aa4823f`.

2026-10-04 07:47-07:50 UTC: `s0-fleet-001`. Public plan at `8c27b690` checked by the launcher (SHA-256 `729cd1b2c193308849126e69329c616e7498dbda47daa22efc76de9fd07e0b92`, published bytes equal local bytes). Experiment registered with that immutable link. Six bundles done, 12 valid scripted episodes, 0 model calls, USD 0, 42 artifacts hash-verified against the hub. The study ledger does not exist yet. See [s0-fleet-001-post](reviews/s0-fleet-001-post.md).

The paid stages are pinned to the commit that adds the pre-run review [phase2-pre](reviews/phase2-pre.md); its hash and the server redeployment are recorded in the next receipt. Source and design are unchanged from `8c27b690`, so the S0 gate applies.

2026-10-04 07:58 UTC: `setup` at commit `d1e80164e8fabe6bbe814ff686590b98d479b24d`, the commit that contains the pre-run review for I0, Q0 and S1. This is the pinned revision for the paid stages. 18/18 offline tests passed on the server again; engine and design hashes are unchanged from `8c27b690`. Public plan at this commit: SHA-256 `e998c6c46c521488b5741ac4832aa8da7134adf5fb08d950cad6804f37e29fd8`, published bytes equal local bytes, required sections present. Zero-cost checks run against the live hub from the server: the coordinator gate refuses Q0 and S1 (`matching_interface_probes_incomplete`), the three paid attempts' reviews are committed and frozen at this commit, and the launcher refuses a paid stage without `--confirm-paid`. No ledger file exists, no worker is running, and no model inference call has been made. Phase 1 ends here; the next action is the reviewer's go.

2026-10-04 about 08:10 UTC: reviewer's go received with one amendment (study dollar cap USD 60 to USD 160; [phase2-go](reviews/phase2-go.md)). The pin `d1e80164` above is superseded before any paid call. New hashes: engine `56c67cd08ea1a99a55c1a31dea8899663cbe91aae30970e384dbf39cc39c047b`, design `8d952af0314ab58835c93b90eb0d7b4c2ccc8497c64170f7948596d8393a687d`. The paid stages are pinned to the commit that contains the amendment and the verdict; receipts follow.

2026-10-04 about 08:00 UTC: `setup` at commit `b097331b874f2dcab2b31a830e54cdc39f9d321d`, the pinned revision for the paid stages (amendment and reviewer verdict included). 18/18 offline tests on the server. Public plan at this commit: SHA-256 `99e8133f7e3317cf827c7700c1cc657122287a473395874f37953bad0eac22be`, published bytes equal local bytes. `s0-fleet-002`: 6/6 scripted bundles, outcomes identical to `s0-fleet-001`, 42 artifacts verified, 0 model calls ([post](reviews/s0-fleet-002-post.md)).

2026-10-04 08:01-08:02 UTC: `i0-001` passed 6/6; 6 calls, USD 0.060992 ([post](reviews/i0-001-post.md)). The study ledger was created at this stage. The model key reached the worker over ssh stdin only.

2026-10-04 08:02-08:05 UTC: `q0-001` passed 4/4 at 100% of the reference; 32 calls, USD 0.333348; exact replay 32/32; 14 artifacts verified ([post](reviews/q0-001-post.md)). Ledger 38 calls, USD 0.394340, all priced. Projection for S1 inside all three limits (study about USD 11.5).

2026-10-04 08:05 UTC: `s1-001` enqueued (18 bundles) and the first finite worker of nine bundles started. One worker; the remaining bundles follow in further finite workers, one at a time.
