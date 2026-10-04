# Post-mortem: receipt-native-a1 setup

Execution stopped before model construction, before hub run creation and before output-directory creation. Sanitized worker result: ValueError. The protocol omitted exact headings required by public_plan.validate; local validation reproduced public_plan_sections_missing. This is a documentation integration defect, not a model result. Ledger remains 240 calls, USD 1.815067 reserved, unchanged from baseline. Zero assignments dispatched.

Repair: required section headings, unchanged scientific protocol, a public-plan regression test and new attempt receipt-native-a2. Original setup log retained on the dedicated host. No retry of a scientific outcome, no extra budget. Next action: repair-and-rerun; acceptance is public-plan preflight pass before any provider dispatch.
