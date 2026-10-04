# Does the informative-check result survive removing free attacker-internal links?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-factory; source `577cc1de` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — claude-sonnet-4-6, none internal links, pass=0.1, checks=12: No interpretable treatment contrast; qualification/transport stopped before complete paired outcomes. Basis: Transport or clean-screen failure prevents treatment inference. All failed and unstarted outcomes are retained.
- **sample_size_summary:** Observed: 0/48 complete paired synthetic roots; main 0/192 valid; all stages 0/204 valid, 4 failed, 200 unstarted. Qualification planned 12. Parent roots reused; no independent-real-world sample.
<!-- experiment-evidence:end -->

Status: **lead**, exploratory, not independently reviewed. No accepted hypothesis or multiplicity-adjusted inference.

## Question

Does the informative-check result survive removing free attacker-internal links?

## Method and results

Frozen one-file [spec](../../specs/split-sonnet-no-links-strong.json), parent simulator and prompt from [Dmarz's split study](../../../../dmarz/notes/sybil-split-opus/README.md). Model: `claude-sonnet-4-6`, temperature 0, local Anthropic pool, no paid fallback. Internal links: `none`; attacker pass probability 0.1; 12 checks.

Primary: (k=27 minus k=1 rare-skill wrong fraction under degree) minus the same under coverage. **unavailable**. Complete paired roots: 0/48, equally weighted graph-family means. All-assigned worst-case bounds: [-2.0, 2.0]. Bounds cover missing calls, not sampling uncertainty.

Calls: 4/204 attempted; 0 valid; 4 failed; 200 unstarted. Main: 0/192 valid. Qualification: 0/12 exact, gate not passed. No retries or outcome replacements. External paid spend $0; pool usage 0 input / 0 output tokens (not a claim of zero compute cost).

[Cell table](cells.csv), [summary](summary.json), [all outcomes](records.jsonl), [execution provenance](provenance.json).

## Interpretation and limits

This small synthetic robustness check extends the parent result without claiming a novel Sybil defense. Removing internal links addresses an explicit confound in the parent review.

The 48 synthetic roots are reused from the parent, not new independent evidence about real swarms. Four calls within a root are paired; skills and identities are not sample units. The five queue specs share roots and are not five independent replications. The 12 clean fixtures are a reduced capability screen, not the parent's 60-fixture qualification. This changes the model and request configuration together: Sonnet uses temperature 0 and an explicit JSON instruction instead of Opus effort-low schema-constrained output. All comparisons remain exploratory. A negative label means the prespecified directional/useful-size criterion was not met, not equivalence or absence of an effect. No published Sybil defense or in-the-wild claim is tested.
