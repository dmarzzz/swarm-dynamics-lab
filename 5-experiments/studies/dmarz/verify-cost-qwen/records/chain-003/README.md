# Records of chain 003 (verify-cost-qwen on gpt-6-luna)

Copied on 2026-10-04 by dmarz/pipeline-verify from the archive the operator (dmarz/fleet-monitor) delivered from the run server's results directory. Launch commit `61a7269f`, code commit `c74da5bc`, source hash `b1b15d25…`. See [the post-mortem](../../reviews/chain-003-post.md) and [RESULTS.md](../../RESULTS.md).

- `results/chain-status.json` and, per hub run, `summary.json`, `analysis.json`, `failures.json`, `assignments.jsonl.gz`, `requests.jsonl.gz` (the exact system and user text of every request) and `episodes.jsonl.gz` (one terminal row per unit: answer as returned, grade, accounting). Runs: `390ff085` S0, `72e26f72` P0, `01699c85` Q0, `80380bb4` S1.
- `ledger.jsonl.gz`: the chain's ledger (reservations, attempts and settled cost per call id).
- `launcher-status.json`, `launcher-verify.json`: the launcher's `status` and `verify` outputs as saved by the operator. `verify` exited 1 with `chain_status_is_for_another_model`; the post-mortem explains why that is not a discrepancy.
- `offline_verify.py`, `offline-verify.json`: every check of `chain.py verify` that needs no hub, run again on these files with the chain's model set: `python3 records/chain-003/offline_verify.py records/chain-003`.
- `recompute.py`, `recompute.json`: the grades, the twelve strata and the primary recomputed from the request texts and the returned answers without the study's scorer: `python3 records/chain-003/recompute.py records/chain-003`.

Not copied: frames and the replay GIF (not in the delivered archive), the uncompressed duplicate of the rows, and the chain's log. Scanned before committing: no credential, request header, hub address or server address. Paths under `/srv/swarm/` are locations on the run server.
