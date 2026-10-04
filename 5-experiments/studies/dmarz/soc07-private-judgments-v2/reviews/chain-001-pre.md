# Pre-run assessment: SOC-07 v2, chain 001 (s0-a1, p0-a1, s1q-a1, s1r-a1, s1l-a1)

Follows [RUN-REVIEW.md](../../../../toolkit/agent-experiments/RUN-REVIEW.md) and the [pre-run template](../../../../toolkit/agent-experiments/templates/pre-run.md). This is the owning operator's assessment, written 2026-10-04 UTC before any v2 run. It is not an independent review and not launch permission.

- Study / owner / stages / attempt / parent: soc07-private-judgments-v2 / dmarz (operator dmarz/orbital-orchestrator) / S0, P0, S1-Q, S1-R, S1-L / chain 001, attempt 1 of every stage / parent study soc07-private-judgments (design v1), manifest m3.
- Status: **ready for launch on dmarz's go; blocked until then.** No approval record exists (`launch/s1-approval.json` is absent at the commit that adds this file). Every paid stage refuses to start without it.
- Previous post-mortems read: v1 [s1q-post.md](../../soc07-private-judgments/reviews/s1q-post.md) (Haiku, 7 of 12), [s1q1-post.md](../../soc07-private-judgments/reviews/s1q1-post.md) (Sonnet 4.6, 9 of 12), [s1q2-post.md](../../soc07-private-judgments/reviews/s1q2-post.md) (Opus 5.5, 12 of 12). The v1 S1-R result is in its hub run summary (`soc07-private-judgments/807dfab8`); the v1 S1-L post-mortem will state that the ceiling was already visible in S1-R.
- Researcher review: waived by dmarz for SOC-07 ([launch/review-waiver.md](../launch/review-waiver.md)); dmarz/fleet-monitor reads the package before it is queued (same-researcher check).

## Question, design and precision

- Question and decision: does keeping first answers private until after one discussion round change team accuracy, relative to publishing them, on a task where first answers actually disagree? The decision is whether a confirmation would be worth planning; nothing here is confirmatory.
- Why a new design version: v1 S1-R on Opus 5.5 reached team success 1.00 in PRIVATE and in PUBLIC (difference 0.000, 192 of 192 episodes, 672 of 672 valid calls, measured). The comparison had no information at that difficulty.
- Prediction: PRIVATE at least as good as PUBLIC; better in the informed-minority regime. Plausible null: Opus solves eleven-record worlds with reasoning as reliably as five-record ones, and teams sit at ceiling again. Uninformative if the manipulation check is below 50% or both arms are at ceiling; S1-L reports both.
- Independent unit: the world (24 S1-L worlds, 8 per regime). Arms, repeats and agents within a world are paired and dependent; intervals resample whole worlds within regime.
- Allocation: S1-Q 12 worlds; S1-R 24 worlds x 2 repeats (192 episodes, one focal model agent and four scripted peers); S1-L 24 worlds x 2 repeats x 5 arms (240 episodes, 5 model agents). No power claim: this is a pilot sized for feasibility, as in v1.
- Difficulty and mechanisms: three options; eleven records with superseded estimates; conflicting-audit worlds where the first audit alone points to a wrong option; cost margins 1-9; deadline-boundary worlds. Half the worlds are decided by cost, half by feasibility; audit patterns alternate.
- Splits: seed roots 731071 (development), 731072 (holdout, unused by any code path), 731073 (bootstrap). S0 fixtures, P0 (S0 fixture world 0), S1-Q, S1-R and S1-L worlds come from separate seed keys.
- Manipulation fidelity: offline, S0 checks that in every minority world the estimates-only answer differs from the full-record answer, and that the scripted evidence-following policy's first answers split in every minority episode. At run time, S1-L's `informative` gate requires at least 50% of minority-regime PUBLIC episodes to have non-unanimous valid first answers.
- Evaluator: deterministic scorer through the per-repeat label mapping; truth never enters a context (canaries checked in S0).
- Primary endpoint and stopping: as v1 (README Metrics); fixed sample, no effect-dependent stopping.

## Changes and unresolved issues

| Issue / prior evidence | Chosen change | Alternative explanation | Acceptance check and result | Owner / stage it blocks |
|---|---|---|---|---|
| v1 ceiling at S1-R (1.00 vs 1.00) | Harder three-option generator | The model is simply at ceiling on any rule-application task of this form | S1-L `at_ceiling` flag and manipulation check reported | none; S1-L reports it |
| No runtime check that first answers disagree | `manipulation_check` in analysis, `informative` gate for live mode | Disagreement could be high while teams still converge | Self-test: gate fails below 0.5 and passes at 0.5; S0 evidence-follower 40 of 40 minority episodes split | S1-L gate |
| Probe was ad hoc in v1 | P0 is a hub stage between S0 and S1-Q with its own ledger entry (1 call) | none | Self-test: `coordinator.params('p0')`, ledger caps for p0 | S1-Q (prerequisite) |
| Longer contexts | Input-token cap 8,192 and request-byte limit 32,768 (v1: 4,096 / 16,384); stage timeout 6 h (v1: 4 h) | none | Measured v2 request bytes: max 5,813 (final phase); v1 maximum reported input on Opus was 2,061 tokens | none |
| Stale-citation flag assumed one audit | Generalized: cites any superseded record without the record that superseded it | none | Self-test | none |

## Frozen execution and collection

- Runtime fingerprint (all `src/*.py`, `design.json`, `execution.json`, `experiment.json`, `requirements.txt`): `4c3065790a0879031c2380616412e466a58d59b79f746f0a8f269cfca37ff292`. Hash groups: prompts `e592d2c0…`, generator `a76f4c2d…`, scorer `f257fe7c…`. Self-test 59 run, OK (0 skipped) on orbital-one, 2026-10-04. The approval record pins this fingerprint at launch; setup on the server must print the same value.
- Offline S0 on orbital-one (`src/worker.py --stage s0 --attempt local-s0-a1`, not a hub run): 73 of 73 checks, 1,500 scripted episodes, 21,300 scripted calls, 0 model calls. It ran while the stage time limit in `execution.json` was still 4 h; that limit does not affect S0, and the server S0 runs at the fingerprint above.
- Model and settings: `claude-opus-5-5`, adaptive reasoning, effort medium, 4,096-token allowance, no temperature, structured output per phase, no fallbacks, no tools. As v1 manifest m3, which ran 684 Opus calls with zero invalid responses (S1-Q.2 and S1-R).
- Collected: every planned call with its context hash, response text, usage, failure category and attempts in a hash-chained journal; one terminal record per planned episode; ledger events; hub metrics `model_calls`, `input_tokens`, `output_tokens`, `cost_usd`, `first_answer_split_share`, `at_ceiling`.
- Budget: own ledger at `/srv/swarm/soc07-v2-budget/ledger.jsonl` (empty at launch). Study cap USD 150 (110 public, 40 auxiliary), a runaway guard; cost is not a gate per dmarz. Hard call caps: P0 1, S1-Q 12, S1-R 672, S1-L 4,080. Estimate about USD 55 (README Cost estimate).
- Retries: only HTTP 429 and 529, at most two, within the 60-second request budget. No answer retries, no repairs.
- Allocation: a fresh dedicated server and exclusive claim `dmarz-soc07-private-judgments-v2`, taken at launch; one experiment and one run per server. Not taken by this commit.
- Credentials: aliases `SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`, passed over ssh standard input into process memory only.

## Visualization mapping

Mapping v1 of [render.py](../src/render.py), unchanged, with three-option labels:

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding | Actor-visible or evaluator-only | Missing/failure display |
|---|---|---|---|---|
| Episode `decision` per (regime, arm) | correct decisions / terminal assigned episodes | grouped bars per regime, one color per arm | evaluator-only | cell drawn as pending, never zero |
| Controller totals | calls, tokens, dollars, failures | header counters | evaluator-only | failures shown as a count |
| Blocks completed | logical time (blocks) | replay frame index | evaluator-only | unfinished blocks not drawn |

- Live view: `progress.png` every 20 s or at block completion; final frame `final_frame.png`; replay `replay.gif` over completed blocks; all 1800 x 1200.
- The manipulation-check share and the ceiling flag are hub metrics and summary fields, not frame elements.
- Acceptance: final frame matches `analysis.json` team-success counts; checked in the post-mortem.

## Admission

- Part A done (2026-10-04 ~10:00 UTC): S0 `s0-a1`, hub run `soc07-private-judgments-v2/f2131af5`, on sim-dmarz-3 at revision 26c20dab9af93969fd974534c32c24c8608c188d, fingerprint 4c306579…: 73 of 73 checks on 60 fixtures, 4 policies and fault injections; 0 model calls. Server self-test 59 of 59. Claim `dmarz-soc07-private-judgments-v2` (agentops PR 254).
- **Futility rule (added 2026-10-04 ~09:45 UTC, before any v2 data, on dmarz/fleet-monitor's same-researcher check):** v1 showed that a replay at team success 1.00 in both arms makes the live stage a null by construction. If S1-R ends with PRIVATE and PUBLIC team success both 1.00 in every regime (the `at_ceiling` flag), S1-L is not launched; the study stops there, that is reported as the result, and a harder generator is a new design version. The chain is therefore launched in parts: A `s0`; B `p0,s1q,s1r`; C `s1l`, only after the operator has read S1-R's hub metrics and `at_ceiling` is 0. The S1-Q gate is unchanged.
- Decision: ready for dmarz's go. Blocked on: approval record, fresh server, claim.
- Next action on go: follow SETUP.md "Launch", but in the three parts above (A, then B, then C after reading S1-R's `at_ceiling`); each part stops by itself at a failed gate. Part B waits until the sybil-scale-xl main stage has stopped calling the shared Opus workspace (expected 429s from ~09:55 UTC, and S1-Q tolerates only one invalid call). Server: sim-dmarz-3 (idle, unclaimed at 09:39 UTC).
