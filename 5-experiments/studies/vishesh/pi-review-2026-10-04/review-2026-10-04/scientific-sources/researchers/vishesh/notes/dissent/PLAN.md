# The Right Dissenter: bounded evidence challenges

Design version RD-1, 2026-10-04. Owner: vishesh/codex-decision-models. Areas: **dissent**, **decision-models**. Canonical question DM-03, formerly Stop-Signal Swarm. This is an exploratory design and implementation plan requested by the owner, not an accepted hypothesis. It is written before implementation. No native experiment has run.

## TLDR

Can a small minority improve a collective decision by earning a bounded independent check, while avoiding false reversals, repeated interruption and missed deadlines? Three synthetic scenarios test copied evidence, applicability of a counterexample, and changing facts. Compare a bounded evidence protocol with majority, unconditional veto, unconditional checking, resource-matched random checking and a pooled-evidence solver. Measure correct on-time decisions over all assigned cases, correction and corruption separately, checking cost, withdrawal and recovery. All environments are controlled; results would not establish reliability on real maps, deployments or operations. Model-free fixtures validate software only. Native execution needs a registered immutable public plan, independent review, a dedicated host and a separately authorized budget.

## Question and prediction

The practical construction is an **evidence challenge protocol**, not an agent instructed always to disagree. A dissenter specifies the disputed action, cites available records, proposes a permitted discriminating check and states the result that would make it withdraw. Every participant has this route. A scarce check is allocated by current evidence, not rank, vote count or a privileged role named “correct dissenter.”

The exploratory prediction is that a bounded evidence protocol can recover some wrong majorities with fewer false reversals than unconditional dissent, and less checking than checking everything. It may fail: the Jev judge may not interpret evidence well enough, copied records may still dominate, or a simple exact rule may outperform it. This study must record those outcomes. It does not assume that minority opinions are usually right.

Closest priors include minority-aware aggregation [[he-2026-minority]], withholding and reconsideration [[mansuri-2026-multi]], honeybee cross-inhibition [[seeley-2012-stop]], reused evidence [[hamdi-2013-removal]] and correlated model judgments [[rao-2026-jev]]. The proposed increment is a bounded, auditable acquisition-and-withdrawal protocol across three different information failures. Biological precedent motivates inhibition; it does not establish model equivalence or novelty.

## Setup

Three scenarios share a common action vocabulary: **PROCEED**, **HOLD**, **DEFER**. DEFER is an unresolved decision with a cost; it never counts as a correct completed decision. Scenario-specific text defines what proceeding means. All action execution is simulated.

| Scenario | Concrete decision | Correct dissent | Incorrect dissent / control | Distinct scientific question |
|---|---|---|---|---|
| **The Missing Bridge** | Send a simulated survey convoy over a bridge or hold it | One fresh inspection contradicts several endorsements copied from one old survey | Wrong bridge, stale survey, correlated copies, noisy sensor, already-correct majority | Can independent evidence outweigh apparent numerical agreement? |
| **The Passing Build** | Release a synthetic build or hold it | One reproducible failing test matches the build, platform and required capability despite a green aggregate summary | Wrong build/platform, optional test, cached result, passing rerun | Can the group recognize an applicable counterexample and distinguish it from an impressive irrelevant one? |
| **The Alarm That Became True** | Continue a simulated process or pause it at successive decision epochs | A previously disproved alarm is followed later by a genuinely new event | Repeated disconfirmed record, stale alarm, new record with no change, true-to-false reversal | Can dissent withdraw without permanently silencing its source, and reopen only on new evidence? |

Actor inputs contain the current task, permitted actions, frozen criteria, logical time, visible evidence, votes, challenge and bounded verification result. They never contain gold labels, condition names, correctness flags, the planned future change or evaluator-only outcomes. Agent and source names are neutral and counterbalanced. Persistence lives in explicit records and policy state, not model-weight changes.

The initial causal screen uses explicitly scripted votes and challenge packets so majority correctness and challenge quality can be independently manipulated. It estimates response to controlled consensus, not spontaneous formation of a right minority. The native qualification path collects private Jev votes from disjoint agent views before social exposure. A later natural-minority stage uses those model-produced votes and reports every case, including unanimous teams and cases without a useful dissenter. No successful-right-minority filtering is allowed in the main denominator.

## Protocol

1. **Private decision:** retain each agent's initial action before exposing peers' votes. Evidence allocation is frozen per root case. In fixture mode these votes are labelled scripted.
2. **Challenge:** a participant submits `{claim, alternative, evidence_ids, check, withdraw_if, expires_at}`. Check names come from a fixed allowlist. Evidence IDs must be visible; a new identity cannot create a new source. User-authored instructions inside reports are untrusted text.
3. **Admission:** hard checks reject invalid references, wrong scope, expired challenges and an already-resolved identical evidence fingerprint. These checks are identical in all applicable arms. A typed Jev decision then selects CHECK, KEEP or DEFER from the public packet. The model cannot alter tool permissions, budgets or the world.
4. **Verification:** at most one independent check per static decision and at most two per temporal episode. The check consumes one logical tick and one observation unit. Timeout, absent data and invalid responses remain explicit. The check returns an observation with its own provenance, not an evaluator verdict about whether to trust the dissenter. Sensor-error and unavailable-check conditions are separate cells.
5. **Resolution:** given the same task criteria plus the returned observation, select PROCEED, HOLD or DEFER. A model failure produces an unresolved terminal outcome, never a silent majority fallback. All outcomes remain in the assigned denominator.
6. **Closure:** record supported challenge, withdrawn challenge, unresolved challenge or unavailable check. The proposed alternative and final action determine support/withdrawal for the trace; evaluator truth independently judges correctness. This is a protocol state, not evidence of an agent's private belief.
7. **Reopening:** identical records cannot repeatedly consume capacity. A new source observation or changed task version can open a new challenge. The previously wrong source is not permanently blacklisted. Memory expiry and scope prevent yesterday's closure from suppressing today's change.

The source-aware gate cannot see true source reliability unless that reliability is explicitly available to every comparator. Hidden ancestry is an additional condition. A full-provenance oracle is labelled an upper bound. A model is never asked to infer malicious intent from being wrong.

## Comparators and resource accounting

| Arm | Policy | Purpose |
|---|---|---|
| majority | Commit the initial majority; ties defer | No-intervention reference |
| blind-veto | Adopt the challenger's alternative after basic validity checks | Exposes the cost of trusting every dissent |
| always-check | Check every valid new challenge within the cap, then resolve | Strong baseline; if it wins, selective admission may be unnecessary |
| evidence-gate | Typed admission followed by a bounded check and typed resolution | Proposed construction |
| matched-random | Allocate the same predeclared check quota independently of evidence quality | Separate informed selection from simply spending checks |
| pooled | One solver receives the same union of initially available records | Separate collective benefit from information pooling |
| exact-reference | Deterministic interpretation of the controlled report grammar | Engineering ceiling within this synthetic domain, never native model evidence |

Compare policies on paired root cases with the same initial records and potential observation tape. Check use can differ; report cost–quality frontiers rather than calling that equal resource use. A quota-matched secondary comparison freezes the quota on development cases; it must not choose test-case checks after seeing another arm's success. All final adjudicators see the same verifier output for an equal-acquired-information comparison. Shared private votes may be cached across policies only when those votes were collected before treatment and attributed once to collection cost; per-policy counterfactual cost is also reported.

## Conditions and parameters

The complete parameter ledger is in PARAMETERS.md; the initial implementation exposes scenario, seed, decision truth, majority action, challenge scope, report freshness, duplicate ancestry, check availability, check correctness, check delay, deadline and temporal change. Later sweeps are explicitly separate from implemented factors.

Core coverage crosses majority correct/wrong with challenge correct/wrong/irrelevant/absent. Do not use only favorable right-dissenter cases. Balance PROCEED and HOLD truths, object IDs, source IDs and answer order. Include good-majority/bad-minority and bad-majority/bad-minority cases. DEFER and no-evidence cases test answerability.

Development case seeds 1100–1199 are for construction and unit examples. Fresh qualification seeds 2100–2199 and confirmatory seeds 6100–6199 are reserved; do not inspect them while repairing development behavior. Root scenario/seed is the unit of dependence; temporal steps, agent votes and policy arms are not independent samples. The first native screen is competence and mechanism qualification, not a powered scientific sweep. Freeze any larger assignment table and power calculation in a later version before holdout access.

## Metrics

Primary: **correct on-time committed decisions / all assigned decision opportunities**, separately by scenario and paired policy difference. For temporal episodes report both decision-level completion and episode-level cumulative loss. Failures, timeouts, DEFER and unstarted assignments remain visible; unstarted cases do not silently vanish.

Secondary: wrong-majority corrections / initially wrong commitments; harmful reversals / initially correct commitments; unnecessary holds on safe cases; wrong proceeds on unsafe cases; unresolved decisions; verification count and failures; calls, tokens, elapsed time and reserved/actual cost; repeated challenges suppressed; supported challenges, withdrawals, valid reopenings and latency after a true change. Report raw counts and denominators, including zero-denominator cases as unavailable.

Use an explicit loss vector in sensitivity analysis rather than hiding asymmetric costs in one accuracy number. Initial illustrative weights: wrong PROCEED 5, unnecessary HOLD 1, DEFER/deadline miss 2 and check 0.1; these are design preferences, not empirical facts. Show raw outcomes and sweep harm ratios before any deployment recommendation. Bootstrap paired root cases for uncertainty only once independent roots are numerous enough. Small qualification samples support debugging, not broad effect claims.

Acceptance before a broader native study: no truth leakage or assignment loss; strict response/schema/model checks; clean competence on both action labels and scope variants; manipulation actually produces both helpful and harmful challenge opportunities; timing/cost checks pass. Prospective competence targets are at least 90% valid completions, 85% exact clean-action accuracy and 75% in each scenario, with sample counts and uncertainty shown. Failure blocks a broad sweep and calls for a new diagnostic version, not repeated qualification until a lucky pass.

## Visualization mapping

Version RD-V1. A saved-event replay shows initial votes, the challenge, its evidence ancestry, a bounded check, and the final action. The Missing Bridge has a route diagram; The Passing Build has a version/platform/test matrix; The Alarm That Became True has a timeline with disconfirmation and a later new event. Shared panels show votes, unique sources, checks used and outcome. Agreement and evaluator correctness are separate encodings.

Time is logical ticks; wall latency is a distinct recorded field. Show pending, failed, unavailable and not-run records explicitly. Retain every event, initial and final states, source/request hashes and evaluator-only truth in separate data compartments. Actor payload construction must whitelist fields and be checked by mutation tests. A viewer may reveal truth, but that overlay is never sent to the model.

The initial preview uses clearly labelled unit-test fixtures with scripted decisions. It is an interface and state-machine check, not a pilot or evidence of Jev behavior. A real run will render only its saved traces; unsupported HTML on Swarm Live needs a public image/GIF fallback and verified playback. No Cloudflare deployment is authorized here; DMars/CD owns shared deployment. Local preview does not establish public hosting.

## Execution gates and publication

Write and commit this plan before implementation. Before any scientific or qualification run, register its immutable GitHub URL with a condition-specific TLDR and verify the public page using public_plan.py or equivalent. Native launch additionally requires the completed prior-art/review gate or an explicitly scoped exploratory diagnostic approval, an exclusive experiment allocation, fresh model/provider qualification and a non-overlapping authorized spending cap. An implementation request does not supply a dollar allowance. The default cap is zero and the runner must refuse live dispatch while gates are missing.

Offline local unit tests are permitted and do not allocate a fleet machine. They must be labelled software validation and cannot produce a scientific success claim. Source/plan hashes, assignments and outcome accounting are validated before exporting native request packages. Credentials stay in the local protected store; exported payloads and logs contain no credentials or private fleet information.

## Interpretation and stop rules

If majority is already correct everywhere, the corpus does not test correction. If dissent is always correct, it does not test selective trust. If a check always reveals the answer without cost, the practical question is underspecified. If the deterministic reference solves all semantic cases, describe the learned component as unnecessary for those cases. If checking every valid challenge dominates, do not prefer selective admission for aesthetic reasons. If harm increases, a positive correction count does not justify deployment.

Every new attempt has a fresh output directory and a pre/post assessment. Protocol changes increment the design version and invalidate prior source approvals. Holdout failures are outcomes, not permission to retune on the holdout. No claimed result precedes execution.

