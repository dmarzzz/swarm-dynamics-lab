# Post-mortem: receipt-native-a2 — stopped for wrong cloud account

- Experiment / owner / date: Immune Response, vishesh/codex-immune, 2026-10-04 UTC.
- Pre-run: [receipt-a2-pre.md](receipt-a2-pre.md); runtime `d38cd4397fdc2132ac5be7e9f40b6fa8577f3f93`, pinned Haiku 4.5.
- Run: [1004-034657-73913b](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-034657-73913b).
- Disposition: **blocked — cloud account boundary correction**. This is an operator interruption, not a completed capability test.

## What ran and what happened

The user identified that sim-immune-response was created in the wrong DigitalOcean account. Investigation confirmed the earlier provisioning helper read the local default doctl credential, used researcher ownership as its owner selector, and checked resource names/actions without verifying the billing account. The checked local account contained this machine but none of the checked Dmarz Swarm Lab hosts. This was the agent's authorization/provisioning error; fleet registration did not make that account correct.

The experiment process group was terminated after verifying its exact worker identity. A follow-up process scan found zero experiment workers. Planned 16 episodes; four commander episodes started, three completed, one partial, twelve unstarted. Six advisory responses and twenty commander decisions were durably recorded. The persistent ledger increased from 240 to 267 reserved calls; the 27th request has no recorded response and is treated as unresolved, not free. No retries or additional requests will be sent on this machine.

Three completed episodes and the partial fourth trace remain in their original order. All assigned-but-incomplete outcomes remain missing; there is no full-grid qualification result and no causal receipt-effect claim. The hub run is failed with an explicit operator-stop reason. Raw manifest, episodes, events and available live frame were uploaded. Local verified archive contains all earlier native outcomes and the persistent SQLite spend ledger, ready for a controlled transfer only after the original authority is fenced.

The USD 8 cap is unchanged. Conservative reserved total is USD 2.059367, including USD 0.244300 for this interrupted attempt. Prior complete attempts' actual cost is USD 0.441259. Exact actual cost of the interrupted attempt is unavailable from the current adapter: it accumulates usage in memory and writes the total only on normal completion. Do not substitute reserved dollars for billed dollars. Persisting per-call usage is a required reporting repair before any resume. Machine charges are separate and continue until deletion; stopping the model worker does not stop DigitalOcean billing.

## Visualization review

Live frames cover only complete episodes and label remaining cells unrecorded. No final full-grid animation or qualification frame is claimed. Initial state and all twenty recorded action frames are retained in events.jsonl, including two ticks of the incomplete fourth episode. Previous complete scientific artifacts remain intact. A terminal interruption notice supersedes the normal final-result deliverable. Resume must not overwrite the failed attempt or omit its partial data.

## Experiment-quality assessment

The paired protocol and offline checks remain useful preparation, but this interrupted selection of cells cannot answer the registered comparison. The cloud-account check was missing from the pre-run gate even though host ownership and exclusivity were checked. Those are separate concepts. Scientific and infrastructure readiness must both pass before execution. Do not reinterpret this stop as poor model performance or merge partial results into a complete fresh cohort without a prospective amendment.

## Failure and repair ledger

| ID / kind | Evidence and verified cause | Repair and acceptance | Status |
|---|---|---|---|
| CLOUD-1 / authorization | Local default credential chosen without approved account match | Explicit Dmarz account/team verification required before create/apply; no implicit default; corrected workspace and shared workflow | Guard documented and old helper fails closed; correct provisioner still needed |
| CLOUD-2 / containment | Wrong-account worker was active | Exact process group stopped; zero workers verified; hub failed; 93-file evidence/budget archive verified locally | Contained; deletion plan prepared, not applied |
| RUN-1 / interruption | 3 complete, 1 partial, 12 unstarted | Preserve all 16 assignments and partial event history; no qualification claim | Preserved |
| COST-1 / durability | Actual-usage accumulator lost on termination | Add durable per-call usage receipts before another native attempt, including unresolved request states | Open; budget reservations are preserved |
| PLAN-1 / documentation | Previous setup failed required headings | Nine current tests include public-plan contract; native a2 passed preflight | Closed by actual dispatch |
| METRIC-1 / design | Any probe regression wrongly treated as customer damage | Separate regressions from healthy-service loss; reference migrated-data path passes with one visible regression | Closed offline; no native robustness claim |

## Next action

Do not relaunch the disputed machine. Correct the cloud account through Dmarz's established authorized provisioning route, verify account/team and state/project before creation, and preserve the same grant and ledger without concurrent authorities. A cleanup plan is restricted to the mistakenly created droplet, its dedicated firewall/root-key registration and generated local inventory; no other cloud resource may change. Deletion awaits explicit approval because it is irreversible. The cloud-account identity and credentials remain private; never ask for a token in chat.

After account correction, finish durable usage/error recording, freeze a new attempt and missing-data policy, and rerun only the justified bounded diagnostic. The existing USD 8 authorization remains the ceiling; moving hosts creates no new budget. The interrupted attempt is not silently replaced.
