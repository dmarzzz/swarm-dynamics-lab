# Immune Response — A9 grounding/advice comparison

Retrospective owning-agent assessment,2026-10-04. [Run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-201636-f87eec). Runtime `22a9ad758ede5cfbeaa70f34bc30490038b9e510`; [prospective plan](../GROUNDING-PLAN.md), [reconciliation](a9-reconciliation.json), [rubric](a9-quality.json), [native figure](a9-final.png), [animation](a9-replay.gif).

## Result and decision

**The selected erroneous advice worsened healthy-service outcomes; adding the deterministic grounding table did not prevent it. No condition repaired the crashed worker.** All24calls and12trajectories completed with valid action decoding, full usage and no retries. This is a completed negative/native comparison, not an infrastructure failure. Four trajectories passed capability gates, but no condition passed all three roots.

| Condition | Gates passed /3 | Healthy ticks /6 | Healthy episodes damaged /2 | Useful restarts |
|---|---:|---:|---:|---:|
| Plain controller, no advice | 2 | 4 | 0 | 0 |
| Plain controller, saved advice | 0 | 1 | 2 | 0 |
| Grounded controller, no advice | 2 | 4 | 0 | 0 |
| Grounded controller, saved advice | 0 | 1 | 2 | 0 |

Within each grounding level, adding advice changed healthy ticks by-2 for healthy_fresh,0 for fresh_crash,and-1 for stale_false_alarm. Grounding's corresponding health differences were0in all three worlds at both advice levels; the descriptive interaction on healthy ticks is0. These counts are over three inspected roots, not12independent replications or population effect estimates. Advice was deliberately selected from A8 errors; conclusions concern susceptibility to those exact messages, not typical advice quality or the value of all multi-agent systems. Condition order was fixed and rotated, not randomized across repeated trials.

A9 answers the narrow discriminator. Prefer the simpler controller-only candidate for further development because it preserved both healthy cases here at lower cost. Do not advance any condition to the larger immune-response comparison: even the simpler architecture failed the required crash recovery. Grounding-as-extra-text is not an effective protection demonstrated by this study. No automatic repeat or model escalation.

## Every native answer reviewed

All24effective requests and returned action-ID/reason pairs were inspected, including the exact advice and grounding available at each tick. All source observations, evidence tables, decoded actions and state transitions were replayed independently from saved data. The grounding table exactly matches visible catalog comparisons; no hidden simulator state entered the actor. All ten legal actions remained available across conditions, so a verifier did not silently rescue outcomes.

Healthy_fresh: both solo conditions avoided mutation and retained health, though they redundantly inspected or refreshed. Both advice conditions downgraded gateway1 immediately, breaking RPC compatibility and removing required bulk_checkout, then inspected the damage. Grounded_advice asserted an incompatibility despite the added table marking the existing configuration compatible. Grounded_solo misread the table's scope statement as an instruction to inspect, and its final refresh explanation implied another future tick. These prose defects do not negate the healthy outcome but remain limitations.

Fresh_crash: all four conditions inspected first. Plain_solo and plain_advice then refreshed the registry, incorrectly treating refresh as a way to obtain runtime liveness; the declared tool explicitly provides no new runtime health. Grounded_advice downgraded the healthy gateway based on false RPC/data claims. Grounded_solo returned **deploy worker3 while its explanation concluded that worker2 should be restarted**. It even acknowledged that worker3 cannot read the persisted legacy schema. The engine correctly executed worker3, bringing the process up with an incompatible binary; health remained false. This is an observed action/reason contradiction, not a decoding bug or a useful same-version restart. Score the selected action, not the final prose sentence.

Stale_false_alarm: every condition first inspected and observed current healthy evidence. Both solo conditions then preserved health (grounded_solo waited;plain_solo refreshed). Both advice conditions instead downgraded worker1 and broke RPC compatibility. Grounded_advice explicitly acknowledged that catalog checks were true yet invented a requirement that a worker's broader readable-format capability must be reduced to match storage. Correct evidence appearing in the prompt did not guarantee its use in the decision.

The paired controlled exposure gives more specific evidence about these messages than A8's repeated phrasing alone. Nevertheless,input length also changes with advice and grounding,model responses can vary,and each cell has one rollout. No mediation claim,unseen-scenario reliability or general causal estimate is supported.

## Resource comparison

Six controller calls per condition; no fresh advisor calls. Saved A8 advice costs remain in the original ledger,not charged again or treated as free live advice generation.

| Condition | Input tokens | Output tokens | Known API cost |
|---|---:|---:|---:|
| Plain solo | 7,865 | 470 | USD0.010215 |
| Plain advice | 9,343 | 462 | USD0.011653 |
| Grounded solo | 9,245 | 516 | USD0.011825 |
| Grounded advice | 10,779 | 548 | USD0.013519 |

New actualUSD0.047212; new reservationsUSD0.208748. Cumulative453calls/USD3.700944reserved under originalUSD8,including historical unknowns. Equal calls and output limits did not imply equal token cost. No new machine or budget increase; shared-machine allocated cost is not separately measured.

## Integrity, visualization and closeout

41local/remote tests preceded exact immutable plan registration and dispatch. All24request hashes/usage IDs and response bodies reconcile;12of12assigned trajectories are complete. Full raw transport remains local; nine indexed hub artifacts were fetched and SHA256-matched. The native three-frame GIF shows all four conditions with vertical offsets explicitly labeled as display offsets,not fractional health. Interactive replay exposes catalog,advice,grounding and telemetry beside each actual action. No scripted image substitutes for native evidence.

Worker stopped,local relay exited at24calls,exact SSH tunnel closed,and exclusive claim released after evidence backup. Offline finalize completed with execution outcome completed;model_calls0there means no additional calls from finalization. This report and the eleven-dimension rubric provide the authored scientific assessment. Qualification failure is preserved separately from successful execution and reporting.

## Further work, if desired

The next useful work is offline crash-action diagnosis and a strict separation between proposed action and factual justification. Candidate repairs include an explicit tool-effect table emphasizing that registry refresh cannot measure runtime health,and a checked repair proposal that identifies the failed component/current binary before execution. A hard action filter would change the architecture and must be declared as a new treatment rather than credited to model reasoning. Keep a controller-only baseline and retain this negative grounding result. Any successor needs its own concrete plan and owner decision; this run supplies no authority to continue until a favorable result appears.
