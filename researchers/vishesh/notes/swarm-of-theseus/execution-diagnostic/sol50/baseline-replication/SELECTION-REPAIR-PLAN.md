# Selection/writeback repair: prospective bounded diagnostic

Written after the Q3-A2 failure and before repair implementation. No new native authority is implied. Preserve Q3-A2 source074eff22,69nativecalls and all original outcomes. P1 remains unstarted because its qualification condition failed; no gate relaxation or paid retry is permitted by this document.

TLDR: Test one authoritative model-selected pair used for routing and private writeback,against exact history/controller reference,on three inspected changed/preserved contexts. Require3/3correctpairs,18/18decisions,0harm,6calls≤USD0.15all-in. Scripted witnessdelivery,not fullnativequalification or independentreplication.

## Observed bottleneck

Both release/failover founders acquired6/6policies and initial decisions were36/36each. Both direct handovers passed. Release terminal12/12;failover preserved successor6/6 but updated incumbent3/6. The updated incumbent's selection named the correct new pair while its separate note retained the old pair. Transport faithfully persisted that note and delivered exactly the selected records. All six later answers were defer;three were wrong(two legitimate approvals and one requiredhold),with no harmful approvals. All69requests/results replay exactly. This is an observed action/writeback inconsistency under a redundant two-field interface,not evidence of handover failure or an established transport/scorer bug. The prompt did not explicitly state the equality invariant,which limits attributing this solely to agent competence.

## Proposed contract

Return one authoritative model-selected pair from the select phase. Persist the exact chosen pair as the local note and route to that pair. Do not infer a replacement from gold/history,repair a wrongpair,or alter old outcomes. The private policy note is still inherited and updated by model choice; the interface merely removes duplicate serialization of the same intended state. Keep owner inputs,phase count,model,provider,scenario labels and acceptance thresholds unchanged. An adapter may derive the old engine's internal note representation from the sole returned pair,with provenance explicitly recorded; the native trace retains the actual single-field answer.

Offline checks must demonstrate:(1) correct and wrong choices are both persisted identically;(2) no gold data is required by adapter;(3) extra/divergent output fields are rejected;(4) exact route and wire bounds unchanged;(5) the archived selection would persist its correct chosenpair under the proposed new mapping,without relabeling the archived decision result;(6) old and changed controller predictions on the saved evidence explain the downstream difference. Record the last result as a counterfactual software calculation,not a new native response.

## Smallest useful native diagnostic: D1

Propose three inspected qualification contexts:the failed changed failover incumbent,the unchanged failover successor,and the changed release incumbent. For each,one new selection under the single-field contract and one new decision after persisting that exact choice. Deliver raw records only from the actually selected witnesses using deterministic addressed transport;no model witness-copy calls. This isolates selection/writeback/decision readiness and is explicitly narrower than Q3's full native consultation contract.

Six requests maximum,USD0.1359API at existing bounds,existingexclusiveapprovedhost≤10minutes/hosting≤USD0.011905 at current tariff,proposedall-in≤USD0.15. Require3/3correct native pairchoices and18/18correct decisions,0harm,complete usage,no retry/fallback. Structural selection/note equality is guaranteed by design and is not counted as learned competence. Stop on an invalid response/transport failure;retain every started result and unstarteddependency. These reused development contexts are not an independent sample or holdout. Frozen P1/P2 inputs remain untouched.

A D1pass would establish only this local selector/decision contract. Full three-familyQ3qualification with native witnesses and handover must then be rerun as a separately named/source-bound approvedattempt before conditionalP1. A D1failure remains a failure;do not keep rerolling it. The actual PI decision must bind the new diagnostic and any amended conditionalqualification/main scope within the original cumulative ledger. No current unused grant becomes fresh money by renaming stages. Native dispatch still respects any approved deadline and observedlatency; no P2authority.
