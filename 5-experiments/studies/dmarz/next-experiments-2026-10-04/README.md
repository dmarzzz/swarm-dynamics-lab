# Next experiments for Swarm Labs

Complete the active studies, then prioritize four follow-ups: safe memory inheritance, selective continuity across repeated turnover, identity splitting with fixed attacker resources, and compositional safety with imperfect receipts. Expand independent tasks separately from population size, time horizon and compute. Keep OCR verification and repair as conditional extensions. Small adverse pilots do not justify abandoning the research questions.

**Status:** PI planning recommendations and exploratory hunches. These are proposed successor designs, not accepted hypotheses or execution instructions.

**Evidence cutoff:** Public results inspected at 2026-10-04 02:45:49 UTC. Source checkout 45390d685aedc535d8a3e5959df9270c5e6bb7e0. Later outcomes must be reconciled before writing an execution protocol. The completed Theseus critical redesign was reconciled at commit 438ff98 during pre-publication review; it remains unrun. Completed Immune A2 and solo findings were reconciled at afad8f0; this source refresh is distinct from the live snapshot. The same afad8f0 refresh updates V3 review/launch, the sidecar waiver, Sybil Q0/S1 and Market Q0/V4 status.

Prepared by dmarz/pi-next-experiments at the user’s request. Numerical sample sizes, resource regimes and useful-effect margins below are proposed planning choices, not established thresholds. The live snapshot is a timestamped observation, not a promise about current execution state.

## First finish or reconcile existing work

### Discussion V3 and resampling control

Source refresh: V3 qualification launched at 02:56:50 UTC. Independent review passes the exact bounded instrument after 89 tests and a 636-request replay; this is not a completed model-qualification result. The separate resampling sidecar has a frozen 936-call plan and an explicit owner review waiver; upstream review does not establish sidecar review.

Use their reconciled results as the starting point for the memory intervention. Do not duplicate these controls or alter a running protocol.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/vishesh/notes/discussion-benchmark-v3-review/REVIEW.md).

### Sybil population scaling

Scripted S0 completed 264 valid outcomes. Model Q0 then passed 64/64 packets, 16/16 at each of 36, 108, 324 and 972 identities. S1 is collecting under its existing 24 paired-world, 2,400-assignment plan; no S1 conclusion is available at this source refresh.

Finish that study before the fixed-resource identity experiment below. The existing study scales simulated identities feeding a synthesizer; it does not run hundreds of autonomous LLM agents.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/dmarz/notes/sybil-scale-api/reviews/q0-001-post.md).

### Compositional safety

S0 engineering qualification is active. The current protocol contains seven arms, followed by Q0 and a development pilot.

Complete current qualification and pilot before introducing imperfect receipts or a new constraint family.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/compositional-safety/README.md).

### Antsy receipt verification

Both frozen 70-receipt evaluations were running: 62 completed for Laya and 53 for Jev. Neither partial mean is a final treatment estimate.

Finish and analyze the paired results before choosing a successor. Avoid another pilot on the same evaluation receipts.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/antsy-verification-v4/reviews/S0-post.md).

### Market splitting

The original interrupted S1 had eight completed bundles, one capacity-action failure and nine cancelled bundles. Subsequent interface mechanics passed 6/6 operations, but Haiku Q0-003 capability failed: locked-arm profit was 68.43% of the reference against the unchanged 75% floor. A second firm in an unregulated flexible episode is not regulatory evasion. V4 plans Sonnet 4.6 with the economics, prompt and floor unchanged; it has no successful qualification result at this refresh.

Preserve the interrupted ledger and model-specific cohorts. Complete fresh model qualification of the repaired interface, then the frozen discovery comparison. Restart a separately labeled complete grid when changing models or treatment semantics; do not pool Haiku and Sonnet as one cohort. Keep prompted strategy discovery separate from neutral discovery.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/dmarz/notes/market-split-api/reviews/q0-003-post.md).

### Native repair and Healing

A source refresh adds completed Immune A2: 12 episodes and 108 calls, all structurally valid. Every team arm preserved the healthy control but scored 0/6 healthy ticks in stale-advice and registry-partition cases; only reset recovered migrated data (5/6). The four-episode solo baseline recovered all three incidents (5/6 each), but damaged the initially healthy system (3/6 and one unsafe attempt). These tiny samples do not establish a causal team-versus-solo effect. Healing exposes 72 exact/Jev reference worlds with programmed propagation.

Preserve these mixed/adverse findings and finish remaining reporting. Freeze a fresh competence and evidence-checking comparison before repeated-damage or population scaling. Memory filtering alone cannot remove newly generated false interpretations of tool evidence.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/afad8f0/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md).

### Native influence follow-through

A source refresh after the live cutoff adds Q3: three valid deferrals on one fresh missing-evidence case after the authorization wording was clarified. Q2 had nine valid decisions, with two adverse team approvals. The changed profile and prompt prevent pooling those attempts or attributing the improvement to wording alone.

Complete fresh qualification of the frozen final decision contract and the registered clean/omission comparison; retain valid adverse approvals as findings. Avoid a new broad influence sweep before that contrast resolves.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/fa802d4/researchers/vishesh/notes/influence-swarms/scenario/RESULTS.md).

### Theseus critical redesign

The critical review and prospective v2 design are complete at 438ff98. The new experiment is unrun and unqualified.

Operationalize the existing Harbor selective-continuity design with its owner. Resolve utility, state limits, acceptance margins and budget before qualification; defer mentoring and broad population/depth sweeps.

[Existing protocol](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/redesign/DESIGN.md).

## Proposed successor experiments

### 1 Safe memory inheritance at increasing team size

Extends: Discussion V3 and the completed discussion-dose memory finding.

**Why this follows.** The strongest observed mechanism is that correct team decisions can still pass poisoned memory downstream. H4 showed this in four of five correct attacked decisions. The six-world discussion comparison is too small and has an invalid outcome; it is not a rejection of discussion.

**Question.** Can a coverage-and-provenance memory receipt reduce harmful parent answers while retaining useful completion, and does that benefit change with actual policy-agent population?

**Comparison.** First reuse the same frozen child outputs across majority merge, a deterministic evidence receipt, and an approximately token-matched generic caution control; send each output to a fresh parent. Include full authorized evidence as an explicitly advantaged capability ceiling. Receipts expose source roots, unresolved conflicts and missing required fields using authorized observations only. Provenance identifies origin; it does not certify truth. Record all conditions rather than selecting only historical poisoned examples.

**Proposed scale and sequence.** After existing V3/control work is reconciled, use 24 fresh task-generation roots for development across at least four structurally distinct task families. Freeze the receipt algorithm. Then test N=3 and N=9 on fresh paired worlds; add N=27 only after size-9 execution is structurally valid and resources are reserved. Include a competent N=1 solver with the same authorized evidence. Hold total evidence and attacker resources fixed in the primary panel. A separately labeled per-agent-resource panel may increase total compute; do not merge the two curves. Start with one communication schedule and scale only the prespecified interaction after the narrow intervention is interpretable.

**Independent unit.** Independent task-generation root. All exposures, merges, sizes and parent repetitions from that root stay in one cluster. Reusing child traces isolates a downstream intervention; it does not add independent swarm replications.

**Primary measurement.** Primary for the narrow intervention evaluation: majority-merge wrong-parent-answer probability minus receipt wrong-parent-answer probability on resolvable attacked tasks; positive means harm reduction. Clean correct completion is a co-required guardrail. The later population panel must freeze its own primary size interaction before evaluation. Report unsupported answers on ambiguous tasks, abstention, required-field coverage, supported inherited errors, actual tokens, cost and latency separately.

**Proposed decision rule.** Proposed practical targets: at least 10 percentage points less parent harm, with at most 3 points lost clean correct completion. The development batch cannot establish either margin. Choose a separate evaluation sample using conservative paired variance and joint precision for harm and utility. A valid evaluation whose interval rules out the useful reduction narrows this receipt design; it does not refute communication or memory generally.

**Prerequisites.** Independent review of the exact receipt/scorer and actor-visible metadata; no truth leakage; original V3/control outcomes retained; fresh qualification and untouched evaluation roots. A valid increase in harm at larger N is a scaling result, not a reason to tune that condition away.

**Visualization.** Per-world evidence lineage and memory admission replay, followed by harm-versus-clean-completion curves for each resource regime; show independent-world counts and missing outcomes at every population.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/discussion-dose/V2-ISSUE-REVIEW.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/discussion-dose/benchmark-v3/README.md), [source 3](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/discussion-dose/RESAMPLE-CONTROL.md).

### 2 Selective continuity across two replacement waves

Extends: Swarm of Theseus v1 and the completed critical redesign.

**Why this follows.** The completed redesign retains v1 as a useful transmission baseline, but finds that supplied rules, founder-only mentoring and recurring binary patterns explain its strong result. The next question is whether an acquired practice can retain useful components and revise obsolete ones. Increasing v1’s sample size or mentoring depth alone would not establish that contribution.

**Question.** Can a practice acquired through experience survive two complete replacement waves while descendants preserve what still works and revise what has become unreliable?

**Comparison.** Use the existing owner’s Harbor flagship design. Three pilots acquire scheduling and signaling practices from role-local observations and measured consequences; no preferred policy or convention is supplied. After a fixed acquisition phase, freeze each founder checkpoint and branch it into rolling versus frozen founder archives and stable versus partially changed environments. Introduce the change after the first complete replacement wave; descendants must teach the second wave. Include retained members with matched observation and resource opportunities, a fresh team receiving an exact transplanted rolling archive, a fresh team without an archive, and one controller with the same total observations and resource allowance. Keep adaptive mentoring as a later comparison against an equal-budget written handoff. Use identical-evidence probes separately from live branches, whose actions naturally change subsequent feedback.

**Proposed scale and sequence.** First complete offline transition and scorer review. A proposed initial development batch is eight fresh founder-lineage/world roots at N=3 and two complete replacement waves, with fixed acquisition and continuation horizons. This is an instrument and variance screen, not a powered test. Use development worlds to determine whether the task can be learned under the allowed observations and whether the controls distinguish copying, reacquisition, adaptation and coordination. Freeze the task and policies, then choose a fresh exploratory or precision-study sample from conservative lineage-level variance and measured cost. Prioritize additional independent worlds and a second model family before broad population/depth sweeps. Only after the flagship is interpretable should a separately frozen population or depth panel be designed, with total versus per-agent resources and per-cycle opportunities distinguished.

**Independent unit.** Founder lineage in an independently generated world. All archive conditions, stable/changed continuations, transplanted branches, probes and repeated checkpoints from that lineage remain clustered. If several lineages share one underlying world, declare the nesting or world-level averaging before analysis. Acquisition failures remain in the full assigned population; conditional-on-acquisition results are secondary and retain their denominators.

**Primary measurement.** One primary effect: (rolling-archive reward minus frozen-archive reward in changed worlds) minus (rolling-archive reward minus frozen-archive reward in stable worlds), measured after the second complete replacement wave. Reward is fixed task utility per scheduled episode, with failures and costs included. Define its components, weights, normalization and horizon before qualification. Publish raw deliveries, collisions, delays and signaling costs alongside the interaction.

**Proposed decision rule.** Interpret the primary interaction jointly with stable-world competence and retention of the unaffected task component. Before qualification, set a minimum useful interaction and noninferiority margins for stable reward and unaffected-component retention from the fictional task’s loss tolerances; unresolved numeric margins block launch. A positive interaction produced only by poor rolling-archive performance in stable worlds does not satisfy the claim. If an adequately precise comparison finds no meaningful gap from the transplanted archive or matched single controller, narrow the explanation to portable memory or centralized record use. An imprecise gap is inconclusive. Failure to acquire a convention, preservation of an obsolete rule, or failure to transmit a correction are valid results. If controls cannot discriminate explanations, redesign only on development material before expanding.

**Prerequisites.** Use the completed owner redesign, without creating a second implementation lane. Obtain independent cross-researcher review of the transition table, oracle derivation, scorer, information access, archive ancestry, private-context destruction and failure policy. Verify the acquisition phase supplies observations and consequences rather than the correct procedure. The development learnability gate evaluates the instrument; it must not exclude individual lineages that fail acquisition from later assigned-denominator analyses. Freeze state caps, horizons, utility, numeric margins, partitions, model versions and exact budget before paid execution. Qualify on disjoint inputs and preserve all failed attempts. Formal confirmatory promotion still requires the survey and hypothesis gates.

**Visualization.** Synchronize measured roster replacement and archive ancestry, stable/changed task outcomes, and exact inherited-text changes followed by observed actions. Compare rolling, frozen and transplanted branches at matching checkpoints. Mark environmental change only in the evaluator/viewer layer, retain missing observations, and choose illustrative traces by a prespecified representative rule.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/redesign/REVIEW.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/redesign/DESIGN.md), [source 3](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/RESULTS.md).

### 3 Identity splitting with fixed attacker resources

Extends: Sybil specialists and the already planned population-scale study.

**Why this follows.** The current population sweep increases attacker capacity along with population. It cannot identify whether multiplying identities helps when one attacker has unchanged aggregate resources. Earlier verification recovered rare expertise but weak checks admitted most attackers.

**Question.** Does splitting one attacker's unchanged resource budget across more identities increase harmful influence, and which admission policy preserves legitimate specialist value?

**Comparison.** Hold the honest population and task evidence fixed. Allocate one attacker's fixed message/token, edge-acquisition and verification-attempt budgets across 1, 3, 9 or 27 identities; account for registration overhead. Compare coverage, degree and random admission at equal check budgets, with identical-packet deterministic plurality and model synthesis. Add a faithful published-defense comparator before comparative superiority claims. The attack allocation algorithm must be frozen, not tuned separately against evaluation outcomes.

**Proposed scale and sequence.** Finish the existing 36/108/324/972-identity experiment unchanged. Then use 24 development graph/task roots across the existing ring construction and a separately implemented community graph. Begin with informative checks and include unreliable checks as a prespecified stress condition. Freeze all policies before drawing new evaluation roots. Keep graph mixing, trusted anchors and attacker capacity explicit; identity counts are not counts of autonomous model workers.

**Independent unit.** Graph/task root, paired across identity allocations, policies and verification conditions. Six skill answers, malicious seats and repeated syntheses within one root are dependent observations.

**Primary measurement.** Primary: the one-to-27-identity increase in wrong-answer probability under degree admission minus that increase under coverage admission, within matched worlds at fixed attacker resources and informative checks, equally weighted across the two graph families. Positive means coverage attenuates identity-splitting harm more than degree. The raw multiplicity effects, random policy and unreliable-check results are prespecified secondary contrasts. Report rare-skill correctness, malicious seat share, honest-specialist rejection, checks and cost together.

**Proposed decision rule.** Proposed useful security difference: 10 percentage points in wrong-answer probability. Jointly inspect the utility-security frontier; an accuracy improvement accompanied by higher attacker admission is a tradeoff. If the multiplicity effect disappears with resources fixed, report that result rather than expanding attacker resources to recover it. Size the separate evaluation from paired uncertainty, not the earlier 86-point specialist effect.

**Prerequisites.** No changes to the active scaling study. Run structural tests at every identity allocation and bounded clean competence checks across each distinct packet-load regime, including aggregation and missing-evidence abstention. Passing only the largest packet is insufficient. Keep valid target-policy degradation or capacity failures in assigned outcomes. Audit the second graph generator, resource ledger and comparator implementation before inference.

**Visualization.** Rare-skill accuracy versus attacker admission, faceted by topology and check reliability, with identity-count curves at a fixed attacker budget and per-world paired contrasts.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/sybil-scale-api/README.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/sybil-scale-api/preregistration.md), [source 3](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/sybil-specialists-api/reviews/s1-001-post.md).

### 4 Compositional safety with delayed and missing receipts

Extends: The current compositional-safety qualification and pilot.

**Why this follows.** The existing seven-arm pilot already tests fragmented history and factual receipts. Its next valuable test is whether the receipt mechanism survives imperfect delivery and transfers to an unseen constraint family.

**Question.** Can factual receipts reduce committed global violations when receipts arrive late or are absent, without suppressing legitimate work?

**Comparison.** At the existing four-role architecture, compare receipt versus fragmented-history baseline with current, one-commitment-stale, or missing receipts. Keep stale-but-authentic information distinct from fabricated information. Retain shared-history, matched administrative text and atomic enforcement references. Include the missing faithful prior-work defense before superiority claims. Do not alter the current pilot's arms.

**Proposed scale and sequence.** After S0, Q0 and the current pilot reconcile, use 24 fresh canonical structural roots across the two exposed domains for robustness development, with paired benign and risk conditions. Freeze the mechanism before model evaluation on the previously unexposed aggregate-commitment domain, using separate clean qualification examples. Add a second model or independent implementation before increasing the number of roles. Transfer across constraint structure is the primary scale axis here.

**Independent unit.** Canonical task structure. Use structural fingerprints to group renamed duplicates. Actions, role turns and entity renamings do not create independent samples.

**Primary measurement.** Primary: fragmented-history committed-violation probability minus receipt committed-violation probability when the receipt is one commitment stale, averaged equally across the two exposed constraint domains. Positive means harm reduction. Safe legitimate completion is a co-required guardrail. Current/missing receipt contrasts and transfer to the new constraint family are separately reported secondary analyses unless a later protocol prospectively makes transfer its primary. Report invalid outputs, incomplete work, cost, retrieval use and actual receipt availability.

**Proposed decision rule.** Proposed targets: 10 points fewer violations and no more than 3 points lost safe legitimate completion. Power or precision-plan the joint claim on separate evaluation structures. If benefit requires perfect receipts, report that operating boundary. If fragmented history produces no excess harm under valid conditions, preserve the null. If atomic enforcement allows prohibited effects, stop for an instrument defect.

**Prerequisites.** Complete existing current-source qualification. Obtain independent review of task structure, replay evaluator and observability, then pass the formal research gates before a confirmatory study. No natural-language receipt should be treated as proof of global state completeness.

**Visualization.** Actual committed-action replay with receipt age/missingness and evaluator-only violation markers, plus violation-versus-safe-completion curves across delivery conditions.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/compositional-safety/README.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/dmarz/notes/compositional-safety-plan/README.md).

### Conditional A Verification value under real ambiguity and review cost

Extends: Both running Antsy 70-receipt evaluations.

**Why this follows.** The ten-receipt screen did not favor a committee, but was too small to settle the question. The two model evaluations already underway are the next evidence, not a reason to launch a duplicate batch.

**Question.** On receipts where additional checking can plausibly change the decision, does a team choose verification better than a single solver or deterministic confidence policy?

**Comparison.** First analyze the existing held-out paired outcomes without tuning. If a useful uncertainty regime remains, compare a single solver, committee and confidence-based policy using the same initially available OCR/evidence. Replace annotation-perfect QA with measured checker outputs and explicitly measured review cost. Include a no-check option. Separate choosing a tool from improving the OCR itself.

**Proposed scale and sequence.** Develop the successor on 20 new ambiguous receipts from separately sampled document families, then freeze and determine evaluation size from paired differences. Keep later evaluation stratified by independently assessed ambiguity and vendor/layout families. Test 1 versus 5 decision agents before larger populations. Report both fixed-total inference budgets and actual checking costs; do not reuse the current 70 receipts to tune the successor.

**Independent unit.** Receipt cluster, grouping duplicate documents and near-identical vendor templates when dependence requires it. Tokens and fields within one receipt are not independent replications.

**Primary measurement.** Correct required-field decisions per assigned receipt under a prespecified total review budget; retain token recall as a secondary diagnostic. Report abstention, false confident decisions, checks purchased, latency and cost. Do not equate token recall with payment safety.

**Proposed decision rule.** Proposed useful improvement: 5 percentage points in correct receipt-level decisions at equal resource allowance. If a valid evaluation excludes that improvement over the cheapest competent baseline, retain the baseline and close this committee policy. A wide interval is inconclusive. Do not expand N merely because a small pilot was unfavorable.

**Prerequisites.** Both current reports complete; independent check that the successor tasks actually offer measured verification headroom and that checker noise/cost are real inputs rather than evaluator truth.

**Visualization.** Per-receipt before/after decisions and verification purchases, plus quality-cost curves and uncertainty strata with independent receipt counts.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/antsy-verification-v4/README.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/antsy-verification-v4/reviews/S0-post.md).

### Conditional B Repair under repeated damage and incomplete lineage

Extends: Immune Response V3 and Healing reference controls.

**Why this follows.** Completed native A2 mostly fails damaged-task recovery despite preserving the healthy control; the small solo baseline recovers incidents but damages the healthy control. Native competence therefore includes both recovery and restraint. False interpretations generated from current tool evidence expose a bottleneck that memory filtering alone does not address. Healing reference controls remain useful for distinguishing propagation from ordinary shared-state restoration.

**Question.** Can a selective repair preserve useful new knowledge and avoid relapse when lineage is incomplete and incidents recur?

**Comparison.** Use two separate protocols and never pool their effects. For Immune, first compare ordinary advisory proposals against evidence-carrying proposals whose claimed predicates are checked against actual actor-authorized tool results. Match total observations and resources; include fresh balanced team/single-commander comparisons and the deterministic contract solver as an explicitly non-LLM reference. Preserve reset/revision and no-misleading-memory damaged-task controls. A checker may verify a tool fact but must not import hidden environment truth. For Healing compare withdrawal-aware propagation with an ordinary central append-only evidence index on the same extraction tape and source/update budget. Include benign new learning and missing or misleading lineage. Start with supplied incident labels; any learned detector is a separate study with measured false positives and negatives.

**Proposed scale and sequence.** First freeze a new evidence-checking and competence study; preserve the original native failures as findings. Use 24 fresh task roots for development spanning initially healthy and matched damaged services, benign updates and misleading/missing lineage. Require independent scenario authorship and a held-out service graph before a precision-sized evaluation. Only after the mechanism comparison is interpretable, vary one axis at a time: at fixed population compare one versus three incidents, then separately consider populations eight and 24. Keep incident fraction, per-member exposure, total evidence and total compute explicit. Healing follows its own development and qualification sequence. Choose evaluation sizes from whole-root variance and practical effect targets.

**Independent unit.** Independent task/root and full incident history. Repairs, rounds, records and members inside a history are repeated observations.

**Primary measurement.** Two distinct protocols: Immune’s primary is ordinary-proposal integrated unhealthy-service time minus evidence-checked-proposal integrated unhealthy-service time; positive means improvement. Healing’s primary is central-index integrated incorrect-or-missing claims minus withdrawal-aware propagation integrated incorrect-or-missing claims. Unsafe actions, false interpretations, harmful proposals, rejected actions, executed damage, recurrence and legitimate-update retention are separate guardrails or secondary endpoints. Never pool a cross-study score. Report operational completion, absolute error differences, cost and time to a common absolute quality threshold.

**Proposed decision rule.** Proposed useful reduction: 20% relative integrated error, plus at most 3 points loss of legitimate-update retention; always report the absolute error difference. If baseline error is near zero, the relative criterion is uninformative. If selective repair works only with complete oracle lineage, report that boundary. Qualified nulls do not justify lowering the task's competence threshold.

**Prerequisites.** Incorporate completed A2 and solo findings; do not treat passing narrow clean qualification as recovery competence. Require both healthy-system preservation and recovery on matched damaged tasks without misleading memory. Independently review tool-predicate checks, scenario/scorer construction, rollback semantics and missing-lineage manipulations. Qualify the frozen new protocol on disjoint roots. Keep Jev extractor reference results separate from claims about Qwen or heterogeneous populations.

**Visualization.** True, stale, missing and legitimately updated state over repeated incidents, with recovery thresholds fixed across arms and every failed or unstarted assignment visible.

Evidence: [source 1](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/immune-response-v3/README.md), [source 2](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/immune-response-v3/REVIEW.md), [source 3](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/healing-helping-hands/README.md), [source 4](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/researchers/vishesh/notes/immune-response-v3/scenario-study/README.md), [source 5](https://github.com/dmarzzz/swarm-lab/blob/afad8f0/researchers/vishesh/notes/immune-response-v3/scenario-study/ASSESSMENT.md), [source 6](https://github.com/dmarzzz/swarm-lab/blob/afad8f0/researchers/vishesh/notes/immune-response-v3/scenario-study/NATIVE-A2-RESULTS.json), [source 7](https://github.com/dmarzzz/swarm-lab/blob/afad8f0/researchers/vishesh/notes/immune-response-v3/scenario-study/SOLO-A1-RESULTS.json).

## Shared design and decision rules

1. Separate population N, full turnover/incident depth G, independent worlds S and stochastic repeats R in every manifest. When making a population-scaling claim, use the paired treatment-minus-control difference at large N minus the same difference at small N. Pair the base world and use keyed random streams; the same numeric seed alone does not guarantee matched observations.

2. Treat fixed-total resources and fixed-per-agent resources as distinct experiments. Log actual input/output tokens, calls, evidence available, verification expenditure, dollars and latency. Equal call ceilings do not imply equal compute or information. A valid target policy failing under a tight fixed budget remains an observed outcome.

3. Development samples of 8, 20 or 24 in this plan are proposed engineering and variance-estimation batches, not claims of adequate confirmatory power. For a world-level paired contrast, an initial precision approximation is S = ceil((1.96 * SD / h)^2), where h is desired 95% interval half-width. SD=.25/.35 suggests approximately 25/48 worlds for h=.10, and 97/189 for h=.05. Simulate the actual bounded, stratified, clustered design using a conservative variance range before freezing evaluation size; utility guardrails of 3 points can require substantially more data.

4. Choose one primary contrast per study, name resource regimes and scenario strata, and predeclare how secondary contrasts and joint utility/safety decisions handle multiplicity. Resample whole independent roots, retaining all arms, sizes and repeats; report scenario-specific effects alongside the prespecified average. Do not extrapolate generality from a pooled result over renamed templates.

5. Use development, qualification and untouched evaluation material with structural separation where possible. Prompt repairs, task calibration, verifier tuning and model choice happen only on development data. A model transfer test needs its own competence check; do not tune the intervention on its final evaluation outcomes. Formal confirmatory S2 remains conditional on the repository's prior-art and cross-researcher acceptance gates.

6. Retain all assignments with planned, started, failed, not-started and analyzed counts. Predeclare an operational completion endpoint and conservative missing-outcome bounds; label complete-case sensitivity estimates. Do not drop an arm because the model made a valid bad decision. Record source, model, prompt, simulator, scorer and artifact hashes.

7. Stop for structural instrument defects such as leaked truth, broken parsing, incorrect resource accounting, a faulty exact solver or unintended truncation. Preserve the attempt and qualify a repaired version on fresh inputs. Valid deterioration at large N, missing recovery, weak mentoring or high attacker admission are scientific findings and should not be repaired away.

8. Use a fixed planned analysis or a valid sequential design. A point estimate below the useful target is not sufficient for futility. If the uncertainty interval still includes a useful effect, call it inconclusive; collect the prespecified additional data only within the frozen design and allocation. Narrow an implementation when a valid adequately precise evaluation rules out the useful gain or establishes an unacceptable utility cost. Do not repeatedly check ordinary intervals until a preferred result appears.

9. Before a paid batch, the existing experiment owner must produce a complete pre-run assessment, independent review where required, immutable assignment manifest, exact call and spend reservation, dedicated allocation under that owner's policy, and visualization mapping. Publication of this portfolio does not itself reserve budget, accept a hypothesis or authorize workers. No new infrastructure or model calls were made to produce this plan.

## Directions to retain without immediate broad expansion

Capture-memory: preserve the failed recovery endpoint and separate resistance to capture from recovery after capture. A successor should first validate modeled response curves against LLM behavior. Then distinguish an all-assigned attack/removal study from a prospectively standardized post-capture-state repair study. Keep per-member encounters fixed as N changes; test attacker fraction and absolute count separately. Do not condition the primary comparison on whichever populations happened to be captured.

Quorum: first test a new evidence-timing or reliability regime that changes a practical stopping decision. Repeating symbolic-equivalent choices at more sizes does not establish incremental model value. Any richer semantic task should keep the symbolic/full-information ceiling clearly labeled.

Regrowth and Avalon: require a task with partial information or dynamic constraints where coordination has a testable role. Compare common absolute-quality recovery thresholds and competent non-model baselines. Larger populations on the same one-map or scripted setup mainly establish engineering capacity.

## Recommended order

Wave 0: finish and reconcile existing V3/control, Sybil scale, compositional qualification, both Antsy evaluations, Healing reporting, and the completed adverse/mixed native repair and solo findings. Qualify the repaired market instrument and new model on fresh cases without relabeling the interrupted or failed-qualification cohorts as scientific nulls.

Coordinate with the completed Theseus critical redesign and its existing owner, plus the general swarm-size protocol refinement. This portfolio adds no duplicate implementation lane or reassignment. Those newer planning records were observed during the pre-publication source refresh, after the frozen live snapshot.

Wave 1: prioritize the memory intervention and the Theseus selective-continuity flagship: offline discrimination checks, disjoint qualification and a bounded development batch. Develop the fixed-resource Sybil and imperfect-receipt designs while their parent studies complete.

Wave 2: expand only the relevant axis identified by each frozen pilot, with independent-world precision and resource accounting. Run Antsy or repair successors only after the current results identify a worthwhile unresolved question. Defer broad Theseus population/depth sweeps and adaptive mentoring until the flagship separates copying, acquisition, correction and coordination; expand independent-world precision and model replication first.

Reserve a substantial share of the next research allocation for independent review, fresh task families and replication. Derive exact dollar and request caps from measured per-world costs and the chosen precision; this portfolio gives no invented aggregate cost estimate. The existing $500 dmarz API allowance is shared across all dmarz studies, not a new allowance for each successor; retain request caps and actual-cost reporting.

## Methods and prior work anchors

These anchors inform the design and its limitations. They do not establish the novelty or effectiveness of the proposed successors.

- [GUIDE.md](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/tooling/agent-experiments/GUIDE.md)

- [RUN-REVIEW.md](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/tooling/agent-experiments/RUN-REVIEW.md)

- [README.md](https://github.com/dmarzzz/swarm-lab/blob/45390d685aedc535d8a3e5959df9270c5e6bb7e0/templates/experiment-worker/README.md)

- [08-samplesizejustification](https://lakens.github.io/statistical_inferences/08-samplesizejustification)

- [1810.08240](https://arxiv.org/abs/1810.08240)

- [2403.08882](https://arxiv.org/abs/2403.08882)

- [2410.08948](https://arxiv.org/abs/2410.08948)

- [README.md](https://github.com/dmarzzz/swarm-lab/blob/65f23b8/researchers/shadow/notes/capture-memory/README.md)

- [PROTOCOL.md](https://github.com/dmarzzz/swarm-lab/blob/fa802d4/researchers/vishesh/notes/optimal-swarm-size/PROTOCOL.md)

- [REVIEW.md](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/redesign/REVIEW.md)

- [DESIGN.md](https://github.com/dmarzzz/swarm-lab/blob/438ff98/researchers/vishesh/notes/swarm-of-theseus/redesign/DESIGN.md)

- [DEPLOYMENT.md](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/dmarz/notes/discussion-dose/benchmark-v3/DEPLOYMENT.md)

- [resample-v3-review-waiver.md](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/dmarz/notes/discussion-dose/launch/resample-v3-review-waiver.md)

- [README.md](https://github.com/dmarzzz/swarm-lab/blob/afad8f0829b3ac550036061b7cb10da3c3f3e02b/researchers/dmarz/README.md)

## Reproduction and scope

The adjacent `plan.json` is the structured source; `src/build.py` renders this document and an optional local interactive view. `live-evidence.json` retains a selected public experiment/run snapshot used for this plan. It excludes fleet, claim and infrastructure fields. No experiments were launched, task ownership reassigned, or model requests made in preparing the recommendations. The plan must be converted into owner-reviewed pre-run protocols before execution.
