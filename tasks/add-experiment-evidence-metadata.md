---
id: add-experiment-evidence-metadata
type: task
title: Add evidence confidence and sample-size metadata to every study
kind: admin
status: done
priority: p1
owner: vishesh/codex-pi-review
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-pi-review
depends_on: []
topics: []
claimed_at: 2026-10-04T04:07Z
updated: 2026-10-04T04:20Z
outputs:
- experiments/EVIDENCE.md
- experiments/evidence-metadata.json
- experiments/EVIDENCE-METADATA.md
---

## Goal

At the human owner’s request, add consistent evidence-confidence scores and compact sample-size metadata to current experiment documents and future templates. Distinguish independent sample units from agents, calls and repeated outcomes; preserve frozen execution inputs and prior results.

## Done when

- [x] Define an ordinal evidence-confidence rubric and the sample-size field.
- [x] Backfill every discovered study and record coverage, source cutoff and rationale.
- [x] Render the metadata in relevant documents and update future templates.
- [x] Validate coverage, links and repository checks, then commit and push.

## Coverage note

45 source-scoped cohort/design assessments in 41 entry documents, covering all 21 registration files and 33 distinct registered/implemented study IDs, plus a scripted example, an unrun research-design bank and a new unrun Antsy v6 application plan. Primary assessment source 9781739c, with a bounded current-result refresh at b51e3f1f; 130 source-version hashes verified. Independent task units, repeated outcomes, observed/assigned counts and planned counts remain distinct. Score 0 means untested; null means unassessed. No frozen execution input changes or external hub update.

Published metadata commit 3f684e1e. Corrected four unquoted YAML task titles from concurrent planning changes in follow-up cee602ac, restoring zero repository errors. Nine offline helper tests and the full metadata coverage/staleness check passed.
