# Evidence depth: prospective saved-data analysis plan v1

Owner: shadow/sol-audit-gap. Written 2026-10-04 before computing corpus aggregates. Status: descriptive forensic analysis of an existing public export, not a formal hypothesis, new agent experiment or success-rate estimator. Zero new model calls. Source schema and published limitations were known from the owner brief and source report.

## TLDR

Build a reusable parent-graph evidence-coverage card for SwarmTraces. Count how many payload artifacts have a linked response, only another recovered artifact, or no linked child; compare raw rows, distinct redacted texts, and parent components. A response-kind row is evidence of a recorded response artifact, not evidence an attack succeeded. No payload code is executed, decoded or sent to a model; the corpus is untrusted input.

## Question and prediction

How much of the released artifact corpus supports payload-to-response inspection, and how misleading is its raw record count as a count of separate events? No directional prediction is registered. Report the whole export even if coverage is high or duplication low. This adds exact provenance denominators to the source authors' existing statement that outcomes are mostly unknown. It is not a discovery that the dataset is incomplete.

## Setup

Input: `--data` path to public `redacted.jsonl.gz` from https://swarmtraces.org/data/final/redacted.jsonl.gz. Read only top-level `id`, `kind`, `parent_id`, `time_utc`, `text`. Fingerprint compressed input and analyzer source. Retain no raw dataset rows in git. All text comparisons use SHA-256 of exact released text; redaction may create collisions of meaning, so identical released strings are not asserted to be identical original events. Missing/empty texts are reported separately, not all collapsed into one event.

One source corpus, not 189,579 independent experiments. The selected export is not a random sample. Population coverage outside the release is unknown. Full-export counts get no IID confidence interval; even a precise row bootstrap would not estimate selection uncertainty. Bound actual execution/success as unidentifiable rather than fitting it from artifact type.

## Protocol

1. Validate unique nonempty ids, allowed kinds and parent references. Fail on duplicate ids/unknown kinds/cycles. Report orphan parent references and self-links explicitly rather than dropping records. Missing timestamps remain missing; never infer a clock from row order or embedded text.
2. Compute a directed child-to-parent graph. For each payload, tabulate direct response children, any response descendants, recovered-text-only descendants and no descendants. A linked response under another payload is counted for ancestry reachability but not asserted to be a direct response to all ancestors; direct and descendant counts are separate.
3. Count kind-to-kind edges, orphan links, roots, weak components, size distribution and timestamp coverage. Components are provenance groups, not necessarily independent events or agents.
4. Count exact nonempty redacted-text duplicates within and across kinds, repeat multiplicities and cross-kind hash intersections. This is artifact duplication sensitivity, not a semantic copying model and not a replacement for AskSwarm clustering.
5. Stratify response attachment by fixed payload text-length bins: 0, 1–255, 256–1023, 1024–4095, 4096+ characters. These are descriptive selection diagnostics, not causal predictors. Do not label a contrast statistically significant.
6. Produce aggregate JSON/CSV, a static SVG/HTML card and FINDING.md. Static visuals are appropriate because top-level clocks are absent; no temporal replay is manufactured.

## Metrics

Primary: payload ids with at least one direct response child / all payload ids. Secondary: payload ids with response descendants; exclusive any-response / recovered-only / no-descendant categories; response rows with payload parent / all response rows; exact distinct released text / nonempty rows; provenance components and multiplicity concentration. Every percentage includes numerator and denominator.

Controls: tiny hand-authored fixtures for direct versus indirect responses, same-text unrelated roots, cross-kind equality, empty text, unknown parents, cycles, duplicate ids, self-links, null times, deterministic output and HTML escaping. Independently recompute primary direct response coverage using a separate set-based reference. No holdout or power calculation applies to a fixed-export census.

Stop: at most one full corpus pass per material analyzer version plus deterministic rerun/reference checks; repair only instrument defects, recording them. One local CPU process, nice 10, <1GB memory target and <100MB outputs; no fleet provisioning, paid requests, target traffic or persistent jobs. Hard output deadline 22:00Z.

## Closest work and novelty limit

- https://swarmtraces.org/ already reports incomplete reconstruction, unknown outcomes, duplicated payloads and missing timestamps. Our contribution is the parent-aware reproducible coverage instrument and exact release-level denominators, not rediscovery of the incident.
- arXiv 2609.09150 concerns copying on the wiki. We do not fit copying, identity turnover or adoption, leaving those to other lanes.
- The team's Sybil/lineage results motivate distinguishing artifact multiplicity from evidence multiplicity, but this analysis does not establish a causal link between incident duplication and any model's reasoning.
- Existing surveys' gaps are not claimed resolved: no content-only independence detector is built, and components do not identify ultimate independent sources.
