# Pre-run assessment: S1-Q, S1-R and S1-L (attempts s1q-a1, s1r-a1, s1l-a1)

## Manifest m3 (written 2026-10-04 UTC by dmarz/orbital-orchestrator, before any m3 model output)

This section governs attempts s1q.2-a1, s1r-a1 and s1l-a1 under manifest m3. The m2 and m1 sections below are kept as written; where they differ, this section applies.

- Parent attempts: s1q.1-a1 under m2 failed competence, 9 of 12 correct ([s1q1-post.md](s1q1-post.md)); s1q-a1 under m1, 7 of 12 ([s1q-post.md](s1q-post.md)). S0 under m3 is attempt s0-a4 (below).
- Change: README section 11, A6. `claude-opus-5-5`, adaptive reasoning at effort medium, 4,096-token allowance per call, no temperature, USD 4 / 20 per million, qualification set 2 (namespace `s1q.2`), study cap USD 500 (375 public / 125 auxiliary). Prompts, generator, scorer, arms and gates are unchanged.
- Authorization: dmarz, directly in the operator session at ~08:00 UTC: "switch SOC-07 to Opus 5.5" and a new cost cap $500. Cross-researcher review remains waived. Exploratory.
- Prediction for S1-Q.2: a reasoning model clears 10 of 12 on the clean task. If it does not, the chain stops and the decision goes to dmarz.
- Interface risk: the reasoning path has been tested only against a fake transport. One probe call through the study adapter, outside the study's worlds, is made after deploy and before S1-Q.2; a failed probe blocks the launch.
- Expected spend (estimate, not a measurement): S1-Q.2 at most about USD 1.1 (12 calls at the worst case of input plus 4,224 output tokens). S1-R and S1-L are estimated from S1-Q.2's measured tokens per call and reported; cost is not a gate per dmarz. Every run reports `cost_usd` to the hub.
- Chaining: per dmarz's goal of keeping runs going, S1-Q.2, S1-R and S1-L run back to back; each starts only when the launcher's software gate for the previous stage has passed at the same fingerprint, and the chain stops by itself at a failed gate.
- Server and claim: sim-dmarz-8, exclusive claim `dmarz-soc07-private` (extended to cover the chain). Live ledger on sim-dmarz-8.
- Instrument repair (A6): the decision rule now states that delivery at or before the deadline meets it, matching the generator and scorer. S0 s0-a4 ran at the superseded fingerprint `f8c2c3d0…` before this repair and is kept as run; s0-a5 is the S0 for this fingerprint.
- Runtime fingerprint: `7237fa8a794d68304d4b98a948cc9ff6c857075e9a19a6a38ae436f502d2272e`. Self-test 59 run, OK with 2 skipped, on orbital-one.
- Visualization mapping: v1, unchanged.
- S0 under m3 (s0-a5): result recorded here after it runs and before the approval is written.

## Manifest m2 (written 2026-10-04 UTC by dmarz/orbital-orchestrator, before any m2 model output)

This section governs attempts s1q.1-a1, s1r-a1 and s1l-a1 under manifest m2. The m1 assessment below is kept as written; where they differ, this section applies.

- Parent attempts: s1q-a1 under m1 failed competence, 7 of 12 correct and 12 of 12 valid ([s1q-post.md](s1q-post.md)). Nothing else ran under m1. S0 under m2 is attempt s0-a3 (below).
- Change: README section 11, A5. `claude-sonnet-4-6`, thinking off, temperature 0.7, caps 256 / 256 / 64 / 64 and qualification 128, USD 3 / 15 per million, qualification set 1 (12 fresh worlds, namespace `s1q.1`). Prompts, generator, scorer, arms, gates and the USD 40 cap are unchanged.
- Authorization: dmarz instructed the operator to "use a strong model that's great" after the m1 failure. That instruction is the go for m2. dmarz/fleet-monitor reviewed m1 only; its review does not cover m2 and no m2 record is written in its name. Cross-researcher review remains waived ([launch/review-waiver.md](../launch/review-waiver.md)). Exploratory.
- Expected finding: unknown. Prediction for S1-Q: a stronger model clears 10 of 12 on the clean task. If it does not, the study stops under m2 and the next decision goes to dmarz; a bounded reasoning allowance is the remaining permitted change.
- Gates: unchanged. S1-Q.1 needs at least 10 of 12 correct and 11 of 12 valid with no halt; S1-R needs `gate_passed = 1`; the launcher refuses a stage whose prerequisite did not pass at the same fingerprint.
- Runtime fingerprint (all `src/*.py`, `design.json`, `execution.json`, `experiment.json`, `requirements.txt`): `475140d431efd134de71f71d1a043b94e14d368018f4a7ae156bc08e0226a350`. Self-test 58 run, OK with 2 skipped, on orbital-one.
- Expected spend (estimate: m1's estimate times three for the price change, not a measurement): S1-Q.1 about USD 0.04, S1-R about USD 3, S1-L about USD 18; about USD 21 in total, under the unchanged USD 40 cap. The m1 ledger (USD 0.010669 for s1q) is carried forward on the new host, so the cap covers both manifests.
- Server and claim: a fresh one-run box, sim-dmarz-8 (agentops fleet, created for this run because sim-dmarz-3 now holds another experiment), exclusive claim `dmarz-soc07-private` by dmarz/orbital-orchestrator. The study ledger is copied from sim-dmarz-3 before any m2 call and the sim-dmarz-3 copy is retired.
- Visualization mapping: v1, unchanged.
- S0 under m2 (s0-a3): hub run `soc07-private-judgments/eed24e49` on sim-dmarz-8 at revision 45f9c48d07b9be865c8e1e1ba5a1f341706ba1bc, fingerprint 475140d4…: done, 69 of 69 checks on 60 fixtures, 4 policies and the fault injections; 0 model calls. Server self-test 58 run, OK with 2 skipped. The carried ledger on sim-dmarz-8 is byte-identical to the sim-dmarz-3 copy (SHA-256 471a7635…, 12 calls, USD 0.010669); sim-dmarz-8 holds the live ledger from here on and the sim-dmarz-3 file is retired.

- Experiment / owner / stages: soc07-private-judgments / dmarz (agent dmarz/soc07-private) / S1-Q qualification, S1-R controlled replay, S1-L live teams. Written 2026-10-04 UTC, before any model output.
- Parent attempts: s0-a1 and s0-a2 (scripted, fleet), see [s0-post.md](s0-post.md). No earlier paid attempt exists.
- Status: **blocked until the reviewer's explicit go**, then ready. Reviewer: dmarz/fleet-monitor. Cross-researcher review is waived by dmarz ([launch/review-waiver.md](../launch/review-waiver.md)); this is a same-researcher check and is not independent approval. Everything is exploratory. S2 is closed.
- Question and decision: does withholding five agents' first answers until after one discussion round change the correctness of the team's final decision, compared with publishing them first, on this generator and this model? S1 decides only whether a confirmation would be worth planning and how large it would have to be.
- Expected finding: unknown. A plausible and valid result is no difference, because after the factual release every communicating agent holds the decisive audit and the task is easy. That result would say this task cannot separate the protocols for this model; it would not say the protocols are equivalent.
- Uninformative if: S1-Q fails (the model cannot do the clean task); first answers in the minority regimes are not wrong where the design intends them to be (no opportunity to observe a correction or a corruption); validity is below the gate; or team success is at ceiling in every arm and regime (then only the revision and mismatch tables carry information).

## Design and assessment

- Closest evidence and comparator: section 1 of the [plan](../README.md). PUBLIC is the primary comparator. NEVER, PREPARE and VOTE are diagnostics. The full-information single solver in S1-Q is a competence check, not a cost-matched baseline.
- Units: the world is the cluster and the unit of inference. S1-R has 24 worlds and S1-L has 24 other worlds, 8 per regime, each run twice. Agents, messages, arms and repeats inside a world are not independent. With 8 worlds per regime every interval is descriptive.
- Pairing: within a (world, repeat) block the four arms PRIVATE, PUBLIC, NEVER and VOTE continue from one shared first pass; PREPARE generates its own. Arms run in a recorded random order inside the block. Arm order positions are random, not balanced (S1-L counts by position, first to fifth: private 11/10/11/10/6, public 7/10/10/9/12).
- Coverage: per stage and regime, half the worlds are decided by cost (gap bins 1-3, 4-10, 11-20) and half by feasibility; the displayed correct label is A in exactly half the worlds of each regime and flips on the second repeat. The special role rotates over agents but 8 worlds cannot balance 5 agents (S1-L: agents 0, 1 and 4 four times each, agents 2 and 3 twice each).
- Splits: S0 fixtures, S1-Q, S1-R and S1-L worlds come from different seed keys (the stage name is part of the key). The holdout root 730072 is not referenced by any code path.
- Manipulation check: reported per regime, never used to select episodes: first answers correct, wrong and abstaining; episodes with first-answer disagreement; eligible counts for both revision rates.
- Evaluator: deterministic, in [src/score.py](../src/score.py). The answer key is produced by the generator and re-derived for every world by a separately written solver before a stage starts; a mismatch aborts. Scoring goes through the per-repeat A/B mapping. No model judge.
- Truth separation: the context builder receives records, the display mapping and published board snapshots only. A truth canary is searched for in every request before dispatch; a hit blocks the call and halts the stage. Vault reads are logged and any read by a non-owner agent is counted on the episode.
- Primary metric: correct public team decision (at least 3 of the 5 assigned agents give the same valid A or B, and it is correct) over **all assigned** episodes, PRIVATE minus PUBLIC, averaged over repeats within world, worlds within regime, regimes equally weighted; stratified world-cluster bootstrap, 10,000 resamples, seed stream from 730073. A 5-point difference is the plan's practical threshold; S1 cannot resolve it.
- Timing: logical phases with barriers. Wall time is recorded per call and per episode; the 600-second decision deadline is scored but cannot bind (see the plan's section 11, A4 row 10).

## Launch manifest (recorded on every run)

| Parameter | Value in manifest m1 |
| --- | --- |
| Model id | `claude-haiku-4-5-20251001` |
| Reasoning allowance | off (0 tokens) |
| Temperature | 0.7 (omitted automatically if a reasoning allowance is ever set) |
| Per-call output caps | first answer 256, discussion 256, public final 64, private final 64, qualification 128 |
| Prices | USD 1 per million input tokens, USD 5 per million output tokens |
| Qualification set | 0 (worlds `s1q-w0000` to `s1q-w0011`) |

These live in `launch_manifest` in [execution.json](../execution.json), and are stamped on each hub run as `model`, `reasoning_tokens`, `output_caps` and `launch_manifest`, in the journal header and in `summary.json`. Changing any of them is a dated amendment, changes the runtime fingerprint, and therefore requires S0 again and a new approval record.

## Assignment manifest and call counts

| Stage | Worlds x repeats | Arms | Model agents per episode | Episodes | Calls: public path + auxiliary private = total | Manifest hash |
| --- | --- | --- | --- | --- | --- | --- |
| S1-Q | 12 x 1 | full-information single solver | 1 | 12 | 12 + 0 = **12** | `e9422b08f00dcc26…` |
| S1-R | 24 x 2 | private, public, never, prepare | 1 focal (+4 scripted peers) | 192 | 480 + 192 = **672** | `f3191b5561c36af2…` |
| S1-L | 24 x 2 | private, public, never, prepare, vote | 5 | 240 | 2,880 + 1,200 = **4,080** | `04c36e50daf12f2f…` |

The manifest hash covers the planned blocks, episodes and calls together with the runtime fingerprint and the launch manifest, so it changes whenever either changes. Per block: S1-R makes 1 shared first-pass call, 1 PREPARE first-pass call and 4 x 3 later calls (14). S1-L makes 5 + 5 first-pass calls and 5 arms x 5 agents x 3 later calls (85). Each call id is `stage/wNNNN/rNN/arm/aN/phase`, for example `s1l/w0007/r01/shared/a3/initial`; each episode id is `soc07-s1l-w0007-r01-a-private`. The full list of planned episodes and calls is written to `manifest.json` before the first call and uploaded with the run. Command to reproduce the numbers offline: `python3 -c "import sys; sys.path.insert(0,'src'); import study; print(study.manifest('s1l')['counts'])"` from the note directory.

Fixed inputs: development root 730071; bootstrap root 730073; streams world, allocation, labels, order, initial, policy, analysis. The API accepts no seed, so `initial` and `policy` seeds are recorded per call but do not control the model.

## Gates between stages

A stage is queued only if the previous stage's hub run is `done` with `gate_passed = 1` and the **same runtime fingerprint**, and the approval record covers it. This is enforced in [src/coordinator.py](../src/coordinator.py) and again on the server.

**S1-Q blocks S1-R when** fewer than 10 of the 12 answers are correct, or fewer than 11 of 12 are valid, or the stage halted or crashed. Valid means: the response ended normally, is exactly the requested JSON object and its confidence is between 0 and 1. ABSTAIN is valid but not correct.

- *Competence failure* (the 12 calls completed, but fewer than 10 correct or fewer than 11 valid): manifest m1 is not competent on this task. Nothing else runs under m1. I report to the reviewer with the per-world table (regime, kind, displayed labels, answer, validity reason). The next step is a dated amendment to the launch manifest (for example Sonnet with a bounded reasoning allowance, which is what passed in market-split tonight) with `qualification_set` 1, a budget entry for `s1q.1` (12 calls), S0 again because the fingerprint changes, a new approval, then a fresh S1-Q on 12 new worlds. No prompt is tuned against the 12 worlds already seen, and those worlds are not reused as evidence. If the second model also fails, the study stops as `blocked` and I say so.
- *Execution failure* (provider error, halt, crash, budget): not a competence result. I write the post-mortem, repair, and qualify again on a new qualification set through the same amendment route, because the 12-call cap of `s1q` is already spent.

**S1-R blocks S1-L when** any of these holds (all computed by `analyze.s1_gate` and reported as `gate_passed`): valid outputs below 95% of dispatched calls; budget, timeout or overflow failures at or above 5% of planned calls; more than 5% of the calls of any one phase truncated at the output cap (the plan then requires a caps amendment); any detected leak; any duplicate or unplanned call id; a halt or crash; or the focal agent's public final answer correct in fewer than 13 of the 16 clean-regime episodes in PRIVATE or in PUBLIC (the team prompts are first used here, and below that they would be suspect). The direction or size of any PRIVATE/PUBLIC difference in S1-R never blocks or unblocks anything. In addition, before asking to start S1-L I read every invalid output and the first-answer table by regime; if the minority regimes produce almost no wrong first answers, I say so in the S1-R post-mortem and the reviewer decides whether S1-L is still worth its cost.

**After S1-L** there is no further stage. The same software gate, without the clean-regime replay check, decides whether effect estimates are reported as usable or as diagnostic-only.

Between stages I stop, write the stage post-mortem and report to the reviewer; the next stage starts only after that report.

## Failure handling

- First-pass or discussion call fails (invalid, truncated, refused, timed out, refused by the budget, over the input limit): that participant makes no later call in the arm and has no final vote. A failed shared first pass ends the participant in PRIVATE, PUBLIC, NEVER and VOTE; PREPARE is separate. Its fixture facts are still released. PUBLIC shows `record unavailable`; boards show `message unavailable`. Raw malformed output is never shown to a peer.
- Public final fails: the private final is still collected. Neither final sees the other.
- Team decision keeps the 3-of-5 threshold whatever failed. ABSTAIN and missing votes never count. An unfinished episode counts as a failed decision in the assigned denominator and is listed as `interrupted` or `incomplete`.
- Every planned episode gets exactly one terminal record (`completed`, `interrupted`, `incomplete`) and a separate decision (`correct`, `wrong`, `no_majority`, `unavailable`); planned calls never reached are counted as `not_reached`.
- No resume and no automatic re-execution. The hub re-queues a silent run after 20 minutes; the worker refuses any second assignment. A new attempt is a new batch id with its own pre-run note and never replaces the earlier record.

## Retry policy

Zero answer retries and zero repair calls, as planned. **Amendment A2:** at most 2 transport retries, only for HTTP 429 or 529, where the provider reports that it did not run the model; waits of 2 and 6 seconds or the provider's retry-after capped at 20 seconds; all attempts and waits inside the single 60-second request budget; every attempt counted against a per-stage attempt cap (18, 706 and 4,284). Timeouts and all other failures are final. Retried calls are reported as a count in each post-mortem.

Stage halt (no new calls): HTTP 400, 401, 403, 404 or 413; low credit balance; a response naming another model; reported cache usage; a billed amount above its reservation; missing usage; a blocked leak; public-path budget exhausted; five consecutive provider failures; the 4-hour stage limit.

## Budget reservation

- Enforced cap USD 40 for the study: USD 30 public-decision path, USD 10 auxiliary private finals, with separate call caps per stage and pool (table above). Hard `max_calls`: 12, 672, 4,080.
- One durable ledger on the server, shared by all three stages, appended under a file lock with fsync. Before dispatch the controller reserves `(request bytes + 1,024) x input price + output cap x output price`; request bytes bound input tokens from above. The largest possible reservation is USD 0.0187 per call. After the response the reservation is replaced by the billed amount from reported usage. An unknown outcome keeps its reservation. At most 5 reservations are open at once.
- Expected spend (an estimate from prompt sizes in the scripted run, about 4 bytes per token, not a measurement): S1-Q under USD 0.02, S1-R about USD 1, S1-L about USD 6; about USD 7 in total. Actual tokens, calls, attempts and dollars are reported per stage.
- Remaining shared allowance: dmarz's USD 500 total for all experiments; this study can commit at most USD 40 of it.

## Frozen execution plan

- Revision deployed and tested on the server: swarm-lab `61de92259f045fdd97255317a5f93dd0010119ad`. The paid stages will be pinned to the later commit that adds this file and, after the go, `launch/s1-approval.json`; neither file is part of the runtime fingerprint, so the fingerprint below must still match at that commit. If the review leads to a code or configuration change, the fingerprint changes, S0 runs again, and this section is re-pinned before the approval is written.
- Runtime fingerprint (all `src/*.py`, `design.json`, `execution.json`, `experiment.json`, `requirements.txt`): `afacff913d48c50a8fb5b00efd8775454cfbc62dba841a8f6be919ea7144d9fe`.
- Prompts hash (`prompts.py`, `contexts.py`): `231ca3a349410bd7ac391634f8d08ef3a4da9cfc146b5cadcfc41d06ba37198d`.
- Generator hash (`generate.py`, `seeds.py`): `f953c881242db9bce8886420fedbe5143fb80d3d4e78f846bd40423b7b138868`.
- Scorer hash (`score.py`, `parse.py`): `f379ca60223095f7852992ba3e4f143ae7ad05f4f46fc31ca97a02eb186868a5`.
- Public-world hashes: S1-Q `690f19736c9baa17…`, S1-R `adc4b28d5d03dce3…`, S1-L `73edca61d05e4c19…`. All of these are recomputed by the worker and written into `manifest.json`, the journal header and `summary.json`; a worker whose fingerprint differs from the queued run refuses to start.
- Server: Python 3.12.3, Pillow 11.3.0, standard library HTTP. One finite worker process, at most 5 requests in flight, 60 seconds per request, 4 hours per stage.
- Commands (private launcher, agentops): `scripts/run-soc07-private.py <commit> s1q`, then `s1r`, then `s1l`; `status` and `verify` after each. Credentials are referred to by alias only (`SWARM_MODEL_API_KEY`, `SWARM_MODEL_WORKSPACE_ID`), decrypted locally and passed over ssh standard input into the worker's environment.
- Server claim: `dmarz-soc07-private` on sim-dmarz-3, exclusive. Hub experiment `soc07-private-judgments`; one hub run per stage.
- Regression checks: 58 unit tests pass on the builder's machine with this file present; on the server at the deployed revision 57 pass and 1 is skipped (the approval-pinning test needs this file, which is committed after that revision). They include the full S0 suite and a scripted rehearsal of the complete paid path for all three stages (same manifest, ledger caps, reconciliation, analysis and frames, with a scripted provider and the approval gate substituted). S0 on the fleet: see [s0-post.md](s0-post.md).
- Not verified by running, because it needs a model call: the real HTTP exchange with the provider. The adapter is tested against a fake transport only. The request body has the same fields the sybil-scale-api adapter sent successfully tonight, with temperature 0.7 instead of 0 and, from S1-R on, several conversation turns. If the first S1-Q request is rejected as malformed, the stage halts after one call and that is an execution failure handled as described above.

## Visualization mapping

- Mapping version v1, source [src/render.py](../src/render.py) at the pinned revision. One hub run per stage; bindings: `stage`, `batch`, `source_hash`, `code`, `model`, `reasoning_tokens`, `output_caps`. Arms and worlds are inside the run; each episode record carries world, repeat, arm, regime and seed inputs.
- Behaviour to make visible: whether teams reach the correct decision in each arm and regime, and how often first answers are corrected or corrupted on the way.

| Recorded signal | Unit, denominator | Visual encoding | Actor-visible or evaluator-only | Missing or failed |
| --- | --- | --- | --- | --- |
| `decision == correct` per episode | count over assigned terminal episodes of a (regime, arm) cell | bar height, labelled k/n; three regime groups; arm colours private teal, public gold, never violet, prepare blue, vote grey; fixed 0-100% axis | evaluator-only | a cell with no terminal episode shows "pending", never a zero bar; an unfinished episode is not drawn as a decision and is counted in "not completed" |
| `transition_public.useful`, `.eligible_useful` | wrong-to-correct over first answers that were wrong, all agents pooled | table row per arm, k / n | evaluator-only | "pending"; PREPARE row states that revision is undefined |
| `transition_public.harmful`, `.eligible_harmful` | correct-to-wrong over first answers that were correct | table row per arm, k / n | evaluator-only | same |
| S1-Q: `decision`, `valid` | counts over 12 worlds | bars per regime plus a line with the gate | evaluator-only | same |
| blocks done, episodes recorded, not completed, failed calls | counts | status line | operator | always shown |
| unique calls, input and output tokens, stage cost | provider-reported usage | footer line | operator | zero until the first response |

- Time axis: completed blocks (logical), 0 to 12 for S1-Q and 0 to 48 for S1-R and S1-L. Elapsed wall time is printed, not used as an axis. Arms are compared within the same frame.
- Event markers: none inside a frame; a halt appears in the hub message and in the status line counts.
- Cadence: `progress.png` re-rendered and uploaded at most every 20 seconds and at the end. Replay: at most 25 frames sampled evenly from the per-block prefixes, first and last included; 1800 x 1200 pixels.
- Live view: the latest `progress.png` on the run page. Final: `final_frame.png` (sent first among the final images so that it fills the contact sheet), `replay.gif`, `initial_frame.png`. No `frame.json`: the site's point-cloud view does not fit a non-spatial study, so the image and GIF are the supported fallback.
- History for replay: `episodes-<stage>.jsonl` in completion order and the hash-chained `journal-<stage>.jsonl` (every call with its rendered messages, raw output, usage, seed and snapshot hashes) stay on the server and are uploaded compressed as team-private artifacts. Public images contain aggregates only: no credentials, addresses or individual answers. Truth never enters an agent context.
- Uncertainty is not drawn: with 8 worlds per regime, intervals belong in `analysis.json`, next to the counts.
- Validation done: empty, partial, failed and complete traces render at 1800 x 1200 in the unit tests; the scripted rehearsal checks the GIF frame count against the summary; the S0 fleet frames were compared with the recorded counts (see s0-post.md).
- Rendering failure policy: a failed progress render or upload is recorded in `reporting_errors` and never stops or changes the run. A failed final upload fails the hub run but leaves the complete record on the server. Artifact owner: dmarz/soc07-private.
