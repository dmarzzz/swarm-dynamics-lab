# Janitor finder, 2026-10-04

Finder: `shadow/sol-janitor-find`. Findings are triage requests, not fixes or merge approval. First five reached main at `83273081`; the following batch extends the append-only queue. Baseline inspected: `952a618c`, then `83273081` after rebasing the initial queue. Findings include shared code, Shadow's adapters/factory, and explicitly authorized local orchestration scripts. No model calls, metered collector runs, credential transfers, or external messages were made.

Read [FINDINGS.jsonl](FINDINGS.jsonl) in severity order. IDs remain stable. The fixer owns `janitor/<id>` branches and requests independent Fable and Astra approval before squash merge. Teammates' data, execution ledgers, READY files and preregistrations remain read-only. Shared-code PR descriptions must credit the original researcher. Local orchestration paths are outside this repo: propose a reviewable copied wrapper/patch and clearly distinguish a merged patch from deployment to the live script.

## Initial priorities

1. J006-J009, J013, J016, J019, J027-J030: enforce spend admission and preserve unresolved liability.
2. J021-J022 and J026: stop false-green verification and push success.
3. J010: require requested/returned model receipts.
4. J003 and J018: make claims and batching safe under concurrency.
5. J032: add an immutable-evidence diff guard without editing historical evidence.

The capture-memory-mix correction lane is already active. Coordinate with that lane before proposing overlapping adapter changes; do not invalidate a running attempt by silently changing its pinned runtime. Every cap finding refers to code, not an assertion that actual overspending occurred.

## Offline evidence

`python3 researchers/shadow/notes/janitor-2026-10-04/probes/offline_probes.py` uses synthetic responses and patched transport only. It reads no keys and makes no network calls. Saved [results](probes/offline-results.json) establish:

- Wrong returned model is accepted by the old HTTP adapter.
- Two mocked retry dispatches count as one request against its call cap.
- A negative ledger adjustment is accepted.
- Talk instructions create blogs; web instructions target talks.
- A crashing `lab.py check` produces an empty `tree_errors` set.

Static tools were installed in an ephemeral `/tmp/swarm-janitor-tools` virtualenv, not the project environment. Pyflakes 4.0.2 on `scripts/` found only unused imports/variables and placeholder-free f-strings ([raw output](probes/pyflakes.txt)); these are not promoted to findings. Ruff 0.16.10 F821/F822/F823/E9 found no runtime issues in scripts/Shadow/dashboard. Its all-repo pass flagged a `match` variable after a semicolon in Vishesh's OCR corpus, but Python AST parsing accepts that file: this tool diagnostic is not a confirmed syntax finding. AST parsing and `bash -n` found no syntax failures in tracked repo Python/shell and the requested local orchestration scope. A redacted regex scan for OpenRouter/Anthropic/GitHub tokens and private-key headers found no matches in those files. This limited-pattern scan is not a secret-free certification.

No teammates' experiment outcomes were modified. `lab.py check` passed before the initial push (0 errors, 5 preexisting unresolved-link warnings).
