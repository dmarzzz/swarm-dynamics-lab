# B2 semantic and decision scoring — frozen before native outputs

No native B2 response has been observed. This contract accompanies prepared/gold.json and applies to both arms and both fresh blocks without output-dependent changes.

## Decision endpoint and competence

The source rule determines GO or HOLD. Parse the declared response decision without repairing it from prose. Score correct, false GO (GO on HOLD gold), false HOLD (HOLD on GO gold), UNKNOWN, invalid and missing separately. Contradiction between declared decision and prose is an additional assertion-level inconsistency, not permission to replace the recorded decision.

First-hop correctness is direct-source competence: each of twelve roots is assessed separately in each arm/block. The prospective ten-of-twelve screen is descriptive, not a confidence guarantee. Terminal correctness and false GO measure downstream operational harm. A correct first hop does not guarantee a correct terminal decision; a wrong first hop is not evidence that handoff transmission caused the error. Report all transitions, including error recovery. Do not drop roots failing first-hop competence or score a persistent HOLD as preserved source meaning by default.

Primary comparison is paired R minus P terminal correctness per root and block. Average the two differences within each root before summarizing twelve roots. Publish all twenty-four root/block pairs. Summarize repeat decision agreement per arm, paired-effect disagreement, reversals, ranges and actual differences between block estimates. Matching aggregate signs alone is not stability. Zero errors on this small selected benchmark is not high reliability in deployment.

## Semantic targets and ambiguous judgments

Each root has seven source-meaning targets: its entire rule and six dated evidence records. Total is 84 targets across twelve roots, evaluated at every available hop (1008 planned hop-target cells across two arms, three hops and two blocks). Targets include history and qualification, not just the final state: a threshold correction should preserve what changed without inventing a new measurement. Events split into multiple conjuncts retain a target only when all required conjuncts are entailed. Record exact source and response spans; equivalent paraphrase is acceptable, literal quotation is unnecessary.

Label each target retained, lost or ambiguous. Lost includes omission, contradiction or partial preservation. If the two documented same-operator passes cannot resolve an entailment, keep ambiguous and explain alternative readings. Primary report-content retention is retained / 7, with ambiguity interval [retained / 7, (retained + ambiguous) / 7]. Literal source content can be retained despite an added unsupported verification caveat; record that caveat separately. Strict status-integrated sensitivity additionally loses a target if an unsupported new status materially qualifies it. Report both frozen views; never choose whichever favors an arm.

A historical statement carried without its later correction can mislead even if the historical quotation itself is accurate. Score the old-report target on report preservation, lose the omitted correction target, and separately record a misleading current-state assertion if one is made. Do not treat a later event as erasing the existence of an earlier report. A proposed action, sent request or forwarded copy is not an executed action, granted approval or independent receipt.

Audit every factual assertion, including additions outside the seven targets. Use supported / unsupported / ambiguous and a criticality flag. A critical addition changes eligibility, applicable scope, provenance independence, approval or execution status. Reference actor-visible source spans rather than an unexpressed author belief. Two passes by the owning operator are not independent annotator validation. Preserve disagreements and all annotation revisions with response hashes; scoring guidance itself remains frozen.

## Missingness and invariants

Invalid and unstarted outputs have null semantic scores. Retain returned invalid raw responses for diagnostics, not silent repair. Show assigned, started, returned, valid and scored denominators separately. Every downstream unstarted node remains in the manifest. Report conditional observed comparisons and worst/best assignment-level bounds for missing outcomes; do not silently impute missing as wrong or drop incomplete roots.

Semantic drift never changes the handoff or triggers in-chain repair. The source-access arm alone receives the original source by design. Gold, mutation controls, scoring guide, operator history and labels never enter native actor context. Full-copy retention and the authored-vocabulary rule controller are offline comparators, not learned model outputs. The controller fails on unfamiliar wording; it cannot grade generated paraphrases and is not a claim of general natural-language competence.
