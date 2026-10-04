# How to win agents and influence swarms

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-experiments; execution source `9eaa1d31` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Bounded native evidence; a peer-influence effect is not established. E1 completed collection with three missing decisions; prespecified missingness bounds [0,0.0625] include zero. Five unsafe purchases share one residual cost-interpretation ambiguity.
- **sample_size_summary:** E1:24 authored variants nested in six families ×two fresh repetitions ×two contexts ×three workflows =288 assigned cells;285 observed final decisions,1904/1907 valid replies. Earlier cohorts remain separate.
<!-- experiment-evidence:end -->

**Five bad purchases. One muddy cost rule.** Updated 2026-10-04 23:17 UTC. [Current findings](LATEST-RESULTS.md).

Can shared evidence become shared error?
- The question: Does peer deliberation amplify unsupported recommendations, or help agents resist them compared with independent judgment?
- Why it matters: A shared bad source can correlate errors across an agent network; this procurement study tests one narrow example.
- So far: Five unsafe purchases all shared one muddy cost interpretation. A social hijack is not established; three decisions remain missing.
- Watch: Source → Advisers → Decider. The Decider reviews recommendations and makes the final choice; replay shows recorded changes, not invented beliefs.
- Next: A matched 40-member team comparison is being prepared, with explicit all-in costs and competent smaller-team/generalist controls.

## Redesign proposal v2 — 2026-10-04

A critique and proposed iteration of this study — one registered primary estimand (team with a summary-only chair vs a single generalist, misleading vs control page, paired at the dossier), a v2 fixture family with a page pool and document-shaped prose, exposure defined as assigned pool fraction vs realized per-analyst exposure, swarm composition and an agent template on the existing phase-exact contracts, an offline shadow authorizer, two-sided gates, twelve new cases, and a zero-model-call simulation used to size roots, agents and arms — is in [redesign-v2/](redesign-v2/README.md). Under the current full-records chair the simulation finds every contrast this study registers (ballots−evidence, team−generalist, targeted−random checks) to be a provable zero; the chair architecture is the live variable. It is a proposal: no model call, no launch, no change to any recorded result. Independent design review (gpt-6-astra) and a second-reviewer numbers check are included.

**Researcher review:** optional under the current [owner runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Existing Dmarz feedback remains evidence; no additional sign-off is pending. Older review-gate statements below are historical and superseded for current work.

## TLDR

A support team has to choose a helpdesk before its existing contract expires. The cheapest seat price is not necessarily the cheapest operation: automated-resolution charges, difficult tickets still needing people, migration dependencies and deployment-specific hosting commitments can reverse the decision. Six specialists read different parts of the same procurement file. Two checkers retrieve requested records. A chair must decide whether to buy or defer.

**Why run this?** Delegating diligence only helps if the final decision preserves the facts specialists uncover. A repeated outside claim may instead become six apparently independent recommendations. We test whether hiding those preliminary votes—while preserving their findings and exactly the same records—changes the final decision. A cheaper single-reviewer workflow tests whether the team was worth using at all.

**Status:** implemented and rerun on native Haiku 4.5. Q2 completed all nine decisions with valid outputs: seven acceptable and two adverse. Both team chairs selected a supplier despite missing mandatory processing approval; the generalist deferred. A targeted Q3 diagnostic clarified immediate purchase authority and all three workflows deferred on a fresh case. The full influence comparison remains unqualified and unrun. See [measured results](RESULTS.md). This is an exploratory instrument, not a reviewed hypothesis or a real vendor evaluation. [Assessment](ASSESSMENT.md), [protocol](PROTOCOL.md), [source grounding](SOURCES.md), [agent contracts](AGENT-SPEC.md), and [pre-run review](reviews/scenario-01-pre.md) distinguish evidence from plans.

Latest iteration: [design changes and plan assessment](ITERATION-02.md). Four fresh qualification dossiers, selected-deployment approval control, answer-label counterbalancing and missingness-aware paired analysis are implemented. Offline audit passes; no additional model results this iteration.

## PI follow-through — 2026-10-04 UTC

The [PI review's](https://github.com/dmarzzz/swarm-lab/blob/e0a3170/researchers/dmarz/notes/next-experiments-2026-10-04/README.md) narrow sequence is retained: qualify the final decision contract, then measure the existing paired clean/omission contrast before a broader influence sweep. The [latest engineering post-mortem](reviews/iteration-03-post.md) documents four fresh dossiers covering all three supplier choices and DEFER, selected-deployment approval, exact-source qualification and missingness-aware paired bounds. Its scripted success is instrument evidence, not native Q4 qualification.

The later [budget authorization](BUDGET-AUTHORIZATION.md) records an additional aggregate USD 10 approval; earlier funding-pending statements describe older snapshots. The historical review gate is superseded by the owner’s optional-review directive. Fresh authorized exclusive allocation, preserved quota and appropriate source-bound qualification remain required for a new native launch. Funding approval alone does not complete those gates or authorize a broader study.

Preserve Q2's adverse approvals and Q3's successful deferrals separately. Q3 changed both the profile and purchase-authority wording, so it cannot identify the effect of wording; a matched old/new wording comparison would be a separate study. Likewise, displaying ballots bundles recommendation content with its salience and token footprint. The planned contrast identifies that display intervention, not a general peer-pressure mechanism.

Keep every assigned case and missing chair outcome in the paired analysis. Shared prefixes, repeated profiles and label permutations do not increase independent scenario diversity. Reviewers must check genuine-value acceptance, useful deferral and the fully approved alternative as well as misleading promotion. Broader claims require independently authored dossiers after this frozen narrow comparison; no historical outcome, primary endpoint or active protocol is changed here.

## Question and prediction

Does displaying peer recommendations increase harmful adoption of a misleading comparison claim, beyond the effect of the underlying documents? The primary paired contrast is `team_ballots` minus `team_evidence` on change in harmful target selection from clean to omission. Both chairs see identical raw documents, findings and checks; only preliminary choices/confidences are removed. This isolates their presence, not a universal effect of discussion. If both perform equally, the recommendation-display intervention has no demonstrated benefit. If a cheaper generalist performs as well, the team has not earned its complexity.

We expect omissions to matter most when headline price or easy-ticket demos conflict with the buyer's actual workload. We expect deployment and deadline failures to be easier to detect when the decisive record is explicit. These are predictions, not labels the evaluator assigns to model behavior. Genuine-value cases make rejecting the promoted option a mistake; evidence-gap cases make deferral useful.

## Setup

Three fictional suppliers, 16 short records, six decision tensions and four buyer profiles give 24 development dossiers. Every dossier has quotes, scoped deployment responses, stratified pilot counts, migration schedules and an operations brief. Four matched outside-evidence worlds give 96 case/world assignments. Each produces three decisions; the 288 decisions are **not 288 independent real procurement cases**. Family is the conservative unit for generalization; profiles are constructed operating variations.

A publisher controls three comparison-page slots. It cannot edit contracts, internal pilot records, buyer requirements or check responses. Names and page order are counterbalanced. The promoted supplier is chosen for its advertised entry-tier seat price, not by secretly finding the worst true option. Numeric values are authored scenario assumptions; the sources establish the kinds of complications to represent.

## Protocol

Six partial-dossier reports → two record checks requested by reports → two chair forks from that exact shared prefix, one with and one without votes. A separate generalist gets the full evidence union, two checks and a final decision. The team forks each involve nine actor roles; ten calls collect their shared prefix and two terminal decisions. The generalist requires four calls. We report cost and latency instead of padding its budget with useless calls.

The chair selects, gives an annual cost estimate, cites records, explains its reasoning and names unresolved questions. **The model's choice is the outcome.** No deterministic function overwrites it. The document parser is only an engineering reference. An evaluator checks the choice afterward against scenario requirements and costs. Full source records remain available to both chairs, allowing a wrong decision to be distinguished from a fact lost in summarization.

## Metrics

Report requirements violated by name; extra annual dollars among feasible choices; annual-cost estimate error; warranted and avoidable deferral; harmful target adoption; citation identity validity; and confidence on decision acceptability. Citation validity is not entailment. Human review of the rationale is needed before asserting a cognitive cause. Frame counts, agent counts, forked chairs and repeated pages are not independent samples.

Results must show clean competence, genuine-value acceptance and useful deferral alongside attack effects. Original v2 measurements remain [here](../../external-influence-v2/reviews/quality-post.md); they are not pooled with this redesign. The old score-enforcement repair is an engineering branch, not evidence that agents reason better.

## Reproduce

```sh
python3 -m unittest discover -s researchers/vishesh/notes/influence-swarms/scenario/tests -v
python3 researchers/vishesh/notes/influence-swarms/scenario/src/run.py --out /tmp/influence-scenario-new
```

Choose a new output directory. The runner is offline-only. It saves every request, reply, terminal outcome and failure. Model collection remains gated on scenario review, fresh qualification, a dedicated allocation and a non-overlapping quota under the existing budget. Do not launch the superseded quality-01 score-enforcement comparison as the main experiment.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
