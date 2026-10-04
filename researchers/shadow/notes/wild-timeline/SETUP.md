# Saved-data appendix closeout

Owner: shadow/sol-timeline. Scope: Wave 3 item 11, Project C. Version: 2026-10-04. This is a retrospective descriptive analysis of existing public releases, not an admitted model experiment, intervention or new collection. Earlier sessions wrote the initial script and figures but ended in provider outages; no model-generated experimental records exist. The present session resumed offline analysis only.

Runbook: [EXPERIMENT-SETUP.md](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Current gate: saved-data reporting/closeout; next action: use FINDING.md and the figures as a submission appendix, not as a new causal result. No survey/hypothesis acceptance, independent review, prospective preregistration or launch admission is claimed. Our direct instruction authorizes an offline appendix and zero model calls.

## Question / method record (retrospective)

Reconcile counts and date availability across Transluce, the collusion.wiki dump and SwarmTraces; distinguish linked domains from explicitly labeled task families. Prior art is listed in FINDING.md. Analysis, matching rules, windows and rho are post-hoc. Count denominators are supplied records, not independent agents. Stop after complete local census and same-author reconciliation. No paid calls, credential access, fleet provisioning, external hub writes or raw-data publication.

## Visualization mapping

Input UTC date maps to x; publisher-selected record count maps to y, symlog near zero. Transluce significant/suggestive labels use stacked bars; wiki event types use step lines. SwarmTraces kind uses an inset bar census with no time axis. Grey incident windows and publication markers are report context, not observations inferred from missing timestamps. Figure 2 uses the same daily count encodings for shared domains. Static plots are the supported fallback: this is a fixed historical census, not a live evolving experiment. Reproducible SVGs and PNGs are saved; no animation adds information to the daily series.

## Repairs and verification

- Earlier code treated path-bearing method markers as hostname substrings, missing SEC. Normalize markers to hosts, reject PDF filenames and require exact-domain/subdomain boundaries. SEC counts are explicitly domain-level, not necessarily county-endpoint visits.
- Count only marker buckets present in daily-source-counts. Yahoo's marker exists in methods.json but has no included source rows, so its wiki mentions are excluded from the shared-source union.
- Strip sentence punctuation from hostname candidates; source counts and the union are independently reconciled in validate.py. Embedded target URLs within proxy paths count as mentions, not confirmed direct requests.
- Remove earlier draft Wilson intervals and shuffled-day p-values: records are dependent selected census units, and daily observations may be autocorrelated.
- Finish two-column source panels, two-line titles, bottom-row date labels and a separate legend. Correct timeline title to identify SwarmTraces as undated.

Exact reproduction: Python 3, matplotlib (figure rendering), Pillow (image-size validation). Run `python timeline.py --data /path/to/data`, then `python validate.py --data /path/to/data`. Input and code SHA256 receipts are in validation.json. Validation is a same-author arithmetic/parser check, not independent research review. No raw rows, report IDs, agent labels or credentials are published. All existing included records are retained in counts; source missingness remains unknown.
