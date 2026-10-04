# D7: OpenRouter worked; the adapter dropped the output schema

Retrospective closeout, 2026-10-04. [Native run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-185452-ea3df2), [prospective plan](https://github.com/dmarzzz/swarm-lab/blob/abedc39236f22d397a0cae4906660f1b848e4287/researchers/vishesh/notes/influence-swarms/scenario/ITERATION-07-ROUTE.md), [audit](D7-audit.json), [native artifacts](native-D7-01/summary.json).

| Assigned contract | Acquisition | Output contract | Reported cost |
|---|---|---|---|
| Matrix reviewer | Complete response | Invalid: Markdown instead of JSON | $0.014422 |
| Typed reviewer | Unstarted after first failure | Unassessed | No request |

## Outcome and first divergence

The approved OpenRouter route returned one complete Haiku4.5 response through the pinned Anthropic provider:4042 prompt tokens,2076 completion tokens, finish_reason stop, reported costUSD0.014422. There was no HTTP429 or other provider error. This establishes successful acquisition on the new route at that moment; it does not diagnose or repair the original direct Anthropic account's429.

The first matrix answer was a Markdown report. The strict JSON decoder failed at character0, so contract validity was0/1 and the second typed condition remained unstarted. One physical request, zero retries, no chair or broader cohort. The raw answer and exact request remain intact. Neither a repaired parse nor a hand-copied choice enters the scored dataset.

The primary instrument defect is verified by comparing the actual wires: D6 included `output_config.format.schema`; D7's adapter copied model/messages/sampling but omitted that schema instead of translating it to OpenRouter `response_format`. The validator still demanded the original JSON contract. The prompt alone did not require JSON. Offline fixtures always emitted valid JSON, and the preservation test compared the fields it copied without checking the omitted source field. Thus88 passing tests failed to catch a consequential migration defect. Source pinning and byte equality faithfully preserved a defective request; they did not prove semantic contract equivalence.

The missing schema is a supported explanation for the format failure, not proof that structured output will cure all behavior. The narrative marks Aster's rollout FAIL even while calculating38 days against a61-day limit, because inference location is unconfirmed—a different field. It marks Cobalt service coverage FAIL and then corrects itself to PASS in prose. It prefers Birch conditionally while explicitly withholding purchase authority. These are visible, unscored diagnostic observations, not valid matrix statuses, executed purchases, causal architecture evidence or a new accuracy estimate. Typed extraction remains untested live.

## Control, cost and process assessment

Both assignments remain visible: matrix failed, typed unstarted. The response provider/model, complete usage and cost are verified from the retained body; the wire hash matches the public frozen packet. No operator conversation, credential or private account data was added to model input. Automatic review initially blocked export; the coordinating task verified anonymous access to both exact already-public synthetic payloads and obtained approval for the same unchanged command before execution. No denied attempt created a worker or charge. Researcher review was not required.

The deployed source was `abedc39236f22d397a0cae4906660f1b848e4287`.88 offline tests passed on the pinned worker. Immutable plan and both condition-specific TLDRs were registered and read back before dispatch. The actual migration nevertheless failed output-contract preservation, so process admission must not be called complete instrument qualification.

The originalUSD8 ledger now reservesUSD4.966112 across248 physical requests, leavingUSD3.033888 unreserved. D7 added oneUSD0.048640 reservation; reported actual cost isUSD0.014422 with no missing usage for this attempt. Prior uncertain D5/D6 reservations remain. No new machine was created. The worker exited, zero blocking processes remained, the local relay and forwarding closed, retained artifacts were collected, and the exclusive allocation was released. No successor is running.

## Repair and decision

[D8 preparation](../ITERATION-08-PREP.md) delivers the original schema through the new provider contract and explicitly requests JSON. It adds actual-wire schema equality, missing-schema/instruction mutation checks and a regression against the original Anthropic schema.92 offline tests pass. The corrected wires are19706 and26375 bytes, within the original32768-byte envelope. The proposed two-call maximum remainsUSD0.097280, from the same ledger.

This repair is prepared only. A next-run decision and fresh source/runtime/public-plan/allocation admission are required; no extra researcher approval is needed. Do not replay D7 or silently overwrite its evidence. No schema or endpoint fixture establishes native typed competence, a realistic procurement outcome or an influence effect. The useful next question is whether the correctly delivered contract is usable, before spending on behavioral comparisons.
