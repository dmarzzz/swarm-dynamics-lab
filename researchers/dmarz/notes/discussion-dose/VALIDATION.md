# Validation record

## Completed engineering checks

The offline suite passes **16 tests**, including 300 generated worlds, hand-written boundary/truth-table cases, source exposure locality, private context and board barriers, nonfeedback ballot probes, quorum/merge behavior, deliberately harmful outcome scoring, failures and all-assigned denominators, provenance hashes, no-overwrite behavior, compressed/chunked artifact round trips and a local mock HTTP endpoint. No paid calls were made.

A manual review of the three rendered task families identified a predictable preference-position shortcut in the initial implementation. Before fleet collection, the generator was revised to use numeric objectives and explicit ties; the attack counterfactual checker verifies the wrong option would win under the altered value. The entire suite was rerun. This is engineering validation by the implementation author, not independent scientific review.

The fixed S0 task IDs contain correct labels A:3, B:1, C:2; the fixed twelve-world S1 set is balanced A:4, B:4, C:4. Each stage spans all three reasoning families. This does not establish real-model difficulty or generalization.

## Fleet deployment

Deployed on **sim-test-01** through the private agentops deployment script, in `/srv/swarm/discussion-dose-lab`. No new server, exposed port or framework dependency was created. The deployed runtime revision is `cf872ef669c7451261bf8d0538c2661bf1607a58`. Documentation may advance independently; manifests preserve the actual execution revision.

| Run | Execution revision | Computation | Hub outcome |
| --- | --- | --- | --- |
| [Initial S0](https://swarm-live.pages.dev/#/r/discussion-dose%2F1443b334) | `98bf48c06e9aadce5932451cce09718b1fc30d8e` | 48 scripted episodes, all valid; 13.794 seconds for computation | Failed during artifact upload because the raw trace exceeded the proxy's 2 MB request limit. Artifacts subsequently recovered without repeating episodes. Failed status intentionally preserved. |
| [Transport verification](https://swarm-live.pages.dev/#/r/discussion-dose%2Fc1d09e7d) | `cf872ef669c7451261bf8d0538c2661bf1607a58` | 8 additional scripted episodes on new engineering world 6, all valid | Done; compressed artifacts uploaded successfully. |

The scripted canonical-source policy returned correct final choices and correct fresh-parent answers in all 56 episodes. That is an implementation expectation, **not evidence of LLM robustness**. No real LLM ran; `scientific=false`, actual HTTP model calls = 0, and model spend = $0.

## Read-back verification

For both runs, downloaded the manifest, episodes, event journal and summary from the hub using `artifact-index.json`. Verified compressed and raw SHA-256 hashes, reconciled every planned episode against the result records, checked event-chain hashes, recomputed strict-majority decisions and memory merges, and recomputed all episode evaluation fields. All 48 + 8 records passed. Original raw local outputs remain on the server; hub artifacts are compressed, with chunk support for larger future payloads.

The upload issue was a transport failure, not a policy failure. It is recorded in the protocol amendments and the original run timeline. Artifact recovery does not add a replicate or convert the failed run into a successful behavioral sample.

## CI and repository checks

[Runtime CI](https://github.com/dmarzzz/swarm-lab/actions/runs/37162353668) passed on Python 3.10 and 3.12. The lab check and dashboard build passed for the same revision. Local `lab.py check` reports zero errors and five existing unrelated library-link warnings. Flight Deck strict validation reports zero errors and warnings. Agentops validation reports zero errors and warnings.

## Remaining scientific qualification

Paid model runs are deferred at the user's request. The compatible HTTP adapter has only been tested against a local mock server. A real endpoint/model, source/model pricing and run limits must be pinned and qualified before S1. The independent task-review request remains [open](../../../../tasks/review-discussion-dose.md). Formal hypothesis acceptance and confirmatory S2 remain pending; this deployment is an exploratory environment.


## First native Anthropic attempt, 2026-10-03

Pinned runtime `c53cb78b9ca7f23af39578a839296cc6a0e9097e` passed 18 offline tests locally and on `sim-test-01`. Model-list authentication succeeded and confirmed Haiku 4.5 availability. Run `discussion-dose/775e3cd6` assigned all eight preflight episodes (world 6, seed 1). Both acquisition calls failed before any model response, making all eight episodes invalid. A separate minimal generation diagnostic returned HTTP 400: Anthropic API credit balance too low. No behavioral conclusion can be drawn; the reported zero correctness/attack rates are invalid-outcome bookkeeping, not model performance. No generated tokens or billed usage were returned. S0 qualification was not queued.

The worker originally marked process completion as done even with 100% invalid outcomes. A corrective fail event now states the billing blocker; the earlier event and all artifacts remain. The subsequent revision makes qualification failures explicit automatically, records safe provider failure categories, and tests the billing-error path (19 offline tests). `haiku45-preflight-v2` is a declared engineering restart after account funding; it does not replace v1 and must not launch while the billing blocker remains. No task, prompt, model or scoring rule changed based on behavioral outcomes, because there were none.
