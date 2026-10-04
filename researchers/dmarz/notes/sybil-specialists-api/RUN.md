# Run and inspect this study

This folder was copied from templates/experiment-worker, then adapted to reuse the owned prior simulator. It remains an exploratory S0/Q0/S1 instrument. Never open the reserved holdout or promote it to formal S2 without the survey/hypothesis gates.

## Local checks

Install requirements.txt in a local environment, then run src/selftest.py and the parent sybil-specialists/src/selftest.py. They make no network calls. For a new offline rehearsal, commit a pre-run assessment and run `python3 src/worker.py --stage S0 --attempt NEW_ATTEMPT`; existing output directories are refused. Analyze the resulting folder with `python3 src/analyze.py results/NEW_ATTEMPT`.

## Fleet workflow

Use the private agentops launcher in PR47. Obtain and verify a fresh exclusive claim before any server work; the initial study uses dmarz-sybil-specialists-api on sim-dmarz-4. Every launcher operation fetches the merged claim state and refuses overlap/expiry. Setup requires a full public Git SHA and verifies 27 offline checks. Launch S0 first. Q0 requires successful S0 with the identical runtime digest; S1 requires successful Q0 with that digest. Pre-run and previous post-mortem review must also be complete before each launch.

The launcher obtains credentials from the existing encrypted private alias only for Q0/S1. Values travel through SSH stdin into the detached worker environment, never arguments, tracked files, logs or public reports. No model SDK or automatic retries. The finite worker takes exactly one hub assignment and rejects a second attempt. The launcher refuses an existing batch or worker and preserves outputs on failure.

The budget ledger is outside the checkout on the claimed host. It has one fixed identity for this whole study: do not delete it, reset it, change its cap, or copy it to create capacity on another host. Fsync before POST, nonrefundable conservative reservations, aggregate USD 5 and 300-call ceilings. Observed token usage is priced at the frozen documented rates; the displayed cost is computed from reported usage, not independently reconciled to an invoice. Any uncertain response retains its full reservation.

## Reconcile and finish

Status is read-only. Verify after the worker is terminal: it checks artifact hashes against the authenticated hub and recomputes every evaluation from saved assignments and answers. An in-progress verification can refuse because final artifacts do not yet exist; this is not permission to replay the batch. Inspect the public final image and actual animated playback. Retain the full 24/192 denominators, including unstarted and failed rows, for a failed paid attempt. Write a post-mortem before diagnosing or escalating. A legitimate adverse scientific result is complete evidence, not a reason to rerun.

S0 and S1 overview rare_accuracy is pooled across completed pilot cells, not the primary contrast. Q0 uses qualification_passed and its clean-task chart; the overview rare_accuracy placeholder is not an attack result. Per-cell estimates and primary paired contrasts are in analysis.json and the final report. Images are public synthetic outputs; raw records remain on the protected hub and dedicated checkout.

After durable upload and analysis verification, confirm no worker remains and release the fleet claim. Preserve outputs and the budget ledger for audit. A repair that changes runtime/prompt requires a recorded new batch identifier and fresh qualification worlds; do not edit old results or replay an old batch.
