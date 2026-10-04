# Validation receipt

## What ran

- `test_trace_loop.py`: six unittest methods passed. Cases cover typed statuses, wrapper errors, missing/running statuses, no content or untrusted identifiers in exports, malformed/incomplete records, usage nulls, manifest scope, duplicate source rejection and secret detection.
- `demo.py`: reproduced all four per-lane outcomes and the saved totals from public status histograms.
- JSON Schema validation: all ten records in `results/episodes.json` passed `episode.schema.json` using the locally installed `jsonschema` validator. The collector, demo and unit tests use only Python stdlib.
- Histogram reconciliation: every lane's bin count equals its projected tool-result count; nonzero bins equal its projected nonzero-status count.
- Source integrity: `results/replay-result.json`'s `code_sha256` matches the complete bytes of `trace_loop.py`.
- Secret/privacy scan: all release source, documentation and derived JSON files scanned for credential prefixes, key/token/secret assignments, private-key headers, AWS-style access IDs, JWT-shaped strings, prohibited private-context identifiers, local private paths and em dashes. No matches after replacing a synthetic test sentinel's misleading variable name. Relative Markdown links were checked.

The suggested existing `leakscan.py` was inspected but not run: it is a Discord-channel crawler, not a filesystem scanner, and was not appropriate for this export. The local release audit used filesystem regex checks plus the stricter allowlisted output projection. Regex checks do not prove semantic anonymization. No free-text source fields were exported.

## R0 result

- Four replay lanes, all retained.
- Explicit nonzero tool-result statuses: B0 recognized 0/40; B1 recognized 40/40.
- New flags among explicit zero statuses with no wrapper error: 0/702.
- Wrapper errors retained: 1/1.
- Parse integrity for all ten episode projections: parsed, with no malformed or incomplete lines. This does not prove complete session capture; seven compactions were observed.
- Model calls launched by the scripts: zero.
- Research-quality effect: not measured.
- Candidate brief behavior on a later model task: not measured.
- Scientific policy promotion: blocked, no independent evaluation.

The saved observations are tool-result events, not necessarily unique process executions. Negative-control failures and normal nonzero statuses are not labeled research mistakes. The four-lane replay tests a metadata parser contract on saved sessions, not research generalization or a causal treatment effect.

## Reproducibility boundary

The committed histograms and scripts reproduce the reported engineering endpoint without private data. Raw source snapshots, file-to-alias mappings and exact source hashes remain local to the operator. An authorized local reviewer can use those receipts to audit source provenance. A public reader cannot independently establish the raw transcript provenance from aggregate files alone; this limitation is intentional and must accompany the result.

No shared experiment code, provider services, live agent briefs or teammate traces were modified. All changed repository files are in this owned directory. No external approval, budget increase or credential change was performed.
