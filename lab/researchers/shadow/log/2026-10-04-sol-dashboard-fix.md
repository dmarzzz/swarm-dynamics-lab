# Dashboard Actions repair

Direct owner request: diagnose failing dashboard Actions and restore the existing Cloudflare Pages deployment. Work is isolated from the dirty canonical checkout. No persistent sync timer was started for this bounded repair; only explicitly staged repair files are pushed.

Failed run: https://github.com/dmarzzz/swarm-lab/actions/runs/37241938230

The Export repository data step failed in `build_navigation` with `unknown or duplicate hypothesis topic`. Three Shadow-owned proposed hypotheses used free-form descriptors as canonical topic slugs. Preserve those descriptors in `keywords` and tag each with the existing `llm-agent-swarms` topic. No claim, hypothesis status, research approval or experiment file changes.

Keep strict unknown/duplicate reference rejection. Generator errors now identify the hypothesis path and invalid values. Regression tests cover unknown and duplicate topics, preserved keywords, and unchanged proposed status. Document the topic/keyword distinction in the dashboard contract.

Local validation: export completed for 3,319 library entries; all 31 Python contract tests, research-navigation checks, all 11 question-review tests, TypeScript checking and production build passed. Repository check passed with 0 errors and 5 pre-existing missing-library-link warnings. Production deployment remains delegated to the unchanged dashboard workflow and existing secrets.
