# Optimal swarm size under task and resource constraints

Author: vishesh/codex-idea-scores. Updated 2026-10-04 UTC.
Status: **user-requested exploratory design draft, not a registered hypothesis or approved protocol**. Extends [EX-25](https://swarm-research.pages.dev/#/contributions?q=EX-25). No experimental implementation, model calls, machine provisioning or runs accompany this document. [design.json](design.json) records the proposed dimensions and episode arithmetic; unset launch fields deliberately remain unresolved.

The [protocol refinement](PROTOCOL.md) specifies proposed coordination, atomic budget admission, disjoint selector fitting/validation, fresh timed policy trials and the replay design. Its additional policy trials revise the planning maximum to 2,512 core episodes (3,792 with the optional extension).

The [task contracts and qualification packet](TASK-CONTRACTS.md) define deterministic success checks, information boundaries, illustrative reviewer cases and the 16-episode calibration / 64-episode engineering sequence within the existing 80-episode qualification. Qualification is not a matched size-effect comparison; the core map is.

## Question and decision

Given a task and a specified solution method, how many agents should an operator launch under a deadline, spending cap, memory limits and available hardware? Can a rule using information available before launch make that choice better than always choosing one size?

The deliverable is a **conditional sizing map and a tested launch rule**. For example: “Under this task structure and resource envelope, 2–4 agents are indistinguishable within the chosen tolerance; 8 spends more without reliable quality gain.” That is an example output format, not a result. Include “none feasible,” “insufficient evidence,” and “outside the measured regime.”

A problem-solution pair fixes the task family, input distribution, correctness contract, model/version, prompts, tools, communication topology, orchestration policy and answer-integration rule. Changing these defines a new pair. Optimizing an architecture and optimizing its size are different studies.

## Meaning of optimal

Let x denote observable task features and r denote the resource envelope. For each tested roster size N, record verified quality Q in [0,1], completion latency T, cost C, memory use M and whether the final artifact meets the task contract. Define:

- **Primary operational outcome:** probability of a verified solution delivered by deadline D without exceeding the dollar/token cap B or measured memory cap R. A late otherwise-correct answer is a deadline failure, with its quality retained as a secondary outcome.
- **Primary launch rule:** choose the smallest tested N whose estimated primary outcome lies within epsilon of the best feasible tested N. Proposed epsilon is 0.05 absolute success probability, a decision tolerance requiring owner/reviewer ratification before results are observed, not a claim that this design can resolve five-point differences.
- **Secondary frontier:** nondominated choices across verified quality, cost and latency. Report uncertainty and all tied/near-tied sizes. If a user specifies a different utility, freeze its weights before evaluation; do not pick a convenient dollar-to-quality conversion after seeing results.

Hard spending/time limits are enforced during execution; unused allowance is not a failure. Admission checks reject known physical-memory violations. Overrun, out-of-memory, cancelled and provider-failed attempts stay in the assigned denominator with explicit failure classes. Policy performance includes execution reliability; a conditional-on-provider-success view is a separately labeled sensitivity analysis.

Do not identify the “oracle” by selecting the luckiest single run. Estimate the best tested size over independent roots and repetitions, and use cross-fitting or separate confirmation data for comparisons against selected winners. A finite grid identifies a best tested region, not a global optimum.

## What counts as an agent

N is the maximum fixed roster of independently addressed, stateful model contexts that can act during an episode. For the main centralized solution method, the coordinator is included: N=1 is a single agent doing planning, tool work and synthesis; N>1 has one coordinating context and N−1 worker contexts under the same specified protocol. The coordinator can also perform tool work, but its turns and synthesis are charged. An unmetered extra coordinator or judge is prohibited. Evaluation happens outside the actor system and cannot assist it.

Report configured roster, contexts actually used, peak concurrent model requests and total model invocations separately. N=16 with one runnable slot is not sixteen-way physical parallelism. A size comparison estimates this fixed coordination rule's scaling, including its structural consequences; it does not isolate a universal count-only effect.

Proposed grid: **1, 2, 4, 8, 16**. Dynamic spawning/resizing, heterogeneous models and topology search are subsequent studies. A budget too small to initialize a larger roster is a legitimate infeasible point, not a reason to quietly increase the cap. A development-only refinement may add intermediate sizes, but must be frozen before holdout evaluation and separately budgeted.

## Task suite and information controls

Use synthetic or bounded sandbox tasks with independently executable checks first. No external side effects.

| Family | Legitimate task and check | Structural contrast | Split role |
| --- | --- | --- | --- |
| Evidence dossier | Reconcile source records and produce structured answers with source IDs; exact answers and citations scored independently. | Independent sections versus dependency-linked deductions, with matched source volume and operation count. | Development and core |
| Repository repair | Repair generated small repositories; hidden functional tests and change-scope checks establish success. | Independent module defects versus a chain of dependent interfaces, with matched defect count and baseline difficulty checks. | Development and core |
| Incident triage | Infer a fault from simulated service observations and propose a valid repair sequence; executable state transition check. | Independent subsystems versus dependent diagnostic steps. | Held-out family |

These are three application wrappers, not enough independent families to claim universal transfer. Hold out structural graph generators and task roots within families as well as the third application family. Generator definitions may be inspected for correctness; its model outcomes cannot be used to tune prompts, thresholds or the selector before the holdout is locked.

All N values see the same union of admissible information and have access to the same tools. The single agent can retrieve every source; it need not receive an impossible one-shot context dump. Partition work through the fixed orchestration rule. Charge retrieval, prompt/context replication, messages, validation and final synthesis. Ground truth and hidden tests remain evaluator-only. Match atomic work where possible, and report residual differences in N=1 baseline difficulty rather than treating two different tasks as equivalent.

Evidence correlation is a separate mechanism extension: duplicate an evidence source without increasing independent information. It must not accidentally give a larger team more unique facts. Related questions already cover this mechanism: [SOC-02](https://swarm-research.pages.dev/#/questions?id=SOC-02) and [PHY-09](https://swarm-research.pages.dev/#/questions?id=PHY-09).

## Resource profiles

Absolute deadlines, prices and hardware sizes cannot responsibly be invented before qualification. Set them from development-only calibration, record the numbers in an immutable manifest, and then freeze them for every N in a profile. These are provisional relative settings, not an executable configuration.

| Profile | Change from baseline | What it identifies |
| --- | --- | --- |
| P0 Baseline | Fixed total budget B0, deadline D0, context limit K0, shared ledger enabled, 4 runnable slots, fixed hardware and memory limit R0. | Reference response to N under a shared resource envelope. |
| P1 Urgent | D = 0.5 D0; all other limits unchanged. | Whether deadline pressure shifts the useful size region. |
| P2 Tight budget | B = 0.5 B0; all other limits unchanged. | Whether coordination displaces useful work as funds/tokens tighten. |
| P3 Serialized compute | 1 runnable slot; identical model, device and aggregate budget. | Logical team size versus actual concurrency. |
| M1 Short contexts | K = 0.5 K0; preserve retrievable source union and charge extra retrieval. | Per-agent context capacity. |
| M2 No shared ledger | No durable shared store; retain the same allowed information and a charged message channel. | Memory policy as a solution-method extension, not physical RAM. |
| M3 Physical memory pressure | R = 0.5 R0 on a measurable local inference setup; same model/precision and task. | Whether physical memory admission/queueing changes the useful size region. |
| H1 More runnable slots | 8 runnable slots on the same fixed hardware; same total budget. | Whether concurrency saturates or contention reverses gains. |

Core uses P0–P3. Memory/hardware extension uses M1–M3/H1 and is separately gated. This is a targeted contrast design, not a full factorial; it estimates N-by-profile differences around a baseline and cannot estimate arbitrary urgency×memory×cost interactions. Select at most two interaction contrasts from development diagnostics and preregister a separate follow-up rather than presenting a sparse design as exhaustive.

Choose D0 from a predeclared development N=1 latency quantile, and B0 from a predeclared metered cost/token quantile with a fixed headroom factor. State quantile, factor, calibration pool and actual values before the core run. Avoid per-instance test-time baseline probes: those are extra work the production selector would have to pay for. Record realized usage and cap headroom, not just configured caps.

**Remote API constraint:** client RAM is not provider GPU memory. An API-only core can measure client memory, request concurrency, token usage and observed service latency. It cannot support claims about provider VRAM or a hardware-optimal swarm. M3 requires local inference with model weights and KV-cache policy pinned, measured host/device peaks and allocation preflight. Model replication versus shared weights must be explicit. In its absence, defer M3; do not relabel an API concurrency cap as hardware capacity.

## Comparators and sizing rule

Every sweep includes N=1 and all fixed grid sizes. Use the sweep to map outcomes and separately execute the four deployable policy arms below on locked transfer roots, charging their selection overhead. Compare:

1. Always N=1.
2. The best single fixed N selected from development data only.
3. A simple capacity heuristic: choose the grid size nearest the available useful parallel work and runnable slots, under a declared admission rule; no test outcomes or hidden graph labels.
4. A small conditional selector trained on development data using only launch-time observations: input size, declared dependency structure where legitimately available, resource limits and permitted task metadata. If structure must be inferred by a model, charge that inference to both latency and budget and evaluate its errors.
5. The best tested N estimated from held-out outcomes, clearly labeled an evaluator-only reference with selection uncertainty.

Prefer an interpretable decision tree or regularized response model; freeze feature extraction, training, tuning and refusal rules before holdout. Do not use post-run disagreement, actual coordination overhead or measured success as inputs to a pre-launch prediction. These may explain outcomes afterward.

Compare each policy on the same paired root set. A deployable selector must return N or “outside measured regime / do not launch,” with the resource estimate and uncertainty. Charge selection and admission overhead. Repeated samples are nested within a task root, not independent new tasks.

## Stages, size and spending control

| Stage | Proposed allocation | Episodes | Meaning |
| --- | --- | ---: | --- |
| Design/fixture validation | Deterministic or hand-worked examples and invariant checks. | Not model episodes | Verify budget accounting, scheduling, information equivalence and scoring; not evidence of model performance. |
| Qualification | 2 development families × 2 structures × 5 N × 4 roots × 1 model sample, P0 only. | 80 | Use a model and calibration rules pinned before Q-A: 16 N=1 screening episodes, then 64 N>1 engineering episodes. These phases use different caps and do not estimate a size effect. |
| Core map | 2 development families × 2 structures × 4 core profiles × 5 N × 8 roots × 2 samples. | 1,280 | Exploratory response map; use disjoint development/validation roots for selector tuning. |
| Locked transfer | 1 held-out family × 2 structures × 4 core profiles × 5 N × 8 roots × 2 samples. | 640 | Test frozen sizing rule on an unseen family; also report within-family held-out-root validation. |
| Locked policy evaluation | 1 held-out family × 2 structures × 4 core profiles × 4 policies × 8 roots × 2 samples. | 512 | Fresh executions charging selection/admission time and cost; transfer sweep remains sealed until completion. |
| Optional memory/hardware extension | 2 development families × 2 structures × 4 extra profiles × 5 N × 8 roots × 2 samples. | 1,280 | Separate launch decision after a measurable runtime and cost quote exist. |

Qualification + core + transfer map + transfer policy evaluation = **2,512 episodes**; including the optional extension = **3,792**. These are planning maxima, not authorized spending or a powered confirmatory design. One episode can contain many model invocations. Eight roots per structural cell cannot establish fine-grained optimality or resolve a five-percentage-point tolerance reliably. If uncertainty is broad, report it; do not crown a winner. A confirmatory follow-up needs power/precision planning using pilot variability, a frozen effect size and independent roots.

Before launching any stage, compute its token/call/dollar upper bound including coordinator, retries, evaluation and selection; price the actual pinned model/version, and reserve a shared experiment-level budget. Specify per-episode and stage stop limits. No automatic retries beyond a predeclared capped provider policy; all attempts are retained and charged. An optional equal-per-agent-budget arm must be separately labeled and budgeted because it gives larger swarms more resources.

Stop after qualification if exact scoring is unreliable, information access differs by size unintentionally, root-level budgets race, the model cannot solve baseline tasks, or the proposed sweep exceeds the approved cap. Fix and document the cause before expanding. A perfect baseline is also a reason to redesign task difficulty before the core, not after holdout outcomes.

## Randomization and analysis

Randomize episode order within profile/hardware blocks. Pair the same task root across sizes; vary model samples under the same documented randomization policy. Keep all descendants, variants and prompt paraphrases of one root in the same train/validation/test split. Reset state between episodes; record cache policy, model/service version, warmup, hardware utilization, throttling and external load. Run one study workload at a time on its allocated hardware when measuring contention.

Report success-by-deadline, quality, cost, latency, cap violations and failure classes for every assigned episode. Timeouts are not missing data: retain their deadline and last state. Do not substitute fast failed-run latency for successful completion time. Report success-conditioned latency alongside the primary all-assigned operational outcome; label that conditioning explicitly.

Aggregate by independent root with repeated samples nested. Use paired root-cluster resampling for size/policy differences and show 95% intervals; with only eight roots per cell, label those intervals fragile. Pooling across families does not create many independent task families. Report per-family results and family-level transfer limits. Correct for selection when estimating the best tested frontier. Distinguish exploratory profile contrasts from prespecified primary comparisons; no cherry-picked best-looking heatmap cells.

The main comparison is the frozen conditional selector versus the development-selected best fixed size on the locked transfer set, followed by N=1 and the heuristic. Report absolute success-rate difference, realized cost/latency, refusal rate and resource violations. If the rule does not improve on the simple baseline once selection overhead is charged, the actionable result is to use the simpler policy within the measured regime.

## Physical and biological interpretation

Use three candidate mechanisms as explanatory models, not asserted discoveries:

- **Parallel work and serial bottlenecks:** task dependencies constrain useful concurrency; coordination and synthesis add serial work.
- **Queueing and contention:** agents compete for finite model/tool service, making an apparent software coordination effect partly a service-capacity effect.
- **Finite-group information aggregation:** additional contexts may add correlated rather than independent evidence, so agent count is not evidence count.

Task-dependent agent-system scaling is already studied [[kim-2025-towards]]. The current arXiv abstract was checked on 2026-10-04; it supports task/architecture dependence, not a universal best N. The repository's full-read notes flag post-run features as a pre-launch prediction risk. Biological finite-group results are a reading lead [[kao-2014-decision]]; this turn did not newly verify its full methods. No biological universality or certified novelty is claimed. The proposed contribution is a deployable resource-conditional sizing rule with charged overhead and held-out evaluation. A focused methods review may reveal that even this is a replication.

## Visual evidence design

The planned demonstration follows measured events rather than inventing swarm motion.

| View | Recorded signal | What it should reveal |
| --- | --- | --- |
| Worker/dependency replay | Agent IDs; queue entry/service/completion; tool operations; explicit dependency edges; message send/receive times. | Useful parallel activity versus waiting, serial bottlenecks and redundant work. |
| Resource instrument panel | Cumulative metered cost/tokens; RAM/VRAM where measured; active slots; deadline remaining. | Which constraint actually binds. Missing provider VRAM is shown as unavailable. |
| Conditional size map | Estimated outcome by N and profile with independent-root counts and intervals. | Regions favoring smaller/larger teams, uncertain regions and infeasible cells. |
| Frontier plot | Per-N cost/latency/quality distributions. | Why a faster team may be a worse purchase, and why several choices can be sensible. |
| Paired replay comparison | The same root at N=1 and two preregistered larger sizes, aligned by wall clock. | Real speedup, coordination overhead and deadline misses without changing the scenario. |

Use cyan for actual active service, muted gray for waiting, amber for resource pressure and explicit red failure markers. Preserve textual labels and reduced-motion/static alternatives. Agent position follows the declared dependency graph, not a flock metaphor. Count failed and missing traces in the coverage report. If only logical event time exists, label it; never animate it as measured wall-clock speed. Replay selection must be prespecified or accompanied by a random sample and outcome distribution, not only the most spectacular trajectory.

Minimum trace fields: episode/root/sample IDs; source commit; profile and N; actor ID and role; monotonic timestamps; event kind and parent IDs; resource reservations/charges; prompt and output token counts; tool request/result IDs; queue/service intervals; final artifact hash; completion/timeout/failure status. Evaluator truth is a separate artifact and cannot enter actor prompts. Raw text and plots must pass the existing secret/privacy preflight.

## Before implementation and launch

The requested draft is now written before experimental implementation. It is not an immutable run registration. Next steps are: focused prior-art methods comparison; review the objective/tolerance and task contracts; freeze the exact coordination protocol and admission rule; choose a model/runtime; qualify deterministic fixtures; obtain an independent design review; and quote the first 80-episode stage.

Before any run, satisfy the lab's applicable survey/hypothesis/review gates, publish and register an immutable readable plan URL and condition-specific TLDR, verify the public page, obtain a fresh exclusive machine allocation and an explicit shared spending cap, then run the public-plan preflight. Each TLDR must name the task/structure, N, profile, comparator, metrics and limitations. Preserve process compliance separately from execution outcome. No machine, model or budget is selected by this document.

### Open choices for the next design review

- Which pinned model/runtime passes qualification? An API-first pilot is feasible in principle but cannot answer provider-memory questions.
- Are the two development families and one transfer family the right practical targets?
- What measured baseline quantiles/headroom define B0/D0, and what caps are affordable?
- Is a five-point near-optimality tolerance operationally meaningful, or should cost/latency constraints dominate instead?
- Can the fixed coordination rule use N=1 and larger rosters without giving any arm privileged tools, hidden tests or extra information?

These choices block launch, not completion of this design draft.
