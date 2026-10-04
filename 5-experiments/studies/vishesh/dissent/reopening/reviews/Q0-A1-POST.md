# RD6 qualification startup post mortem

**Q0-A1 stopped before native dispatch. Qualification was not run and the scientific question was not tested.** All 18 planned requests remain unstarted; D0 is unrun. This is an operational failure, not an accuracy result. The owning agent reviewed all eleven run-quality dimensions; no independent review is claimed or required.

## Evidence and cause assessment

Source revision `177a2041301bf3c007e895bfaf311e702c0b400b` passed 73 offline checks both locally and on the allocated Linux host. The public plan, account/allocation, original ledger and runtime were checked. The coordinated supervisor was launched through ordinary platform approval and exited unsuccessfully. The local relay started and stopped, but its accounting contains zero calls and no reservation event. The original ledger retains 488 calls and USD0.022699069 committed API; the Q0-A1 stage row remains stopped.

The remote output directory and its parent were both absent. Replaying the directory-creation operation from the deployed source reproduced `FileNotFoundError` before any transport call. That is a verified implementation defect. The original worker stderr was suppressed, so this is not proof of the sole historical cause. Admission evidence was also restaged during coordination; a timing race is plausible but unverified. New diagnostics and immutable staging address both vulnerabilities without claiming either model behavior or a fully recovered historical trace.

Remote owned workers and local relay/processes were verified stopped. The startup evidence bundle contains the original packet, relay events/accounting, supervisor state, safe diagnosis and full assigned/unstarted summary. It is deliberately not a fabricated native response bundle. Both exclusive allocations are now released; [resources](../results/q0-a1-startup/resources.json) carry the USD0.026925142 allocation estimate forward, with no invoice claim. The shared offline finalize hook recorded outcome `blocked`; its handoff digest is `c4763ff165d85ecd6be08cb33f79e0dd829a8283c77d1de1f2cf51b9816ee68f`.

## Run quality assessment

| Dimension | Assessment | Evidence and next action |
| --- | --- | --- |
| Question | Pass for declared diagnostic scope | The frozen plan states the context contrast and outcome-dependent component decision. No conclusion can be estimated from this attempt. |
| Scenarios | Pass for inspected development scope | All 162 labels agree with the literal reference; 12 authored D0 cases share six families and three grammars. No field realism or held-out generalization is claimed. |
| Controls | Unknown in native execution | Nothing reached the actor. Native Q0 must establish its prespecified controls before D0. |
| Capability | Unknown | Zero native answers; 18/18 semantic qualification remains required. Parse/transport readiness cannot substitute. |
| Measurement | Pass for failure accounting | The evidence preserves assigned18, dispatched0, responses0, unstarted18. Accuracy is absent, not 0%. |
| Sample size | Pass for denominator disclosure | No independent empirical units were collected; the planned 12 paired development cases are unchanged. |
| Agent context | Unknown in delivery | Frozen requests exist but no effective native input was delivered. A successor must retain exact wire hashes and route receipts. |
| Data integrity | Gap in startup diagnostics | Original worker error detail was discarded. Preserve the partial record; require safe phase diagnostics and receipt digest matching before any successor dispatch. Zero ledger rows and relay events support the zero-dispatch conclusion. |
| Resources | Pass for API reconciliation; infrastructure estimate retained | Original ledger and reservations are unchanged; no paid model call. Both allocations are released; USD0.026925142 incremental allocation estimate is retained in the resource record. |
| Reproducibility | Gap | Frozen code reproduces the missing-parent failure, but the original reason for exit is not fully recoverable. Add nested-directory and failed-start tests, plus a remote no-provider startup check. |
| Visualization | Not applicable to native outcomes | There are no model observations to plot. Existing previews remain explicitly synthetic; display counts and status without an accuracy chart. |

## Repair decision

Select **repair**, not advance. The [prospective startup proposal](../STARTUP-REPAIR.md) fixes nested-directory creation, safe diagnostics, receipt staging and a narrowly authorized zero-dispatch replacement. It leaves all scientific cases, labels, controls, sample counts, stopping and cumulative caps unchanged. A1 remains a failed attempt; a new attempt cannot inherit a fabricated qualification pass or erase the ledger fence. Finish the concrete code and offline checks, then obtain the corresponding owner decision before allocating or launching the replacement.
