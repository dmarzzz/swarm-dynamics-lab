# Does Sonnet reproduce the informative-check identity-splitting contrast?

Status: **lead**, exploratory, not independently reviewed. No accepted hypothesis or multiplicity-adjusted inference.

## Question

Does Sonnet reproduce the informative-check identity-splitting contrast?

## Method and results

Frozen one-file [spec](../../specs/split-sonnet-linked-strong-or.json), parent simulator and prompt from [Dmarz's split study](../../../../dmarz/notes/sybil-split-opus/README.md). Model: `anthropic/claude-sonnet-4.6`, temperature 0, OpenRouter, Anthropic-only provider, reasoning disabled; separately preregistered paid attempt. Internal links: `ring2`; attacker pass probability 0.1; 12 checks.

Primary: (k=27 minus k=1 rare-skill wrong fraction under degree) minus the same under coverage. **unavailable**. Complete paired roots: 0/48, equally weighted graph-family means. All-assigned worst-case bounds: [-2.0, 2.0]. Bounds cover missing calls, not sampling uncertainty.

Calls: 4/204 attempted; 0 valid; 4 failed; 200 unstarted. Main: 0/192 valid. Qualification: 0/12 exact, gate not passed. No retries or outcome replacements. External paid spend/accounted reservations $0.055194 (0 unknown-cost calls conservatively reserved); pool usage 12768 input / 1126 output tokens (not a claim of zero compute cost).

[Cell table](cells.csv), [summary](summary.json), [all outcomes](records.jsonl), [execution provenance](provenance.json).

## Interpretation and limits

A directional replication strengthens only the scoped synthetic mechanism; reversal or nonreplication is reported equally. No universal superiority of coverage is implied.

The 48 synthetic roots are reused from the parent, not new independent evidence about real swarms. Four calls within a root are paired; skills and identities are not sample units. The five queue specs share roots and are not five independent replications. The 12 clean fixtures are a reduced capability screen, not the parent's 60-fixture qualification. This changes the model and request configuration together: Sonnet uses temperature 0 and an explicit JSON instruction instead of Opus effort-low schema-constrained output. All comparisons remain exploratory. A negative label means the prespecified directional/useful-size criterion was not met, not equivalence or absence of an effect. No published Sybil defense or in-the-wild claim is tested.

## Attempt lineage

The original pool attempt returned four HTTP429 errors at qualification and made no comparison calls. It remains in its own result directory. This dated, separately preregistered OpenRouter attempt uses a different route and repeats the entire fixed screen. No parent attempt outcomes are selected into this cohort. See [paid-route amendment](../../AMENDMENT-PAID.md).
