# R60 development case audit

Owning-agent content audit,2026-10-04. All 24 candidate claim/evidence/verdict records were read; eight middle records were reread after tool-output truncation. This is an operator audit of externally published labels, not a new independent human adjudication. Source indices/hashes are in case-preparation.json. No native model collection. All inspected material is development-only.

## What the first candidate set revealed

Independent annotation is useful but not automatically clean. Preserve the published labels; the audit below neither changes them nor asserts current external truth. Evidence answers are supplied annotations, not verified verbatim extracts from the linked web page. An agent may quote an answer exactly while its answer-to-source attribution is wrong. The intended task must say this explicitly.

| Case ID suffix | Assessment of the supplied packet | Development disposition |
|---|---|---|
| 6a6408e6702b | Direct reported quotation plus later institutional comment; duplicate Guardian evidence; unrelated archive URL needs resolution | Limited; provenance fixture only |
| 80b6b4d27012 | Distinguish what a speaker said from whether industry profits equal that amount; tax windfall distractor | Retain for speech-attribution control |
| 76ba652cbd2e | Date-specific price statement supported by contemporaneous evidence; later evidence includes a boundary inconsistency | Retain with explicit as-of date; later evidence is a distractor |
| 2d87bf8c9d80 | Natural wax, washing and applied wax distinguished; four records from one source | Retain single-source/repetition control |
| 793733573a1d | Allegation versus conviction and friendship; historical wording and degree remain subjective | Quarantine from pilot |
| 6e82b8197ce2 | Increased fact-checking does not establish unprecedented misinformation volume | Quarantine: label/evidence mismatch |
| 62f6d46c48c7 | Claim describes a simulation, while refutation answers whether it predicted an actual pandemic | Quarantine: scope mismatch |
| 25dac95b8f59 | Search result/no reports treated as refutation; supplied evidence is not exhaustive | Quarantine: unknown/refuted boundary |
| 01a0123885eb | Specific recorded cause of death contrasts with allegation; source-quality distractor | Retain historical supplied-evidence control, no new factual claim |
| 8c40a6d264e5 | No documented link plus expert improbability; not an exhaustive impossibility proof | Limited: label-boundary fixture only |
| 2c58b3a68ac9 | Text directly contrasts respiratory symptoms with bloodstream entry; source provenance not audited | Limited: semantic fixture only |
| 3404e567432e | Exact original quotation contrasts with transformed assertion; article-spinning context | Retain quotation/interpretation control |
| 10817df0e157 | Experimental confounding supports uncertainty, but a direct Snopes verdict is exposed | Quarantine: answer disclosure |
| 2f99e0fa3453 | General health effects do not resolve named products and exact death count; fact-check material present | Quarantine: answer disclosure/source selection |
| 4d51741118d9 | Definition change makes historical unemployment rates incomparable; direct fact-check answers | Quarantine from native pilot; retain denominator-change development fixture |
| c66bbe9d118f | Different institution scopes give incompatible counts; broad total unresolved | Retain scope/abstention control |
| aedec0d0ca66 | Planned, in-construction and completed projects cannot be substituted; total explicitly unverified | Retain status/abstention control |
| 18d37c950a3e | Fragmentary claim, empty question and missing original report; justification conflicts with listed evidence | Quarantine: ill-posed packet |
| b53a7292b38e | Different bill versions/votes; date/version changes resolve apparently conflicting statements | Retain temporal qualification control |
| 22fc91dc876c | Trace residue and long-term tablet effects differ; no direct dose-risk evidence | Limited: exact label depends on interpretation |
| 9532f197bbc8 | Domestic import discretion differs from foreign export restrictions; two placeholder annotation URLs | Quarantine: unverifiable provenance |
| fd68fcf88c30 | Intended removals and future suspension differ from completed removal; later ruling postdates claim | Quarantine from as-of pilot |
| 9400f1b21cb5 | Some promises versus unspecified universal quantifier makes exact label disputable | Quarantine: semantic ambiguity |
| f2bdda2192b2 | Moving away is observable; rhetorical abandonment is not a precise factual predicate | Quarantine: rhetorical target |

Eight retained development controls, four limited fixtures, twelve quarantined candidates. Retained means useful for instrument development against the supplied packet, not independently reverified real-world truth. None is a sealed native test case. No performance-based exclusion occurred.

## Prospective corpus repair

Before further selection, reject blank questions, search-result/annotation-placeholder/404 evidence URLs, archived aliases of the fact-check article, and evidence from any fact-checking domain found in the source metadata. Preserve exclusion counts. This is a conservative rule that changes the population and may sharply reduce unknown/conflicting coverage. Do not silently relax it to fill a quota.

Hide URL paths (which can reveal verdicts) in actor context: expose stable document IDs and source host, keeping original locator mapping evaluator-side. Unwrap archive URLs for identity matching, preserve distinct question/answer records, and record exact-text duplicates. Document identity remains NOT an independent-acquisition receipt. Source URL maps alone cannot determine whether two outlets copied a common origin.

Use candidate record dates only as supplied; no assertion that all evidence predated the claim. Primary pilot is retrospective supplied-evidence synthesis. An as-of/real-time deployment claim needs reliable per-document timestamps and a new audit. Retain prediction, allegation, proposal and unknown semantics in development fixtures. Do not alter externally authored verdicts to fit our decoder.

## Case-quality assessment

- Decision relevance: pass for evidence-assisted review; no deployment efficacy yet.
- Answerability/label validity: mixed; sixteen limited/quarantined candidates show why automatic intake is insufficient.
- Actor isolation: gold fields structurally removed; source URL and answer text leakage requires repaired intake and content audit.
- Mechanism: native first-turn states fork into exchange/private review; model-selected quotation still needs entailment audit.
- Challenge/coverage: four verdicts, temporal/scope/status/conflict/source-sharing mechanisms; no independent acquisition claim.
- Baselines: literal citation validator, duplicate-aware board and plurality aggregation implemented; native single/six/private60 comparisons unrun.
- Realism: real published claims and independent published labels; annotation-guided evidence, public-data contamination and label noise remain limits.
- Independence/precision: event-group audit required; eight pilot roots are feasibility only.
- Holdout: all 24 inspected development candidates excluded from fresh test selection.
- Robustness/reproducibility: ten offline contract checks pass; source and per-case hashes retained; no native qualification/admission granted.

Readiness: development controls available; fresh qualification/pilot corpus requires content audit and event grouping under the revised intake. Do not run60 agents on the 24-candidate intake as if it were a clean benchmark.

## Intake repair verification

Implemented the above archive identity, source-domain, blank-question and placeholder screens, plus actor document IDs in place of URL paths. The source scan now has 405 eligible rows (91 supported,264 refuted,10 insufficient,40 conflicting) before manual semantics/event review. A new24-candidate development intake is recorded in case-preparation-v2.json; this is not a new independent dataset or a native outcome. Original candidate report and audit remain unchanged. Thirteen offline checks pass; no case gains native readiness from those software checks.
