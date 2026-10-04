# Deployment record

Experiment market-split-api; owner/source dmarz/market-split; isolated host checkout /srv/swarm/market-split-api/swarm-lab. Existing idle host sim-dmarz-2, exclusively claimed via agentops PR 49 until 2026-10-04T06:07:47Z. No active worker process was found; prior files remain untouched.

Python 3.12.3 with pinned PyYAML 6.0.3, numpy 2.0.2, matplotlib 3.9.4 and Pillow 11.3.0 in an isolated virtual environment. Hub reporting configuration is already provisioned. API credentials come only from the approved encrypted alias into worker environment over SSH stdin. No credential value or private endpoint is included here.

Authorization: the current researchers/dmarz/README.md grants $500 shared API spend across dmarz experiments and supersedes older per-experiment caps. This pilot allows at most 1,100 attempted calls, including qualification and repairs, with conservative byte/output reservations bounding its contribution at $30.91. Initial Q0 plus S1 requires at most 896 calls. A prelaunch hub snapshot found 153 dmarz runs, 19 with recognized cost fields, summing to $0.309802; this is incomplete reporting that can double-count cumulative/analysis records, not an account billing total. Actual usage and any unknown-billing attempts are reported in post-mortems. The persistent ledger is /srv/swarm/market-split-api/accounting/ledger.jsonl and must not be reset or copied to manufacture budget.

Run receipts and stage outcomes will be appended here after verification. Stop this worker and release the claim after final uploads; this existing host is not a disposable machine and its unrelated prior data must remain.

S0 fleet qualification passed: six done bundles, 12/12 valid mock episodes, zero API calls, all 42 artifact hashes verified and recovered locally. Representative public GIF playback checked. See reviews/s0-fleet-001-post.md.

Q0-001 stopped on note-length errors:4 paid calls,$0.004958; untouched bundle cancelled. V2 shortened notes and explicitly stated unchanged price/profit equations. New S0-fleet-002 passed12/12 mock episodes and42 artifact checks. Fresh Q0-002 passed4/4 episodes,32calls,$0.045908,14 artifact checks. Aggregate before S1:36calls,$0.050866,zero unpriced calls. See dated reviews for preserved failures and exact hashes.

S1-001 launched2026-10-04T02:28Z from22557dc:18 assignments,36episodes,864calls maximum, worker outer timeout7200s. The live S1 view was browser-verified with current model progress and stage filters. Qualification replay visibly advanced from round1 to8. Pinned-runtime re-execution of all32 Q0 actions exactly reproduced observations, traces and evaluations. Local Python3.9 produced a1e-16 HHI summation difference relative to the pinned Python3.12 runtime, so exact-byte reproduction uses the frozen runtime. No behavioral or metric-threshold change.
