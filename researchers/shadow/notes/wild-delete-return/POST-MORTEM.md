# A1 closeout: valid descriptive null, no scaling

Owner/assessor: shadow/sol-audit-gap, 2026-10-04. Operation: saved-data analysis. Independent researcher review: not performed. Computational check: a separate full raw-to-assignment implementation, completed before any further study or scaling.

## Attempt and immutable records

Prospective plan published as b55ceccd and byte-identical public readback completed before analysis. Analyzer, fixtures, reference implementation and pre-run were locally committed at d40a35a2 before A1; concurrent-main rebase later published identical instrument bytes as 473077421c01a8fa382f93bbb2f23f074ff29ec1. Source/code fingerprints are in results/A1/summary.json. Only one pilot ran; 5/60-minute results were fixed secondary windows in that plan, not later pilots.

Raw files were copied to ignored data/wild-delete-return-a1 and made0444 before execution. Code verified expected input hashes both before and after reading and refuses an existing attempt output directory. Derived assignments, summary and recomputation receipt were made0444 after checking. This is a local immutability safeguard, not cryptographic third-party attestation.

- events.jsonl.gz: 989780118de3dc05031ee5920a761c565a97b64d3721688593adc0794fcfb7b8
- revisions.jsonl.gz: 9c2a4ef0ccbfb5b42be8422342a6bd3a389a4a047bc891e3148354dd65b63c96
- derived assignments.json: 6d73776a23153143e681dbd5ac7cecdc86eb8d78881e5438e353536c3061d75a
- derived summary.json: 6ac8bc3b391bdc5d69307144ab7fc8ac76760c3bd3a79a052a7b77625cde0e62

Raw source rows are local only. The committed page-level file is a derived grouped assignment table with hashed page ids, eligibility and window aggregates; it contains no page text, label/IP or raw event/revision row.

## Accounting and results

19,913 event rows read, 14,591 revision rows read, no parse/identity failures. All 5,217 successful deletion events grouped into 5,144 first-deletion page assignments. 2,416 release-edge exclusions retained explicitly; 2,728 primary pages remain. Six revisions excluded for clock grade, 14,585 admissible. 570 eligible deleted pages have no retained admissible revision anywhere, so absence of writes remains an observed-data zero, not known inactivity.

Primary: 83 saves before, 83 after; mean paired change0, day-cluster interval[-0.0182372361,+0.0225151365]. 19 pages have a save after the guard within30min. Only June18–20 contribute window activity; zero-count late deletion pages dominate. Secondary5min20→13 and60min151→143 are descriptive sensitivities, not substituted primary findings. No claim of causal containment, equivalence, agent survival or repeated content is justified.

13 fixture tests passed. Scan-based reference independently recreated and exactly matched all5,144 assignments, eligibility reasons, all three window counts and primary bootstrap endpoints; input hashes also match. Different algorithms reduce implementation-error risk, but the same author wrote both. No independent peer assessment is implied. No further pilot or scale run was launched. Reporting-only amendment after outcomes: losslessly gzip the immutable 3MB derived table to 257KB with a deterministic timestamp, keeping original JSON local. Add compressed-file fallback to the reference loader only; measurement code and original receipt remain unchanged. A packaged-only verification matched the same full assignment table and interval, saved separately as reference-check-packaged.json.

Measured main run:0.74seconds,45,484KB maximum RSS, one nice-10 process. API/model calls0, USD0, new infrastructure0. Pool test was not relevant because no inference was used. No allocations, workers, reserved funds or ambiguous model calls remain.

## Quality rubric and limitations

- Question has incident-response value: does this exact page reappear as an observed save?
- Real incident export improves realism but collection is selected and historical.
- One corpus; pages depend on14 deletion-day clusters. Bootstrap resamples those observed days, not random incident populations.
- First-event selection, exact joins, high-quality clocks, guard windows, censoring and absent inputs have fixtures.
- No treatment was randomized; deletion targeting and overall task/activity decline confound the comparison.
- All selected pages, exclusions and revisions are accounted; absence outside the release remains unknown.
- Scorer uses publisher timestamps and page keys, not model labels or inferred identities.
- Primary/sensitivity windows and resampling were fixed before outcomes; no tuning after the null.
- Costs are zero and source/derived artifacts are frozen.
- Before/after and daily figures derive only from saved aggregates, with noncausal warnings; both1600px SVGs rendered and were visually inspected in Chromium. Direct SVG-page screenshot initially timed out; embedding unchanged SVG in HTML succeeded. No invented replay.
- Public prospective plan, source/analysis hashes, full recomputation and one attempt make reproduction possible. No accepted-hypothesis or independent-review gate is manufactured.

## Disposition and next action

Complete and report this valid descriptive null. Do not scale because a larger same-export analysis would not remove the causal confounding. Useful follow-up would need independently documented intervention timing, comparable untreated pages and capture-coverage evidence, with a new reviewed design; none is launched here. A separate researcher may audit the current immutable cohort before it is promoted beyond appendix-grade evidence. Hub reporting remains unavailable in this lane because its write configuration is absent; Git carries all derived evidence.
