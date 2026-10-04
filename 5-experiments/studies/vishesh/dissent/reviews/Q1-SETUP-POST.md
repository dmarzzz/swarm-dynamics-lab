# Q1 setup post-mortem: allocation boundary

Q1 model execution did not start. All 42 prospective requests remain unstarted, and the cumulative provider ledger remains at Q0's 18 paid calls / $0.00042966. Source a77e88205a8cd4bb113de84ee42476f2cdc23d74 and 51 software checks passed locally and on the temporary host. Public registration/preflight succeeded; it did not override the subsequently failed allocation check.

## Verified defect

The Q0 provisioning helper read the local default DigitalOcean credential and validated price, researcher ownership, duplicate-resource absence and the resource plan, but **did not verify Dmarz's billing-account identity**. A later exact account fingerprint comparison confirmed the account was the one already identified as the wrong account in the parallel allocation correction. Researcher ownership in the shared fleet is not billing authorization. This was an operator/process failure; the user's cap approval did not authorize changing accounts.

The updated [machine runbook](../../experiment-machine-workflow.md) was read before Q1 dispatch. Further provider calls stopped. The Q0 result remains valid as an observed classification result but the attempt is process-noncompliant for allocation. The Q0 public-plan check did pass. There was no secret exposure in the transcript or public artifacts.

## Containment and verification

All seven Q0 hub artifacts were downloaded and matched against local SHA-256 hashes, including the final image. The public PNG rendered and displayed the recorded 6/6, 3/6, 3/6 and qualification FAIL. Evidence and the original SQLite ledger are backed up in the owner's workspace. The worker had exited, exact /proc inspection showed no remaining worker, relay and SSH tunnel stopped, and claim vishesh-right-dissenter was abandoned through private agentops PR 117 and mirrored to the hub. [Cleanup receipt](../CLEANUP.json) verifies removal of the host and dedicated resources, with all other droplets unchanged.

A reporting update that pinned Q0's historical plan inherited the copied report.env host/source defaults. A corrective event restores the actual source/host. Hub implementation resets terminal ended time on later log events; its displayed duration is consequently inflated. The immutable saved summary retains the measured 8.35-second worker time, and the run message explicitly identifies that discrepancy. This reporting issue changes no decisions or costs.

## Remaining blocker and next action

Blocked on a verified Dmarz-account provisioner or newly dedicated authorized host. All current eligible Dmarz fleet simulation hosts have active claims (the research host's old expired claim cannot establish idleness). Do not take an occupied host or use the local default account again. The create helper now refuses default-credential provisioning.

Rebind Q1 to the approved allocation, current expiry and verified account receipt; revalidate frozen source and public plan; launch exactly the prospective paired diagnostic. The $2 cap remains approved and the original ledger must be reused. No additional cap confirmation is needed. Q1's competence gate, its post-mortem and S1's pre-review are still prerequisites to the broader comparison. Do not count offline tests as native qualification.
