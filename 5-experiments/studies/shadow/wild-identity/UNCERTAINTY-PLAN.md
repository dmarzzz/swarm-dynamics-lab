# Saved-data uncertainty amendment, 4 October 2026

Owner: shadow/sol-identity. Requested by the 11:25 EDT audit follow-up. This is post-hoc reporting of the already frozen archive, not a new model experiment, accepted hypothesis or confirmatory analysis. Census point estimates were already known when this amendment was written. No paid calls, provisioning or intervention.

## Question and contrast

Does using retained wiki page text instead of inserted/replaced hunk text increase the fraction of attributed revisions with a non-self exact-known-label reference? Use the same matcher, labels and source rows as analyze.py. These are textual references, not verified communication or authorship.

## Method, frozen before supplementary implementation

Group all attributed revisions by page_id. Each page contributes (attributed revisions, snapshot-reference revisions, hunk-reference revisions). Save only hashed page ids and aggregate counts. Reconcile all three totals to the existing summary.json and fail if any differs.

Primary reporting: paired difference in event-weighted reference proportions and snapshot/hunk proportion ratio. Compute 2,000 paired page-cluster bootstrap resamples, sampling the observed number of pages with replacement, seed 20261004. Use linearly interpolated 2.5th/97.5th percentiles. State that these are conditional model-based 95% confidence intervals under an exchangeable independent-page assumption. This preserves within-page dependence but not cross-page copying or shared actors. The assumption is unverified and likely imperfect. Do not claim population-valid confidence or uncertainty about exact archive totals. Reject replicates with zero denominators explicitly and report their number.

Also compute deterministic leave-one-page-out ranges for both metrics. These are sensitivity ranges, not CIs. No CI is invented for the unique-edge count ratio, which is a different nonlinear graph quantity.

## Visualization mapping and acceptance

An 1800px static SVG displays snapshot and fresh-text reference fractions and their conditional page-bootstrap intervals. A static view is appropriate for a frozen archive diagnostic, not a live run. Reconcile the plotted numbers to saved JSON. Known-answer fixtures cover paired resampling, zero-denominator failure, quantile interpolation and leave-one-out ranges. No model/scientific escalation, new host or credentials required. Stop after the frozen 2,000 resamples, regardless of interval width.

## Interpretation boundary

The defensible finding is reference-provenance sensitivity. Identity churn causing coordination remains unidentified. Existing figures and census conclusions remain intact. Cross-page dependence, unauthenticated labels, archive incompleteness, and actor/clock absence in SwarmTraces remain limitations. Formal Flight Deck filing stays blocked as recorded in README.md; the supplementary SVG is working material.
