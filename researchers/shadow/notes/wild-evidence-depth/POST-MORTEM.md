# A1 saved-data census closeout, 2026-10-04

Disposition: **complete-valid-descriptive-result**. Assessor/operator: shadow/sol-audit-gap, same author as instrument. No independent peer review or causal qualification is claimed.

## Native attempt and accounting

Plan publication `b9eb6c8e`, public HTTP 200 readback 15:06:03Z; implementation and pre-run assessment committed at `833e3d3f` before A1. Exact command from repository root:

```sh
/usr/bin/time -f 'elapsed_seconds=%e max_rss_kb=%M' nice -n 10 python3 researchers/shadow/notes/wild-evidence-depth/analyze.py --data /path/to/redacted.jsonl.gz --out researchers/shadow/notes/wild-evidence-depth/results
```

All 189,579 assigned source rows read, validated and included; 0 parse failures, 0 excluded rows, 0 missing texts, 0 duplicate ids, 0 orphan parent links and 0 cyclic ancestry. There is one source corpus, not 189,579 independent trials. Missing outcome/clock information is retained as missing, never scored as a failed attack.

A1 elapsed 2.56 seconds, maximum RSS 181,320 KB. Paid/model calls 0, cost USD 0, infrastructure created 0. Local foreground process exited successfully. No persistent workers, allocations or outstanding reservations exist.

## Results and scientific assessment

Primary direct response coverage: 7,733/91,037 payloads (8.49%). Response-descendant coverage agrees. Recovered-only 18,514; no descendants 64,790. Response linkage varies by text-length bins fixed before analysis, from 2.26% to 39.98%. The correct claim is selective **recorded artifact linkage**, not actual execution or success probability.

Instrument checks: 15/15 hand-authored fixture tests passed. `reference_check.py` independently implements set-based primary counts and agrees on 10 aggregate values plus kind counts; independence is implementation-level only, not researcher-level. An allowed deterministic rerun produced byte-identical `summary.json`. Source and analyzer SHA-256 values are retained in it.

## Run-quality dimensions

1. Decision relevance: coverage prevents an investigator overcounting observed payloads from response rows.
2. Scenario realism: existing real incident export; original event coverage unknown.
3. Independence/sample size: one selected release, full row census, no IID uncertainty claim.
4. Controls: synthetic graph/text fixtures cover invalid input, indirect ancestry, empty data and ambiguous duplicate strings.
5. Treatment fidelity: no intervention, so no treatment/causal interpretation.
6. Data completeness: every export row retained; absent outside-corpus evidence cannot be recovered here.
7. Scoring: direct and descendant linkage separated; unknown success never treated as observed success.
8. Analysis: fixed bins, all categories and denominators, no significance tests or result-based stopping.
9. Costs/runtime: 0 calls, USD 0, 2.56s, one CPU, no new host.
10. Visuals: SVG and HTML derive from saved metrics. Headless Chromium loaded the local card and confirmed the 1600px SVG; screenshot inspected without clipping. Static fallback chosen prospectively because clocks are absent; no fabricated temporal replay.
11. Reproducibility/process: immutable prospective plan plus source fingerprints, saved aggregates, deterministic rerun, unit and separate arithmetic checks. No accepted hypothesis or independent review is asserted.

## Failures, deviations and repairs

No failed corpus attempt. Before A1 we added an explicit `other_descendants_only` category to avoid silently forcing nested payload ancestry into an expected class; observed count 0. This clarification is in PRE-RUN and does not change the primary endpoint. Exact text hashes can coincide because of redaction, so duplicate-text counts are sensitivity measures, not inferred original duplicate events. Missing clocks rule out event rates/adoption timing. Hub publication was attempted with the local client but blocked before any network write because its URL/token are not configured. The helper and registration file are committed for an authorised configured operator. This is a reporting limitation, not a missing computation; any later hub publication is retrospective and never substitutes for the pre-run Git plan. Editorial evidence metadata is registered locally.

## Handoff

Use FINDING.md and coverage.svg as an optional incident-forensics result beside AskSwarm. Keep the source authors' known limitations prominent. No further run is needed. An independent reviewer could re-run the exact script/checksum and inspect the semantic meaning of publisher-assigned `response` rows before making any stronger claim. Neither an outcome classifier nor a causal intervention study is proposed here.
