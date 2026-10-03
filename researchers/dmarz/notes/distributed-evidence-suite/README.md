# Distributed evidence experiment plan

Working design for SOC-07, SOC-09, SOC-08, SOC-19 and SOC-02. Prepared 3 October 2026 by dmarz/decision-suite-plan at the user's request to write and push the plan without shipping experiment code.

## Recommendation and scope

Build one small, objectively scored decision environment and use it for five studies of collective reasoning. Start with private initial judgments and evidence-seeking criticism. Then add evidence-based stopping, addressed communication and team-size comparisons. The purpose is to identify useful protocols at a fixed team resource ceiling, including when they cause harm. Faster agreement is not itself success.

This document is a **working plan for review**, not an accepted hypothesis, frozen preregistration or executable configuration. It contains proposed experimental choices and directional expectations, not findings. The user explicitly requested this plan before implementation; it stays in researcher notes pending the normal research gates. This task adds documentation only. It does not launch models, claim servers, create a formal experiment or authorize spending.

The existing [SOC-07 plan](../soc07-private-judgments/README.md) remains the standalone disclosure study. This suite reuses its fixture and disclosure semantics but proposes a smaller shared first study with a critic factor. It does not silently replace that plan's five-arm design, replay study, private-final probes, sample allocation or adoption criteria. Register either design explicitly; do not combine their counts or call results from one a replication of the other.

| Study | Candidate | Main decision | New capability beyond the common runner |
| --- | --- | --- | --- |
| A | SOC-07 and SOC-09 | Does private preparation help, and does an evidence-seeking critic improve correction? | Disclosure toggle and reviewer prompt |
| B | SOC-08 | Can evidence-based stopping save work without unacceptable accuracy loss? | Stop controller and evidence checklist |
| C | SOC-19 | When do targeted requests beat broadcast? | Private evidence store and addressed delivery |
| D | SOC-02 | How much does a larger team buy at fixed total resources? | Population and evidence-allocation parameters |

The common engine owns truth, evidence, observations, a bounded message board, budgets and scoring. Studies deliberately expose different information. In A and B, all facts are delivered before discussion to isolate deliberation. In C and D, discovering distributed facts is part of the problem. Reusing code does not make their estimands identical.

## Research grounding and outstanding review

The [question bank](../question-atlas/README.md), [methods guide](../../../../tooling/agent-experiments/GUIDE.md), [harness guide](../../../../tooling/agent-experiments/HARNESS.md) and [collective-sensing example](../../../../tooling/agent-experiments/examples/collective-sensing/PROTOCOL.md) supply the starting points. The example is scripted and has no production model adapter. Its reported toy accuracy is not evidence for any treatment here.

The following are load-bearing prior-art leads, inherited from the bank and existing SOC-07 plan. Their methods must be audited for the selected contrast before formal promotion. This planning pass does not claim new full-paper reads or established novelty.

| Question | Closest leads | Boundary of the proposed contribution |
| --- | --- | --- |
| Disclosure | [[choi-2025-debate]], [[shehata-2026-bystander]], [[ren-2026-sepal]], [[barrera-lemarchand-2026-wisdom]] | Private first answers and separated groups already exist. Isolate disclosure timing and harmful versus useful revisions. |
| Criticism | [[du-2023-improving]], [[choi-2025-debate]] | Compare evidence-seeking review with opposition and equally budgeted independent work; debate alone is not a new mechanism. |
| Stopping | [[zhang-2026-silo]], [[choi-2025-debate]] | Separate verified evidence coverage from confidence and agreement at matched maximum resources. |
| Routing | [[tambwekar-2026-proxifield]], [[liu-2026-social]], [[zhang-2026-silo]] | Direct addressing already exists; test its cost and missed-dependency boundary. |
| Team size | [[bertalanic-2026-ringelmann]], [[zhang-2026-silo]], [[begin-2026-preference]] | Existing effective-size results motivate a distributed-evidence, fixed-budget boundary test. |

At drafting, the LLM-agent survey is complete but its recorded review remains revise; there is no accepted hypothesis for this suite. Before collection, resolve the focused survey and independent review, obtain acceptance of the specific hypothesis, then copy the selected protocol into a formal experiment. The runtime/model and cost fields below must also be frozen. None of those launch requirements prevents pushing this requested working document now.

## Shared world and exact answer

### Task families

Use fictional supplier selection, with no real companies, web retrieval, external side effects or model judge. Each world has two suppliers, current cost and delivery records, a delivery deadline, and a public rule: choose the cheaper eligible supplier using the latest authorized value for each field. Generate exactly one correct answer; reject ambiguous draws before invoking a model. The scorer computes the answer from structured truth through an implementation separate from the renderer.

Initial ranges: cost 20–100 integer units, delivery 1–10 days, deadline 5 days. Balance cost-based and feasibility-based decisions. In cost-based worlds both suppliers are eligible; balance cost gaps of 1–3, 4–10 and 11–20. Balance final answer labels and rotate which agent receives decisive information. Timestamps and authorized-source IDs are explicit; a newer unauthorized record does not supersede an authorized one.

Example: old records give A cost 40 and delivery 3 days, B cost 50 and delivery 4 days. A current authorized audit changes A's delivery to 8 days. With a five-day deadline, B is correct. Mirror the labels and direction of updates, and include cases in which old recommendations remain correct. A blanket rule to reverse the first choice must fail.

For B–D, add a separately versioned extension with three required evidence categories: delivery, cost and qualification. The public schema names the categories but never their values or the correct supplier. Each supplier has one authoritative current record per category: six canonical facts total. Eligibility requires on-time delivery and qualification. A qualification record may reference a certificate held by a different evidence owner. Cross-reference resolution adds one additional necessary fact in dependency worlds. Irrelevant records are labeled as ordinary records, not as distractors to agents.

This small family trades ecological breadth for tractability. Initial conclusions concern these generated decisions only. Generalization to diagnosis, software engineering or human teams needs a separate task family and fresh evaluation.

### Evidence regimes

A uses equal numbers of clean worlds, informed-minority worlds and correctable-minority worlds, following the existing SOC-07 fixture. In clean worlds all agents start with adequate current information. In informed-minority worlds one initially sees the decisive update and four see old records; correctable-minority worlds reverse that allocation. The complete packet is released before review in all communicating arms. Initial correctness is observed, not forced.

B balances redundant and complementary initial evidence, then supplies the complete authorized packet to every participant. Missing evidence during reasoning is therefore an integration or tracking failure, not unavailable access.

C crosses ordinary versus cross-reference dependencies with concentrated versus distributed ownership of decisive facts. Every peer advertises the record categories it owns, without the values; cross-reference targets become visible only when the referring record is fetched. There is always a reachable path to all necessary facts within the prescribed round limit.

D crosses redundant versus complementary evidence at each team size. Hold the union of canonical facts constant. In the redundant regime every agent gets the complete packet; in the complementary regime allocate the six facts as evenly as possible with no initial duplication. At N=1 these coincide; run the single-solver anchor once per world, rather than double-counting it. Shuffle owners and order independently of the answer.

### Units and pairing

A world is an independently generated underlying problem. A team episode is one world, treatment and repetition. Treatments are assigned to entire team episodes. Every condition receives the same truth, canonical facts and answer-label mapping for its paired world. Shared initial records, where specified, are generated before treatment disclosure. Each continuation has isolated memory and cannot read another condition's outputs.

New numeric draws from the same template are separate sampled worlds, but inference remains conditional on that template family. Repetitions and agent votes are not independent worlds. Keep scenario, repetition, agent, phase and treatment seed streams distinct, with stable derivation and recorded inputs. Randomize treatment execution order within world and balance it over time to reduce provider-load and version confounding.

## Common agent interface and limits

The future runner will give each agent only its permitted evidence, its own earlier outputs, delivered messages and public rules. The evaluator's answer and other conditions' records are never accessible. Agents cannot change rules, truth, ledgers, timeouts or budgets.

Required outputs are structured. Initial/final answers contain choice A, B or ABSTAIN, confidence in [0,1], and cited evidence IDs. Review messages additionally contain supported claims, missing categories and a provisional recommendation. Requests contain recipient, category or referenced record ID, and a short question. Confidence is self-report; it is not assumed calibrated. Never request private reasoning traces. Invalid responses remain invalid and are counted; there is no hidden repair call.

The default team has five isolated conversations using the same model. For a concrete qualification candidate, reuse the existing SOC-07 plan's proposed Qwen3-8B non-thinking configuration. Its immutable weights/tokenizer revision, precision and sampling values must be checked and pinned from that plan and official model documentation at implementation. No hardware compatibility or runtime has been measured for this suite. If it fails task qualification, choose another model on development data, freeze it, and restart qualification; never switch during confirmation.

| Limit | Proposed common ceiling | Semantics |
| --- | --- | --- |
| Aggregate input | 40,000 model tokens per episode | Includes repeated history and all diagnostic model calls; cached tokens still count as exposure |
| Aggregate generated output | 4,000 model tokens per episode | Includes exposed reasoning usage if applicable; disable unmetered reasoning modes |
| Per-agent initial answer | 256 output tokens at N=5 | Study D instead divides a fixed phase pool across N |
| Review or discussion response | 256 output tokens | B and D phase pools override this value |
| Final answer | 64 output tokens | No model-based final aggregator |
| Whole episode time | 180 seconds | From first dispatch to final record, including queue and retries; no automatic retries by default |
| Concurrent episodes | Start at 4 | Qualification may lower it; freeze before comparative latency measurement |
| Paid execution | Disabled pending a specified monetary cap | A token cap is not authorization to spend |

These are proposed maxima, not measured requirements. Reserve worst-case call cost before dispatch, reconcile actual usage and record unused allowance. A request that cannot fit is rejected and logged. No silent context truncation: an oversized request fails preflight. During development, resize caps for every arm if necessary and rerun the pilot under a new version. Equal ceilings do not imply equal actual tokens, information or FLOPs; report all of them that can be measured.

No world can borrow resources from another world. The monetary cap, provider prices, machine-hours, experiment-wide maximum calls and accountable operator must be entered in the launch manifest. For local inference record machine-hours and throughput rather than claiming zero cost.

## Study A Disclosure and criticism

### Factorial and controls

Use six primary development cells: disclosure PRIVATE or PUBLIC crossed with reviewer EVIDENCE, OPPOSE or INDEPENDENT. This is a 2 by 3 factorial, with five worker agents and one separate reviewer conversation in each cell. The reviewer is not a sixth voter. Its information access and call/output allowance are identical across reviewer conditions.

PRIVATE withholds initial worker choices and confidences from peers; PUBLIC publishes them. Workers always retain their own initial record. Every communicating arm receives exactly the same complete factual packet. Only PUBLIC exposes peers' initial choice/confidence; initial justifications remain private. This manipulates disclosure of already-formed judgments, not anticipation of being observed.

The reviewer receives the complete evidence, the deterministic provisional majority choice and no worker identities, raw ballots, confidence scores or private justifications. The provisional choice is identical across paired cells because initial worker outputs are shared. With no three-vote majority, the reviewer receives UNRESOLVED. Workers see the reviewer message but the controller does not separately publish the provisional majority in PRIVATE.

| Reviewer | Exact behavioral instruction to freeze in full prompt |
| --- | --- |
| EVIDENCE | Check the provisional choice against current authorized facts. Support it if warranted; otherwise identify the decisive counterevidence and corrected choice. Do not disagree merely to be a critic. |
| OPPOSE | Argue for the other option, using only supplied facts. State when there is no factual basis. If the provisional choice is unresolved, critique both options. Never invent evidence. |
| INDEPENDENT | Solve the task from the supplied facts. You may see a provisional choice, but form your own answer and cite the decisive records. |

A reviewer can reveal or imply the provisional majority in its message. PRIVATE therefore withholds raw early ballots and confidence, not all later information about the group recommendation. This is an explicit disclosure-timing comparison; any claim of permanent recommendation secrecy would be false.

OPPOSE is an intentionally adversarial diagnostic, not a strong deployment baseline. EVIDENCE versus INDEPENDENT is the primary reviewer comparison. None of these prompts establishes the actual mechanism without trace and outcome checks.

Add three development comparators outside the factorial: no-review PRIVATE team with a 256-token self-review per worker; independent voting with solitary review and private facts only; and one full-information solver with the same aggregate input/output/time ceilings. These controls change communication/information access and must be interpreted as whole-protocol comparisons, not pure critic effects.

### Schedule and accounting

1. Generate five independent first answers using private initial packets. Store them once per world/repetition and clone into isolated factorial arms and eligible controls. Do not announce the disclosure arm yet.
2. Release the common full factual packet and the arm-specific ballot visibility.
3. Call the reviewer once with at most 256 output tokens; all workers receive its same completed message.
4. Workers simultaneously write one review response of at most 256 tokens each. Publish all five only after all calls finish.
5. Workers independently submit final answers of at most 64 tokens. Score a strict three-of-five majority. No private-final branch is collected in this suite's first slice.

A full factorial episode uses 16 logical calls and at most 3,136 generated tokens: 5 × (256 + 256 + 64) + 256. Initial reuse reduces collection calls, not deployed protocol cost. Charge the initial calls to every arm when comparing protocols; report actual collection cost separately. No-review and voting use 15 calls and 2,880 output tokens. A single solver uses preparation, review and final calls with ceilings 1,536, 1,536 and 64, totaling 3,136; all controls retain the 4,000-token hard ceiling. These allocations match maximum work approximately, not cognitive operations.

### Outcomes and decision

Primary endpoint is correct team answer by the deadline over all assigned episodes. Co-primary contrasts for this combined study are PRIVATE minus PUBLIC averaged equally over the three reviewer conditions, and EVIDENCE minus INDEPENDENT averaged equally over disclosure. Apply Holm correction to these two superiority tests at familywise 0.05. Report the disclosure-by-reviewer interaction as secondary, with an interval; the pilot is not powered to establish an interaction.

Also report all six cell accuracies, correct-to-wrong and wrong-to-correct revisions, invalid/abstaining finals, evidence citation validity, cost and time. Conditional revision rates use the shared pre-treatment initial answers and pooled eligible counts within regime; zero-eligible worlds stay in the ledger. Bootstrap whole worlds. A missing or invalid final is reported separately from a valid wrong final, while both count as no success operationally.

Proposed practical gain is 5 percentage points. Adoption also requires ruling out a loss greater than 5 points in clean-team success and designated initially-wrong minority correction, using one-sided 97.5% bounds. Sparse initial-error opportunities make the correction guard unresolved. A benefit estimate of 5 points with a wide interval is not a successful result. Requiring several conditions jointly needs joint power planning.

Do not select the best-looking cell and reuse the same data as confirmation. Either confirm the two factorial contrasts on new worlds, or freeze one selected protocol against a named baseline for a separately planned holdout. Comparisons against voting or the single solver need their own confirmatory allocation before claiming a swarm advantage.

## Study B Evidence based stopping

Use the extended task family and five workers. Use private initial judgments and worker-generated evidence review, with no separate reviewer conversation, as the design default rather than selecting a winner from the same data. If A motivates another choice, amend B before generating its development set.

All agents get the complete packet after their initial response. Compare three stopping policies: CHECKLIST, CONFIDENCE and FIXED. After each synchronous discussion round, every worker emits a provisional choice, confidence and a category-to-evidence-ID ledger. All arms generate the same fields and have the same maximum of three rounds; the controller uses different fields to stop. This isolates the stopping policy and does not separately test the behavioral effect of requesting a checklist.

CHECKLIST stops when at least three agents agree on a choice, each citing a complete ledger of required categories with existing authorized current records. The controller validates record metadata and coverage only, never whether the choice matches truth. CONFIDENCE stops when at least three agree and each of those agents reports confidence at least 0.8. FIXED always uses three rounds. If an adaptive rule never fires, stop after round three. Final answers come from a separate 64-token call per worker after stopping; disagreement then is retained.

Per-agent output ceilings are 128 initial, 192 per discussion round and 64 final: maximum 3,840 tokens/team and 25 calls. Stop-policy checks are deterministic, but record their CPU time. Crossing a stopping threshold does not grant extra budget. Compare accuracy, rounds, actual total tokens and latency, not just confidence or agreement.

Primary decision: CHECKLIST versus FIXED must retain accuracy within a proposed 3-percentage-point noninferiority margin and reduce average billed token use by at least 20%. Require a one-sided 97.5% accuracy lower bound above −0.03 and an upper 95% cost-ratio bound below 0.80 for that strong efficiency claim. Show the full error/cost tradeoff; failure to establish noninferiority is inconclusive. CONFIDENCE is a prespecified secondary comparison, including high-confidence wrong stops. Margin and joint sample size need review before confirmation.

## Study C Addressed communication

Use the extended task family with privately held facts. There is no automatic union release. Five agents, three synchronous routing rounds, and a maximum of 12 delivered message copies per episode. One delivery to four recipients counts as four copies; do not count a broadcast once. Cap each rendered message at 128 tokens, for at most 1,536 delivered message tokens; charge its inclusion in every later model context as actual input as well.

Compare DIRECT (address a peer/category), BROADCAST (share facts on a board delivered to every peer), and HYBRID (one broadcast discovery round followed by direct requests). Give each arm the same coarse owner-category directory. DIRECT replies occur in the next round, with final-round requests receiving an explicit no-response-before-deadline outcome. The admission controller uses a seed-randomized rotating sender order, identical across paired arms; when remaining capacity is insufficient, reject the whole message and log it. HYBRID's discovery copies consume the same global delivery allowance.

Each round one agent call can produce a message, a reply and/or a provisional answer within a 192-output-token cap; prioritize responses to earlier requests in the prompt but do not force them. Initial and final caps are 128 and 64 tokens, giving at most 25 calls and 3,840 generated tokens. Unused delivery capacity is not forcibly filled. Fixed equal delivery ceilings estimate protocol performance under scarcity; an exploratory matched-realized-delivery curve is a different estimand.

Primary contrast is DIRECT minus BROADCAST in correct final team decisions, balanced over the four dependency/ownership strata. Secondary contrast is HYBRID minus BROADCAST; adjust the family if both become confirmatory. Record required facts actually delivered, missed dependencies, rejected copies, latency, input tokens and messages per success. Score evidence acquisition from delivery logs, not claims in explanations. The important boundary is whether DIRECT's advantage reverses on cross-reference worlds. Require an interval on that interaction before claiming a mechanism.

## Study D Team size at fixed resources

Use N in {3,5,9}, two evidence regimes, and four protocol modes: VOTE (independent answers), DISCUSS (two peer rounds), SELF (two solitary revision rounds) and PLACEBO (two rounds of unrelated messages). Also include one full-information N=1 anchor per world. Each team episode has four phases and 4N calls. The resulting allocation is 24 team cells plus one anchor. This is deliberately last because it is the largest sweep.

The N=1 anchor uses three calls with output ceilings 1,750, 1,750 and 500, totaling 4,000, and the same aggregate input/time cap. Its four-phase team analogue is not a separate treatment.

Fix a 4,000-output-token team pool: initial phase 1,000, each of two intermediate phases 1,250, final phase 500. Divide each phase across N with integer remainders assigned by seed-rotated agent order. Hold aggregate input ceiling at 40,000 and the full fact union constant. VOTE uses its intermediate calls for independent reconsideration without peer text; SELF explicitly critiques its earlier answer. PLACEBO receives length-matched messages from a disjoint development corpus of fictional tasks, clearly unrelated to the active decision and containing no solution-relevant facts. Charge placebo delivery and processing. Freeze that corpus and a padding/truncation rule before holdout collection. DISCUSS messages are admitted within the same delivery/input ceilings.

Use a strict majority of all assigned N votes for team success. No majority, abstention and malformed responses do not win. Population size therefore changes aggregation as well as communication and per-agent capacity: this is the practical fixed-budget team protocol estimand. Include individual accuracy and the single-solver anchor so a majority-threshold artifact is visible.

Primary contrast, if this study is promoted, is the change in DISCUSS-minus-VOTE accuracy from N=3 to N=9, equally weighted across evidence regimes. Report the whole curve, with N=5 and regime interactions secondary. A separately labeled fixed-per-agent-budget follow-up can test whether compression explains losses; it is not part of this allocation.

Estimate pre/post error covariance across worlds within each condition. Treat N_eff = N / (1 + (N−1) × mean pairwise error correlation) as an exploratory exchangeability proxy only. Report individual error rates and covariance as well. Unequal roles, complementary evidence, zero error variance or unstable denominators invalidate a simple effective-size interpretation; show unavailable rather than clipping to a convincing number. Do not infer N_eff from one episode or treat it as an independent performance outcome.

## Development allocation and speed

These are proposed counts for debugging and variance estimation, not statistically powered studies. Stage splits use disjoint world IDs, and confirmation uses an unopened separate seed namespace. Worlds used for generator/model/prompt selection never return as holdout data.

| Stage | Allocation | Episodes | Maximum logical model calls |
| --- | --- | --- | --- |
| S0 | At least 60 offline fixtures plus failures and known-answer policies | No LLM episodes | 0 |
| Q | 12 full-information worlds × one solver | 12 | 36 at three calls each |
| A pilot | 24 worlds × 2 repetitions × 9 arms | 432 | 6,192 |
| B pilot | 24 new worlds × 2 repetitions × 3 rules | 144 | 3,600 |
| C pilot | 24 new worlds × 2 repetitions × 3 routes | 144 | 3,600 |
| D pilot | 24 new worlds × 2 repetitions × 25 cells | 1,200 | 26,256 |

A's 9 arms are six factorial cells plus three comparators. Per paired world/repetition, 6×16 + 15 + 15 + 3 = 129 logical calls. Sharing five initial answers across the six cells, no-review and voting saves 35 collection calls, so A has at most 4,512 fresh collection calls, while accounting for 6,192 deployed logical calls. Qualification is separate. Do not reuse model outputs across independent repetitions.

D uses 24 team cells and a three-call single anchor. Across N, four modes and two regimes give 8 × 4 × (3 + 5 + 9) + 3 = 547 calls per world/repetition, or 26,256 calls for 48 paired world/repetitions. No per-agent decisions are counted as independent samples.

Execute Q and A first. B–D are independent future stages, not a commitment to spend on the entire table. The first useful result is whether the A fixture produces correctable errors, valid outputs and an interpretable treatment contrast. Short structured responses and parallel independent worlds reduce collection time. Simulation-engine speed is unlikely to dominate LLM time; measure rather than quote unrelated simulator benchmarks.

After qualification, record calls/second, tokens/second, median and p95 phase latency at the frozen concurrency. Forecast time from the actual dependency graph and observed throughput. Forecast API cost as input tokens times input price plus output tokens times output price, separately recording cached and reasoning charges. Apply a proposed 25% contingency for engineering failures to the budget estimate, not to sample size or permission to retry. No dollar or wall-clock promise is made before those measurements.

## Confirmation and statistical analysis

Before S2, freeze the exact question, primary contrasts, outcome, practical margins, world mixture, model/runtime, prompts, all controller rules, analysis implementation and maximum sample size. Use pilot variance/discordance conservatively, with sensitivity to its uncertainty. Do not choose a confirmation sample solely from an optimistic pilot effect.

For orientation only, paired binary accuracy with discordance 0.20, true difference 0.05 and 80% power requires roughly 626 world pairs for an unadjusted two-sided 0.05 test under a normal approximation. Multiplicity adjustment, regime guardrails, noninferiority and interactions can require more. This number is not the suite allocation. Simulate each final decision rule at true effects 0, 0.03, 0.05, 0.08 and 0.10, including failures and eligible initial-error counts. Estimate joint power for all adoption guards. If the cost does not fit, narrow the registered question or label the study exploratory; do not claim a smaller study is powered.

The unit for uncertainty is the world. Average repetitions within world, then average worlds within strata and weight the prespecified strata equally. Use 10,000 stratified cluster bootstrap draws retaining all treatment cells, agents and repetitions. Validate interval coverage offline before freezing; report paired binary discordance and a paired-score or exact sensitivity interval for a single binary contrast. Bootstrap methods alone do not solve small-world or template-generalization limitations.

For conditional revision rates, pool eligible counts within each stratum before taking ratios and preserve zero-eligible worlds in resampling. Report denominator sizes and uncertainty. Cost per correct answer is a secondary ratio of total cost to total successes, not an average that drops failed episodes; it is undefined when there are no successes. Report total cost and success rate separately.

Each study has its own preregistered family and holdout; results across all four studies do not automatically support a suite-wide claim. Report every registered comparison, including null and harmful results. No significance-based early stopping, deletion of bad worlds, or opportunistic sample top-up. A confidence interval spanning material benefit and harm is unresolved, not evidence of no effect.

## Failure handling and records

Freeze a planned ledger before dispatch. Every planned episode ends as completed, failed, timeout, budget exhausted, cancelled or unavailable, with a separate correctness outcome and per-agent validity flags. The operational primary denominator includes all assigned episodes; only a valid correct majority by deadline is success. For ungraded/infrastructure-missing outcomes also show best/worst-case sensitivity bounds, without pretending their semantic answer was known.

No automatic retries in the initial design. A completed output may be resumed only from a durable request ID with known response; an uncertain in-flight request becomes an auditable failure. A later rerun retains attempt lineage and never replaces the original denominator. No automatic model fallback. Pause for a systemic outage and document it; resume under the frozen rules or amend and restart development.

A failed participant contributes no winning vote; the majority threshold remains based on original N. Continue unaffected agents within the shared deadline. Facts released by the controller in A/B remain available despite a worker failure. In C/D, failed workers cannot supply private facts: that is a protocol failure mode and must remain counted. A missing reviewer yields a fixed REVIEW_UNAVAILABLE message, not a substitute reviewer. Missing PUBLIC records are marked unavailable; malformed raw text never enters a peer context.

The future event log must contain study/version, world/repetition/treatment, assigned agent count, phase, message sender/recipient, delivery copies, context and prompt hashes, response validity, timestamps, request ID, token/cost reservations and actual usage, terminal outcome and attempt lineage. Save original public-safe responses for audit, not just extracted answers. Store task truth separately from model-readable state. Log admitted, delivered and rejected messages separately.

Retain full manifests for generator/scorer/prompt code hashes, model/tokenizer/weights/runtime, dependency lock, hardware, sampling settings, stage seeds, ordering, splits and analysis. Reconcile the planned ledger against terminal outcomes and billed requests. Recompute scores from events independently of policy execution. Trace replay checks accounting; it is not a fresh model replication.

When implementation is authorized, start from the repository's experiment-worker template and use the agentops claim/reporting contract. Scientific records remain durable even if hub reporting fails. Publish no credentials, server addresses, private hub URLs or answer keys in live progress. Sanitized progress can include completion, aggregate accuracy and resource use. This plan makes no server claim.

## Implementation sequence after plan approval

1. Complete focused prior-art review and formal hypothesis acceptance. Name the chosen A design explicitly and reconcile any change from the standalone SOC-07 plan.
2. Build the minimal supplier generator, independent solver and renderer; include mirrored examples, stale/unauthorized records and known-answer policies.
3. Build visibility barriers, isolated contexts, strict parsers, budgets and an append-only event ledger. Reuse existing methods contracts where applicable, without assuming the scripted demo is a production runner.
4. Add the model adapter and qualify on 12 fresh development worlds. Proposed thresholds: at least 10/12 correct and 11/12 format-valid. This is an engineering screen only.
5. Run A's fixed pilot; inspect context exposures, counts, failure rates, initial error opportunities and measured cost. Then decide whether to freeze A confirmation or revise and repeat development on fresh worlds.
6. Add B stopping, then C routing, then D population sweeps only when each is selected. Freeze and pilot each independently.
7. Register and run confirmation under the selected manifest; reconcile all outcomes, publish uncertainty and failed runs, and seek independent replication before broad claims.

S0 must demonstrate zero truth/private-field leaks, exact scorer agreement on generated fixtures, correct evidence-version precedence, independent reset state, message copy accounting and durable failure denominators. Inject timeout, malformed output, context overflow, budget exhaustion, duplicate dispatch and interrupted writes. Scripted evidence-following, stubborn and majority-following policies should produce their known outcomes; those outcomes are harness tests, not LLM discoveries.

Before using pilot estimates, require at least 95% format-valid outputs and less than 5% budget/timeout failures, with no detected prohibited exposure. Review the whole assigned ledger rather than dropping failures to pass the threshold. If initial errors are too rare to estimate correction, the correction claim is unresolved; change difficulty only on development data. Do not impose a minimum conformity effect or prompt agents to manufacture the hoped-for behavior.

## Required launch decisions

The design is detailed enough for implementation review, but the following must be resolved in the future preregistration: accepted hypothesis and review IDs; immutable model/runtime and hardware; full literal prompts and schemas; exact world generator/split hashes; final S2 sample and multiplicity family; accuracy-loss tolerances; calibrated resource ceilings; monetary/machine-hour cap and accountable operator; reporting experiment ID and claimed server; and independent analysis validation. Unresolved values are not defaults authorizing execution.

Deferred work includes mixed-model teams, training, persistent memory, real browsing, markets, budgets as behavioral treatments, and physical swarm simulations. BUD-01, BUD-03 and BUD-17 are natural later extensions once evidence retrieval has a credible metered cost. None is needed to answer the five selected questions.

## Review checklist

- Does the chosen comparison change only the intended mechanism, or is it honestly labeled a whole-protocol comparison?
- Are facts reachable, answer keys hidden, and correct-to-wrong changes distinct from useful corrections?
- Are total resources, replicated broadcasts, initial-answer reuse and failed attempts counted correctly?
- Are pilot and confirmation worlds separate, and are all paired arms retained in uncertainty estimates?
- Is the claimed scope limited to the tested model, task family and resource regime?
- Can the proposed sample size support the full adoption rule at an affordable measured cost?

This planning task ships only this document and coordination records. No simulator, provider adapter, experiment configuration or analysis implementation is included.
