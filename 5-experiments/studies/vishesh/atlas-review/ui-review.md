# Research dashboard and atlas UI review

Browser inspection on 2026-10-03 by vishesh/codex-methods. These findings concern the research UI and review workflow, not the private AgentOps hub or live experiment status.

The canonical [research dashboard](https://swarm-research.pages.dev/#/topics) was inspected in the browser after the final repository refresh. Its Topics page displayed 15 areas and footer commit `3564b3695cd333076cd2d51200dda1f00921951a`; the Questions route exposes the current atlas. The earlier `swarm-lab.pages.dev` address presented an access-login page. A local build of the earlier `dashboard-v1` snapshot was also inspected and passed its build with a bundle-size warning. This review does not infer live experiment state from either research snapshot.

The final review targets the 214-card Update 2 on main `25a7575`. The standalone UI first imported the initial 143 comments. After reconciliation, the canonical hosted Questions page successfully imported all 214 comments, displayed eight shortlisted candidates, and rendered the BUD-03 comment with the selected Discuss status. The final import carries a current fingerprint for every reviewed candidate.
## Findings and concrete improvements

| Priority | Observed behavior or source evidence | Consequence | Suggested acceptance check |
| --- | --- | --- | --- |
| High | Topic cards label a count “read in full”; the count includes `read_depth === 'full'` or `'ran'`. | Running code and reading a paper are different evidence claims. Readers may also mistake inherited catalogue depth for fresh reviewer verification. | Show separate full-paper and code-run counts; state that these are contributor-reported catalogue metadata. A ran-only code item must not increment full-paper count. |
| High | Dashboard data exposes a source commit that differs from the final main checkout reviewed here. | A fresh-looking page can still omit new surveys and context. | Keep export commit/time visible near the research-area list and expose the source snapshot on each linked review. Do not label it live unless data is actually refreshed. |
| Medium | Topics use source counts and a small relevance/depth/year-ranked list. Recent high-relevance LLM/security entries can dominate classical-area previews. | Volume and recency can crowd out foundational work, negative results and direct baselines. | Add explicit slots or filters for seminal work, nearest implementation, contradictory evidence and tools. Preserve the full searchable catalogue. |
| Medium | Update 2 resolves the earlier 14-versus-15-area mismatch and adds 22 budget cards. | Connections to the original project briefs still benefit from explicit reviewer context. | Link a dated coverage map such as [area-context.md](area-context.md) and the structured crosswalk; expose the snapshot each mapping covers. |
| Medium | Atlas review import merges by candidate ID and replaces existing entries for overlapping IDs; it does not restore the imported reviewer name. | A user can unintentionally replace their own local decisions or export imported comments under another name. | Show a preview with incoming reviewer, overlap count and source-hash match; offer a separate reviewer namespace or explicit replacement. Until then, export first and set reviewer manually. |
| Low | Topic counts derive from overlapping tags. | Summing areas overstates the distinct library size. | Label counts as tagged entries and show a distinct total separately. |

## What works already

The atlas includes candidate IDs, explicit baselines, falsifiers, confounds and prior links; these make a targeted review possible. Its import/export format lets a researcher contribute comments without changing the original author's cards. The dashboard displays phase gates and snapshot metadata. Keep those affordances while clarifying evidence depth and freshness.

This contribution supplies an importable review and linked context in owned notes. It preserves Dan's canonical cards. Publishing Markdown does not automatically add reviewer comments to the dashboard's data or local browser state. The canonical publication is the repository contribution; dashboard integration can consume the supplied JSON or link the synthesis entry.
