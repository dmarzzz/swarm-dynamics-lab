# D5 operator handoff — prepare now, launch later

D5 implements the concrete repair suggested by [D3](RESULTS-D3.md). It is a new, prospectively specified development diagnostic, not a reroll of D3 or continuation of the gated D4. [Plan](ITERATION-05.md), [pre-assessment](reviews/native-D5-01-pre.md), [setup](SETUP.md). No provider call, credential access, fleet allocation or budget renewal was performed during preparation. Researcher review is optional under the current owner runbook; do not introduce another approval bottleneck.

## Implemented behavior

- Require all three candidates, four primary-record groups and 36 typed fields per extraction response. Explicit unknown-field masks normalize to null; typed wire placeholders never count as facts. Reject duplicate JSON fields, invalid types, nonfinite values, invalid pilot denominators and unsupported fields.
- Preserve the original extraction. Verify candidate-specific citation, exact supporting excerpt and value alignment with labelled source fields. An unsupported number is rejected into unknown evidence; the correct source number is not silently supplied to the agent.
- Compile five mandatory checks using one buyer-policy version and Decimal arithmetic. Each receipt shows its policy clause, observed value, operator/threshold, source IDs, result and reason. Future mitigation and qualitative concerns cannot modify policy.
- Keep raw choice and separate purchase authority distinct. Refuse an unsupported or excessively expensive purchase; list eligible alternatives on an unnecessary deferral without silently selecting one.
- Cross matrix versus typed-fact review with inherited interpretations versus primary records only. Same reviewer evidence within each context, same standard chair prompt, same model/caps, 48 nominal calls, 24 decisions on six frozen D2 cases.

The excerpt verifier is a synthetic-template parser. It does not prove general language understanding or validate arbitrary vendor contracts. The paired matrix comparison tests this complete application architecture, not a pure formatting change. Existing flawed reports remain a candidate cause until D5 actually runs.

## Offline commands

From the repository root, use the existing Python environment with Pillow. These commands do not load credentials or import the reporting client:

```sh
python -m unittest discover -s researchers/vishesh/notes/influence-swarms/scenario/tests -q
python researchers/vishesh/notes/influence-swarms/scenario/analysis/typed_diagnostic.py prepare \
  --parent data/influence-native/native-D2-01 \
  --out data/influence-native/D5-packet.json
python researchers/vishesh/notes/influence-swarms/scenario/analysis/typed_diagnostic.py fixture \
  --packet data/influence-native/D5-packet.json \
  --out data/influence-native/scripted-D5-01
python researchers/vishesh/notes/influence-swarms/scenario/analysis/typed_report.py \
  data/influence-native/scripted-D5-01 \
  data/external-influence-v2/visuals/D5-readiness.html
```

Output paths are exclusive. Never delete an old result to reuse an attempt ID. If the paths already exist, inspect them and choose a new justified fixture ID. `source_dirty:true` packets support development checks but are refused for native execution. The packet hashes cases, original observations, every reviewer input, config, instrument files and prospective plan. The native check also verifies instrument bytes against the deployed commit.

## Remaining run-time admission

Preparation is complete only after the published-source fixture, source audit, exact wire-size probe and report inspection pass. A later launch still requires fresh operational receipts; do not reserve an idle machine now.

1. Refresh the private Dmarz fleet registry and actual workload; obtain a new exclusive claim. Never reuse the released D3 claim or run alongside another experiment. Follow [the machine workflow](../../experiment-machine-workflow.md) and [credential policy](../../../../toolkit/agent-experiments/SWARM-LAB-CREDENTIALS.md).
2. Preserve the existing canonical grant and persistent host subledger. Last known values: cap8USD,reserved3.178320,calls198. D5 maximum reservation4.669440USD versus historical remaining4.821680. Recheck current values and prices; any depleted remainder blocks admission, not a reason to reset the ledger or infer a new default allowance. Renew the existing allocation receipt for the new claim without adding budget.
3. Deploy the packet's exact published source commit and same Python/provider dependencies. Verify the immutable public ITERATION-05.md bytes. The native runner writes its non-secret preflight receipt before starting a hub run.
4. The secure dispatcher performs the actual inventory/SSH-host identity, merged unexpired exclusive claim and idle-workload checks before reading the single approved Keychain alias. Core dumps disabled; minimal environment; separate exact secret/routing allowlists; verified SSH stdin only. No keys in commands or files.
5. Supply `SWARM_D5_ADMISSION_RECEIPT`, a non-secret JSON file with exactly: `packet_hash`, `source_commit`, `host`, `claim`, `operator`, `checked_utc`, `inventory_identity_match`, `exclusive_claim_current`, `workload_idle`, `credential_policy`. The three verification booleans must reflect actual checks, operator must be `vishesh/codex-experiments`, and policy must be `tooling/agent-experiments/SWARM-LAB-CREDENTIALS.md`. Receipt age must be0–300seconds. Match host/claim to the current `SWARM_ALLOCATION_RECEIPT`. These are operator attestations, not independently verified by the native process.
6. Set the existing approved runtime variables through the secure dispatcher: config must resolve to `model-config-facts.json`; preserve `SWARM_BUDGET_LEDGER`; provide current allocation and D5 admission receipts. The provider receives only the approved credential and verified workspace route in memory. Then invoke `typed_diagnostic.py run --packet <frozen-packet> --out <new-native-D5-directory> --public-plan <immutable-plan-url>`.

No launch command has been executed during this preparation. No local dispatcher is presented as a fleet authority; refresh/rebuild its host-specific bindings at launch rather than reusing old D3 scripts with stale pins.

## Evaluations and reporting

Raw extraction accuracy is scored against evaluator facts after responses only; alignment is separately scored. Requirements and final decisions are reconciled against an independent Decimal calculation from primary records. Track false FAIL/PASS and UNKNOWN confusion, contradictory purchase, avoidable deferral, cost-claim error and authorized outcome. Invalid assignments remain in denominators; unavailable paired effects are null. No model answer or evaluator label replaces a native decision.

Live/final PNGs show six case rows ×four workflows; pending and invalid states are explicit. Saved events retain elapsed time. The HTML report switches raw/authorized actions and exposes original extraction, evidence alignment, policy receipts and actual events. Fixture labels are mandatory. Native report failures are recorded separately from scientific outcomes and repaired from saved data without recollection.

D5 has no automatic successor. Even6/6 correct typed decisions are only a development signal on inspected cases. Fresh qualification and independent scenario authorship remain necessary before an external-influence claim.

## Preparation closeout — 2026-10-04 UTC

Prepared, not launched. Frozen published source: `528c4f70260f6c3fcda55633a06458cd1e9027b1`. Packet: `d0fe44becee7386e667b84f727317d91e3cbd68be2b28a89f33d24b7419efe44`, with clean source. The immutable public plan was fetched and byte-verified. Subsequent documentation commits do not change this deployment pin.

All 59 scenario tests pass, including deadline failure accounting and admission rejection checks. The published-source `scripted-D5-01` rehearsal completed 24/24 valid decisions using 48 scripted calls: zero model calls and USD 0 spend. Independent reconciliation passes. Both typed arms produced 216/216 correct and aligned fixture facts; all four arms produced 90/90 correct fixture statuses. These scripted outputs validate plumbing and arithmetic, not agent competence.

The largest encoded fixture request was 28,941 bytes against the 32,768-byte input cap. The interactive report was inspected for fixture labeling, case/arm selection, raw versus authorized outcomes, and source-linked policy receipts. Provider schema acceptance remains untested by a live API call. Readiness metadata: [D5-readiness.json](reviews/D5-readiness.json). Local preview: `http://127.0.0.1:8766/D5-readiness.html`.

The next run is 24 decisions / 48 nominal calls, with a conservative reservation ceiling of USD 4.669440 from the existing cumulative budget. Fresh dedicated-host, remaining-budget and secure-dispatch checks above are required immediately before launch. No researcher review is pending or required. D3 remains the latest measured model result; D4 and S1 remain unrun.

## Live run requested — 2026-10-04

The owner authorized live D5 execution. Current fleet policy now requires orbital-one queue dispatch, superseding the laptop-launch steps above. The frozen experiment source and packet remain unchanged. A tested central receiver and credential sender, plus the frozen packet, were merged in private agentops PR215; run request217 asks for one D5 attempt only. Three additional launcher tests and fleet CI pass. No D5 model call has started at this update.

The previous host is occupied by another experiment. The central operator must allocate a different idle dedicated machine and migrate the original budget with verified single-writer fencing; never spend from duplicate ledger copies. A read-only check of the existing subledger confirmed cap USD8, reserved USD3.178320, calls198 and remaining USD4.821680. Pricing is unchanged at the pinned rates. No new grant or top-up was created.

The originating session supplies the already-authorized dedicated Keychain credential only after central receiver readiness and fresh claim/source/budget/host verification. The API key remains in process memory and verified SSH stdin. Central readiness, credential acceptance, first native dispatch and terminal result must be recorded separately; queued is not running. No new researcher approval is required.

## Readiness update — 2026-10-04

The owner renewed the live-run request. Deployment now passes all59 scenario tests and the no-model-call preflight against the frozen source and public plan. The original cumulative budget is preserved. Detailed allocation and migration evidence remains in the private fleet record. No D5 model call has started. The central dispatch request remains pending; an owner decision on a direct-dispatch exception is awaited. This changes no experiment input, treatment, endpoint or scientific source pin.
