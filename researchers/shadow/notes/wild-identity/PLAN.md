# Identity observability analysis plan

Owner: shadow/sol-identity. Written 2026-10-04 after inspecting schemas and candidate sign-off patterns, before calculating the lifetime/concentration results. Descriptive and post-hoc, not a preregistered hypothesis or experiment.

## Scope and units

Compare the downloaded collusion.wiki revision archive, SwarmTraces redacted JSONL, and a frozen swarm-lab git snapshot at `4959a80b`. Labels, sign-offs and commit-message agent ids are observable names, not verified independent people, processes or models. No new model calls, no paid calls, no live endpoint probes. Raw datasets and raw commit-message exports remain local.

## Measures

- For each nonblank wiki label and bracket-prefixed researcher/agent commit id: revision/commit count, first and last observed timestamp, observed span (last minus first), singleton status. This is not biological lifetime or survival time. Include zero-span identities; report positive-span sensitivity and observation-window-normalized spans. Report missing and anonymous events separately.
- Empirical CDF of observed spans and Lorenz curve of activity counts; population Gini, top-10% share (ceiling), event counts and identity counts. These describe a finite, dependent archive; do not pretend an iid confidence interval estimates unseen agents.
- Graph: known actor id -> exact known label/id mentioned in its text, excluding self references, deduplicated within one event. Wiki full bodies retain inherited content, so separately score only added/replaced text using stored diff hunks. Count copied standalone sign-offs and their editor-label mismatch. The conservative graph is still a text-reference graph, not proof of communication or coordination.
- Cross-tab above/below median observed span against any outbound fresh-text reference. This is descriptive association, not a churn effect: more events mechanically create more reference opportunities.
- SwarmTraces: audit `kind`, `time_utc`, author-like metadata and name/sign-off candidates. Do not impute times from record ids, parent ids, embedded payload dates, or author identity from variable names/redaction placeholders. If unavailable, return not-identifiable rather than fabricate a third comparable graph.

## Robustness and tests

Test Gini and graph logic on synthetic fixtures; check lifetime arithmetic, row accounting, exact token boundaries, deduplication and removal of inherited references. Compare computed wiki per-label counts/spans against the supplied labels table. Keep all identities including potentially human labels in the primary descriptive census; report why source-study denominators differ. No significance or causal claim. Figure/table conclusions must distinguish snapshot provenance from new references.

## Deliverables

One-page FINDING.md; reproducible stdlib CLI `analyze.py --data PATH --repo PATH --commit SHA --out PATH`; aggregate JSON/CSV, SVG plot and tests. An optional PNG plot is generated locally from the derived curve CSV and filed through Flight Deck if used as a submission figure. No raw text or dataset rows in git.
