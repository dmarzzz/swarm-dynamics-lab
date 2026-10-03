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
- `questions.json` is a separate, faithful JSON projection of `researchers/dmarz/notes/question-atlas/candidates.json`. It preserves the complete object and array order; only whitespace is compacted. There is no dashboard-specific wrapper, prose truncation, source re-enrichment or review-state insertion. These are **unreviewed hunches**, never entries in `hypotheses.json`, `experiments.json` or their summary counts.
- Every JSON artifact is capped at 5,000,000 bytes. Full-text entry bodies are deliberately not exported. The current library is comfortably below the cap.

Validate committed data with `python dashboard/scripts/test_export.py`. CI exports fresh data into the deployment, without writing bot commits back to the repository.
- `threads.json` (additive, optional) carries X thread extras for the X threads view, one row per `kind: thread` entry: `id`, `handle` (author_handle frontmatter, else the first archived post header), `name`, `date` (root post date from the archived text, nullable), `likes`/`reposts`/`replies`/`views` (parsed from the `metrics` frontmatter string, nullable when not recorded), `posts` (count of archived author posts, minimum 1) and `first_line` (opening line of the archived text, 160 chars). Lone surrogates from scraped text are dropped.

## Question atlas

The top-level `questions.json` fields are copied from the canonical atlas:

- `version`, `date`, `status`, `source_snapshot`, `previous_atlas_commit`: atlas revision and research provenance. `source_snapshot` is the atlas's research snapshot, not necessarily the dashboard's current `summary.head_sha`.
- `topics`: topic-slug-to-display-name object.
- `changes`: `new`, `revised` and `unchanged` arrays of candidate IDs in atlas order.
- `content_sha256`: digest of the complete enriched candidate array.
- `candidates`: complete candidate records, currently 202 across 15 areas. Counts are derived from this payload, not fixed limits.

Every candidate retains `id`, `area`, `title`, `question`, `hypothesis`, `test`, `baseline`, `metrics`, `falsifier`, `confounds`, `prior`, `novelty`, `feasibility`, `needs`, `briefs`, `candidate_sha256`, `change`, `lane` and `status`. The `hypothesis` string is tentative reasoning inside a hunch, not a formal hypothesis record. Candidate `status` stays `unreviewed-hunch`; the top-level status stays `Human-requested unreviewed hunches`.

Each `prior` relationship retains `id`, `relation`, `title`, `path`, `url` and `catalogued_depth`. Source paths and brief paths are repository-relative. Catalogue depth describes the source record's metadata; it does not claim the atlas author read that source at that depth. Local browser review decisions and notes are separate from this immutable export and cannot authorize experiments.

Before writing any artifacts, export validates the atlas's required fields and types, unique candidate IDs, declared topics, novelty/feasibility/change values, source-ID/path correspondence, existing in-repository brief files, change-index consistency and both hash levels. Hashes use the canonical builder's `json.dumps(value, sort_keys=True)` UTF-8 encoding, including its default ASCII escaping. The per-card hash covers the 15 editable fields and the original prior `id`/`relation` pairs; the aggregate hash covers the enriched candidates. Export verifies these existing hashes without replacing them, so stale content fails with a rebuild error rather than silently changing review identity. The artifact uses the same 5 MB limit as every other export.

Contract tests compare the entire exported atlas to its canonical input, check separation from the formal research funnel, and exercise rejection of duplicate IDs, missing or mistyped fields, accepted-status changes, unknown sources/areas, mismatched source paths, missing or escaping briefs, stale per-card/aggregate hashes and stale change indexes. No test downloads sources or runs research experiments.
