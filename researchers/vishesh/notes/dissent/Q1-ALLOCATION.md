# Right Dissenter Q1 allocation amendment

Prospective 2026-10-04 amendment, before replacement-host implementation or native Q1 dispatch. Read Q1-SETUP-POST.md: the wrong-account host was deleted, while Q0 outcomes and budget remain preserved.

The previously occupied Dmarz fleet host sim-shadow was released by Theseus at 04:25:25Z. Fresh fleet metadata verifies owner dmarz and the existing generated/dmarz inventory. A read-only workload check found no experiment worker and no Docker container; only normal system services and the inspection process. The owner explicitly authorized borrowing from Dmarz's machine list. Claim this idle host exclusively through the private fleet workflow; do not create a new droplet or use the local default DigitalOcean credential.

The Q1-PLAN.md decision packets, thresholds, seeds and controls are unchanged. Replace the hard-coded host binding with a launch configuration that accepts only the recorded replacement, verifies the actual machine hostname and requires an allocation-verification flag and private receipt hash. Source, immutable plan, expiry and budget gates remain mandatory. Pin the final immutable Q1 plan revision with this amendment linked before dispatch, register it and visually verify the public page. No Q1 requests have been made.

The original cumulative SQLite budget remains at18calls/$0.00042966. At most42Q1calls are reserved. An exclusive one-hour borrowed-host claim fits within the original six-hour allocation ceiling; no additional infrastructure purchase occurs. Do not destroy this existing Dmarz machine at closeout: stop only our worker/tunnel, verify artifacts, and release our claim.
