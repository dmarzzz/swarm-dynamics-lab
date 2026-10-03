# Deploy

Canonical: **https://swarm-research.pages.dev** (Cloudflare Pages project `swarm-research`, dmarz's CF account).

- `.github/workflows/dashboard.yml` runs on every push to `main` touching research dirs or `dashboard/`, plus every 15 min and on manual dispatch.
- Steps: `scripts/export.py` (repo -> `public/data/*.json`) -> `scripts/test_export.py` (data contract) -> `vite build` -> `wrangler pages deploy`.
- Push to `main` = production. Any other branch that runs the workflow gets a preview at `<branch>.swarm-research.pages.dev`.
- Secrets: `CF_SWARM_API_TOKEN`, `CF_SWARM_ACCOUNT_ID` (repo secrets).
- Look and type match swarm-live (https://swarm-live.pages.dev): void #040306, hue 274 accent, Space Mono body, Doto 900 for brand/headlines/big numbers. Fonts vendored in `public/fonts/`.

Old preview `dashboard-v1.swarm-lab-c3n.pages.dev` (Shadow's CF) is retired.
