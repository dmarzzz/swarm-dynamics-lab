# Post-mortem: Theseus v2 S0-repair

Experiment swarm-of-theseus-v2, vishesh/codex-theseus, 2026-10-04 UTC. Source095534bfab16085ac6f4032cd5137cf1e2c7b875; plan hash7cd472518a76eb901598852847a004c23e8d39836cd9c6523f96284021af4110. ParentS0. Pre-run assessment S0-repair-pre.md. Disposition: **blocked for S1; planned repair limit reached**. Execution complete is separate from qualification failure.

## What ran

12 assigned →12 started →12 complete runs;24 assigned →24 completed →24 scored calls;144/144 case decisions observed. Zero provider or schema failures, no duplicate attempts, no audit discrepancies, all usage recorded. Calls spanned40.18 seconds. Estimated actual cost USD 0.061956,28,181 input and6,755 output tokens; conservative reservation USD 0.210741. Across both attempts:48 calls,USD 0.165211 actual estimated,USD 0.568098 conservatively reserved. No pilot calls. The central USD 15 allocation and local deadline were never reset.

| Scenario | Ceiling stable | Ceiling changed/interface | Learner stable | Learner changed/interface | Individual qualification |
|---|---:|---:|---:|---:|---|
| Release | 9/12 (75.0%) | 11/12 (91.7%) | 8/12 (66.7%) | 6/12 (50.0%) | Fail |
| Incident | 11/12 (91.7%) | 11/12 (91.7%) | 12/12 (100%) | 7/12 (58.3%) | Pass |
| Migration | 8/12 (66.7%) | 9/12 (75.0%) | 9/12 (75.0%) | 10/12 (83.3%) | Fail |

Gate unchanged: all scenario/checkpoint ceiling cells >=0.90 and each stable learner >=0.75, valid output throughout. Incident passes locally, but the prespecified joint gate fails. Selecting incident for the originally blocked pilot now would change scope after observing qualification. No such post-hoc escalation occurred. Changed learner accuracy is descriptive; low values there are not capability-gate failures.

## Quality and diagnosis

The compact representation and clean ceiling did not solve action application across all scenarios. In release302 stable ceiling, the recorded rule maps classB to ledger; B:0 has ledger signal=YES and fresh=YES. The model nevertheless returned hold while its notebook itself acknowledged YES/YES. Migration302 stable similarly holds A:0 despite the designated canary source being true/fresh. This establishes wrong application in saved outputs, not the model's internal cause.

Hypotheses still open: batched row binding, source/column binding, conjunction application, and note-writing interfering with decisions. Dense nested JSON alone is not an adequate explanation because errors remain under compact tables with no history in the ceiling. The repair also specified the rule family and used new worlds; before/after scores are not a randomized effect of formatting. No evidence about culture surviving replacement was collected, because turnover never began.

## Failure ledger

| ID | Evidence and status | Next acceptance check |
|---|---|---|
| C1 current-rule execution | Release/migration ceilings fail after repair; unresolved | Prespecified clean atomic and batched controls on fresh worlds before any continuity run |
| C2 mapping acquisition | Incident stable learner12/12; release8/12; task-specific | Diagnose acquisition separately from applying a known mapping |
| P1 publication provenance | Four invalid harness enum fields corrected, bytes/digests/session preserved | Full jsonschema-enabled strict check passes; closed |
| E1 evaluator mismatch | None in either attempt | Same-author raw-response recomputation matches48 events; closed for observed traces |
| V1 qualification clock | Initial generic crew labels misleading for a one-reader stage | Repaired checkpoint labels; qualification-specific final evidence browser delivered |

## Visualization review

Both attempts retain measured progress, every event and their raw replay/1800px frame. Qualification is two checkpoints, not a ten-step turnover trajectory; the final qualification viewer uses stable/changed selectors and explicitly says that no turnover pilot ran. It shows actual case evidence, command, semantic action and evaluator truth, so false extra caution is visible. No scripted fixture is substituted for model outputs. Current evaluator truth is viewer-only and never added to learner prompts.

## Next action

Stop paid dispatch under this plan and release the exclusive host after evidence upload verification. Preserve the rejected attempts and unopened400/401 pilot. Draft a separate future diagnostic that crosses atomic versus batched application and decision-only versus note-writing; consider a separately qualified model only after freezing its pricing/budget and new plan. An incident-only study is a possible prospective successor, explicitly selected using qualification data, not a rescue of the original joint test. No additional launch is authorized by this post-mortem and no threshold was relaxed.

Evidence bundle SHA256 c96cd6876c1f9e1826be5b1a33953f64f4830365d4bc5a0247b3a2d45022dcf0. Full events, exact rendered user text, provider outputs, usage and public receipts are retained in the local evidence package. Same-author audit remains distinct from independent researcher review.
