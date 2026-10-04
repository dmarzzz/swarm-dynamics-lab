# Agent traces as authorized research orderflow

Start with [TRACE-SPEC.md](TRACE-SPEC.md), protocol `swarm-trace/0.2.0`.

**Default after research-cohort enrollment: public envelope, sealed content.** Searchers propose bounded work from allowed hints; a builder proposes ordering; the controller owns execution; independent reviewers own quality. No raw disclosure or payment is authorized by this proposal.

## Run the offline example

Requires Python 3.9+ and `jsonschema` 4.x. No provider credentials, raw transcripts, model calls or network access are used by these commands:

```sh
python3 researchers/shadow/notes/rsi/test_protocol.py
python3 researchers/shadow/notes/rsi/demo.py
```

The example validates three real, privacy-projected pool envelopes, then illustrates a synthetic metadata-contract improvement bundle. A candidate passes four of four developer-authored cases versus two of four for a naive baseline. A competing overclaim is rejected. The displayed $1 allocation is hypothetical, and actual settlement is zero.

## Files

- `trace.schema.json`: strict event/content-projection/bundle schema.
- `build_schema.py`: reproducible schema generator.
- `protocol.py`: canonical bytes, commitments, record integrity, validation, offline selection and conserving split arithmetic. No live signatures, escrow, worker dispatch or permissions service.
- `pool_to_spec.py`: local-only explicit-cohort adapter. Never exports raw text or reveal nonces. Original identities/lineage and scientific outcomes remain unknown where not captured.
- `examples/pool-events.jsonl`: three real derived envelopes; unsigned historical imports, not live orderflow.
- `examples/pool-content-public.jsonl`: fixed omission markers, no source text.
- `examples/worked-bundle.json`: bundle, competitor, test policy, synthetic evaluator fixture and result.
- `VALIDATION.md`: test and privacy/provenance verification receipt.

For the earlier real-session observability repair and proposed research-quality evaluation, see [rsi-loop](../rsi-loop/DESIGN.md). Its measured 0/40 to 40/40 status-capture repair and this synthetic bundle example are separate results.
