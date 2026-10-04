# PC-3 manual runbook

Read SETUP.md, PLAN.md and preceding post-mortem. Source entry point src/run.py prepare/run; no resume. Offline: python -m unittest discover -s researchers/vishesh/notes/phantom-coast/pc3/tests -q (Pillow 12.2.0). prepare makes assignments only; run requires current private admission, public registration, pinned source/runtime and lineage-bound ledger. Q0 before S1. No bypass or fallback credential. Owner permits direct dispatch rather than queue.

Saved-data audit: reporting/audit_saved.py DIRECTORY --output AUDIT.json. Analysis: reporting/analyze_saved.py DIRECTORY --output ANALYSIS.json. Replay: reporting/build_replay.py DIRECTORY. These make no model calls. After hash-verified upload/readback, backup ledger, remove temporary credential, stop owned processes and release claim. Preserve uncertain reservations and previous cohorts.
