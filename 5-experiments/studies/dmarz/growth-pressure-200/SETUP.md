# Experiment setup record: growth-pressure-200 / plan v2

**Status: PLAN ONLY — not launch-ready; no experiment or provider request has run.** Prepared from the [setup record template](../../../toolkit/agent-experiments/templates/experiment-setup.md) under the [setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md). Owner: dmarz. Planning agent: dmarz/astra-ultra-review (Astra Ultra attribution requested by the owner).

## Ownership and question

- Question: does assigning rival incumbents to evade a firm-size levy change sustained evasion by explicitly rule-bound challengers, and does enabling peer messaging change that effect?
- Decision: whether a larger investigation of economic pressure and rule adherence merits further work; a valid negative result remains useful.
- Research status: prospective exploratory hunch in owner notes. No formal accepted hypothesis or independently reviewed experiment is claimed. Formal survey/hypothesis and applicable review status must be resolved before launch. Historical waivers for predecessor runs are not silently extended.
- Design review: three parallel subagents of the same dmarz planning session reviewed economics, resource arithmetic and inference. [Original review](reviews/design-review.md) and [v2 review](reviews/design-review-v2.md). This is not a different-researcher review.
- Prior evidence and diagnosis: [PLAN, Question and prediction](PLAN.md#question-and-prediction), predecessor [results](../sybil-rules-180/RESULTS.md) and [replication post-mortem](../sybil-rules-180/reviews/chain-004-post.md). The former prohibition result did not establish resistance to successful cheating peers; population topology, growing capital and the levy all change here. See also the [diagnosis runbook](../../../toolkit/agent-experiments/DIAGNOSIS.md).
- Current stage: publish prospective design and arithmetic, before experimental implementation. Next action: resolve applicable research-review scope, then implement only this design from the worker template and prepare its offline checks. There is no launch command or server allocation in this publication.

## Gate evidence

Assessment by dmarz/astra-ultra-review, 2026-10-04. Publication checks are separate from scientific gates.

| Gate | Status | Evidence | Next action |
|---|---|---|---|
| G0 Question and applicable research gates | pending | Closest prior work and claim boundaries in PLAN; same-researcher design review | Resolve current formal/exploratory research and applicable reviewer requirements before any experimental run |
| G1 Plan written before implementation | pass for planning scope | PLAN.md and design.json precede any simulator/dispatcher implementation in this study | Preserve this revision; amend prospectively if needed |
| G2 Instrument and offline checks | pending | Arithmetic validator only; no experimental runtime | Implement accounting, observations, role overlays, evaluator, fork and failure tests |
| G3 Current attempt admission | pending | No attempt prepared; no model/price/quota/resource/budget receipts | Publish/freeze runtime inputs, verify exact public plan, reserve shared budget and current exclusive allocation |
| G4 Qualification before scientific escalation | pending | Fixed qualification envelope in PLAN; zero observations | Execute only after its admission; main requires fresh stage admission after pass |
| G5 Reconciliation and closeout | pending for future runs | This publication spent no simulation/API budget | Reconcile every future assigned outcome, charge, artifact and claim |

## Design and instrument index

- Prospective design: [PLAN.md](PLAN.md), [design.json](design.json). v2, dated 2026-10-04; [prospective amendment](AMENDMENT-02.md) preserves the unrun v1 publication. Git publication supplies an immutable revision; operational preregistration must pin its complete commit and content hash, not a moving main URL.
- Independent units: 12 isolated 50-owner markets, paired across four continuations, scheduled as three 200-owner batches. No cross-market communications, shared economic state or shared sampled shocks. Primary 24 focal owners/arm; secondary 552 fixed ordinary owners/arm. Counts are planned, observed zero.
- Precision: exploratory 12 market pairs in one task family and one model, no empirical variance/power claim. Primary D − B (four versus zero assigned evaders, messaging on); secondary interaction (D − B) − (C − A). Five silent opening rounds precede the four-way fork. The same neutral communication invitation is present in every arm; A/C cannot send or receive messages. Paired market bootstrap resamples all four arms jointly; three batch-level sensitivities and all market differences shown. Boundary intervals and missing-outcome bounds respect the interaction range [−2,2].
- Development/qualification/scientific namespaces, treatment overlays, context limits, accounting contract, missingness and stopping rules: PLAN. No sealed case file or production runtime yet exists.
- Agent definition: persistent beneficial-owner state/memory, one decision per live owner/round; firm identity does not multiply agents. Effective JSON schema, rendered prompts, exact snapshot, source/evaluator/dependency hashes remain implementation outputs to freeze before qualification.
- Native configuration: proposed gpt-6-sol, low effort, 6,144 maximum input tokens and 1,024 total completion tokens. Current route, served revision, prices and remaining quota are unverified. No inherited qualification after changing the environment.
- Startup/reset/fork: required behavior specified in PLAN; not implemented. No template interface is asserted to enforce this design automatically.
- Offline checks: the included src/check_plan.py validates counts, accounting examples, timing arithmetic and local links; it does not simulate agents, test the proposed economics over time, or establish qualification.
- Visual mapping: market/arm/round trajectories of output and capacity share, levy, wealth and first evasion; seeding-by-messaging/exposure table and paired-effect plot. Any later renderer must use saved ledger values, mark missing states, retain history and offer Markdown/CSV fallback. Native memos do not expose private reasoning.

## Current attempt admission

Operations entry: manual, documentation only. No experiment adapter or hub registration is created. Follow the [operations guide](../../../toolkit/agent-experiments/OPERATIONS.md) when implementing one.

| Operation | Exact command or unsupported reason | Evidence |
|---|---|---|
| Inspect and validate this plan | `python3 5-experiments/studies/dmarz/growth-pressure-200/src/check_plan.py` from repo root | Offline arithmetic/link check; no model calls |
| Rebuild publication copy | `python3 5-experiments/studies/dmarz/growth-pressure-200/src/build_plan.py` | Renders the same prose with repository links for a filed document |
| Prepare or dispatch a stage | Unsupported: runtime and admission not implemented | No run prepared |
| Resume interrupted execution | Unsupported: no attempt; future attempts retain ledger and ancestry, never reset clock | No resume command claimed |
| Analyze model evidence | Unsupported: none collected | No results inferred from this plan |
| Stop and close out a run | No workers exist; future finite runtime must implement the documented deadline | No resource claim to release |

- Attempt/stage/status: none / publication / complete after GitHub verification. Execution remains not started.
- Current pre-run assessment: not ready. This describes existing work; it is not a request for the user to approve an unspecified implementation.
- Immutable public plan URL and expected content hash: obtained from the final publication commit and PLAN file at launch preparation. There is no public-preflight receipt yet; publication alone cannot substitute for current native admission.
- Registration: later create experiment and condition-specific TLDRs with run/arm/seed bindings and exact source revision. Use registration id growth-pressure-200 after the research gates permit it.
- Budget authority: current researcher README records $500 total API spend across dmarz experiments. No fresh $500 allocation is assumed. No spend or reservation has been made here. Reconcile existing portfolio charges and holds before the bounded qualification; main admission also requires the measured projection with 25% margin to fit the remaining allocation.
- Caps: 54,096 planned native decisions, 541 additional transport attempts, maximum 54,637 HTTP attempts; 128 globally in flight; 60-minute execution clock including qualification and closeout; stop new requests by minute 52. Configured token caps and per-request maximum reservations are mandatory.
- Runtime capacity: 12 claimed simulation workers, one active run per server, proposed but not allocated. Current approved-account identity, workload, claim expiry and deployed hashes must be verified privately before use. No private address, hub URL, account ID or credential appears here.
- Credentials: project-specific OpenAI credential alias to be resolved by the operator using current approved configuration. Availability and transfer status are unverified. Do not fall back to a personal/default account, expose credential values, or assume the predecessor's credential remains available.
- Go/no-go: future operator must attach current receipts. The user requested a plan and GitHub publication; this task launches nothing.

## Attempt and repair history

No attempts, paid probes, scripted experimental episodes or runtime repairs. v1 was published at commit 88faf68173b29a4874ea87565ce366b02f32579c and remains available unchanged in Git and the filed v1 artifact. The owner requested publication of the proposed communication comparison; v2 replaces the dose ladder prospectively before implementation or collection. See AMENDMENT-02.md. Proposed mechanics are not represented as measured or qualified.

## Closeout

- Execution: not started. Response validity: not measured. Qualification: not run. Scientific conclusion: none. Publication: prospective plan and arithmetic only.
- All later outcomes, failures, incomplete arms and unknown charges must be retained; no treatment-based stopping or silent sample reduction.
- Actual simulation/model cost for this planning task: zero. Infrastructure changes: none. There are no workers or claims to release.
- Reproducible document builder and input provenance filed through Flight Deck. Repository checks and strict project checks must pass before final push.

## Completion and successor handoff

Latest native attempt: none. Operational and scientific post-mortems: not applicable until a run exists. [Run-quality rubric](../../../toolkit/agent-experiments/RUN-QUALITY.md) remains required for future attempts.

Next action: implement the exact prospective contract after resolving G0 scope; complete G2; then prepare a bounded G3 qualification packet. Acceptance: accounting/evaluator/branch isolation and deadline fault tests pass, full packet fits, source/plan/model bindings are immutable, and current resource/budget receipts are present. Only native qualification can determine whether the one-hour main comparison is feasible. Do not launch a reduced or changed study from this handoff without a prospective amendment.
