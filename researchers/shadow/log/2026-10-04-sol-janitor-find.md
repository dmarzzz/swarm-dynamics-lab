# Janitor finder

Inspected shared scripts/lab/CI, Shadow adapters/factory, alternate collectors, and the explicitly scoped local orchestration. Published five initial actionable defects early (`83273081`), then expanded FINDINGS.jsonl to 40 stable IDs with evidence, proposed small fixes, severity and effort estimates. No paid calls, external messages, or changes to teammates' data/preregistrations/ledgers/READY files.

Two saved offline synthetic probe suites demonstrate wrong-model acceptance, retry undercount, negative ledger costs, incorrect batch instructions, fail-open checker crash, duplicate-candidate crash, model-mismatched resume, missing-arm resume, and lost resumed spend. Ruff/Pyflakes/ShellCheck and redacted credential-pattern scans ran locally. No matching credential values or actual leak reproduced. False-positive Ruff corpus diagnostic was not promoted.

Fixer should prioritize concurrent spend reservations, model receipts, fail-closed verification and resume provenance. Coordinate capture-memory-mix fixes with sol-cm2 to avoid runtime pin drift. Local orchestration fixes need reviewable repo patches plus a separate live-application step. Finder does not merge fixes or spend money.

## Artifact registration follow-up

Added high-severity J041 at the orchestrator's request. Traced cmd_add -> refresh_lock -> fill_lock/ingredient_facts -> write_statements. A temporary synthetic full-add probe independently changes two unrelated lock entries, drops one missing artifact entry, rewrites two old statements, loses a private input digest and rebinds an old build to edited input bytes. No real registries/provenance were touched. Proposal scopes add to the new id@version, retaining old entries and statement/bundle bytes. Fixer must use janitor/J041 PR, explicitly name dmarz (@dmarzzz), and obtain independent Fable/Astra approval. Lane rollback reports are cited and distinguished from our synthetic counts.
