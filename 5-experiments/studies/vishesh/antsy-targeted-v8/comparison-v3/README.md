# Antsy: is a second receipt reader useful after fixing the parser?

**Offline comparison package prepared. Native qualification and evaluation have not run.**

The [prospective plan](PLAN.md) defines original primary, repaired primary and selective checker fallback. [Case quality](CASE-QUALITY.md) records strengths and limits. [Fixture results](FIXTURES.json), [real-case QA](CASE-QA.json) and the [development text baseline](DEVELOPMENT-BASELINE.json) are software/data-preparation evidence, not OCR accuracy results.

## What is built

- 36 actual pinned CORD receipts:12 inspected development,6 untouched qualification,18 untouched evaluation. The actor sees only pixels. Two evaluation totals are unscorable and remain in the denominator/accounting.
- 24 parser controls cover8 failure/control families at3 amounts, plus order and layout invariance.
- A bounded native controller collects paired RapidOCR/EasyOCR observations, calculates all three policies, distinguishes wrong accepts from abstentions and failures, and reports rescues/harm, shared wrong answers and service-time accounting.
- The standard [shared receipt contract](../../../../../tooling/agent-experiments/TRACE-RECEIPTS.md) is integrated at dispatch: complete roster, durable start state, actual worker configuration declaration, image/output/parser/grade/phase/stream hashes, terminal and unstarted states. Transition/API usage are explicitly not applicable. Raw OCR/runtime paths remain private.
- Source/input/context/admission mismatch prevents or stops dispatch; first execution or trace error stops the stage. Interruptions preserve unresolved starts. No automatic retries or evaluation launch. A saved, hash-bound passing qualification is required for the evaluation CLI.
- A1600×1000 results figure distinguishes correct, wrong, abstained, unscorable and failed/missing outcomes. It is rendered from retained policy rows.

The native worker uses the established cold CPU engines and preserves the original parser output before parent-side alternative parsing. A90s censoring ceiling is separate from45s service eligibility. Source/context receipts describe the declared and observed worker configuration; they are not hardware determinism guarantees. Images are not resized externally; native engines retain their own internal preprocessing.

## Offline validation and reproduce

```sh
python3 -m unittest discover -s researchers/vishesh/notes/antsy-targeted-v8/comparison-v3/src -p test_comparison.py
python3 -m unittest discover -s scripts -p test_trace_receipts.py
python3 -m unittest discover -s scripts -p 'test_experiment_*.py'
```

`src/pack_cases.py` accepts the pinned downloaded parquet file, an unused private output directory and a QA destination. It freezes separate actor/evaluator files. `src/development_audit.py` replays only development annotation text through the two parsers. `src/runner.py --help` documents the native entrypoint; it requires private current admission/runtime receipts and has no bypass flag. `src/cases.py` constructs the authored observation controls. Full source hashes/test counts are in validation.json.

Before native launch, publish/register immutable condition-specific plan and verify the public page; verify the original cumulative ledger, approved-account exclusive allocation, actual package/model fingerprints and case/instrument hashes. Retain the original budget: no new charge allowance. Package preparation does not establish native capability or current access. Finish the native attempt with standard `experiment.py finalize` plus the scientific review and verified artifact retention, then release the allocation.

## Concrete next run

Q0-comparison:6 receipts,12 cold OCR calls maximum,20minute ceiling. Qualification requires full trace coverage and valid outputs from both engines on all6, all labels scorable, repaired primary at least4 correct with0 wrong accepts, and fallback0 wrong accepts. Any error stops the stage.45s eligibility is reported separately.

Only after Q passes: E0-comparison,18 receipts,36 calls maximum,40minute ceiling. The native CLI requires the saved Q summary and its receipt hash; it never launches E automatically. Both stages together maximum48 OCR calls/60minutes, zero incremental charge, no hosted-model calls, no new machine or spending allowance. A new approved-team allocation is required because the previous one was released.

**Interpretation limits:** fixed small feasibility cohort, two unscorable E labels, no demonstrated error independence, no merchant-cluster audit, and no proof that a second engine adds value. The clean-text development miss on Netto remains a known shared parser limitation. A null/adverse result is a reason to park the checker, not tune on evaluation or silently widen the experiment.
