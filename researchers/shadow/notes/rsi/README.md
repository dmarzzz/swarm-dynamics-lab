# Agent traces as authorized research orderflow

Start with [DEMO.md](DEMO.md) for the real-record offline loop and two-minute script. The protocol is [TRACE-SPEC.md](TRACE-SPEC.md), version `swarm-trace/0.2.0`.

## Real-record loop (R1)

566 validated envelopes feed saved agent-authored reporting proposals. Over 327 historical episode records, the lineage-preserving bundle passes **195/195** accounting assertions versus a **75/195** selected-only baseline. A clamp-only shortcut also scores **75/195** and is rejected. The ledger conserves 1,000 non-transferable demo attribution units; actual payment is zero.

```sh
python3 researchers/shadow/notes/rsi/replay_loop.py --verify
python3 researchers/shadow/notes/rsi/test_replay_loop.py
```

Open [the self-contained HTML replay](r1-results/replay.html) locally. No credentials or new model calls are required. The searcher is the current coding agent; proposals are saved artifacts, not fresh inference during replay. This is same-author, post-hoc maintenance validation, not an independent research effect. See [post-mortem and limits](R1-POSTMORTEM.md).

**evidence_confidence:** 1 / exploratory for the historical reporting-contract demonstration; 0 / untested for agent research-performance improvement. Assessed by shadow/sol-rsi2, 2026-10-04.

**sample_size_summary:** One historical cohort, 327 physical records / 180 logical cell-task-seed-arm keys, 127 invalid records, 15 reporting groups and 195 assertions per policy. No independent research-effect sample; no fresh model execution.

**Default after research-cohort enrollment: public envelope, sealed content.** Searchers propose bounded work from allowed hints; a builder proposes ordering; the controller owns execution; independent reviewers own quality. No raw disclosure or payment is authorized by this proposal.

## Earlier synthetic protocol example

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
