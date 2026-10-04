# Records of chain 003 (memory-handoff-qwen on gpt-6-luna)

Copied on 2026-10-04 by dmarz/pipeline-memory from the archive the operator (dmarz/fleet-monitor) delivered from the run server: `chain-status.json`, the chain log (one line), the launcher's saved `status` and `verify` outputs, the summary of each stage, and for P0, Q0 and S1 the gzipped assignments (every message sent, with evaluator labels), answer rows and hash-chained journal; for S1 also `analysis.json`. Not included: the S0 rows (scripted, regenerable), the ledger file (its totals are in the status), the frames, `replay.gif` and `replay.html`. Scanned before committing: no credential, request header, hub address or server address. Paths under `/srv/swarm/` are locations on the run server.

`recompute.py` recomputes every number of the "Chain 003 (gpt-6-luna)" section of [RESULTS.md](../../RESULTS.md) from these rows and checks them against the package at the launch commit:

```
git archive f717bb2d 5-experiments/studies/dmarz/memory-handoff-qwen | tar -x -C <dir>
python3 recompute.py <dir>/researchers/dmarz/notes/memory-handoff-qwen
```

`recomputed.json` is its output on 2026-10-04 (15 of 15 checks true). See the [post-mortem](../../reviews/chain-003-post.md).
