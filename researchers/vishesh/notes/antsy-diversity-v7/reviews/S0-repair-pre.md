# S0 bounded repair pre-review

2026-10-04, vishesh/codex-methods; same-author assessment. Prospective to repair collection.

S0-attempt-1 was interrupted after both RapidOCR workers returned process errors repeatedly. Import-only diagnosis, with no extra inference, identified missing system library `libGL.so.1`. Pinned Python dependencies were insufficient to reproduce a native OpenCV runtime on this server. This is an execution defect, not low perception competence or a diversity result. Preserve all original records and private partial outputs. No S1 data was opened.

Repair: install official Ubuntu `libgl1` and `libglib2.0-0t64`, verify imports without constructing the OCR engine, record package versions in runtime metadata, and rerun all offline tests on the host. Strengthen the launcher to check imports before first inference, journal every worker start/terminal status, stop before another receipt after an execution failure, and record operator interruptions as failed attempts. These additions change auditability and environment checks, not extraction, decisions, qualification thresholds or metrics.

Use the single reserved train40–59 qualification set under the unchanged PLAN. Fresh source, public registration, browser/content verification and admission required. At most100 invocations; zero hosted-model calls/new infrastructure charges. If this bounded qualification fails, stop before S1 and report the remaining defect or competence limit without relaxation. Exact start count in the interrupted parent cannot be reconstructed perfectly because its ledger was incomplete; distinguish completed records from partially started work rather than inventing a total.
