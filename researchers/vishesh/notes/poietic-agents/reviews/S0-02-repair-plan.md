# After S0-02: explicit action contract and bounded diagnostic

Prospective offline repair plan written 2026-10-04 after reviewing every started S0-02 trace, before implementing these changes. This is not a preregistration of S0-02 or authority to start another attempt. Preparing agent: vishesh/codex-heterogeneous. Proposed successor: **D0-01, interface diagnostic only; owner approval pending**. S0-02's frozen f3621c649311f4e7a6c110c1b56f97b818927f9e source and outcomes remain unchanged.

## Evidence and decision

The one S0-02 request received HTTP 200 from the pinned Haiku/Anthropic route. It asked for exactly one JSON action and supplied a map from action names to required fields, but did not state that `type` belongs at the top level. The response supplied a Markdown-fenced nested `fetch` object. Strict JSON parsing failed; removing fences alone still leaves an object rejected by the engine. This is verified from saved data, not a demonstration of agent inability to choose an endpoint. The relay recorded valid USD 0.00077 usage while the worker left its reservation uncertain until closeout reconciliation.

Accept S0-01's observability and first-error-stop repairs: this attempt retained the exact divergence and stopped after one call. Revise the assumption that the original terse prompt adequately documented the action contract. Reject permissively stripping fences or translating nested actions for scoring: that would retroactively change the contract and conceal the defect. No result is upgraded.

The next empirical unknown is whether each pinned interface can follow an explicit wire contract through fetch, answer, refresh and structural proposal. Saved-data replay can verify parsing and accounting, but cannot establish how the models answer the revised prompt. This is an engineering diagnostic prerequisite to the collective question; it supports no swarm efficiency, model-ranking or topology claim.

## Changes before another run

1. Deliver an explicit format rule: one bare JSON object, top-level `type`, sibling fields listed for that type, no nesting under action name, no Markdown/prose. Supply a generic `directory` example that contains no task answer. Keep strict parsing and engine validation.
2. Settle independently validated provider usage in the worker before action parsing, as the relay already does. A malformed action still fails and triggers the same stop. Invalid/missing usage retains full reservation. Keep actual route validation mandatory for accepting an action.
3. Rehearse the observed fenced/nested failure offline, proving that both defects remain rejected and known usage is retained. Test the full worker closeout on valid-usage/invalid-action and invalid-usage cases. Check request byte bounds on development fixtures only.
4. Before any successor, implement a separately admitted diagnostic manifest/runner with immutable IDs, no retries, per-role interface stopping, whole-attempt integrity stopping, complete missingness and the original cumulative authority. The separate diagnostic dispatcher is implemented and tested offline as recorded below; it is **not admitted or authorized**. The historical launcher remains S0-02-only.

## Proposed collection and controls

Use three fresh templated world roots (400, 404, 408), each paired across the three roles, with four dependent steps per role: fetch, answer from delivered data, version refresh, then one of load-tool/register-service/install. This covers all three structural variants: **3 independent generator roots, 9 role-case sequences, 36 dependent decisions maximum**, one actor per sequence and concurrency1. Six programmed actors remain available in the fixture; only one is queried per sequence. Qualification roots through347 are retired; S1/S2 holdouts remain closed. No native answer or inspected qualification value becomes a prompt example.

These are simple fictional operations tasks with deterministic reference actions and no external API data. They diagnose wire/interface follow-through; three roots cannot estimate reliability, detect rare failures or establish real workload performance. Even 3/3 independent root passes would have only about0.37 lower endpoint in a two-sided95% exact binomial interval; no precision claim is intended. Keep the original later S0 criterion (44/48 correct,48/48 valid,zero protected access per role); passing D0 does not satisfy it.

Same model routes, tariffs, action semantics, information and initial context per paired root. Reset memory between roots; within-root fetches feed answers and refreshes. Jev's finite alternatives still contain the evaluator's expected answer, so this only tests selection/interface execution and cannot support a fair open-generation competence comparison. The reference engine is the exact offline comparator; do not add a paid judge or claim a collective effect. Retain strict invalid/wrong/protected distinctions.

First interface failure stops that role; other roles may still receive their preassigned diagnostic cells. Any protected access, route mismatch, billing-over-reservation, shared transport/auth failure or ledger/integrity failure stops the whole attempt. At most36 physical calls, no retries/replacements. Unstarted cells remain unstarted, never wrong answers or excluded denominators. No automatic follow-up or threshold relaxation.

Success requires12/12 valid,12/12 correct and zero protected actions for each role, with complete route/usage/context evidence. Success permits proposing fresh full qualification only. Recurrent format failure parks that interface pending offline redesign. Valid-but-wrong actions locate a semantic capability gap. Missing/transport-failed data are inconclusive about competence and stop expansion. A successful diagnostic would not identify the prompt change's causal effect: no fresh old-prompt control is proposed because that contrast is not needed to decide readiness.

## Evidence and acceptance

Retain assignment/start/terminal IDs, exact effective messages and context receipts, raw allowlisted response, action parsing outcome, executed action/effect, independent reference score, per-call usage/reserve/settlement, latency and full allocation lifetime. Join local provider receipts with worker physical IDs. Replay every miss and account for all36 cells; separate missing traces from inspected failures. Publish immutable plan and condition TLDRs before dispatch, plus source/runtime/manifest hashes. Verify artifact readbacks and a missingness-aware final frame. Use the offline finalize hook and eleven-dimension owning scientific review at closeout.

Offline acceptance: bare flat actions pass; fenced, nested and extra-field actions fail without repair; valid usage settles despite those failures; invalid usage stays reserved; each development request stays within7500 wire bytes and8192 conservative input tokens. No reserved diagnostic world is opened during this repair. Native acceptance remains unknown until explicitly approved collection.

## Cumulative resources and approval

Retain the original USD 2 total /1.50 API /0.50 infrastructure cap and 37 historical calls. S0-02 added USD 0.00077 known API cost;36 earlier calls retain USD 0.479232 unresolved exposure. Final allocation-lifetime totals are in the accompanying S0-02 cost closeout. No new ledger or allowance.

Maximum new API reservation for36 calls is USD 0.180965376 at existing tariffs (12 per role), with input8192/output1024 per chat call and decision pricing as pinned. One existing approved-account CPU machine is sufficient; no GPU/new resource is justified. Maximum15 minutes staging +60 minutes execution +5 minutes cleanup at USD 0.07143/hour adds at most USD 0.09524. Refresh the approved resource, exclusive claim, tariff, actual source/runtime and original authority before any activation. A changed tariff must be reassessed, not silently budgeted. Expected model collection is minutes; allow0.5–1h offline preparation,0.5h analysis/reporting and0.25h operator work. Stop and release on completion/failure.

Owner decision required: approve this changed prompt, diagnostic sample and per-role stopping contract plus a bounded replacement time window within the remaining original cap. Existing direct approval covered one S0-02 only. No successor allocation, renewal or model request occurs from this document. Researcher review remains waived.

## Offline implementation completed

The scoped runner, manifest, candidate, admission checks, local relay, one-hour renewal helper and diagnostic frame are now implemented separately in `src/diagnostic*.py`. This implements the prospectively specified 36-decision scope; it creates no launch authority. `diagnostic_prepare.py` creates IDs and a blocked candidate without generating reserved worlds. Admission binds the actual future decision to the proposal, source inventory and assignment hashes; it enforces the 37-call prior ledger, original caps, 36-call diagnostic scope, one-hour deadline and 15-minute staging bound. The renewal helper operates only on an existing expired authority with fresh explicit approval/quiescence and unchanged charge fingerprints; it was tested on synthetic ledgers only. No real authority was renewed for D0.

The 106-test suite includes the 85-test strict-format/billing repair plus 21diagnostic and renewal checks. Complete fake-provider execution covers 36successes; the initial format fault yields 25starts (one failed generalist and 24other-role successes), while transport, wrong-route, invalid-billing and protected-action faults each stop globally after 1start. Known charges survive invalid actions; unknown charges retain reservation. Exact expected action and post-action definition/events are retained for replay. All tests use development worlds and local fake transports; diagnostic roots 400/404/408 remain unopened.

Reproduce from repository root using the pinned requirements:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/poietic-agents/tests -q
python3 researchers/vishesh/notes/poietic-agents/src/diagnostic_prepare.py --out data/poietic-agents/D0-01-preparation
```

Prepared candidate admission must fail until an actual owner update decision, new immutable plan registration, fresh approved exclusive resource/source/runtime evidence and a permitted original-ledger window exist. The operational source will be frozen only after that decision; no default environment or prior S0 approval is reused. At closeout invoke the shared offline finalize hook, then complete the eleven-dimension scientific review. The 106software checks are not native diagnostic success.
