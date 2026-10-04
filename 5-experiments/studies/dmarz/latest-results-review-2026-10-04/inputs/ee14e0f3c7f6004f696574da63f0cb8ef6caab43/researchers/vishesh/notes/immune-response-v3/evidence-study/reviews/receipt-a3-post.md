# Immune Response — native A3 post-mortem

Run [1004-075718-66a098](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-075718-66a098), 2026-10-04. Owner/operator: vishesh/codex-immune. [Prospective assessment](receipt-a3-pre.md); runtime `a23f70ca37365fea2df5e688a95eacccdb7e8fb9`. Decision: **completed diagnostic; qualification failed; no automatic rerun or escalation**.

## What happened

All 16 assigned episodes completed with 24 shared reviewer responses and 96 commander decisions: exactly 120 API calls, zero invalid responses and zero missing usage. The instrument ran successfully; the dashboard marks the run failed because its joint capability gate failed. These statuses must remain separate.

| Scenario | Raw healthy ticks | Checked healthy ticks | Interpretation |
|---|---:|---:|---|
| Stale advice, either memory | 6/6 | 6/6 | Repair on first action |
| Registry partition, either memory | 6/6 | 6/6 | Repair on first action |
| Migrated data, either memory | 5/6 | 5/6 | Two-step repair; one probe regression, no loss of already healthy service |
| Healthy false alarm, either memory | 6/6 | 6/6 | Each episode unnecessarily redeployed the current version |

Every one of eight paired healthy-tick differences is zero. All incident-recovery gates pass; all four healthy-preservation gates fail because the prospective rule also requires zero deployments. There was no observed customer-health loss, rejected action or commander probe-claim error. Do not describe the control failure as damage, and do not redefine the gate after seeing it.

The six unique reviewer false booleans occur in the two healthy-control worlds: reviewers claim requested_feature=false despite the visible true probe. Checked receipts correctly identify these contradictions. Commanders nevertheless redeploy the already deployed gateway version. One explicitly recognizes that the current contracts are satisfied, then justifies an idempotent redeployment as confirmation of a hypothetical transient inconsistency. The trace supports unnecessary intervention; it does not prove that the checker caused or prevented it. A transcription check is insufficient evidence of behavioral restraint.

## Evidence and quality assessment

[Audit](../receipt-native-a3/audit.json) recomputes all health frames, reconciles assigned and observed cells, verifies identical paired advice hashes and verifies empty clean-memory traces. [Summary](../receipt-native-a3/summary.json), raw episodes/events, manifest and per-call usage are retained in the verified local archive and the run’s indexed hub artifacts; they are not included in this public publication. Eight paired worlds across four constructed cases and two memory conditions are a bounded diagnostic, not a population sample; 120 calls are not 120 independent units. No unseen graph or production claim is supported. The full [eleven-dimension assessment](receipt-a3-quality.json) includes evidence hashes and separates passes from gaps.

Scenarios show a ceiling for two incident families and a near ceiling for migration. That makes the null receipt comparison unsurprising and limits its practical reach. The informative failure is an abstention decision under contradictory advice on an already healthy service. Additional sampling of this unchanged grid is not justified merely to obtain an effect. A next proposal should first distinguish unnecessary action from customer damage, assess realistic action costs without inventing measured outages, and validate a challenge set where evidence checking could change a necessary decision. This is a recommendation, not an approved new run.

## Cost, infrastructure and process

A3 actual API cost is **USD0.311494**, with 213,844 input and 19,530 output tokens. Durable requests span about 266.4 seconds; visualization/report transport is additional. The original ledger now holds 387 cumulative reservations totaling USD3.179489 under the unchanged USD8 cap. Known actual cost of completed cohorts is USD0.752753; the earlier interrupted cohort's actual cost remains unknown and its exposure remains reserved. Reservations are not billed cost. The temporary machine's posted rate is USD0.03571/hour; infrastructure billing is separate from these model-usage totals.

The dedicated machine's account matched the established Dmarz fleet. Standard provisioning and fourteen offline tests passed. The renewed exclusive claim was merged before launch. The exact immutable public-plan revision and content hash passed immediately before credential transfer. Only the owner-authorized project key traveled through authenticated SSH stdin into process memory; no persistent model-key file was installed.

Orbital-one refused the earlier queue handoff because its mandate covers Dmarz's studies. The owner then explicitly directed this operator to run on our allocation. We closed that queue request before direct dispatch, preserving its history and avoiding duplicate launch. This resolves dispatch for this attempt without expanding the other orchestrator's authority. Researcher review remains waived, not independently passed.

## Visualization and closeout

The data-derived PNG and seven-frame GIF cover all eight case/memory panels from initial state through six action ticks. The artifact index's nine raw-file entries verify by decompression and SHA-256; audited frames match raw events. An interactive HTML replay is retained locally. Visual inspection confirms the paired trajectories overlap. Limitation: healthy lines alone do not expose redundant deployments; read the trace and table above. A future renderer should mark all deployment attempts, including idempotent ones.

The complete raw evidence and final SQLite ledger were retrieved and verified before cleanup. No native worker remained. The standard offline finalize hook wrote an operational post-mortem/handoff, and this document plus the structured rubric supply the owning agent's scientific assessment. Cleanup is restricted to the approved temporary resources; retain historical failure evidence and the cumulative ledger. No further paid attempt is authorized by this post-mortem.
