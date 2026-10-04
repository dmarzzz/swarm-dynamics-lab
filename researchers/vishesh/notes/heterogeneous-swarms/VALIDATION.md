# Validation and provenance

Checked 2026-10-04 UTC by vishesh/codex-heterogeneous. Research-only contribution; zero model calls, experimental runs or paid inference. No independent scientific replication is claimed.

- Added 30 HX records to the existing contribution-bank contract. Each has a source crosswalk, comparison, metrics, falsifier, confounds, mechanism, visualization mapping, score components and explicit exploratory status.
- The 29-source primary ledger includes 19 papers, six code repositories and four first-party posts/API/project pages. Twenty-four entries are newly catalogued; five existing records are reused. Fresh X roots are summarized separately; inherited X records are not counted as fresh reads.
- `lab.py verify --agent vishesh/codex-heterogeneous`: **15 papers checked, zero problems**. The verifier resolves identifiers through DataCite/Crossref and compares titles; it does not validate scientific findings or peer review.
- Public GitHub API metadata obtained for all six code references: commit, date, license, language and star count. No cited code was executed. Historic release-year claims should be interpreted with the explicit creation/commit metadata rather than guessed from star counts.
- `lab.py check`: zero errors; five pre-existing warnings about unrelated unresolved X-library links.
- Dashboard idea-score JavaScript checks passed. TypeScript and production-build results are recorded after completion below.
- Initial export tests reported missing Git-derived `added_at` values for uncommitted new source files. This is expected before their first commit; rerun after committing rather than inventing publication timestamps or weakening validation.

Formal gate status: scoping review only, no newly claimed full-paper reads, no saturation, no independent review, no accepted hypotheses. Follow-up task `heterogeneous-methods-review` records the work needed for promotion. Public-plan registration is not applicable to this literature contribution; it is mandatory before any experimental qualification or run.
