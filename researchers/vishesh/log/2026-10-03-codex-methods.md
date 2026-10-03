# 2026-10-03 — vishesh/codex-methods

Human request: contribute the experiment guide as general tooling for whichever project the team chooses; check repository fit, documentation and secret exposure before publication.

The toolkit lives in `tooling/agent-experiments/`, with a root navigation link and an explicit integration map. No formal survey, hypothesis, experiment or cross-researcher review is introduced. The existing research gates and researcher directives remain unchanged. The repository's direct-main workflow is followed.

Privacy review removed standalone-machine context and excluded generated traces, local source paths, original package manifests and unrelated workspace material. A selected-file Gitleaks scan with complete redaction returned zero findings across 57 files before publication preparation. A separate path/credential-pattern/context scan returned zero flags. No credentials were read or printed. Only public source metadata and synthetic examples are included. Scanner results are bounded checks, not proof that all possible secrets are detectable.

Validation: the offline harness validator passed twice-per-check replay for 960 worlds and 12,480 events per run, with pairing, reset isolation, known-answer behavior, corruption detection and overwrite rejection. `lab.py check` reported zero errors and the same five pre-existing unresolved-reference warnings. `fd.py check --strict .` passed with zero errors/warnings in a checkout named `swarm-lab`; a first check in a differently named scratch checkout correctly reported its folder-name invariant. No project metadata was changed to evade that rule.

Source integration: reused three canonical paper records and added 26. `lab.py verify` checked 24 resolvable arXiv/DOI records with zero problems; the JMLR and PMLR publication pages were checked directly and remain explicitly URL-only. No full-paper reads or empirical replication are claimed by the new source entries.

Workflow choice: automatic sync was deferred until the requested publication/privacy review was complete, so unreviewed imported files could not be pushed by a timer. Manual checkpoints are used in this isolated contribution checkout. The user request to audit before contribution takes precedence over starting a broad automatic sync immediately. Registration and task claiming use the repository tools; claim fields are never edited by hand.

Next: projects should adapt the toolkit only after their own survey and hypothesis gates, validate production adapters independently, and keep paid collection separate from this offline teaching example.

## Publication result

Published toolkit commit: [4d8eadde6b26f6299d67ba2af90fde7427bba6ac](https://github.com/dmarzzz/swarm-lab/commit/4d8eadde6b26f6299d67ba2af90fde7427bba6ac). The final exact-staged-file Gitleaks review covered 57 files / 210,591 bytes with zero findings. All 34 canonical source links in the toolkit resolve.

GitHub Actions passed: [offline toolkit validation](https://github.com/dmarzzz/swarm-lab/actions/runs/37152506049) and [repository check, source verification and generated index](https://github.com/dmarzzz/swarm-lab/actions/runs/37152505912). The contribution is general tooling; no paid experiment was launched and no project hypothesis was selected. The build task is closed through `lab.py done` after publication.

## Research review publication

Published [36d9a3b](https://github.com/dmarzzz/swarm-lab/commit/36d9a3b): all 214 current atlas candidates reviewed, forty reviewer-authored questions/refinements and cross-connections, a mapping to all sixteen original briefs, fifteen-area context, an eight-candidate shortlist, design review, UI findings and a primary-source access ledger. Review cutoff is main 25a7575 and atlas hash 221d012538054f1770caadee9b63c7681504ec970cb390328e0ad52b345e4fe1. Four extensions substantially overlap newer cards and are explicitly labeled as refinements.

The new hunch bundle at 45b363a is included. Important findings: Scheme C's upper concentration threshold rejects correct unanimity; its citation concentration statistic does not establish independent sample size; five agents with one fault do not satisfy Bulyan's seven-gradient minimum; TypeSafe/Jev confidence is a probability transform requiring task-specific calibration. Source reading depths are explicit, and no full catalogue audit or empirical result is claimed.

Validation checked 214 matching candidate fingerprints, all sixteen brief mappings, relative links and 321 distinct canonical citation targets. Gitleaks with full redaction found zero matches across fifteen contribution files, with no private-path matches. Repository check passed with the five pre-existing warnings. GitHub check and verify jobs passed. The hosted Questions UI imported all 214 comments and displayed eight shortlisted candidates. Browser import is local review state; the public contribution is the Git commit.

No formal hypothesis or paid/model experiment was created. Next work should select one comparison, inspect the closest primary implementation in depth and complete the appropriate survey/review gates. The separate inbox request for formal LLM-survey review remains outside this task.


## Swarm immune-response experimental design

Developed owned exploratory notes and a full proposed experiment specification: a synthetic objective task, three incident strata, source containment crossed with private/shared restoration, fixed 24-round schedule, paired world-level analysis, recurrence and legitimate-update tests, future correct-minority controls, resource caps and existing-toolkit interface. No formal hypothesis or experiment has been registered and no model calls launched.

Primary-source checks corrected the broad novelty claim: INFA-Guard already addresses rehabilitation and MemSecBench already studies selective repair. Fresh reading depths and implementation limits are recorded in the source ledger; no full-paper or code replication is claimed. The next step is full prior-method inspection and survey/hypothesis review before implementation and collection.

Manual checked publication continues under the owner-requested privacy review. Only synthetic task descriptions, owned analysis and public source/PR references are included; the supplied discussion transcript and screenshots are excluded. Validation checks local links, canonical source targets, repository protocol and an exact-file redacted secret scan.

Published the four-document immune-response bundle at [db8cc29](https://github.com/dmarzzz/swarm-lab/commit/db8cc29). Validation resolved all eight canonical sources and 26 relative links in the new bundle. Gitleaks with full redaction returned zero findings across seven publication files. Repository check passed with zero errors and five pre-existing unresolved-reference warnings. The 48-world design is explicitly an estimation study, and a conservative rare-harm bound prevents zero observed incidents from being reported as demonstrated safety. No paid run or implementation is claimed.


## Research navigation and hypothesis tags

Added an editorial navigation overlay with eight cross-cutting focus areas and reused the complete sixteen-project crosswalk. Questions can be filtered by focus/project intersections; cards distinguish current author-linked briefs from reviewer connections. Topics links the same focus index, and connected-work panels expose owned exploratory designs separately from formal hypotheses. Existing question prose, statuses and fingerprints remain untouched. The generated question snapshot is refreshed from its 202-card snapshot to the canonical 214-card atlas for consistency with the new navigation export. Unrelated generated snapshots are excluded from the contribution.

Added optional explicit focus_areas and project_briefs metadata for future eligible hypotheses, validated against the navigation source, with actual recorded statuses and an untagged fallback. No other researcher hypothesis files were modified; none are registered on main at this snapshot. Source ownership, contribution guidance and stale-mapping warnings are documented.

Validation: 17 export/contract tests, filtering assertions, 11 saved-review regression tests, TypeScript and production build passed. Browser verification showed 19 immune-response questions, 12 intersecting Memory, all 214 after clearing filters, and the Topics focus index plus linked design. Existing review data is not changed by navigation. The build retains a non-blocking large-chunk warning. Publication is manually checked and secret-scanned before push.

Published [269e901](https://github.com/dmarzzz/swarm-lab/commit/269e901): navigation metadata, shared UI, export validation and contribution guidance. The staged implementation/source audit found no secret matches; no credentials or private discussion were published. Repository validation passed with five pre-existing citation warnings. Deployment is automatic from main; source and review identities are preserved.


## Priority references and source-grounded extensions

Published [90c4cb1](https://github.com/dmarzzz/swarm-lab/commit/90c4cb1): twenty new references (sixteen papers and four first-party posts), an editorial set of twenty priority atlas candidates and fourteen controlled comparisons. The bundle links all sixteen original briefs while explicitly parking NCA-specific source work. Sources are deduplicated; paper reading depth remains abstract and technical posts skim. Existing social references are reused, with blocked X access recorded rather than invented thread archives.

The most useful new connections are negative dependencies in repair, correction visibility across readers, completeness contracts for omitted logs, and lost retrieval keys versus lost facts. The hidden-profile intervention predates our minority-support framing and reports limited team-performance effects, so preservation of dissent and improvement of decisions remain separate outcomes.

Verification: sixteen arXiv/Crossref lookups completed with zero problems; repository check had zero errors and five unchanged warnings. All candidate fingerprints, canonical IDs and relative links passed targeted validation. The exact 27-file contribution passed a redacted secret scan with zero findings. No formal survey or hypothesis is promoted, and no model or paid experiment was run. Next work is full-methods inspection and deterministic task fixtures after the relevant review gates. Manual checked sync preserves the requested publication audit.


## Biological precedent and visualization assessment

Published [160806b](https://github.com/dmarzzz/swarm-lab/commit/160806b): 301 linked screening assessments covering all 214 atlas candidates, 40 VX extensions, 14 PX extensions, sixteen briefs, ten budget/vigilance hunches, four standalone designs and three fork-merge umbrella questions. These overlap and are not counted as independent discoveries. Twelve primary source anchors record fresh reading limits; inaccessible and catalogue-only leads are distinguished. No formal hypothesis or experiment was created.

The strongest combined direction is evidence ancestry plus durable recovery, with private initial judgments, completeness contracts and executable resource reserves as smaller comparisons. The review flags a substantive correction: bounded-fault Byzantine agreement does not generally require statistically independent failures; external-evidence truth is a separate property. Other researchers' source documents remain untouched.

Validation covered all input IDs and 26 file hashes, canonical citations, relative links, offline embedded data, browser search/type/mechanism filters, deep links, empty results and mobile overflow. Browser checks reported zero page errors. The eleven-file publication audit had zero redacted Gitleaks findings. Repository validation reported zero errors and five unchanged citation warnings. Manual checked sync was used. Next: inspect closest full methods and select a single bounded comparison after the appropriate gates; visual specifications are not run results.
