# Pre-run assessment: v3 engineering a1

Status: ready for offline engineering; native launch blocked on a dedicated machine. Parent: native v2 4deeb0f2 and REVIEW.md. This is a fresh instrument qualification, not replacement of v2's invalid primary control.

The original controls separate store restoration from blocking but hide collateral loss and lineage failure. V3 adds these boundary conditions, strict scoring, explicit agent contracts and visualization telemetry. Local dry development checks used 6400 and tests 6500/6504; planned engineering IDs 6600–6615 have not been executed before this assessment. Nine targeted regression tests currently pass. Model calls/spend/workers: zero/zero/one local process. Dataset: 720 assigned scripted outcomes; no paid or fleet worker is launched by this assessment.

Acceptance: all 720 rows retained without invalid execution; all CLEAN/no-incident tasks succeed; rollback loses the legitimate-learning fact while selective restoration preserves it; removing replay eliminates the blocking advantage; missing lineage prevents magical stale filtering. Evaluate variation over all target slots and keep negative results. Commit this pre-run record and protocol before executing the named suite.

Visualization mapping: VISUALIZATION.md, with exact round-event and outcome bindings. Produce both historical native v2 replay and a labeled v3 engineering animation; check against numeric outcomes and show the scientific backend label. Synthetic normal/failure tests and frame inspection validate the renderer. Failed rendering gets repaired from saved traces without repeating model requests.

Native next step: reserve up to USD 8 atomically from the existing shared budget, obtain a merged exclusive host claim and verify it, deploy the frozen version, validate the public plan, then run only design.json native-repair (three outcomes, fresh task 6700). If host or budget is unavailable, record the blocker and retain the engineering evidence.
