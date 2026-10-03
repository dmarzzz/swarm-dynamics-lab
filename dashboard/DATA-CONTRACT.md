# Static data contract

Run `python dashboard/scripts/export.py` from any working directory. Python 3.12 and PyYAML are sufficient. Git history must be available (`fetch-depth: 0` in CI). Optional `GH_TOKEN` enables one bounded `gh issue list` call, otherwise batch issue numbers and URLs still come from ISSUES.tsv.

The shared DASHBOARD-SPEC.md contract is preserved. Clarifications and additive fields:

- All timestamps are ISO 8601 with timezone. `added_at` is the first Git A record for that path. `added_by` prefers explicit frontmatter, then the first-add commit's `[team/agent]` prefix, otherwise `unknown/unknown`.
- `authors` is a short display string, up to three authors and `et al.` when needed. `year` and `date` are nullable. Every library entry always has `topics` and `links` arrays.
- Timeline has chronological per-commit/team/agent/kind groups. It includes all library A records, including files later removed or renamed. Thus its sum can exceed the current library count. Metadata-only edits contribute no entries.
- Agent roster includes registered agents and attributed contributors with no registration. Unregistered contributors have `state: unknown`. `entries_added` counts currently present entries, and `last_commit_at` includes metadata updates whose commit has an agent prefix. Active states are working, active, running, busy.
- Survey `sources` is a distinct known-source count, `reviewed_by` is a reviewer-id array, and `gate` uses `lab.Lab.gate_problems` verbatim. `status` uses `lab.Lab.survey_state`.
- Task records preserve their full frontmatter. `summary.tasks.blocked` is additive.
- Batch records have `id`, `source`, `topic`, `n_candidates`, `state`, `assignees`, `updated`, plus issue `number`/`url` where mapped. API enrichment adds `labels` and `title`. State is free, claimed, closed, or unknown. TSV alone cannot determine whether a mapped issue was closed, so it reports unknown rather than fabricating availability.
- Graph nodes use the first topic as their primary `topic`. Edges are undirected, deduplicated source-target pairs. Wikilinks are included first, followed by sparse four-neighbor topic connections rather than quadratic cliques. Topic expansion stops at 20,000 edges.
- `hypotheses.json` and `experiments.json` are additive frontmatter arrays for the research funnel. They are `[]` when empty.
- Every JSON artifact is capped at 5,000,000 bytes. Full-text entry bodies are deliberately not exported. The current library is comfortably below the cap.

Validate committed data with `python dashboard/scripts/test_export.py`. CI exports fresh data into the deployment, without writing bot commits back to the repository.
