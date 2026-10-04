# Pre-run assessment: v3-d2-a1

2026-10-04 UTC, by `dmarz/v3-d2-opus`. Status: **diagnostic-only**. Not a launch receipt: the paid run needs the
reviewer's explicit go, then a passing preflight and compatibility probe. Parent `v3-d1-a1`; its
[post-mortem](v3-d1-a1-post.md) was read. [Plan and amendment](../benchmark-v3/d2/PLAN.md),
[base design](../benchmark-v3/D2-PLAN.md), [setup record](../benchmark-v3/d2/SETUP.md).

Review: `dmarz/fleet-monitor` checks this assessment and the code. Both agents work for dmarz, who waived
cross-researcher review for this run. It is a same-researcher check, not an independent review.

- Experiment / owner / stage: `discussion-dose-v3` / dmarz / D2.
- Question and decision: does Claude Opus 5.5 pass the canonical-decision and single-option feasibility screens on
  the six worlds where D1's models failed, and do Sonnet 4.6 and Haiku 4.5 pass them on the same items. The result
  decides what the next proposal examines (see the reading table in the plan). It qualifies nothing.
- Context: [D1-Opus](../d1-opus/RESULTS.md) (`d1o-a1`) finished at 08:00 UTC with Opus 5.5 at 6/6 on these worlds
  and 12/12 on a fresh gate, on D1's original packaging. Opus already clears the v3 baseline, so D2 is not needed
  to qualify it. D2's value is explaining why Haiku and Sonnet failed and checking whether Opus is also at ceiling
  on the compact format.
- Expected finding: Opus passes both screens. Plausible negative results: Opus fails a screen it passed on D1's
  packaging; atomic checks pass and decisions fail; a comparison arm passes where it failed D1, which would point
  at D1's evidence packaging or contract rather than at model strength; a comparison arm still fails, which would
  point at constraint application itself.
- What would make the run uninformative: invalid or truncated answers (then no screen is read for that model); a
  rejected request setting on the whole Opus arm, which the one-call probe is there to catch before the batch.

## Design and assessment

- Closest evidence and comparator: D1 on the same six worlds (Haiku 2/6, Sonnet 3/6 full decisions, all 48 facts
  extracted correctly by both). The comparison arms are the D2 plan's own two models with D1's settings.
- Units: six world clusters, two per family. 24 items per model are dependent (three options and one decision per
  world). The three models answer identical inputs; the 72 calls are not independent samples. No population
  inference, interval or significance test.
- Coverage and boundaries: all six open development worlds, every option once in the atomic set, all three options
  in every decision. Labels: 6 feasible and 12 infeasible options per model. No new world, holdout or qualification
  ID is generated or read.
- Manipulation check and fairness: every model receives the same system prompt, user content and schema; the
  selftest compares the three serialized requests for every item. The comparison arms differ from each other only
  in the model id. The Opus arm also differs in sampling (not sent), thinking (always on, effort `high`) and
  output ceiling (4,000 against 2,000), because Opus 5.5 rejects temperature and cannot disable thinking. This is a
  stated difference between arms, not a controlled one.
- Bundled change against D1: D2 changes evidence packaging and the response contract together (no documents,
  catalog, domains, source policy or claim map; a one-field answer). D1 and D2 outputs are not interchangeable
  trials and an improvement cannot be assigned to one removed component.
- Evaluator: gold winner from `bench_v3.scoring.reference_winner`; option feasibility from `tasks.feasible`,
  required to agree with a second predicate that reads the thresholds out of the public instruction sentence, and
  checked again in the selftest by direct arithmetic on all 18 options. Labels never enter a request:
  `reject_gold` runs on every input and the selftest checks each request's exact keys.
- Controls, run through the real execute, score, summarize and audit path: always-right gives 6/6 and 18/18;
  always-infeasible gives 12/18 with 0/6 true positives; always-feasible gives 6/18 and, ranking all options by the
  objective, 2/6 decisions (worked out by hand: worlds 20001 and 20004); wrong-vote gives 0/6 with six constraint
  violations; malformed gives 24 invalid and no screen reading.
- Primary metric and denominators: Opus canonical correct out of 6 and feasibility correct out of 18, with the
  12/18 always-infeasible baseline beside it. The same for each comparison arm. Assigned denominators are fixed;
  failed, invalid and unstarted calls stay in them.
- Timing: wall time only. One call at a time; no rounds.

## Changes and unresolved issues

| Issue or prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| D1-C1: decisions wrong after correct extraction | Canonical fact table and one-field contract; atomic feasibility checks | Separates predicate application from selection | Screens and composition table reported for all three models | v3-d2-opus |
| dmarz asked for a strong model | Opus 5.5 arm as model under test | Shows whether a stronger model with thinking passes | Opus 24 items valid, reported first | v3-d2-opus |
| Another study's Opus batch failed 24 of 24 on a rejected setting | Opus adapter sends no temperature and no thinking field; one-call probe gates the batch | No assignment lost to a request error | Probe returns a parsed answer; otherwise the batch does not start | v3-d2-opus, reviewer |
| Thinking counts against the output ceiling | Opus `max_tokens` 4,000; a `max_tokens` stop is recorded as incomplete, not as wrong | Truncation is visible and rare | `output_ceiling_stops` reported per model | v3-d2-opus |
| D1-Opus ran these worlds at effort `high` | D2 Opus arm uses `high` too, not the default `medium` | The two Opus runs differ in packaging, contract and output ceiling, not effort | Effort recorded in the manifest and in every provider body | v3-d2-opus, reviewer may change before go |
| D1 closeout: launch route changed to the run queue | This run is launched from the fleet-monitor session's machine on instruction relayed by the reviewer | None on the measurement | Deviation stated in the plan and here | reviewer |
| Shared USD 500 pool not re-reconciled by this agent | USD 5 cap for this run; reservation USD 3.387356 | Bounded spend | Per-adapter caps enforced in code; actual cost reported | reviewer |

Not resolved by this run and stated as limits: one response per item, so no estimate of run-to-run variation; six
reused worlds; exactly one feasible option per world, so multiple-feasible tie-breaking is untested; comparison-arm
refusals and unexpected response blocks share one failure reason because the D1 adapter is used unchanged.

## Frozen execution plan

**Assignment manifest.** 72 rows, `d2-000` to `d2-071`. 24 items, each asked of the three models back to back.

| | Opus 5.5 | Sonnet 4.6 | Haiku 4.5 | Total |
|---|---:|---:|---:|---:|
| Canonical decisions | 6 | 6 | 6 | 18 |
| Single-option feasibility checks | 18 | 18 | 18 | 54 |
| Assigned calls | 24 | 24 | 24 | **72** |
| First / second / third in its item | 8 / 8 / 8 | 8 / 8 / 8 | 8 / 8 / 8 | |
| Compatibility probe (not a result) | 1 | 0 | 0 | 1 |
| Maximum physical calls | 25 | 24 | 24 | **73** |

Item order with the model order inside each item (O Opus, S Sonnet, H Haiku):
`atom-20006-B OHS, atom-20004-B HSO, atom-20001-B OHS, dec-20001 SOH, atom-20005-C HSO, atom-20001-A SOH,
atom-20001-C HOS, atom-20004-A OSH, dec-20005 SHO, dec-20004 HOS, dec-20006 HSO, dec-20002 OSH, atom-20006-A OSH,
atom-20004-C SOH, atom-20005-A SHO, atom-20005-B SHO, atom-20002-A HOS, atom-20003-B OSH, dec-20003 OHS,
atom-20002-C HOS, atom-20003-A OHS, atom-20006-C HSO, atom-20002-B SOH, atom-20003-C SHO`.
Haiku precedes Sonnet in 12 of 24 items. Seed `d2-order-v1`.

**Settings.** As in the plan's table: Opus `claude-opus-5-5`, no sampling parameter, thinking on by omission,
effort `high`, `max_tokens` 4,000; Sonnet `claude-sonnet-4-6` and Haiku `claude-haiku-4-5-20251001`, temperature
0, thinking off by omission, `max_tokens` 2,000. All: structured output, 60,000 input bytes, 120-second timeout,
no tools, no fallback, zero transport and repair retries, one worker. The three ids were confirmed on the account
through the Models API on 2026-10-04 (metadata read, no inference); that response lists effort `high`,
structured outputs and adaptive thinking as supported for Opus 5.5 and manual thinking as unsupported. Prices
4/20, 3/15 and 1/5 USD per million input/output tokens were read from the official pricing page on 2026-10-04.

**Budget reservation.** Per call: (serialized request bytes + 512) at the input price plus the full output ceiling
at the output price. Request bodies are 1,615 to 1,798 bytes for Opus.

| | Calls | Worst case USD |
|---|---:|---:|
| Opus 5.5 | 24 | 2.129232 |
| Sonnet 4.6 | 24 | 0.877068 |
| Haiku 4.5 | 24 | 0.292548 |
| Opus probe | 1 | 0.088508 |
| Total | 73 | **3.387356** |

Cap USD 5. Each adapter refuses a call that would pass its own reservation or its 24-call limit (1 for the probe).
D1 used 2,671 input and under 100 output tokens per call on a much larger request, so the expected cost is a few
cents for the comparison arms; Opus depends on how much it thinks and is bounded by the table. D1-Opus spent
USD 1.47 on 72 calls with requests of about 3,600 input tokens.

**Hashes fixed before the run** (canonical JSON SHA-256 unless a file hash is stated):

| Object | SHA-256 |
|---|---|
| System prompt | `f39226260d16a160857f1bfe55be67e13bff98dbe03692dc197736e6185b9a74` |
| Decision schema | `c53c392e37efc6ad9e2d5a49efab38d1711164242ab8dd16d916642212a2b377` |
| Feasibility schema | `f3a727be98dc5dfb244f229739a1f264d1f3178b2f60a7f981f91f0d5f8506ab` |
| `canonical-facts.json` (file) | `aefa5bdd84f3f3265d032175bdd1133fe49742d5bc83c4f8c418ade6703311aa` |
| 24 item request hashes | `96708d089ce85515addcd2d8d59df80bc19ab60e3f3967784412a7596d4ef132` |
| 72-row order (call id, item, model) | `29bf22351c10b89deb151594a4993ddb058142213a70eda9574121fdbffb2bea` |
| 72 provider bodies | `ed5329b15eac84a4322ad956072280bffa2474b8d9c1ab507d54bdab6f3094fc` |
| Probe request | `3b0e358dbce07399ef0bc2be020ff8acd4328918020e58616f3031f54efc8593` |
| Probe provider body | `6789de77ae0adc21faf9c17d83b7618a733ee11058ae91557faca6e66453334d` |
| `src/diagnostic_v3_d2.py` (file) | `b6cf52383b2b9ac13d66c354a87e3de5e515d08cc3fe4c588c97306e49437d08` |
| `src/providers.py` (file, unchanged) | `22a2e672aeb168ab630bcc65ca2eb9838be910f332820b221720ffa09d82d500` |
| Retained Q0 archive (file) | `2c72a9023a0b7b1f346a63bc15ded64d48ddb9739992c89b76ccc9c48166f64e` |

The frozen manifest also records the commit and the hash of all 19 source files and four planning documents. The
manifest hash and the pinned commit are recorded in `benchmark-v3/d2/launches/` in a later commit, because the
manifest contains the hash of this file. The run stays pinned to the commit that contains this file.

**Failure handling.** A provider error, a timeout, a refusal, an output-ceiling stop or an answer that fails the
strict schema is recorded with an allowlisted reason and no raw error text, counts as invalid, and the schedule
continues. Nothing is retried. A timeout or transport error after dispatch is marked `outcome_unknown` and never
sent again. Dispatch stops on a returned model id that differs from the requested one, cached-token usage, a local
call or dollar limit, the one-hour deadline or the stop marker. Unstarted assignments stay in the denominators. A
model with any invalid, missing or unstarted item gets no screen reading. The Opus adapter records refusals with
their category separately from other failures. A failed probe blocks the batch.

**Regression and competence checks.** 29 D2 tests, 15 D1 tests and 57 v3 tests pass on the server (Python 3.12.3)
at the pinned commit; the D2 tests also pass locally (Python 3.9.6). Verified on both machines: all 48
canonical values equal the retained clean Q0 records. The paid path is covered by tests with a stubbed HTTP layer;
it has not been exercised against the provider, which is what the probe is for.

**Server, credentials, artifacts.** `sim-dmarz-3`, claim `dmarz-discussion-v3-d2`, exclusive, until
2026-10-04T15:33Z; preflight requires 90 minutes left. Credential by alias only, memory only. Private journal and
outcomes stay on the server and in the operator's private directory; the hub receives counters and a hash-indexed
private artifact set. Public tables contain scores and accounting only.

## What result means what

For each model with 24 valid answers and complete usage:

- 6/6 and 18/18: the compact representation and contract are nominated for a separate test followed by fresh
  qualification under the unchanged thresholds. D1 is not promoted.
- 18/18 but fewer than 6/6: individual predicates are applied correctly and the selection step fails; the next
  proposal examines decision composition. The composition table shows whether the model's own booleans already
  imply the right choice.
- Fewer than 18/18 and fewer than 6/6: inspect predicate, task and interface semantics before another model or a
  swarm. A feasibility count at or below 12/18 is no better than answering "infeasible" every time.
- 6/6 but fewer than 18/18: inconsistent; not nominated as repaired.
- Opus passes and a comparison arm fails: consistent with model strength or thinking mattering on this contract;
  the run cannot separate the two. Together with D1-Opus it says Opus is at ceiling on both formats.
- Opus fails a screen: unexpected after D1-Opus; report it and compare item by item with `d1o-a1` before
  interpreting, since the two runs differ in packaging, contract and output ceiling.
- A comparison arm passes: the D1 failure for that model is associated with D1's packaging or contract; the run
  cannot say which removed component.

## Visualization mapping

`d2-call-ledger-v1`, in the plan. Bindings: hub run `discussion-dose-v3/v3-d2-a1`; x is terminal call count 0 to
72; time origin is service start; series are started, terminal, physical calls, invalid, missing usage and observed
cost. No frame or replay artifact: the run has no agent state over time, so an animation would invent structure.
Fallback and history: hub counter series plus the private hash-chained journal. The selftest drives the observer
with a fake hub client through a normal run and a run with 24 invalid answers and checks the counters, the
done/fail status and that no vote, boolean or score appears in any hub message. After the run the final counters
are checked against the 72 saved records.

## Gate decision

Diagnostic-only, ready for the rehearsal. If the rehearsal audit, readback or duplicate refusal fails, repair and
re-rehearse before asking for the go. If the probe fails, stop and return to the reviewer. If the batch ends with
invalid or missing items, report them as they are; do not rerun for a cleaner table.
