# First-priority factory pilot: duplication invariance

**First attempt closed, unqualified.** Two requests, zero model answers: pool HTTP400, paid fallback HTTP403. The pool request included unsupported numeric schema bounds; this is a concrete builder defect, not evidence that the model fails the task. [Post-mortem](POSTMORTEM.md), [terminal report](results/FINDING.md), [2,026-check same-author recomputation](results/recomputation.json). Independent agent review and any prospective repair admission remain pending; no process is still dispatching.

This is the **only active new factory scope**, explicitly directed by Shadow. Legacy factory queues stay held. [One-file prospective specification](SPEC.md), [setup](SETUP.md), [pre-run assessment](PRE-RUN.md). This fresh runner does not disable the legacy hold or edit Quorum's runs.

Question: with fixed independent evidence, do 1/4/16 copies change raw synthesis, supplied-ancestry synthesis, or upstream deterministic dedup? A separate irrelevant-padding arm controls changed irrelevant text. Twelve paired synthetic numeric roots, six disjoint no-copy competence cases. Exact cl100k proxy-token matching, not a false claim of exact Anthropic token equality. Strong limits are in the spec.

## Reproduce the offline instrument

```sh
python3 -m venv /tmp/factory-provenance-venv
/tmp/factory-provenance-venv/bin/pip install -r researchers/shadow/factory/provenance/requirements.txt
/tmp/factory-provenance-venv/bin/python -m unittest discover -s researchers/shadow/factory/provenance -p test_pilot.py
/tmp/factory-provenance-venv/bin/python -O -m unittest discover -s researchers/shadow/factory/provenance -p test_pilot.py
```

Tests use fake responses and temporary files, never model requests. Eighteen tests. The separate `recompute.py` uses only the standard library and does not import the runner, generator or scorer.

## Operator commands

These are **not** permission to launch another pilot. The one prepared scope must be public and admitted. Set your existing authorized hub environment and `SWARM_REPORT_PATH`; keys are never passed in command arguments or stored in artifacts. Current operator's authorized local pool and paid-key locations are consumed internally by the fixed route adapter. It never changes provider limits.

```sh
# Only after source is committed and publicly available:
/tmp/factory-provenance-venv/bin/python researchers/shadow/factory/provenance/run.py prepare
# One persisted pool qualification request before the remaining gate/main.
# At most the specified initial-failure fallback, same existing paid ledger:
nice -n 10 /tmp/factory-provenance-venv/bin/python researchers/shadow/factory/provenance/run.py run
# Saved numeric data only:
/tmp/factory-provenance-venv/bin/python researchers/shadow/factory/provenance/analyze.py
python3 researchers/shadow/factory/provenance/recompute.py
```

All attempts and outcomes have unique files created atomically without overwrite. Interrupted attempts close out as unknown; they never resume decisions. `run.py closeout` is offline and enumerates missing outcomes. A duplicate `prepare` is rejected. Do not delete admission/outcome files to get another attempt or copy the paid ledger to reset allowance.

After the fixed pilot, complete the post-mortem and request an independent agent's recomputation. No new scope or scaling until that happens. Builder-authored checks are explicitly not independent researcher review. Completed independently checked contrasts/hour stays zero until an external checker confirms a completed contrast.
