# Post-mortem: fleet-s0-001

Experiment sybil-specialists / dmarz/sybil-specialists / S0 / 2026-10-04 UTC. Parent: local-s0-001; pre-run: fleet-scripted-001-pre.md. Disposition: advance to scripted S1.

## What ran and what happened

Pinned source e3caaf3d77bc46474f2b02145799c5f534adf225, unchanged design digest b7d0aa0ab82b03c9ec5ae705ec90a990c5e29e98c9fe5aa3859c2efcbecb210d. Python 3.12.3, Pillow 11.3.0, PyYAML 6.0.1, sim-dmarz-4, claim dmarz-sybil-specialists. All 16 cells completed: 256 assigned, started, terminal and graded arm records; zero invalid, missing or duplicated experiment attempts. Zero model calls, tokens and API spend. Fourteen controls passed remotely. Reconciliation and runtime manifest are retained in results/fleet-scripted-001 and the dedicated server results directory; each run has durable assignment, summary, episodes and replay-source artifacts.

All arm means match local S0 within 1.12e-16 absolute difference. An initial byte-exact comparison flagged floating-point summation differences between runtimes; inspection found only final-bit rounding, with matching counts. Numeric parity passed at absolute tolerance 1e-15. This is an engineering replication of the same four worlds, not new independent evidence.

## Visualization review

Mapping v1: 32 PNG images and eight five-frame GIFs cover all 16 cells. All three image types loaded at 1800 × 1180 in the actual live browser; the replay visibly advances through check states. Images and recorded first-world metrics agree. Example public run: https://swarm-live.pages.dev/#/r/sybil-specialists%2Fddb820db . The UI originally selected the initial image for its final-frame contact sheet. The deployment reconciliation now refreshes unchanged initial-image metadata after final-image upload, preserving both files while putting final_frame.png first. All 16 artifact lists passed that ordering check. No simulator outcome was regenerated for this repair.

## Experiment-quality assessment

Execution and scripted qualification passed. Informative and uninformative verifier conditions produce different usefulness/risk tradeoffs; clean all-admitted correctness passed. No model competence test has occurred. The small symmetric graph family, privileged seeds, synthetic facts, fixed attacker policy and modeled verifier limit scientific interpretation. No design tuning followed the observed results.

## Failure and repair ledger

| Issue | Evidence and verified repair | Status |
|---|---|---|
| Reporter setup | Missing environment; standard reporter provisioning with explicit local SOPS key-file alias succeeded, without exposing credentials. | Closed before assignment |
| Shared checkout setup | Two launches could not resolve the host while another job rewrote generated inventory. Deployment moved to a dedicated private worktree with committed inventory. | Closed before assignment |
| Wrapper file mutation | A local shell reported a parse error after remote S0 and reconciliation had completed because its script changed while running. Re-executing the stable wrapper queued and ran zero additional assignments. | Closed |
| Preview ordering | Repair first used the wrong hub attempt-field name and stopped; corrected to attempts. Stable wrapper then reconciled all 16 cells and durable final-image priority. | Closed |
| Exact float comparison | Maximum difference 1.11e-16; numeric parity at 1e-15 passed. No rerun or outcome change. | Closed |

## Next run

Read this review and fleet-s1-001-pre.md before queueing S1. Use exactly the same pinned execution source and 12 fresh worlds 200–211. Maximum 864 arm records, zero provider calls/spend, one worker and 30 minutes. Preserve null/adverse results. Stop on invalid records or failed durable artifacts. S2 stays disabled and model work still requires its separately declared cap and qualification design.
