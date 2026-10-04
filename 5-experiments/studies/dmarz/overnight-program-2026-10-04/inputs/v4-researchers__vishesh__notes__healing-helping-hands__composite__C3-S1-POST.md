# C3-S1 post-mortem

2026-10-04 UTC. Verdict: **complete_valid_result**. Execution and qualification passed; the scientific result is adverse to incremental composite benefit and peer superiority. This completes the owner-approved C3 cycle. No further inference is proposed or dispatched.

## TLDR

Can 200 curators repair a shared evidence index after reports change, and does Qwen 0.6B plus Jev improve on Jev alone? We completed 600 paired reports and all 270 programmed worlds. Qwen scored 522/600 (87%); Jev and Qwen+Jev each scored 600/600. Jev corrected 78 Qwen errors without damaging a correct answer, but the composite supplied no incremental accuracy or downstream benefit. Verified central indexing had lower mean post-event error than verified peer propagation in every scenario. Verification resisted false withdrawals; missing lineage remained unresolved.

## Execution and transport

Frozen scientific source `b2a09a420dbfc42f8334543f495a815e9818be73`; prospective S1 admission published in `8de1578f020db9593fbf44dd4c7b808badbe5438` before dispatch. Exclusive existing `sim-dmarz-7` allocation, approved Dmarz account identity checked privately. Worker-local relay plus detached systemd supervision replaced the laptop reverse tunnel. Atomic response caching and usage commits allow read-only response recovery without resending an ambiguous provider request. All 1,800 model calls had terminal responses; zero transport failures, missing reports or skipped worlds. S1 took 1,195.2073 seconds. This establishes one complete healthy native run, not universal failure immunity. C1/C2 failed attempts remain intact.

## Design and measurements

Three fresh synthetic corpora (8821–8823), three extraction arms, five policies, six scenarios, one fixed placement per corpus: 270 worlds, 200 logical curators per world, 30 rounds each. Extraction is measured once and paired across programmed architectures. These are not 270 independent samples or 200 autonomous model calls per round. Repeated templates and only three corpora support descriptive comparisons; corpus ranges are not confidence intervals. Actors receive stateless report context, not evaluator truth or the operating assistant's conversation.

Same-author replay audit reconstructed request hashes, labels, all 270 world results and 8,100 saved frames. It reconciled 1,800 starts and terminal records, 609,044 input and 59,960 output tokens. It is not an independent researcher review. Composite-minus-Jev contrasts are exactly zero for all corpora and scenarios.

| Scenario | Central verified mean error | Peer verified mean error |
|---|---:|---:|
| Benign | 0% | 10.43% |
| Withdrawal | 0% | 21.78% |
| Forged notice | 0% | 10.43% |
| Missing lineage | 33.33% | 39.90% |
| Central outage | 20.75% | 21.78% |
| Combined | 20.75% | 21.78% |

These Jev/composite values average wrong-or-missing queries over rounds 10–29. In the combined scenario, central verified ends with zero error and no stale citations; peer verified ends at 0.167% error and 0.760% stale citations. Both retain all new evidence by the final round. Central traffic is 50,040 item copies versus 87,776.33 for peers. Central bulk access and capped mesh transport are unequal resource mechanisms; logical rounds do not establish real deployment latency or cost superiority.

## Cost, reproducibility and visual evidence

S1 API cost USD 0.022871604; C3 qualification plus full run USD 0.025212768. Original cumulative completed API cost USD 0.040890822 plus preserved C1 uncertain exposure USD 0.001344 leaves USD 0.057765178 under the original USD 0.10 cap. All 859 historical reservations were unchanged; 2,179 total reservations consume the predeclared request envelope. Remote ledger dispatch was disabled and the original local ledger authority restored. No new VM was created; existing fleet capacity was used. API figures are not a total fleet-billing estimate.

Frozen model/runtime identities, prompts, actual calls, corpora and frames are preserved. Hosted-model responses cannot be regenerated from seeds alone; saved-data replay is exact. [Full audit](results/C3-S1/replay-audit.json), [paired effects](results/C3-S1/effects.json), [budget reconciliation](results/C3-S1/ledger-reconciliation.json), [quality assessment](results/C3-S1/scientific-post-mortem.json).

[Interactive replay](https://swarm-live.pages.dev/api/a/healing-helping-hands/C3-S1/replay.html) · [All-scenario chart](https://swarm-live.pages.dev/api/a/healing-helping-hands/C3-S1/outcomes.png) · [Measured animation](https://swarm-live.pages.dev/api/a/healing-helping-hands/C3-S1/recovery.gif) · [Raw evidence archive](https://swarm-live.pages.dev/api/a/healing-helping-hands/C3-S1/healing-c3-evidence.tar.gz).

Visuals use the saved frames and all scenarios, with visible adverse controls. Interactive replay inspected at rounds 0, 10, 20 and 29, with corpus/model/scenario controls; a misleading universal outage-restoration caption was corrected in presentation only. Scientific execution was unchanged. Future real-world relevance would require separately approved, held-out natural reports, more independent task families and an equal-resource replicated central baseline; this completed negative result does not justify another run to seek a favorable effect.

Operational finalize hook completed with zero model calls; handoff SHA256 `e1734543ccb8c0aada72b82e0862a237b672c8ddb3843abccd26b7e4b5178827`. The separate scientific assessment above and its eleven-dimension JSON complete the review; the generated operational scaffold alone is not the scientific review.
