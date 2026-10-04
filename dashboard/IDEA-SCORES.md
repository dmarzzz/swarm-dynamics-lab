# Researcher scores

All 219 atlas questions and 78 contributed ideas received an individual initial assessment on 2026-10-04 UTC. Vishesh requested these ratings from Codex using the most recent conversation rubric. They are assistant assessments on his behalf, not 297 personal human reviews. Each record includes a short, idea-specific rationale. Scores cover started as well as unstarted ideas; research status is unchanged.

The rubric is visual potential 30%, practical usefulness 30%, physical/biological connection 25%, and novelty relative to the team's work 15%. Each dimension is 0–100. The overall score is the weighted sum rounded to the nearest integer, with half points rounded up. A direct physical model scores above a biological metaphor on the theory dimension. Novelty is relative to this team's work, not certified novelty in the literature. Existing implementations reduce novelty, not measured quality. These component-based ratings supersede the earlier conversational totals.

## Source metadata

- `idea-scores/rubric.json` defines the rubric and provenance.
- `idea-scores/vishesh.json` contains Vishesh's initial assessments.
- `idea-scores/dmarz.json` reserves Dimarz's ratings (canonical repository ID `dmarz`).
- `idea-scores/shadow.json` reserves Shadow's ratings.

Every idea has an explicit nullable entry in each initial reviewer file. `null` means no rating and renders as **NA**. Zero is a valid score. There is no imputation or combined team average. New ideas without a record also default to NA for each reviewer. The exporter rejects unknown IDs, invalid reviewer identities, malformed component scores and totals inconsistent with the rubric.

Published data is generated as `public/data/idea-scores.json`, keyed by stable idea ID with `ratings.vishesh`, `ratings.dmarz`, and `ratings.shadow`. Question and contribution source records are not modified. Existing shortlist review hashes and decisions are preserved. Score fingerprints bind assessments to the content reviewed; changed content leaves the rating visible with a review-again label and moves it below current ratings in score sorting. Activity badges alone do not invalidate a score.

## Entering an optional score

On either Questions or Contributions, open **Score breakdown and optional rating**, select your name, enter all four dimensions and a rationale, then save the local draft. No partial overall score is assigned. **Set to NA** clears your rating explicitly; **Discard local draft** restores the published rating.

Drafts are stored in this browser on this site, independently of shortlist notes. They are not authenticated or shared. The page identifies drafts and storage failures. **Export [name] scores** downloads that reviewer's complete JSON file, combining published entries with saved drafts. Unsaved form text is not exported. It does not change any other reviewer's file.

To publish, reconcile the exported file against the latest `dashboard/idea-scores/<reviewer>.json`, retaining unrelated concurrent changes. Commit only the authorized reviewer's file. The repository's existing authenticated Git workflow is the publication boundary; choosing a name in the browser is not authentication. A main-branch push triggers the regular dashboard deployment. Alternatively, edit your reviewer file directly using the same schema and current candidate fingerprints from the public export.

Run `python3 dashboard/scripts/export.py`, `python3 dashboard/scripts/test_export.py`, and `cd dashboard && node scripts/test_idea_scores.mjs && npx tsc --noEmit && npm run build` before publishing. Never edit generated score data directly.

## Record example

```json
{
  "schema": "swarm-idea-review-v1",
  "rubric_version": "vishesh-visual-bio-v1",
  "reviewer": "dmarz",
  "ratings": {
    "SOC-14": null
  }
}
```

A non-null entry has `dimensions` (`visual`, `practical`, `theory`, `novelty`), `score`, `rationale`, `assessed_by`, `assessed_at`, and `candidate_sha256`. Exporting through the editor creates these fields. Unchanged exported records retain their original assessment provenance and fingerprint; exporting does not silently acknowledge revised ideas.
