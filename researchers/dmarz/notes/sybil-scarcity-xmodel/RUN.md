# Runbook: sybil-scarcity-xmodel, chain 001 per model

Nothing here has been run. This file is for the operator who takes a request from the private run queue. The server is a parameter. Public files contain no server address, hub address, token or credential.

Two models are pre-registered; each is its own complete chain on its own server: `qwen/qwen3.7-flash` (tag `qwen`, provider `openrouter`, runnable at this commit) and `gpt-6-sol` (tag `sol`, provider `openai`, refused by the code with `model_not_ready` until the later code commit that adds its adapter and its own pre-run review). Never run the two chains on the same server.

## Before launch

1. The run request is in the private run queue and dmarz/fleet-monitor has done its same-researcher check. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
2. Read [reviews/chain-001-pre.md](reviews/chain-001-pre.md): it names the code commit and the source hash. The launch commit is the first commit on `main` that contains that review and has that source hash. [READY.yaml](READY.yaml) carries the same hash, the selftest count, the caps and `model_ladder` with `providers`.
3. Take an exclusive server claim per model chain (for example `dmarz-sybil-scarcity-xmodel-qwen`).
4. The server needs the repository at the launch commit: this directory and the parent directory `researchers/dmarz/notes/sybil-scarcity-opus/` (its `design.yaml`, `src/`, `manifest.json` and `records/s1-episodes.jsonl.gz`, pinned by SHA-256; a changed or missing file stops S0 or blocks the stage). Python 3.12 with `requirements.txt`.

## Commands (Qwen)

```
python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> setup  --host <server> --model qwen/qwen3.7-flash
python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> chain  --host <server> --model qwen/qwen3.7-flash --confirm-paid
python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> status --host <server> --model qwen/qwen3.7-flash
python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> verify --host <server> --model qwen/qwen3.7-flash
```

The operator also passes `--source <its agent id>`. `setup` runs `python3 src/selftest.py` (about 30 s on a laptop) and compares the test count and the source hash with `READY.yaml`. `chain` runs `python src/chain.py run --stages S0,P0,Q0,S1` with `STUDY_MODEL=qwen/qwen3.7-flash`, `SWARM_OPENROUTER_API_KEY`, `STUDY_BUDGET_LEDGER`, `STUDY_RESULTS_DIR` and `SWARM_SOURCE`. The chain writes under `<STUDY_RESULTS_DIR>/qwen/`, uses the ledger `<ledger stem>-qwen<suffix>` and the hub experiment `sybil-scarcity-xmodel-qwen`; batches are `s0-001-qwen`, `p0-001-qwen`, `q0-001-qwen`, `s1-001-qwen`.

## What the chain does by itself

| Stage | Calls | Passes when | If it does not |
|---|---|---|---|
| S0 | 0 | 168 scripted rows valid; byte-identity with the parent (simulator file, packet texts and labels from the parent's code, manifest lines); clean gate passes under plurality; primary cell not constant | chain stops; nothing paid happened |
| P0 | 1 | response parses, model slug matches, provider named and Alibaba, usage reported, finish `stop`, no reasoning tokens, valid structure; tokens per byte and the raw response metadata are written to the summary, the hub metrics (`probe_*`) and the run message | chain stops after one call |
| Q0 | 48 | before queueing: P0's tokens per byte × 57,092 bytes ≤ 31,000 tokens; then the parent's gate: 48/48 valid, per carrier profile field accuracy ≥ 0.95 and exact ≥ 0.90, null on all 24 withheld facts | `input_ceiling_projection` or `gate_failed`; S1 is never queued; the stop is the result for this model |
| S1 | 1,440 | before queueing: the ceiling projection again and 1,440 × Q0's cost per call within the remaining USD 4; then at most 15 failed calls and no integrity failure | `input_ceiling_projection`, `projection_exceeds_cap`, `failed_units_over_limit`, or an integrity reason |

Every stage's pre-dispatch check also proves byte-identity of that stage's inputs with the parent's manifest (S1: about 2.5 minutes of preparation before the first call).

Exit code 0: all requested stages done. Exit code 3: stopped at a failed stage or gate (`chain-status.json`: `state: stopped_at_gate`, stage, reason). Other non-zero: internal error.

Billing outage: HTTP 402, or a 400/403/429 naming credit, balance, billing or a spend limit, pauses the stage; the same call is re-sent every 60 s for up to 20 minutes; then the stage stops with `provider_credit_balance_low`, nothing counted as failed. After credit is restored: `python src/chain.py resume` (same `STUDY_MODEL`; the launcher's `resume` action), batch `s1-001-qwen-r1`, inside the unchanged cap of 1,440. Record the resume as a dated amendment here.

Limits (hashed): 2 requests in flight; 180 s per request; 14,400 s per stage; 18,000 s per chain; 1,489 calls; 1,700 transport attempts; USD 4 for Qwen. Expected for Qwen: about USD 1.1 and, at 3 to 8 s per call, 36 to 96 minutes for S1.

## After a chain

1. `status`, `verify`, and on the server `python src/chain.py summarize` (S1 headline incl. the parent's primary recomputed from its pinned rows: −95.8 pp). Keep the outputs.
2. Do not rerun a stage. A batch name is refused the second time.
3. Post-mortem per [RUN-REVIEW.md](../../../../tooling/agent-experiments/RUN-REVIEW.md); README results and the evidence row from the saved analysis, per model, never pooled.
4. Confirm the chain process has exited and uploads are verified, then release the claim.

## Offline checks (no server, no model call)

```
python3 src/selftest.py
python3 src/worker.py --stage S0 --attempt <fresh-name>
python3 src/manifest.py --check            # about 2.5 minutes: rebuilds all 1,657 assignments
python3 src/rehearse.py --hub-dir <directory with hub.py and swarm_report.py>
```
