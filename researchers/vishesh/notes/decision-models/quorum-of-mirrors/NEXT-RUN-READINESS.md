# Q1 instrument readiness and operator handoff

2026-10-04 · **instrument prepared; operator completing launch**. Owner requested the design improvements and necessary preparation for the next experiment. The [prospective Q1 plan](NEXT-RUN-PLAN.md) was published in commit `7d50d4b2` before the new code. [Current roadmap](RUN-ROADMAP.md) retains the later M1/C1 stages and budget. No new native call, scientific-world generation, fleet claim or spend occurred.

## Implemented and checked

- `next_stage.py` freezes the 16 Q1 requests, the sole repair namespace, and the future 64-cell M1 contract. Q1 covers both conflict directions and q values under peer/self-review contexts; the exact masks, misleading prior choices, unavailable slot and neutral actor IDs are explicit. Q1 previous choices are constructed qualification inputs. Actor payloads contain no evaluator target or source index.
- `next_runtime.py` is a separate Q1-only entry point. It cannot admit M1/C1. It records the owner-directed exploratory authority without claiming accepted research, and checks source and manifest hashes, current immutable public plan **and registered immutable condition manifest**, endpoint identity/pricing, fresh provisioner allocation receipt and pinned reporting module. It rechecks admission before each request. The provisioner remains responsible for actual account/workload/merged-claim verification; a template is not that evidence.
- The ledger extension refuses a missing/new database, missing historical S0 reservations, changed authority, unresolved prior calls, duplicate attempts/requests and unknown assignments. Reservation precedes provider access. The original ledger was inspected without mutation: **32 calls, $0.043008 reserved, zero uncertain calls**. No refunds or copied budget authority.
- Response handling exports allowlisted fields only; error bodies, headers and credential values never enter receipts. First failed/uncertain request stops the attempt. Unstarted rows remain in the denominator and HTML. Repair requires a documented interface/implementation cause and remains bounded to one whole Q1 screen; reasoning misses do not trigger retries.
- Analysis distinguishes MAP from sampled truth, keeps partial-lineage qualification ungraded, rejects target/receipt mutation, and contains no probability-calibration metric. The future M1 analyzer enforces the predeclared advance/no-headroom rule. No C1 implementation or efficacy outcome is claimed.

**Verification:** 54 study tests pass, including 20 new tests. These cover the 48-case count shortcut, anti-majority fixtures, input masks/label symmetry, target and hash mutation, partial DEFER handling, all-assigned missing outcomes, route/usage rejection, M1 pairing/stopping, ledger/replay/accounting and admission refusal before credential/provider access. Public endpoint metadata still matches the pinned Jev snapshot and conservative price ceiling; that read was not a model call or a reusable launch receipt.

[Machine-readable readiness](analysis/q1-preparation/readiness.json) records source hashes and the ledger audit. [Browser-checked preview](analysis/q1-preparation/cases-scripted.html) is labelled **SCRIPTED — NOT MODEL EVIDENCE**. It shows one constructed DEFER, one constructed failure and 14 unstarted rows; all partial targets say “not graded.” The in-app browser verified all 16 rows. There is no simulated swarm result hidden in this preview.

## Frozen preparation files

- [Primary Q1 contract](spec/QM-Q1-01.json): literal requests, evaluator-only targets, hashes and condition-specific TLDRs.
- [Only repair contract](spec/QM-Q1-02.json): disjoint IDs/permutations, same finite reasoning structures; not an independent cohort.
- [Launch template](spec/launch.template.json): intentionally incomplete and **not admitted**. Null fields are blockers, not defaults. The future hypothesis ID is a binding for this study, not a claim that the hypothesis exists or is accepted.

From this study directory, offline verification is:

```sh
python3 -m unittest discover -p 'test_*.py' -q
```

PyYAML is required for actual repository research checks. Python 3.13 warns about unclosed connections in historical S0 test helpers; those historical source files were not changed. New ledger code explicitly closes connections. The recorded full-suite command suppresses only those `ResourceWarning` messages.

## Exact remaining admission sequence

Execution must follow the authorized operator's current workflow, not a direct launch from this workstation. Internal dispatch instructions are held separately from this public research package. Researcher review is not a launch prerequisite for this owner-directed exploratory screen.

1. Use the pinned OPERATOR-AUTHORIZATION.json and `research_policy: owner-directed-exploratory`. The owner explicitly waived researcher review; do not wait for it or fabricate a pass. The broader survey remains unsaturated and formal hypothesis acceptance remains unclaimed. The historical design findings are addressed in REVIEW-RESPONSE.md.
2. Publish the final plan and current manifest at immutable 40-character commit URLs. Register the experiment description beginning `TLDR:`, including the **exact immutable manifest URL** so each condition-specific TLDR is publicly bound before calls. Confirm the public page; the runtime independently fetches and compares both plan and manifest. The old S0 registration cannot admit Q1.
3. Obtain a fresh exclusive allocation under the approved Dmarz account/provisioner workflow, verify real workload and merged claim, deploy the full frozen study plus the pinned owner-authority record and pin `swarm_report.py`. Produce a private receipt with fields required by `allocation_check`; only safe host/claim status reaches public output. No idle machine is held now.
4. Retain the original ledger as the sole cumulative authority. For a host change, use an exclusive migration with old workers stopped and original state preserved, not two live copies. Verify the original 32 S0 reservations after migration. Use the approved local credential store/file directly, mode 0600; never paste or log a credential.
5. Fill a private launch config from the template with real paths, current deadline/receipt, immutable manifest URL and reporting-module hash. Refresh source hashes if anything changed; re-run checks. Run the only admission command, saving its receipt privately/publicly as appropriate:

```sh
python3 next_runtime.py --config /approved/private/q1-launch.json \
  --manifest spec/QM-Q1-01.json --preflight-only
```

Only after this passes, invoke the same entry point with `--out` pointing to a new durable attempt directory and `--credential` pointing to the approved secure file. It repeats preflight before credential access and every dispatch. Do not use `worker.py`, `relay.py` or an ad-hoc provider probe to bypass admission. The template has no runnable credential, host, deadline or fake research acceptance.

6. Preserve all receipts, summary, budget state, artifacts and any upload failure; reconcile the hub and terminal outcomes before releasing the allocation. Passing Q1 does not launch M1 automatically. Qualification-source binding and M1/C1 execution/registration remain future stage work. Campaign cap stays 672 cumulative calls and $0.903168 reserved at the verified historical tariff, inside existing $1 API authority; infrastructure remains $1 and ≤6 hours.

The remaining work is operator registration, deployment and fresh operational checks; neither researcher review nor renewed spending permission is required. This handoff distinguishes prepared software, actual model qualification and admitted execution.

## Publication status

The code, plan and condition manifests are published. [Publication record](Q1-PUBLICATION.json) retains their immutable URLs. Updating the public experiment registration was attempted but did not complete; the public page still points to the historical S0 plan. Registration remains an explicit operator prerequisite. No run was queued, no credentials were exposed and no model call was sent.
