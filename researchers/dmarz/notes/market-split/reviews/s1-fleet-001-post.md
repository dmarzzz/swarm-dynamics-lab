# Post-mortem s1-fleet-001

- Owner/stage/date: dmarz / exploratory scripted S1 / 2026-10-04.
- Parent: s0-fleet-001; pre-run: s1-fleet-001-pre.md.
- Disposition: scripted environment qualified; do not start model calls or S2.

## Reconciliation and execution

Twelve planned → assigned → completed → verified simulation runs, each with 36 unique episodes: 432/432 valid outcomes from six development market clusters and two seeds. No missing, duplicated or retried episodes. Each trace contains all 24 rounds. Model calls/tokens/API cost: 0/0/$0. One finite worker exited successfully after all 12 runs; no experiment worker remains polling. The aggregate analysis is a separate reporting run, not an extra simulation or independent replicate.

Source commit: 6ca3f16ef9f3a0dbad0ed280c032e78e31195dc3. Engine SHA-256: 8abdfb4e59787213c4518f662af3976a2af31f11904ead4582afd51a3f260312. Design SHA-256: fd5aac6f164ec61a0145245a1277ffc025670de250aebcc4a9eed1d447a29263. These match the qualified S0 engine/design; documentation-only source commits differ. Run IDs, parameters, metrics and artifact hashes are in analysis/s1-reconciliation.json; raw rows are retained in the hub and ignored local recovery copies.

## Findings and limitations

At threshold 0.38 and fee 20, forced splitting gains a paired mean 15450.50 credits versus a one-firm baseline (six-cluster bootstrap 95% interval 14305.20–16623.23). Under owner aggregation or no regulator it loses exactly 163 credits, the registration and incremental overhead costs. Production and owner resources are unchanged. The regulator-independent fragmentation measure appropriately counts programmed fragmentation in control conditions too; successful regulatory evasion is a separate endpoint.

The high-fee manipulation is weaker than a categorical deterrence claim: forced splitting still has positive mean benefit under firm regulation over 24 rounds. The four-round-amortization search policy fragments in only 2/12 high-fee episodes at threshold 0.38 and 0/12 at 0.46, compared with 12/12 and 10/12 at low fees. This is a horizon-dependent scripted choice. Keep all outcomes; do not tune fees after seeing these results and present the revised condition as preregistered. Profit search can also improve production under owner regulation without splitting. Its total profit gain is not all an identity effect.

There is no evidence here about an LLM's spontaneous discovery, competence, intent or communication. The environment uses scripted rivals and a perfect owner-aggregation oracle. It is an exploratory engineering sandbox rather than a replication or a confirmatory scientific experiment.

## Visualization and artifact acceptance

Mapping market-split-v1. Every S1 run contains progress PNG, final PNG, 24-frame replay, raw JSONL, summary, and an empty visualization-errors file. All 72 artifact SHA-256 values match the actual files. Final frames are 1800×1200; GIFs are 1080×720. The selection is fixed at task 10 / seed 21; the other 33 episodes per cell are retained in raw data. The published representative run is market-split/c473a1f2. Browser playback and the recorded registration/HHI/finance traces agree. No renderer errors or dropped rounds occurred. S0 plus S1 account for 90 verified simulation uploads.

## Next attempt and operational close

Keep model API budget zero. A future model attempt needs a frozen model/version and neutral prompt, prices and token/call/dollar caps, implemented transport, a network-mocked transport test, and model S0 schema/profit competence checks before discovery S1. Discovery S1 compares firm versus owner rules and a locked-one-firm control at equal owner inference budget; hinted controls remain separately labeled. Full S2 additionally requires the prior-art gate and independent hypothesis review.

The scripted results are accepted without another experimental rerun. Preserve hub uploads and local recovery copies, release the claim, and destroy the temporary host. Final teardown evidence is in deployment.md.
