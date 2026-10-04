# Reporting tools for market-split-opus

Saved-data tools, outside the frozen `src/` and so outside the engine hash. They read finished run directories and never call a model or enqueue a run. `audit_saved.py`, `verify_hub.py` and `archive.py` are the Sonnet pilot's files unchanged. `usage.py`, `collect.py`, `summarize_s1.py` and `plot.py` are the pilot's with this study's task ids (110-115), caps, output ceiling and model label; `summarize_s1.py` also lists every firm-count change with its note. `verified.py`, `compare_models.py` and `publish_analysis.py` are new.

`compare_models.py` sets the two cohorts side by side. The Sonnet pilot ran tasks 36-41 and this study runs 110-115, so nothing is paired across models and nothing is pooled.

The summary figure uses mapping `market-split-summary-v1` from the pilot: registration by rule, paired flexible-minus-locked profit, and mean owned firms through time, from S1 records of one attempt only. An incomplete collection is labelled PARTIAL / IN PROGRESS.

`publish_analysis.py` reports stage totals under `observed_` keys and reports `model_calls` 0 and `api_cost_usd` 0, because the hub sums `api_cost_usd` over runs.
