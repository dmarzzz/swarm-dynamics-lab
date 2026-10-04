# Operator handoff

**Launch hold (PI review follow-up):** the legacy execution boundary is disabled in the accompanying containment patch, pending janitor review/merge. It lacks the full required registration, per-transport reservation, initialization-receipt and immutable-outcome contract. Do not use the historical resume commands below or refresh old source pins. Read [PI review response](PI-REVIEW-RESPONSE.md). Analysis of saved data is unaffected.

Tool shipped. Scientific queue **blocked on provider availability**, not completed. No factory process is still making model calls at this handoff.

- Anthropic pool: initial8 HTTP429 +12 HTTP503, then native-schema recovery4 HTTP503. No pool credential, account or quota changed.
- OpenRouter: key metadata reports a shared **USD5 daily limit, zero remaining**. This is below the authorized factoryUSD20 ceiling. Paid requests stopped at403. No limit or credential changed.
-100 valid structured answers:12 exact clean controls and88 comparison cells; only2 complete paired roots. Report **lead**, not finding. Bounds cross zero broadly. All52 failures retained; see CORRECTIONS.md and verification.json.
- Frozen original scientific seed: five questions,48 reused roots each. Operational repair variants are **not extra scientific replications**.
- Main script options after an authorized operator restores a route: `pool_structured.py queue` for native structured pool, or `structured.py queue` for already preregistered paid structured specs. Both skip terminal cohorts and execute only unstarted specs with their own fresh qualification. Do not delete terminal.json or edit old specs to rerun failed outcomes. A repair/top-up of an interrupted cohort needs a new prospective spec and explicit missing-outcome accounting.
- Native root-first dispatcher preserves complete paired units if interrupted. The older paid dispatcher shuffled individual cells, which caused poor paired coverage in the interrupted run. Do not combine its partial cells with another cohort without an explicit prospective analysis amendment.
- Paid cap applies across **all** attempts through results/paid-ledger.jsonl:USD1.189149 settled,USD0.617820 still reserved,USD1.806969 accounted. Keep that file when moving execution; never start a fresh ledger to reset the cap.
- Hard deadline is compiled as22:00Z Oct4, no CLI override. All requests have90s timeout. Native429 retries are bounded, logged and respect Retry-After; no answer retry or credential rotation.

## Final recomputation and closeout

```sh
python3 researchers/shadow/factory/verify.py
python3 researchers/shadow/factory/report.py
python3 researchers/shadow/factory/closeout.py evidence
bash researchers/shadow/factory/hub.sh hub
python3 scripts/lab.py check
```

The local hub helper sources `/tmp/hub_env.sh`; other operators supply their own authorized hub environment and `SWARM_REPORT_PATH`. It never commits secrets. Hub terminal receipts include a server readback, not just a locally spooled report.

## Artifact registration caveat

The diagnostic SVG is working material, not a Flight Deck registered submission figure. `fd.py add` produced the new figure, but also regenerated many other owners' attestations/lock entries because inputs are absent in this worktree. Those unrelated generated changes were fully restored, and our attempted artifact was moved to git-ignored `data/factory-flightdeck-staging/`. Global `fd.py check --strict .` reports four pre-existing missing film files and the worktree-directory/project-id mismatch. Do not publish bulk attestation rewrites to force our small figure through; register from a complete canonical artifact checkout if this figure is used externally.

Avoid git rebase/autostash while tracked ledgers are actively being appended. Finish/pause safely at a cohort boundary, or execute in a fixed separate runtime checkout and copy snapshots for publication. Registry merge conflicts must retain other researchers' rows and regenerate only our entries; never choose our entire old registry over a newer team registry.
