# Native deployment record

**Current review status:** one researcher review is required and Dmarz’s design feedback satisfies it by owner instruction. The separate dossier review is retired. Q4 means the next qualification run, not another review. See [review resolution](REVIEW-RESOLUTION.md). Historical pending-review entries below describe earlier states.

Dedicated host: sim-dmarz-3. Exclusive claim: vishesh-influence-scenario-native, through 2026-10-04T06:28:45Z; merged agentops PR 54. Actual Python/node script workload was empty before deployment. No other experiment was stopped or moved. No server was created.

One finite worker per attempt, Python virtualenv with Pillow, native Anthropic Haiku 4.5. Model credential consumed from the existing Keychain alias through encrypted SSH stdin and process memory. No credential values or private fleet addresses enter this repository.

USD 1.40 was atomically reserved from the existing shared USD 45 authority under lease influence-native-q0-01. The separate host ledger can spend only this reservation and persists across repair attempts. Failed calls are not refunded. The request for up to USD 10 additional comparison budget remains pending; no additional spending is presumed authorized.

- Q0-01 source 2189a09ecb0f7ebe466541e37400c51dda5c5b52: nine invalid terminal outcomes, six calls, reported USD 0.021259; single-string citation schema was incompatible with naturally multi-source findings.
- Q1-01 source 05caa3cbc781fa7352507566f1122ba8246ef1b3: two valid/acceptable and seven invalid outcomes, 16 calls, USD 0.04256; confidence-null and unnecessarily narrow citation/text contracts.
- Q2-01 source cb611d379ec2d9aef6cab80017d48ed930e68602: fresh profile 6; nine valid terminal outcomes, seven acceptable, 42 calls, USD 0.118778. Competence qualification failed on the two team approvals.

- Q3-01 source 6585745bfca4cdeba8d1bd7f2c91d642fb521f54: fresh profile 7; three valid/acceptable deferrals, 14 calls, USD 0.040445. Targeted diagnostic passed; full qualification remains false.

All four finite workers completed. Total reported model cost USD 0.223042 across 78 calls. Every attempt has complete usage and zero reported upload errors. Additional budget remains unapproved; no P0/S1 was launched.

Each attempt retains its own manifest, source/config signature, cases, request/reply JSONL, outcomes, summary and frames. Measured replays are reconstructed from those events. No failed attempt is overwritten or silently replaced by a repair. See the corresponding pre-run assessments and post-mortems.

Final subquota: USD 1.005589 reserved across 78 calls, USD 0.394411 remaining; no reservation refunded. Verified zero native workers after uploads. Q2 hub status is failed because competence qualification failed, despite nine valid outputs; Q3 hub status is done for its narrow diagnostic. Q2 has 15 artifacts and Q3 has 10 after supplemental replay uploads, none spooled.

Dedicated claim released after upload verification through agentops PR 64 (merged). Git claim status is authoritative; the local agentops hub mirror could not update because sops is unavailable. No native worker remains.

## Q4 fresh allocation — 2026-10-04 UTC

Local-session reconciliation found Antsy had released sim-test-01 in Dmarz's established fleet. Refreshed claims and actual process/container checks confirmed it was free: no experiment worker and zero running containers. Allocated it exclusively under vishesh-influence-q4, merged agentops PR 103, until 2026-10-04T07:08:17Z. This is a different machine from the occupied sim-dmarz-3; no new droplet or billing-account change occurred. Existing workloads were untouched.

A separate /srv/swarm/influence-q4 checkout and /srv/swarm/influence-q4-venv environment are prepared; all 24 scenario regression tests pass on the host. Reporter is available and the allocation was mirrored to the hub. No model credential or budget ledger was copied. No native model calls are running. Before launch, incorporate the independent verdict, pin reviewed source, reverify this claim (renew if expired), and reserve a non-overlapping quota from the approved authority. Dossier review remains open. Release the allocation if the study cannot proceed before expiry.

The new-droplet proposal sim-influence-q4 was not provisioned; the available existing Dmarz fleet allocation fulfills the dedicated-machine requirement. Known local DigitalOcean contexts did not match Dmarz's fleet; they were not used to create resources.

## Q4 and D1 closeout — 2026-10-04 UTC

The owner retired the duplicate dossier review before launch; Dmarz's existing design feedback satisfied the single-review requirement. Q4 used source 189761c2bd907372562220a0dfdfe1c43fa2cfd3; D1 used 84ee032eda80360cc54c5234f8ffc3afe3649cec. Both ran on the exclusive sim-test-01 allocation above. Q4: 56 calls, 12/12 valid decisions, 10 acceptable, USD 0.160220. D1: four calls, four valid decisions, two acceptable, USD 0.021552. No execution failures or missing usage. Q4 failed competence; S1 was not launched. See LATEST-RESULTS.md and both post-mortems.

The approved shared authority is USD 55. An atomic USD 8 lease funded this iteration; its persistent host subledger reserved USD 0.773396 across 60 calls, leaving USD 7.226604 within the lease. Actual reported usage totals USD 0.181772; reservations are not refunded or reset. Preserve the authority and subledger when reallocating machines.

Raw evidence, final frames and measured HTML/GIF replays uploaded and verified: qualification has 16 hub artifacts and diagnostic has 12. Verified zero remaining native workers. Dedicated claim released through merged [agentops PR 125](https://github.com/dmarzzz/swarm-labs-agentops/pull/125). Git is authoritative; automatic release mirror lacked local sops. No cloud resource was created or destroyed.

## D2 admission — 2026-10-04 UTC

Fresh exclusive claim vishesh-influence-d2 on verified idle sim-test-01, merged agentops PR134, until 06:39:09Z. Zero containers and no Python/node/uv workers; only Docker daemon. Existing USD8 lease renewed in place for this claim, preserving the old receipt and all reservations; host subledger remains /srv/swarm/influence-q4-budget.sqlite. Observed reserved USD0.773396, remaining USD7.226604. No new quota, server or billing context. D2 admission requires remaining >=USD5.972 and exact immutable public-plan bytes. Single finite diagnostic worker; no S1.

27 unit checks pass. Scripted-D2-02 reconciles 30 valid/acceptable terminal assignments and 108 logical calls; zero API calls. Timeout fault yields all 30 invalid terminal assignments with zero dispatch. Initial/midpoint/final grid checked, fixture-label correction retained. Public preflight receipt is written before hub run_start. Full request/event/outcome history and actual usage are required; code/source commit is frozen and recorded in runtime manifest.

## D2 closeout — 2026-10-04 UTC

Run influence-swarms/1004-044202-3747f4 executed frozen source 518d4412bc566a388dd4dc022118ade8dd637fa3, public page visibly inspected before dispatch and exact raw-plan hash checked by worker. All 30 decisions valid, 17 acceptable; 108 calls, USD0.391659. The targeted repair failed (3/6); no S1. All 24 hub artifacts verified after supplemental uploads: audit, report, full HTML replay, 31-frame measured GIF, overview and local-font grid. Zero spooled uploads; PID45132 stopped. Browser overview and final replay state agree with saved outcomes. The shared subledger now records USD2.372320 reserved across 168 calls of its unchanged USD8 grant; USD5.627680 remains reserved for this study. No reservations refunded or copied.

Dedicated claim released through merged [agentops PR144](https://github.com/dmarzzz/swarm-labs-agentops/pull/144) after verification. Git is authoritative; automatic hub allocation mirror lacked local sops. No server was destroyed or other workload interrupted.

## D3 candidate-check diagnostic, 2026-10-04

Frozen source8087faf9fd3399c30774ad71e8f95dcdaa576215, plan ITERATION-04.md. Dedicated sim-test-01 allocation vishesh-influence-d3, merged fleet PR149; no other experiment workload. Same existing8USD lease renewed to new claim, no new authority reservation or ledger reset. Runtime signature75e226df87100c08fbb68529007e912110975f2d22e9e5e55fc4dd3f5fd7c719. Actual dispatcher validated current fleet/claim, inventoried SSH destination and idle processes/containers before selecting the single approved Keychain alias; exact secret/routing allowlists, SSH host-key verification, no agent forwarding, minimal environment, core dumps disabled. Public admission.json contains only non-secret selectors and receipts.

Run influence-swarms/1004-054904-3252ed complete:18 valid terminal outcomes,30 calls, reported0.205670USD. Worker47740 stopped;24 hub artifacts including source/model matrices, events, raw/shadow outcomes, audit, final PNG,18-terminal GIF and standalone HTML replay verified, no uploads spooled. Ledger remains cap8,reserved3.178320,calls198. D4 failed its admission screen and was not launched. No S1. Initial Git transport delay blocked before credential selection and native dispatch; refreshing only main avoided unnecessary trace-branch transfer. Deployment scripts contain no embedded secret; credential only lived in finite worker memory/environment.

Dedicated claim released via [fleet PR171](https://github.com/dmarzzz/swarm-labs-agentops/pull/171), merged. Artifact mirror to the hub was unavailable in agentops locally (sops absent); merged Git claim is authoritative. The experiment artifacts themselves uploaded successfully and the run status is done.
