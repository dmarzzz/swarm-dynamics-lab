# B1 runtime and admission contract

The scientific packet remains canonically `1fb19aa7c8cdcad23dd1acf724acf9febbdf6c7be3e4e075eae78bc79e9799ef`, as reviewed at9f971305. Its file-byte digest is distinct. New runtime files are separately hashed in runtime-manifest.json; no reviewed dossier, prompt, assignment, gate or analysis function is changed by this adapter.

`worker.py` defaults to preflight only and consumes private operator funding/admission/observation receipts. Actual dispatch requires `--execute`, a current funded named-scope receipt, matching clean source and runtime manifest, original ledger identity, current exclusive approved-account allocation, verified route/rates and public registration. Existing-host hourly price, invoice-preview tax treatment and bounded allocation lifetime must fit the hosting allowance. Known historical hosting is recorded separately from unresolved legacy exposure; older canonical portfolio reservations must remain unchanged. A partial historical subtotal is never labeled complete actual cost.

The original study ledger receives an append-only authorization/amendment record for itsUSD50 cumulative ceiling. This is notUSD50 of new spend: the new B1 earmark is at mostUSD11.01. The B1 model-reservation ceiling isUSD18.467936 including the originalUSD7.961696. Dispatch adds at mostUSD0.004864 per request before transport in the same SQLite transaction as its durable attempt row. Ambiguous attempts retain their reservation. Failures never automatically retry or clear the journal. Existing attempts/directives are preserved.

D0 starts at530 historical requests, ends at most770. E0 can start only from complete, usage-reconciled D0 native records tied to the same original ledger and packet, with neutral-only qualification recomputed. E0 ends at most2690 historical requests. The E0 approval is conditional and already named; it is not an automatic retry or a new allowance. Each stage still refreshes admission and public registration before model dispatch.

The local relay holds the credential through the previously authorized local consumer; the experimental host receives no persistent key. Its independent protocol mirror accepts only the exact next wire. On malformed output it preserves and returns the response for usage accounting, stops further relay use, and does not salvage/retry. Raw request bodies contain synthetic experimental data, never authorization headers or operator context.

Per-attempt records preserve raw wires/responses, validated outputs, original-ledger debits, known usage even when a response is wrong, partial/unstarted assignments and an operational post-mortem. The owning session must complete the scientific assessment and standard offline finalize after collection; the scaffold is not a scientific review. A failed run stops further dispatch, retains evidence and releases resources after collection. Frozen scientific design changes require the applicable new PI decision.

Run offline runtime tests with:

```sh
python3 -m unittest discover -s 5-experiments/studies/vishesh/influence-swarms/scenario/b1 -p 'test_runtime.py'
```

No working credentials, private billing/account identifiers, real funding receipts or machine-specific admission files are shipped in the repository.
