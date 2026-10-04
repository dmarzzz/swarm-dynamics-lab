# J041: filing one artifact mutates unrelated historical provenance

Severity: **high**. Finder: `shadow/sol-janitor-find`. This is a confirmed code-path defect, not a claim that the rolled-back local mutations reached main.

Shared tool owner: **dmarz (@dmarzzz)**. Commit `48160f9f` introduced the Flight Deck tooling; `50224c83` is his subsequent check change. The implementation belongs in fixer branch **`janitor/J041`**, with a PR to main that explicitly names/credits dmarz and requests his review. No direct shared-code push; independent Fable and Astra approvals remain mandatory. This document and synthetic evidence are the finder handoff, not an implementation or merge approval.

## Observed publication blockers

- `sol-identity` documents rollback in [README](../wild-identity/README.md) and [log](../../../../lab/researchers/shadow/log/2026-10-04-sol-identity.md), published in `a21ab708` (15:22:56Z). Its worktree lacked private inputs and existing videos; filing changed other researchers' provenance. All unrelated writes were restored.
- `sol-askswarm` [log](../../../../lab/researchers/shadow/log/2026-10-04-sol-askswarm.md), present at `a72ec009` (15:26Z), reports **40+ unrelated attestations** and **approximately 5,600 lockfile lines** rewritten by `fd.py add`. All those changes were restored. These counts are lane-reported, not independently measured from retained rollback diffs.
- Worktree/project-name and media checks are separate blockers. Moving to the canonical checkout is not a scoped-code fix and does not protect historical ingredient digests from subsequent edits.

## Exact code path

1. [`.flightdeck/fd.py`](../../../../.flightdeck/fd.py), `cmd_add` at lines 866-936, appends the new version and serializes `artifacts.yaml` at line 933. At **934**, it calls `refresh_lock(folder, data)` with the **whole manifest**, not the new `(id, version)`.
2. `refresh_lock` at **815-820** calls `ac.fill_lock` on all artifacts, writes the full lock, then calls `write_statements` on all versions.
3. [`.flightdeck/artifacts_check.py`](../../../../.flightdeck/artifacts_check.py), `fill_lock` at **351-395**, initializes `entries = {}` and visits every artifact/version. Missing local artifact files cause an early return at 360-366, so existing lock facts are **dropped**, not preserved. Existing visible files also acquire refreshed filesystem facts after clone/checkout mtime changes.
4. Historical versions always refresh `ingredients` at **378**, even when their artifact bytes did not change. `ingredient_facts` at **320-339** initializes each dependency digest to `null`; unavailable private ingredients do not retain their previously recorded hash. Present but changed ingredients are hashed from **current** bytes, not the original build's bytes.
5. `write_statements` in `fd.py` at **395-413** regenerates every locked version using those changed dependency facts. Its deterministic-text/no-rewrite shortcut does not help: the inputs were changed by bulk refresh. In particular `build_statement` omits a resolved dependency's digest when the new lock ingredient hash is null.

This is more than formatting churn: ordinary publication can erase hashes, rebind old builds to current inputs, drop old lock entries, and change signed statement bytes without refreshing their existing bundles.

## Independent offline reproduction

Run:

```sh
python3 5-experiments/studies/shadow/janitor-2026-10-04/probes/artifact_scope_probes.py
```

The actual `fd.main(['add', ...])` runs only in a temporary synthetic project. No real artifact/manifest/lock/attestation is changed; no API calls, keys or signing involved. Git/session lookups are mocked. [Saved output](probes/artifact-scope-results.json):

- New `new-figure@1` is present.
- **Two unrelated lock entries changed**: `private-input@1`, `changed-input@1`.
- **One unrelated entry dropped**: `absent-artifact@1`.
- **Two unrelated statements rewritten**.
- Previously recorded private ingredient SHA-256 becomes **null**.
- Historical visible ingredient SHA-256 changes to the digest of current input bytes.

## Minimal scoped fix proposal

1. Add an optional selected-version-key argument to `fill_lock`, `refresh_lock`, and `write_statements`. For `cmd_add`, pass **exactly `{f'{a.id}@{n}'}`**, not all versions of that artifact. Adding v2 must not refresh v1.
2. In selected mode, deep-copy the existing lock and its entries, preserve unknown metadata and every preexisting entry, and compute facts **only** for the new key. Missing unrelated artifact files or ingredients are irrelevant to add. If an existing lock is malformed, fail clearly rather than silently replacing it with an empty lock. Fresh projects may start a new lock.
3. Emit only the new version's statement. It may read the previous locked version to obtain the `supersedes` dependency; it must not recalculate that version's facts or overwrite its statement/bundle.
4. In the manifest, change only the target artifact/version data. Avoid unrelated YAML reformatting when feasible; at minimum compare and preserve all non-target parsed entries. Do not solve this by editing existing committed registries manually or running bulk fill on main.
5. Keep full-repository `fd fill` an explicitly invoked maintenance operation, not a hidden side effect of add. Historical provenance repair policy is separate from this small PR.

## Acceptance tests for the fixer PR

Snapshot old lock entries with deep equality and attestation/signed-bundle bytes with byte equality. Add both a new artifact and v2 of an existing one, with fixtures covering:

- An unrelated missing video whose lock entry must survive.
- An unavailable/private ingredient with a saved digest.
- An unrelated edited ingredient that must not be rehashed into old build provenance.
- An unchanged artifact with a changed checkout mtime.
- Existing v1 of the same artifact and its supersedes digest.
- Existing statement/bundle files and unknown lock metadata.

Assert only the new key and new statement are added, target manifest entry is updated, old entries/statements/bundles remain unchanged, and new facts are correctly digested. The saved probe intentionally describes the old behavior; after fixing, its mutation lists should all be empty and the private digest retained. Scope the PR to shared tooling plus fixture tests. Do not include teammate data, ledgers, READY files, or bulk regenerated provenance.
