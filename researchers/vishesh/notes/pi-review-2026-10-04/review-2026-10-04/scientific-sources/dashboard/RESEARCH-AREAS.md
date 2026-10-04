# Research areas, project connections and hypothesis tags

The dashboard offers two complementary ways to browse research. **Literature topics** are the canonical slugs in `library/topics.yaml`; they organize sources and research gates. **Cross-cutting focus areas** connect specific questions across those topics. They do not create another survey gate or imply that a hypothesis has passed review.

The Research area dropdown groups these choices separately. It includes immune response and recovery; evidence and diversity; memory and knowledge continuity; dissent and governance; provenance and trust; budgets and incentives; coordination and adaptation; and measurement and reproducibility. The Project idea dropdown covers the sixteen original briefs. Selecting a project and an area intersects their question sets. Counts beside options are total membership, not the number remaining after every other filter.

## Sources and ownership

- Question prose, primary `area`, tentative hypothesis and review fingerprints remain owned by the [canonical atlas](../researchers/dmarz/notes/question-atlas/candidates.json). Navigation never rewrites those fields.
- The initial focus mapping and design links live in [navigation.json](../researchers/vishesh/notes/research-navigation/navigation.json), owned by `vishesh/codex-methods`. Membership lists are deliberate editorial selections, not automatic keyword tags or claims of exhaustive coverage.
- Project connections reuse the [reviewed sixteen-project crosswalk](../researchers/vishesh/notes/atlas-review/project-crosswalk.json). Question cards distinguish original author links from reviewer-added cross-connections.
- The exporter validates IDs, canonical topics, paths, duplicates and classification boundaries, then writes `public/data/navigation.json`. Do not edit that generated copy.
- If the atlas fingerprint changes, the UI flags the mapping for review. Invalid/deleted IDs stop export. Review the changed candidates before updating a mapping's snapshot; changing the stamp alone is not a review.

The Topics page links the focus areas, project briefs and contributed designs. Questions shows the same connections and a separate formal-hypothesis section. Browser review choices remain local; research navigation changes are committed to GitHub and deployed with the dashboard.

## Tag formal hypotheses without changing their status

Only the owning researcher edits a hypothesis. The existing research gates still determine whether the file may exist and its allowed status. When an eligible hypothesis is created, use existing topic slugs and optionally the following navigation metadata:

```yaml
topics: [llm-agent-swarms, fork-merge-security]
focus_areas: [immune-response, memory-and-knowledge]
project_briefs: [memory, regrowth, casefile]
```

This is a metadata example, not a new hypothesis. `focus_areas` uses IDs from the navigation source; `project_briefs` uses the crosswalk's brief IDs. Use only directly relevant tags. The exporter rejects unknown or duplicate tags, retains the recorded status, and never infers acceptance from a topic, survey or project relationship. Hypotheses without tags remain visible in the unfiltered list as having no recorded research tags. Zero formal hypotheses is shown honestly rather than counting exploratory notes or open-PR drafts as registered work.

To contribute a connection, identify the question ID, focus/project ID and a short scientific reason. Update files you own; have the owner review proposed changes to another researcher's mapping or hypothesis. Add a new focus only when existing choices cannot describe a recurring comparison, and include its scope and explicit question members. A narrower focus such as immune response can span existing literature topics without duplicating the library taxonomy. A genuinely new literature topic still follows the append-only, separate-commit rule in `AGENTS.md`.

## Verification

Run the exporter and `dashboard/scripts/test_export.py`; those tests include navigation validation. In `dashboard/`, run `node scripts/test_research_navigation.mjs`, `node scripts/test_question_reviews.mjs`, `npx tsc --noEmit` and `npm run build`. Verify area/project intersections, clear filters, direct links and existing saved review choices in a browser. No credentials are needed for local preview.

