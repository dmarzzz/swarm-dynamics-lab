# Trace receipts across experiment runs

An execution may finish with unusable or incomplete evidence. The shared operations closeout now checks `trace-manifest.json` in every saved result directory. Missing manifests are **unavailable**, not implicitly complete. Corrupted or incomplete receipts produce an explicit data-integrity gap, without changing the native outcome, scientific review or spending ledger.

This is a common offline audit and retention API. It is not an installed fleet collector. Existing native launchers need their own adapter; frozen attempts must not be rewritten. Antsy's retrospective D1 bridge is the first saved-data example. Its [receipt comparison adapter](../../studies/vishesh/antsy-targeted-v8/comparison-v3/src/receipts.py) now implements prospective start/terminal capture with worker-context verification and fault-tested interruption accounting; native qualification remains unrun. No rollout to every native worker is claimed.

## What a native adapter retains

Before dispatch, freeze the complete assignment list with opaque assignment, unit and arm labels. Reserve the original budget and durably journal the unique physical call before dispatch. Retain effective experimental input/context after construction, visible response before parsing, parsed decision, environment transition, grade, usage and execution phases/streams. Native journals must retain unknown completion and failures. Never silently retry; assign a new planned opportunity and physical ID according to the approved retry contract.

Use `experiment_ops.trace_receipts.retain(private_directory, selected_bytes)` for content-addressed, fsynced, mode-0600 files. It refuses different existing bytes and symlink paths; use a canonical directory path. This primitive does not sanitize content: pass only deliberately selected experimental material, never authorization headers, credentials, provider transport envelopes or operator transcripts. Keep raw experimental data private where required. For subprocesses, capture streams directly to private files so timeout/kill does not lose buffered evidence; Antsy execution-repair-v1 demonstrates that supervisor pattern. No request receipt proves remote delivery, and no visible output reveals hidden reasoning.

After termination, atomically publish the manifest from the authoritative journal. Manifest schema v1:

- Top-level exact keys: `schema_version: 1`, `study`, `attempt`, `source_sha256`, `config_sha256`, `assignments`, `calls`.
- `source_sha256` and `config_sha256` bind the adapter's documented source/configuration reference bytes. The audit validates digest grammar; operators still verify actual source/runtime admission. Document what was hashed.
- Each assignment has exact keys `id`, `unit`, `arm`. Labels must be opaque tokens matching `[A-Za-z0-9][A-Za-z0-9_.-]{0,95}`. Unit labels are not proof of statistical independence.
- Every assignment has exactly one call row: `assignment`, `call_id`, `status`, `artifacts`. Status is `unstarted`, `started` (unresolved), `valid`, `failed` or `interrupted`. Unstarted rows have null call ID and empty artifacts; other physical IDs are unique. Case-only native/CLI attempt aliases are supported.
- For every started call, `artifacts` includes all ten categories: `input`, `context`, `response`, `parsed`, `transition`, `grade`, `usage`, `phases`, `stdout`, `stderr`.
- Each category has either `{path, sha256, bytes}` relative to the result directory or `{absent: reason}`. Reason is `not_collected`, `legacy_missing`, `not_reached` or `not_applicable`. Explain exclusions in the authored review. Input cannot be not-applicable/not-reached for a started call; response cannot be either for a valid call.

Paths may not escape the result directory or traverse symlinks. Public audit output includes only aggregate counts, fixed categories and manifest hash; it never echoes paths, arbitrary IDs, raw answers or exception strings. A manifest itself can contain private paths and stays private. Hash verification is against declared local bytes, not proof that the original logger faithfully captured everything. Scope exclusions require human review.

## Offline audit and closeout

```sh
PYTHONPATH=scripts python3 -m experiment_ops.trace_receipts RESULTS \
  --study STUDY --attempt ATTEMPT
python3 scripts/experiment.py finalize STUDY --attempt ATTEMPT \
  --results RESULTS --outcome completed
```

Audit exits zero only for verified declared coverage; a valid adverse experiment may still have complete coverage. `finalize` records missing or invalid coverage without hiding failed attempts behind a new launch gate. Its scientific review remains unresolved until the owning session completes it. Do not equate the hub's done/progress display with started or valid counts.

## Adoption boundary

Use this contract for new or materially revised Vishesh-owned native launchers and the standard post-mortem process. Other researchers may adopt it without changing their policies. Add adapters during their owning iteration; do not hot-patch running workers, invent historical traces, or rerun experiments to populate missing files. Retrospective bridges must say so, preserve originals and leave absent categories explicit. This change grants no launch, allocation, spending or deployment authority.

Test the adapter on success, transport error, parser rejection, timeout, interruption, missing usage, partial artifact write and early-stop/unstarted cases. Run the common fault suite (`test_trace_receipts.py`) and adapter-specific tests before use. The shared auditor reconciles the declared cohort, not an independent expected roster; compare it to the frozen assignment hash during admission/review.
