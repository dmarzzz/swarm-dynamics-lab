# S0-attempt-1 post-mortem — execution failure

Same-author review, vishesh/codex-methods, 2026-10-04. This assessment is retrospective; [original manifest](../results/S0-attempt-1/manifest.json) and [records](../results/S0-attempt-1/records.jsonl) are preserved.

- Assigned:20 receipts,100 planned worker invocations.
- Fully recorded:10 receipts,50 terminal worker records (30 valid Tesseract,20 invalid RapidOCR).
- Operator interruption occurred during the next receipt. Exact started-call total is unknown because the original runner lacked an immediate start journal. Do not turn50 recorded calls into an asserted exact total.
- Hosted-model calls and new provisioning:0. No S1 receipts opened.
- Execution failed; response validity failed; qualification not reached; no scientific diversity comparison is claimed from this attempt.

All RapidOCR failures were process exits. Import-only diagnosis showed `ImportError: libGL.so.1` missing from the host. Python package pins did not capture this operating-system dependency. The offline tests exercised pure functions and artifact rendering but did not import the actual native engine package on the host; their pass was insufficient evidence of startup readiness.

The operator stopped this study, marked the hub run failed, and preserved the numeric records and private partial outputs. The [bounded repair pre-review](S0-repair-pre.md) adds system dependencies and their version recording, import-only runtime checks before calls, per-call start/terminal journals, earlier stopping on invalid execution, and interruption handling. The repair retains extraction, decision rules and thresholds and uses reserved train40–59. No thresholds were relaxed and no failed runs were erased.

Process gap: the dashboard failed local DNS resolution; the actual immutable public GitHub plan was verified in the browser and planned hub status read back directly before launch. This is a reporting-view limitation, not evidence that the plan was unpublished. Runtime fetched and matched the public plan bytes before native execution.
