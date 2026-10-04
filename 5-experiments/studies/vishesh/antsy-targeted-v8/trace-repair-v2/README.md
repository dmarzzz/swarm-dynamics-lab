# A shared parsing failure, not evidence for another reader

2026-10-04, vishesh/codex-methods. Retrospective saved-data analysis following the [prospective offline plan](PLAN.md). Original Q0/D1 workers, outputs, thresholds and verdicts remain unchanged. No new OCR/model calls, machine allocation or charges.

## What the image and traces establish

The retained train62 image visibly has a total line with quantity60 and amount3,600,000. The item row shows60,000 ×60 and the payment row repeats3,600,000. This is the owning author's visual reading of inspected development material, not an independently retrieved CORD gold label. The image remains in the private evidence archive; identifying receipt content is not republished.

The primary OCR retained the clean label `Total(Qty=60` and one amount. The original shared parser excluded the whole row because it contained Qty. The checker instead returned a damaged quantity label, a spurious numeric token and unrelated text alongside the amount. Its abstention has more than one cause; simply deleting the Qty exclusion would not make that output safely parseable.

A separate candidate recognizes only a whole-word `Total(Qty=<digits>)` annotation, allowing an absent closing parenthesis at the end of that OCR word. It removes that explicitly labeled quantity from field parsing, then applies the unchanged conservative extractor. It does not repair hyphens to equals signs, remove low-confidence words or choose the largest amount. Original and normalized observations have separate hashes. The old parser and historical hashes are untouched.

## Replay and controls

[Replay results](replay.json): all8 saved outputs from3 distinct receipts reproduced their native candidates under the frozen parser. Only Q0 train62 primary changed: missing →3,600,000. The two previously readable receipts stayed unchanged; D1 train62 checker still abstained. Q0 did not retain a completed train62 checker output. Repeated OCR outputs are not independent receipt samples.

Seven test methods cover clean quantity labels, ordinary totals, damaged/incomplete labels, spurious numbers, multiple amounts, conflicting totals, excluded contexts and input immutability. These constructed fixtures test intended semantics; they do not estimate deployment accuracy. The exact inspected case motivated this candidate, so its recovery is development success, not held-out validation.

**Decision: finish this saved-data repair; keep comparative qualification closed.** Both readers share the extraction mechanism, so reader diversity alone cannot eliminate that failure mode. The primary already saw enough information here; the expensive checker has not demonstrated additional value. Next scientific work, if pursued, should validate extraction on independently labeled development layouts and reserve fresh qualification cases, with a primary-only baseline. A warm checker is not yet justified by these results. No native successor is launched or implied.

## Shared receipts contribution

[TRACE-RECEIPTS](../../../../../tooling/agent-experiments/TRACE-RECEIPTS.md) adds a common private retention primitive and offline manifest auditor. Every shared operations closeout now reports coverage independently of execution status. New/revised native launchers adopt the contract through their pre-run assessment. Frozen workers are not hot-patched, and this is not a claim of fleet-wide installed capture.

The [D1 audit](trace-audit.json) is a **retrospective bridge**, built only from retained bytes and separate from original results. It reconciles6 assignments into3 valid starts and3 unstarted, verifies inputs, outputs, parsed values, timing/eligibility results, phases and streams, and has0 byte mismatches. It deliberately reports3 missing effective-context receipts: the bridge does not establish a complete frozen configuration delivered to each worker. D1's earlier native runtime/source checks remain separate evidence.

The bridge marks transition not applicable because OCR did not act on an environment, and API usage not applicable because it invoked no hosted API; these declarations do not erase historical cumulative spend. Its grade artifact is the native timing/eligibility result, not a gold answer score. `source_sha256` hashes the recorded immutable source reference string; `config_sha256` hashes the original manifest bytes. These are reference bindings, not a whole-code/runtime verification. The common audit verifies artifact bytes and declared coverage, not provider delivery, semantic adequacy or statistical independence.

The private manifest and raw observations stay local. Public output contains numeric counts, fixed categories and hashes only. `bridge_d1.py` requires retained local Q0/D1 evidence and a new output directory; `replay.py` similarly refuses to overwrite its report. Neither tool dispatches anything.

## Reproduce offline checks

```sh
python3 -m unittest discover -s scripts -p test_trace_receipts.py
python3 -m unittest discover -s scripts -p 'test_experiment_*.py'
python3 -m unittest discover -s researchers/vishesh/notes/antsy-targeted-v8/trace-repair-v2 -p test_fields.py
```

See [validation](validation.json) for the checked source hashes and test counts. This is same-author software validation and saved-data analysis, not independent replication or experimental-agent performance evidence.
