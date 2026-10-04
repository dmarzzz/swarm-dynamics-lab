# Post-mortem: local-s0-001

Experiment sybil-specialists-api / dmarz/sybil-specialists / S0 / 2026-10-04 UTC. Parent: original scripted fleet-s1-001. Disposition: advance to fleet S0, then clean API qualification.

## What ran and what happened

216 planned → started → terminal → graded → analyzed scripted records; zero invalid, duplicate or missing records. Zero model calls, tokens and API spend. Six clean world clusters yielded 24/24 exact packets, 100% field accuracy and missing-field abstention. Twelve attack clusters yielded all 192 assigned policy/reliability/badge cells. The scripted badge difference is exactly zero, as required; the solver ignores that field. All saved evaluations recompute exactly from frozen assignment packets and evaluator-only truth. See results/local-s0-001/analysis.json for the full local check.

Runtime fingerprint 12ff89f2f54322f07245640708a0c243ad09ab8d933163e71869c3ce08255f6a. The local rehearsal began while automatic sync was completing, so its HEAD field 2b8dc073729f14799a56b33c8208d2df7a78e79e predates the runtime commit. This is an offline provenance limitation: fingerprint identifies the exact code, no paid calls ran, and the forthcoming fleet rehearsal must use a fully committed pinned revision. The source/configuration is unchanged; the fleet gate will establish clean committed provenance before API use.

## Visualization review

Mapping v1 produced 1800×1180 initial/final PNG and 28 GIF frames. Final image was visually inspected: labels fit, four policy panels share 0–100% axes, baseline bars match scripted values, coverage losses at high attacker pass are visible. Every prefix is derived from saved rows; the scripted-only controls make the completed count exceed attack-panel counts by 24, explained in mapping. Failure/pending rendering and two-frame failure replay passed the offline tests. Browser embedding remains to check on fleet publication.

## Experiment-quality assessment

Instrument qualification passed. Clean competence of the LLM remains unknown. This uses one graph family with simulated checks/reports and is exploratory; no scientific finding about real agents follows from S0. Prior-art gates remain intact. No execution, scoring or budget guard failure was observed. The 12 adapter tests and 15 parent simulator tests pass.

## Failure and repair ledger

| ID | Evidence / cause | Action | Acceptance | Status |
|---|---|---|---|---|
| local-provenance | HEAD captured before sync finished | Pin committed runtime before fleet S0 | All source files tracked and clean, fleet exact-source reconciliation before Q0 | pending fleet check |

## Next run

fleet-s0-001 repeats the full 216-packet rehearsal on freshly exclusively claimed sim-dmarz-4. Claim dmarz-sybil-specialists-api merged via agentops PR44; expiry recorded in deployment record. One worker, zero calls/spend, 30-minute deadline, same runtime fingerprint. If all records, uploads and visuals reconcile, proceed to Q0's 24 fresh paid calls; the aggregate USD 5 cap covers all paid stages and repairs. Formal S2 stays blocked.
