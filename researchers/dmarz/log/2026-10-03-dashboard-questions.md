# Dashboard Questions integration

The human asked to add the question bank to the website and explicitly hesitated about deployment because Shadow had deployed the supplied URL. Work is isolated on `codex/dashboard-question-atlas` and draft PR https://github.com/dmarzzz/swarm-lab/pull/81. This overrides AGENTS.md's default direct-to-main workflow: a main push touching dashboard files would publish automatically. No deployment workflow was dispatched and neither deployment branch was pushed.

Deployment inspection found that dashboard/DEPLOY.md identifies `swarm-research.pages.dev` as the canonical project on dmarz's account. The supplied `dashboard-v1.swarm-lab-c3n.pages.dev` is documented as Shadow's retired preview. The current workflow deploys on qualifying pushes to main/dashboard-v1, every 15 minutes from the default branch, or manual dispatch; it has no pull_request trigger. Ownership is documented in the repository, not independently verified through Cloudflare secrets or account settings.

Added an independently loaded Questions view with 202 canonical candidates across 15 areas, complete test details, search, six discovery/review filters, stable candidate URLs, catalogue drill-down and source links. Added local decisions/notes with legacy-compatible import/export and explicit acknowledgement of revised candidates. Formal hypothesis and experiment counts are unchanged. The data export preserves every canonical field and both fingerprint layers.

Validation: 12 Python export/contract tests and 11 focused review test groups pass. Strict TypeScript and production build pass (existing large-main-chunk advisory remains). Browser checks cover 59 new and 36 revised candidates, the 22 budget questions, a stable BUD-01 link, notes/choice persistence after reload, source drawer navigation, legacy import, malformed import rejection, stale-note editing and explicit recheck acknowledgement. Downloaded review JSON contains both fixture reviews and preserves the legacy missing fingerprint. Desktop and 390px mobile layouts have no horizontal overflow; mobile selection scrolls to the detail. The final production preview reports no browser warnings/errors. Test notes/decisions were cleared through the UI.

Peer review caught and fixed async import overwriting intervening edits, import success hiding a failed-storage warning, and malformed imported text fields silently losing content. Browser inspection caught and fixed the hidden file input creating horizontal overflow.

Repository check: 0 errors, 5 existing missing-source link warnings. Flight Deck strict check: 4 artifacts, 0 errors and 0 warnings. Unrelated generated dashboard data was restored; only the new generated questions payload accompanies the exporter. The production preview was built using fresh exports.

Next action belongs to the human: review the local preview or draft PR and decide whether to publish to the canonical team site. Do not merge until the deployment hold is lifted.

## Publication authorized

The human subsequently said “just merge it.” This explicitly lifts the deployment hold. Proceed with PR 81 into main and verify the automatic deployment to the canonical team site.
