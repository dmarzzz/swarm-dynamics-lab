# D2 run plan with the Opus amendment: v3-d2-a1

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/v3-d2-opus; source `aef218e8` ([registry](../../../../../evidence-metadata.json), [rubric](../../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On a compact fact table with a one-field answer, Opus 5.5 answers the six D1 worlds without error (6/6 decisions, 18/18 single-option feasibility checks) while Sonnet 4.6 and Haiku 4.5 each score 5/6 and 16/18 and miss the same two sum-over-budget options. Basis: Measured: 72/72 valid, exact-source audit recomputed all outcomes, known-answer controls discriminate. Limits: six reused dependent world clusters, one response per item with no repeats, only two sum-violating options, and the Opus arm differs from the comparison arms in thinking, effort, sampling and output ceiling.
- **sample_size_summary:** Observed: 72/72 assigned calls valid and analyzed (24 per model: 6 decisions + 18 single-option checks) on 6 reused development world clusters; 3 models on identical items; one response per item; not 72 independent samples. Plus 1 uncounted Opus probe.
<!-- experiment-evidence:end -->

Prospective plan, 2026-10-04 UTC, by `dmarz/v3-d2-opus`. Parent attempt `v3-d1-a1`. The design is
[D2-PLAN](../D2-PLAN.md), published as plan-only by `dmarz/discussion-bench-v3`; that file is unchanged. This
document is the dated amendment that turns it into a run and adds Claude Opus 5.5. Where the two differ, the
differences are listed under [Amendment](#amendment-2026-10-04-what-differs-from-d2-plan). Read with the
[setup record](SETUP.md), the [pre-run assessment](../../reviews/v3-d2-a1-pre.md), the
[D1 results](../RESULTS-D1.md) and the [D1 post-mortem](../../reviews/v3-d1-a1-post.md).

Status at this commit: implemented and tested, **no model call made**. A paid run needs an explicit go from the
reviewer, `dmarz/fleet-monitor`. That review is a same-researcher check under dmarz's review waiver. It is not an
independent review and must not be described as one.

## TLDR

D1 found that Haiku 4.5 and Sonnet 4.6 extracted every fact correctly and still chose infeasible options (2/6 and
3/6 correct full decisions against a 5/6 gate). D2 asks the same six open development worlds, 20001 to 20006, in the
simplest form: a compact table of the complete facts, then either one full decision or one yes/no feasibility check
for a single option.

`v3-d2-a1` makes **72 assigned calls**: 24 fixed items (6 canonical decisions and 18 single-option feasibility
checks) for each of three models. **Claude Opus 5.5 (`claude-opus-5-5`) is the model under test and its 24 items are
the primary result.** Sonnet 4.6 and Haiku 4.5 answer the same 24 items as the matched comparison arms the D2 plan
defines. They are kept for the paired contrast with D1's models; they are not new model tests.

Success for a model is 6/6 canonical decisions and 18/18 feasibility checks with every response valid. Answering
"infeasible" to everything scores 12/18, so the feasibility count is always shown beside that baseline.

Context added before any D2 call: the separate [D1-Opus run](../../d1-opus/RESULTS.md) (`d1o-a1`, another agent)
finished on 2026-10-04 08:00 UTC. On D1's original evidence packaging Opus 5.5 chose correctly in 6/6 of these
worlds and passed a fresh clean gate 12/12. Opus therefore already clears the v3 baseline, and D2 is not on the
path to qualifying it. What D2 adds is an account of why Haiku and Sonnet failed (does a compact fact table repair
them, and can they judge one option at a time) and whether Opus is also at ceiling on the compact format.

Limits: six reused development worlds, one response per model and item, no fresh qualification, no swarm, no
discussion treatment. The Opus arm cannot use the same request settings as the comparison arms (see Setup), so an
Opus difference is a difference of model and configuration together.

## Question and prediction

Question: when the complete facts are given as a compact table and the response contract is one vote or one
boolean, does Claude Opus 5.5 apply the stated constraints correctly on the six worlds where Haiku 4.5 and
Sonnet 4.6 failed in D1, and can each model classify the feasibility of each option taken alone?

This is a diagnostic sub-question of [SEC-47](../../QUESTION-LINKS.md): baseline decision errors have to be
separated from failures caused by corrupted child returns or merge behaviour before another swarm run. It does not
test SOC-07 disclosure, discussion dose, a merge defence or the SEC-52 extension. No new formal hypothesis is made.

Prediction to examine (from D2-PLAN, unchanged): complete explicit facts and a small response contract reduce the
decision failures seen in D1. Added for the Opus arm: Opus passes both screens, as its 6/6 on the original
packaging suggests. Every other outcome is reportable: atomic errors that remain, correct atomic judgments with a
wrong selection, a model that passes one screen and fails the other, an Opus arm no better than the comparison
arms, or an Opus arm that does worse on the compact format than it did on D1's.

A pass nominates a representation and contract for a later, separate test. It does not establish why D1 failed,
does not promote D1 and does not qualify a model or a swarm.

## Setup

**Worlds and items.** Worlds 20001 to 20006, two each of the capacity, total-cost and dependency families. All six
are kept, including worlds a model got right in D1. Each world has three options and exactly one feasible option.
Per model: 6 decision items and 18 feasibility items, with 6 feasible and 12 infeasible options.

**Canonical facts.** [canonical-facts.json](canonical-facts.json) holds, for each world, the family, the public
instruction sentence, the rule thresholds, the option list and all fact values: 48 values in total. It holds no
winner, feasibility label, attack target, earlier model answer or evaluator verdict. `prepare` rebuilds the table
from the world generator and compares all 48 values with the retained clean Q0 full-evidence requests, whose bytes
are bound to the published Q0 receipt, before freezing.

**Requests.** A decision request gives the task (`family`, `instructions`, `rules`, `options`) and every fact for
all three options. A feasibility request gives the same `family`, `instructions` and `rules`, one option letter and
only that option's facts. Fact keys are the same as in D1 (`A.power`, `B.days`, ...). Catalogs, completion domains,
source policy, report wrappers and claim extraction are left out. The system prompt is new and short; its exact
text is `SYSTEM` in [diagnostic_v3_d2.py](../../src/diagnostic_v3_d2.py). Responses are strict structured output:
`{"vote": "A|B|C|ABSTAIN"}` or `{"feasible": true|false}`, nothing else. The schema checks syntax only; a wrong
vote or boolean is a measured outcome.

**Settings per model.** Prices are USD per million tokens from the official pricing page, read 2026-10-04. Model
ids were confirmed available on this account through the Models API (a metadata read, no inference) on 2026-10-04.

| | Opus 5.5 (model under test) | Sonnet 4.6 (comparison) | Haiku 4.5 (comparison) |
|---|---|---|---|
| Model id | `claude-opus-5-5` | `claude-sonnet-4-6` | `claude-haiku-4-5-20251001` |
| `temperature` | not sent (the model rejects sampling parameters) | 0 | 0 |
| Thinking | always on, adaptive; `thinking` field not sent | off (field not sent) | off (field not sent) |
| `output_config.effort` | `high`, set explicitly (the documented default is `medium`) | not sent | not sent |
| `max_tokens` | 4,000 (thinking counts against it) | 2,000 | 2,000 |
| Structured output | `output_config.format`, JSON schema | same | same |
| Fallback model | none (`fallbacks` not sent) | none | none |
| Adapter | `OpusAdaptive`, new subclass | D1 adapter, unchanged | D1 adapter, unchanged |
| Price in / out | 4 / 20 | 3 / 15 | 1 / 5 |

All three: the same system prompt, user content and schema; input ceiling 60,000 bytes; request timeout 120 seconds;
no tools; no retries; no repair call; no prompt caching. The comparison arms keep D1's settings exactly. The Opus
arm differs from them in four request settings because the API leaves no choice: Opus 5.5 returns an error for
`temperature` and cannot turn thinking off. Thinking is billed as output and counts against `max_tokens`, so the
Opus ceiling is 4,000 instead of 2,000 to keep a truncated answer from being mistaken for a wrong one. Effort is
`high` because D1-Opus ran these worlds at `high`: the two Opus runs then differ in evidence packaging, response
contract and output ceiling (16,000 there), not in effort. D1-Opus averaged about 300 output tokens per call on
larger requests, so 4,000 leaves room.

**Server and budget.** Existing server `sim-dmarz-3`, exclusive claim `dmarz-discussion-v3-d2`, one worker. Hard
limits: 24 calls per model adapter, 72 assigned calls, plus one Opus compatibility probe. Dollar cap USD 5, given
for this run inside dmarz's standing USD 500 pool. Worst-case reservation from serialized request sizes and the
output ceilings: Opus 2.129232, Sonnet 0.877068, Haiku 0.292548, probe 0.088508, total **USD 3.387356**. Each
adapter is capped at its own reservation, so the cap cannot be exceeded.

## Protocol

1. **Freeze.** Source, the fact table, this plan, the setup record and the pre-run assessment are committed.
   `prepare` records the commit, the hashes of every source file and planning document, the immutable public URL of
   this plan, the Q0 check, the system prompt and schema hashes, the settings above and the 72-row schedule with a
   request hash, a provider-body hash and a reservation per row.
2. **Order.** Items are shuffled once with a committed seed. The three calls for an item run back to back in one of
   the six possible model orders. The six decision items take each order once and the eighteen feasibility items
   take each order three times, so each model is first, second and third exactly eight times. Each call is an
   isolated stateless request: one model, its own input, no tools, no shared memory. No model sees another request
   or answer.
3. **Rehearsal.** The same harness runs all 72 assignments on the server with scripted known-answer controls in
   place of the models (always right, always "infeasible", always "feasible"), as hub run
   `discussion-dose-v3/v3-d2-a1-rehearsal`, labelled as scripted and not model evidence. It makes zero model calls.
   Its audit, artifact readback and duplicate-dispatch refusal are checked before any paid step.
4. **Admission.** `preflight` verifies the frozen manifest against the committed source, the three native request
   serializations for all 72 rows, the three model ids through the Models API, the immutable public plan bytes and
   page, the dollar cap, the claim (at least 90 minutes left) and the rehearsal evidence. It makes no inference call.
5. **Compatibility probe.** One Opus call on a hand-written synthetic feasibility request that is not one of the 24
   items and comes from no world id. Its only purpose is to confirm that the Opus request settings are accepted and
   a parsed answer comes back, so a rejected setting cannot burn the 24 Opus assignments. It is recorded, capped at
   one per attempt, and is never counted in any result. If it fails, the batch does not start and the reviewer
   decides what happens next.
6. **Run.** One systemd unit with no restart and a 65-minute hard limit; the harness admits new calls for at most one
   hour. A permanent ledger marker and process lock precede the first call, and a second start is refused even with
   a different output path. Every request and response is written to an fsynced hash-chained journal before the next
   call. A provider failure or invalid answer is recorded and the fixed schedule continues. A returned model id that
   differs from the requested one, an accounting anomaly, a local limit, the deadline or the stop marker
   `v3-d2-a1.stop` ends dispatch. A call whose outcome is unknown is never sent again.
7. **Audit and close.** The exact-source auditor recomputes every request and score from the journal. Artifacts are
   uploaded with a hash index and read back. Results and a post-run review are published, then the claim is
   released. No successor starts.

## Metrics

All 72 assigned calls, reported per model: started, terminal, valid, failed by allowlisted reason, unstarted, unresolved,
returned model id, usage completeness, input and output tokens, observed cost and latency. Unknown usage is not
zero. A missing or invalid answer is never counted as correct. The probe is reported separately.

- **Canonical decisions**, out of six per model: correct, wrong non-abstaining, abstain, invalid; whether the chosen
  option is feasible; constraint violations; per family (two worlds each). Screen: 6/6.
- **Feasibility checks**, out of eighteen per model: correct; true positives out of 6; true negatives out of 12;
  each world's three-option vector; per family (six checks each). Screen: 18/18. Always shown with the
  always-infeasible baseline of 12/18 and the always-feasible baseline of 6/18.
- **Composition**, no extra call: from a model's own three booleans for a world, pick the best predicted-feasible
  option with the unchanged objective and alphabetical tie-break. Report none predicted feasible, more than one
  predicted feasible, and disagreement with that model's canonical vote. One invalid boolean makes that world's
  derived decision missing.
- **Paired items**: per-item correctness for the three models on identical inputs, and the differences Opus minus
  Sonnet, Opus minus Haiku and Sonnet minus Haiku. The Opus result is reported first.

Reading, fixed before the run, per model with all 24 responses valid and usage complete:

| Canonical 6/6 | Feasibility 18/18 | Reading |
|---|---|---|
| yes | yes | Nominate this representation and contract for a separate test, then fresh qualification under unchanged thresholds |
| no | yes | The next proposal looks at decision composition |
| no | no | Inspect predicate, task and interface semantics before another model or a swarm |
| yes | no | Report the inconsistency; the configuration is not nominated as repaired |

No confidence intervals, significance claims, automatic model selection or automatic successor. `model_qualified`
is always false for D2. Schemas and scores are not relaxed after a failure.

## Amendment, 2026-10-04: what differs from D2-PLAN

1. **Opus arm added; 72 calls instead of 48.** dmarz asked for testing with a strong model and then said to use Opus
   going forward, as relayed to this agent by `dmarz/fleet-monitor`. Opus 5.5 is therefore the model under test.
   The Haiku and Sonnet arms are the plan's own 48 calls, unchanged in items and settings.
2. **The Opus arm is not request-identical to the comparison arms.** D1 and D2-PLAN hold temperature 0 and thinking
   off. Opus 5.5 rejects both settings. The arm sends no sampling parameter, runs with thinking on at effort
   `high`, and has a 4,000-token output ceiling. What the arm can show: whether Opus 5.5, at the effort level
   D1-Opus used, is also at ceiling on the compact D2 contract, on the same items the weaker models are asked.
   What it cannot show: that model identity alone explains a difference from the comparison arms, how Opus behaves
   at another effort level, or a clean packaging effect for Opus, because the comparison with D1-Opus is across two
   runs with different output ceilings and both are expected to sit at ceiling.
3. **Order.** D2-PLAN alternates the first model 12/12 between two models. With three models the order is balanced
   over the six permutations as described in Protocol. Haiku still precedes Sonnet in exactly 12 of 24 items.
4. **One Opus compatibility probe**, added on the reviewer's instruction after another study's Opus batch failed
   24 of 24 on a rejected request setting. D2-PLAN adds no inference probe. The probe is outside every denominator.
5. **Launch route.** D2-PLAN says a later launch goes through the always-on run queue to a dedicated server. This
   run is operated from the fleet-monitor session's machine on the existing server `sim-dmarz-3` under its own
   exclusive claim, on dmarz's instruction as relayed by `dmarz/fleet-monitor`. No server is created or destroyed.
6. **Budget.** D2-PLAN reserves inside the shared USD 500 pool at admission. This run has a USD 5 cap from the
   reviewer. This agent did not re-reconcile the whole pool.
7. **Review.** Same-researcher check by `dmarz/fleet-monitor` under dmarz's waiver; no independent review.
8. **Details D2-PLAN left open**, fixed here before any model output: the request shapes, the system prompt, the
   meaning of ABSTAIN (the instructions select no option), the seeded order, and the rehearsal controls.

Unchanged from D2-PLAN: the six worlds, the two probe types, the item counts per model, the response contracts,
the comparison arms' models and settings, the screens, the composition rule, the interpretation table, no retries,
no fallback, and that Q1 IDs 50001 to 50006, confirmation IDs 30000 to 30023 and the sidecar namespace stay closed.

## Visualization mapping: d2-call-ledger-v1

Same form as D1's `d1-call-ledger-v1`. The run is 72 independent calls, not a swarm, so there is no agent animation.
The hub run `discussion-dose-v3/v3-d2-a1` reports counters only: assigned 72, started, terminal, physical model
calls, invalid, missing usage and observed cost, against terminal count 0 to 72 with the service start as time
origin. Scores are not sent to the hub during the run; they are published in the results after the audit. The
fallback and the durable history are the hub counter timeline plus the private hash-chained journal and the
published per-item tables. The rehearsal uses its own run id ending `-rehearsal` and says in every message that it
is scripted and not model evidence.
