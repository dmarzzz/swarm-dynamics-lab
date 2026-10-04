# Case quality assessment

Scope: same-author offline construction/validation, prior to any native comparison call. [PLAN](PLAN.md) precedes implementation. Apply the shared [case rubric](../../../../../tooling/agent-experiments/TEST-CASE-QUALITY.md).

| Dimension | Assessment | Evidence and limitation |
|---|---|---|
| Decision relevance | pass for bounded feasibility | Three paired policies isolate parser repair and selective fallback. Native data, not fixtures, must establish checker benefit. |
| Answerability | limited |12 development target crops visually inspected; totals agree with labels, though two are faint. No qualification/evaluation image or answer was displayed to the operator. Automated label checks are not human image audits. |
| Labels/scoring | pass with missingness |12/12 development,6/6 qualification,16/18 evaluation totals parse and match the source's labeled total line. These are two representations of one annotation, not independent annotators. Two evaluation cases remain unscorable and retained. |
| Isolation | pass at interface |Separate actor-image and evaluator-label directories; worker arguments contain image, engine and output paths only. No gold, receipt ID or operator context passed. This is a trusted OCR-process interface, not an OS sandbox against malicious agents. |
| Mechanism isolation | pass |Original/repaired parsers use identical primary OCR bytes. Fallback is triggered by repaired-primary abstention only. Same images to both engines; no claim of independent errors. |
| Challenge/coverage | limited |24 authored controls across8 families and3 amount variants. Real development:4 quantity-bearing,8 subtotal-bearing,7 over1MP; Q:0 quantity-bearing,5 subtotal-bearing,4 over1MP; E:5 quantity-bearing,12 subtotal-bearing,14 over1MP. These annotation categories are broad proxies, not proof of the exact parenthesized-quantity failure. |
| Strong comparison | limited and explicit |Clean annotation-transcription baseline gets11/12 with either parser; the remaining development label is Netto, outside the frozen anchor vocabulary. No new OCR engine can guarantee fixing that shared lexical gap. This comparison tests the stated repair/fallback, not the best possible receipt extractor. |
| Realism | pass for this dataset only |Actual CORD receipt images retain lighting, damage and layout variation. Constructed word controls test parsing only. No claims about invoices, other languages/currencies, live finance deployment or LLM swarms. |
| Independence/precision | limited |36 distinct pixel hashes, no within/across-split duplicates. Merchant/layout cluster independence not established.18 evaluation records,16 scorable; feasibility-level precision only. |
| Holdouts | pass for operator separation |Fixed indices declared before inspection, distinct splits and frozen image/label hashes. Automated packaging accessed all selected labels; human/assistant inspected only development crops/values. Generated manifest is not proof of never having appeared in engine training. |
| Robustness | pass for instrument fixtures |Order and translation invariance; malformed/multiple amounts and unresolved final totals; timeout/interrupt/missing/context-drift tests; all assigned/unstarted calls retained. |
| Reproducibility/cost | prepared |Pinned dataset revision/shard hash, split hashes, source fingerprint, parser controls, complete per-call trace adapter. Native runtime/allocation/admission remain required. No new paid calls or charges. |

## QA repair during preparation

The initial corroboration check attempted to parse the whole annotated total line, including label words, as a number. That incorrectly reported zero corroborated labels. `CASE-QA-initial.json` is retained as failed preparation evidence. The corrected check requires exactly one independently parseable numeric word in the dataset-designated total line and matches it to `gt_parse.total.total_price`. It corroborates all34 usable labels. It does not change any image or ground-truth amount. No engine was run or held-out case selected by performance.

## Data provenance and rights

CORD-v2 is published by NAVER CLOVA under [CC-BY-4.0 in its dataset card](https://huggingface.co/datasets/naver-clova-ix/cord-v2/blob/main/README.md). Collection uses revision `7f0115a4b758a71d6473b8d085751692da2fef98` and the exact first train shard hashed in CASE-QA.json. Raw images/annotations and target crops stay private/local; the public contribution contains code, split indices, hashes and aggregate QA. Images contain masked source information; do not assume every receipt field is safe for publication.
