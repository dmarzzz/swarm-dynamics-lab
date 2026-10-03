# Question review

`#/questions` presents the canonical research question atlas for human selection. It includes each question, tentative hypothesis, proposed test, comparison, metrics, falsifier, confounds, promotion requirements and linked prior work. Search and filters are encoded in the URL; `#/questions?id=BUD-01` links directly to one candidate.

The exporter copies `researchers/dmarz/notes/question-atlas/candidates.json` to `public/data/questions.json` and verifies the existing content hashes. Edit the canonical lane files and rebuild the atlas through `src/question-atlas/build.py` when research changes; do not edit the dashboard copy. See [DATA-CONTRACT.md](DATA-CONTRACT.md) for the exact contract.

Reviews are local to the browser and site. Shortlist, Discuss and Park are selection notes, not approval for an experiment. The page accepts the standalone atlas's `swarm-lab-question-review-v1` export. Export from the old atlas and import here to move a review between sites. There is no shared review server. Import merges known candidate IDs and replaces overlapping choices; export your local review first when combining reviewers. The local reviewer name is retained.

A saved review of a changed candidate is marked for another look. Editing its notes or exporting does not acknowledge the change. An explicit decision or the “Keep my choice after reviewing this update” action does. Legacy reviews without a per-candidate fingerprint remain flagged on revised cards. Malformed imports leave the existing review intact; unavailable browser storage leaves the review in memory with a prompt to export before leaving.

For local verification, first run `python3 dashboard/scripts/export.py`, then `python3 dashboard/scripts/test_export.py`. In `dashboard/`, run `npm ci`, `node scripts/test_question_reviews.mjs`, `npx tsc --noEmit` and `npm run build`. A local preview can be started with `npm run preview -- --host 127.0.0.1`.

Deployment ownership and automatic publishing are documented in [DEPLOY.md](DEPLOY.md). The canonical team site is `swarm-research.pages.dev`; the former Shadow preview is retired. Merging dashboard changes to `main` triggers production publishing.
