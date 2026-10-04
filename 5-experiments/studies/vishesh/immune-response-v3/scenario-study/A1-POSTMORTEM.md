# Scenario a1 post-mortem

Public run: https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-023612-d2bea8 . All 12 assignments and 108 model calls recorded; zero response-contract/provider failures, no missing usage, actual cost USD 0.169049. Qualification failed because the initially healthy false_alarm case regressed in all three arms. This is not an infrastructure outage.

| Case | Retain healthy ticks | Reset | Revision check |
|---|---:|---:|---:|
| Stale advice | 3/6 | 6/6 | 6/6 |
| Migrated data | 5/6 | 5/6 | 5/6 |
| False alarm | 0/6 | 3/6 | 0/6 |
| Registry partition | 3/6 | 6/6 | 6/6 |

In false_alarm, retain downgraded a healthy gateway and then repeatedly attempted a rejected store upgrade; reset also attempted unsafe format changes; revision_check falsely described worker 3 as a bridge reader and ended by asserting all checks passed while data_readable remained false. The advisors already conflated RPC, feature and format requirements before the commander's first action. These are concrete factual/decision errors in recorded outputs, not access to internal reasoning.

The pilot cannot support a clean memory-repair effect while basic competence is inadequate. A2 corrects presentation ambiguity and a leading advisory instruction prospectively, with the same health constraints and equal information across arms. It does not alter or remove these failures. New seeds are presentation identifiers, not independent scenario replications. No population effect, autonomous detection, or benefit from using multiple agents is established.
