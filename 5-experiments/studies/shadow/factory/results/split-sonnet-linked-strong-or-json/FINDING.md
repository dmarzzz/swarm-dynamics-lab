# Does Sonnet reproduce the informative-check identity-splitting contrast?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-factory; source `666aa2f4` ([registry](../../../../../evidence-metadata.json), [rubric](../../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — anthropic/claude-sonnet-4.6, ring2 internal links, pass=0.1, checks=12: paired splitting difference-in-differences +0.5000; exploratory same-family sensitivity, not a general defense claim. Basis: Source-reported exploratory comparison; 48 reused synthetic roots in two graph families, reduced clean qualification, no independent review, model/configuration change and five unadjusted dependent contrasts.
- **sample_size_summary:** Observed: 2/48 complete paired synthetic roots; main 88/192 valid; all stages 100/204 valid, 4 failed, 100 unstarted. Qualification planned 12. Parent roots reused; no independent-real-world sample.
<!-- experiment-evidence:end -->

Status: **lead**, exploratory, not independently reviewed. No accepted hypothesis or multiplicity-adjusted inference.

## Question

Does Sonnet reproduce the informative-check identity-splitting contrast?

## Method and results

Frozen one-file [spec](../../specs/split-sonnet-linked-strong-or-json.json), parent simulator and prompt from [Dmarz's split study](../../../../dmarz/sybil-split-opus/README.md). Model: `anthropic/claude-sonnet-4.6`, temperature 0, OpenRouter, Anthropic-only provider, reasoning disabled; separately preregistered paid attempt. Internal links: `ring2`; attacker pass probability 0.1; 12 checks.

Primary: (k=27 minus k=1 rare-skill wrong fraction under degree) minus the same under coverage. **+50.0 pp (descriptive 95% root-bootstrap CI +50.0 to +50.0)**. Complete paired roots: 2/48, equally weighted graph-family means. All-assigned worst-case bounds: [-0.9305555555555556, 1.2361111111111112]. Bounds cover missing calls, not sampling uncertainty.

Calls: 104/204 attempted; 100 valid; 4 failed; 100 unstarted. Main: 88/192 valid. Qualification: 12/12 exact, gate passed. No retries or outcome replacements. External paid spend/accounted reservations $1.201143 (4 unknown-cost calls conservatively reserved); pool usage 288128 input / 3101 output tokens (not a claim of zero compute cost).

[Cell table](cells.csv), [summary](summary.json), [all outcomes](records.jsonl), [execution provenance](provenance.json).

## Interpretation and limits

A directional replication strengthens only the scoped synthetic mechanism; reversal or nonreplication is reported equally. No universal superiority of coverage is implied.

The 48 synthetic roots are reused from the parent, not new independent evidence about real swarms. Four calls within a root are paired; skills and identities are not sample units. The five queue specs share roots and are not five independent replications. The 12 clean fixtures are a reduced capability screen, not the parent's 60-fixture qualification. This changes the model and request configuration together: Sonnet uses temperature 0 and temperature-0 schema-constrained output instead of Opus effort-low schema-constrained output. All comparisons remain exploratory. A negative label means the prespecified directional/useful-size criterion was not met, not equivalence or absence of an effect. No published Sybil defense or in-the-wild claim is tested.

## Attempt lineage

The original pool attempt returned four HTTP429 errors. The first OpenRouter attempt returned four schema-invalid prose/code-fenced answers. Both attempts stopped before main comparisons and remain saved separately. This repair prospectively adds strict JSON-schema output, uses fresh clean qualification roots, and reruns the entire fixed screen. No outcomes from prior attempts enter this cohort. See [structured-output amendment](../../AMENDMENT-STRUCTURED.md).
