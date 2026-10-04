# Reproduce and audit Antsy v6

## Offline analysis of published evidence

Use a checkout containing this directory, Python3.12+ and Pillow12.3.0. Copy a published `results/<run>` directory to a temporary directory before regenerating audit/analysis files; keep the committed originals immutable. Run from the repository root:

```sh
python -m unittest discover -s 5-experiments/studies/vishesh/antsy-receipt-v6/src -p 'test_*.py'
python 5-experiments/studies/vishesh/antsy-receipt-v6/src/mutation_check.py
python 5-experiments/studies/vishesh/antsy-receipt-v6/src/audit.py --run /path/to/copied-run
python 5-experiments/studies/vishesh/antsy-receipt-v6/src/analyze.py --run /path/to/copied-run
```

46 regressions and six targeted fault injections currently pass. Auditing the known invalid E0 attempt1 with the repaired audit should fail: it has zero scorable references. Earlier saved audit receipts establish only their then-current checks, not retrospective approval of a superseded instrument. `audit.py` checks policy decisions against saved candidates; it cannot independently prove those candidates faithfully represented the pixels. Raw OCR replay and contract/schema tests address that separate layer.

## New real measurements

Follow the repository experiment gate, allocation, pre-run publication and reporting workflow first. The measured environment was Python3.12.3, Tesseract5.3.4 with `ind+eng`, Pillow12.3.0 and PyArrow25.0.1. Manifests record exact runtime, source commit and downloaded shard hash. System packaging/builds may affect timing and OCR; do not describe a different environment as an exact replication.

`study.py --stage E0 --out NEW_DIRECTORY` measures the first20 train receipts. `--stage S1 --development E0_DIRECTORY --out NEW_DIRECTORY` measures the first50 test receipts, rejecting image overlap against development and prior validation. Directories must not already exist. Add `--report` only in the authorized reporting environment; credentials are consumed locally, never printed or committed. The pipeline measures all five OCR configurations once, then replays five decision policies. It does not call an LLM. Model calls and actual OCR calls are distinct from policy checker-use counts.

The first50 test receipts have now been used by this study; a rerun of them is replication or debugging, not a new holdout. A new scientific iteration must specify development and untouched evaluation material before looking at its outcomes. Do not silently expand the sample until a policy wins.

## Targeted measurement-preserving repair

`reparse.py --parent ORIGINAL_DIRECTORY --out NEW_DIRECTORY` reconstructs candidates from the parent's private raw TSVs, then regenerates outcomes/figures/audit. It requires a completed parent with zero execution errors. This version repairs hyphenated subtotal exclusion. It makes zero new OCR/model calls, preserves original measured wall costs, records parser-only repair time and a before/after candidate ledger, and pins both source and parent-record hash. Raw parent images/parquet/TSVs stay on the allocated research host; they are not part of the public artifacts. Published numeric records are sufficient to audit decision and scoring arithmetic, but raw TSVs or a fresh measurement are needed to reproduce extraction.

No controller gets evaluator truth or annotation-guided crops. The shared amount-normalization contract is a remaining common dependency of candidate/reference paths; literal canonical-number fixtures and development label checks support it, while external independent scoring review remains open.
