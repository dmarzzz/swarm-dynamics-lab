# Offline implementation and handoff

2026-10-04. Original source code; no embedded Village records, provider calls or native dispatch. [Prospective implementation plan](INTEGRATION-PLAN.md), [fit decisions](FIT.md), [setup](SETUP.md).

## What is implemented

- `src/inventory.py`: fixed-revision, fixed-table, bounded streaming read; 2,000 file-order rows/table, at most 32 MiB compressed and 128 MiB decoded/table. Projects allowlisted fields into a new private directory; excludes raw model output/hidden reasoning and event commands. Never prints content, credentials, signed redirect URLs or arbitrary exception text. Drops authorization on cross-host redirects. Aggregate counts and consumed-line-prefix hashes are not whole-file verification.
- `src/audit_inventory.py`: counts joins, duplicate IDs, timestamp-order inversions and update timestamps without printing text. Unloaded referenced records remain not loaded, never classified missing from the corpus.
- `src/normalize.py`: writes private draft records for chat, memory and session intentions; converts the schema's timezone-free UTC strings into explicit UTC. Source digest binds the retained projection, not an unavailable original whole row. Visibility is empty, redaction unknown and availability unreviewed. Normalization cannot admit an episode.
- `src/replay.py`: enforces explicit source revision, reviewed visibility/privacy references, row hashes, recipient and availability, cutoff/update boundaries and declared connected-component split separation. Requires study-specific evidence roles. Emits an actor field allowlist plus a separate receipt, with complete-record recent-history or BM25 selection. No model adapter exists.
- `score`: strict three-way categorical scoring from pre-adjudicated labels and sufficient visible citation sets; missing/invalid responses stay distinct. A valid citation ID alone cannot override a wrong label. It is not a semantic adjudicator, calibrated uncertainty metric or the full Theseus task-state scorer.

## Reproduce offline verification

From repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/ai-village-replay-2026-10-04/tests -v
```

Observed: **21 passing tests**, including the CLI and restrictive output permissions. Eighteen original scripted controls cover six semantic mechanisms (negation, quantity, time, scope, uncertainty and attribution), each with supported/refuted/unknown labels. They test packet and scorer plumbing, not model competence or corpus realism. Same-author labels are not independent adjudication. [Fixtures](tests/semantic-fixtures.json) contain no Village text.

An actual source-read failure exposed Unicode line-separator characters inside JSON strings. Python `str.splitlines()` incorrectly splits these valid records; the reader now iterates physical file lines, with a CLI regression test. The audit then completed for all 8,000 projected rows.

## Private source workflow

Use an existing authorized local credential via `--token-file`, never inline token text. Choose a new private directory outside public Git and pass it with `--private-dir`. The inventory intentionally refuses an existing destination, so a partial failed prefix is not silently overwritten. No credential-store paths belong in this shared document.

1. Run `src/inventory.py --token-file <private-credential-path> --private-dir <new-private-directory>`.
2. Run `src/audit_inventory.py <private-directory>`; only reviewed aggregate output may be published.
3. Run `src/normalize.py <private-directory> --out <new-private-jsonl>`.
4. Privately select complete candidate task windows, fetch missing joins through an authorized bounded source process, and annotate actual availability, `visible_to`, redaction/privacy and source-supported roles. The current normalizer covers only projected text tables; tool-turn/screenshot truth requires a separate reviewed extension. Do not infer truth from memories or session intentions.
5. Construct an episode manifest with all connected dependency keys across splits. The checker enforces declared edges; it cannot discover undeclared semantic dependencies. Hash final reviewed normalized rows into `allowed_records`. Set `availability_status` to `reviewed` only after evidence supports it; keep audit receipts. Ordinary human review is required to establish facts, not an independent-researcher approval gate.
6. Prepare privately using the command below. Full actor files contain licensed source text and must remain private. The CLI returns only status and hash; it has no hosted-transfer or launch function.

```sh
python3 researchers/vishesh/notes/ai-village-replay-2026-10-04/src/replay.py \
  --records <reviewed-private-jsonl> --episodes <private-episode-manifest-json> \
  --episode <episode-id> --study healing --method bm25 --max-chars 8000 \
  --out <new-private-output-directory>
```

Supported profile IDs: theseus, dissenter, quorum, healing, phantom, influence, immune. [profiles.json](profiles.json) specifies role names, required comparisons and scientific boundaries. Profile validation establishes that the annotated evidence records are available; it does not certify annotation truth. The fixtures demonstrate the exact schema and separate gold from actor fields.

## Important implementation limits

The character cap applies only to serialized selected records, not the common instruction/question or a provider's tokenization. It is an **offline selection parameter**, not a dollar or native context budget. Selection skips whole records that do not fit; inspect omitted long records and empty packets. Use a pinned tokenizer, full payload caps, output budgets and writer costs before native qualification. Do not describe character parity as matched token spend or equal information.

Timestamps at the cutoff are excluded. Same-availability ties are all quarantined, even where event indices might later resolve them. This deliberately conservative first implementation sacrifices coverage; it does not claim an exact reconstruction. Historical prompt inputs and complete private scaffolding are unavailable. Constructed-information mode must be reported separately from historical visibility.

Recent/BM25 decision selectors see the task query. The existing handoff plan requires P/S writers to receive generic handoff instructions without evaluation questions; no writer implementation exists yet. The current builder must not be reused as a memory-writer prompt. Source-only categorical examples also do not implement the full critical-fact/admissible-action Theseus endpoint.

Review IDs are attestations supplied by the annotator, not cryptographic proof that review occurred. `source_sha256` on drafts binds a retained projection and `allowed_records` binds all normalized fields. Source verification, actual evidence-based annotation, licensed-content handling and question contamination must still be checked by the owning session. Neither this module nor the profile files are production launch admission.

## Handoff and closeout

Offline preparation status: implementation validated, no native attempt. Source acquisition and structural evidence are reported separately from zero scientific outcomes. No experimental model calls, spending-ledger changes, machine claims or deployment occurred. Existing study SETUP files remain authoritative; each new AI-VILLAGE.md links this shared corpus record without duplicating them.

Next: identify and label coherent development components for Telephone and the handoff pilot; current prefixes alone cannot do this. Then freeze eligible counts, provider-transfer terms, actual tokenizer/model/request envelope and native evaluation contract. Present the concrete changed run scope only after those prerequisites are resolved. Maintain all previous negative/failed results and budgets. A source-access success or 21 green software tests is not permission or evidence to launch.
