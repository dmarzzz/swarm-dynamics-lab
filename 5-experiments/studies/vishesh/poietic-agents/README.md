# Poietic Agents

Current next attempt: [D0-02 repaired diagnostic](D0-02-PLAN.md), owner-approved with a new dedicated Vishesh-named machine; [129 offline checks pass](readiness/D0-02/validation.json). [Pre-run assessment](reviews/D0-02-pre.md) is HOLD on verified original provisioner/account/state access. No new machine or calls.

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-heterogeneous; source `38544138` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Reversible self-differentiation improves lifetime swarm efficiency without losing quality; this intended efficacy claim remains untested. Basis: D0-01 stopped after3calls:Haiku fenced JSON, Qwen correct fetch thenHTTP429, Jev unstarted. No full qualification or efficacy comparison; offline checks do not supply missing native behavior.
- **sample_size_summary:** S0-01:36calls;S0-02:1call. D0-01:3/36started on the first of3planned paired roots,1correct action,33unstarted,36terminal;0complete sequences and0swarm efficacy roots. Four steps within a case are dependent.
<!-- experiment-evidence:end -->

**Prospective design and qualification package v0.2 · 4 October 2026 UTC · vishesh/codex-heterogeneous · HX-31**

This revision contains retrospective closeouts for S0-01, S0-02 and the completed D0-01 diagnostic. S0-01 used the [original preregistered plan](https://github.com/dmarzzz/swarm-lab/blob/f502b05a062925bdaa419d822e1e75f912bb4be4/researchers/vishesh/notes/poietic-agents/README.md); this updated revision was not its preregistration.

An initially uniform swarm learns which capabilities to keep, share, simplify and restore. This is the selected self-differentiating-swarm project, including the owner's workflow-hardening interpretation of HX-37. It remains exploratory. The independent researcher feedback has been received and its three measurement changes are implemented; native qualification and the question-specific prior-art work remain open. Both native qualification attempts failed at interface boundaries; no model is qualified and no swarm efficacy result exists.

## TLDR

Can identical generalist agents discover a cheaper division of labor without becoming brittle? Give every agent the same starting model, tools, skills and data permissions, then let agents establish shared data services, unload capabilities, choose cheaper execution and revise their connections. Compare with unchanged generalists, ordinary shared caching, engineered static specialists and, in the later study, a central adaptive optimizer. Count learning, checking, communication and recovery costs, and require correct, fresh, on-time answers. Change the workload and interrupt a provider to test whether useful redundancy and capability can return. This design tests a bounded software mechanism; it does not yet establish novelty, biological evolution or a benefit on real production workloads.

## Question and prediction

**When is it worth letting a swarm discover and maintain its own division of labor?** The interesting outcome is a quality-preserving lifecycle: initially redundant generalists become shared providers and cheaper consumers, then recover flexibility when the old arrangement stops working.

The working prediction is that repeated overlapping jobs can repay differentiation costs, but low-overlap or rapidly changing work may favor generalists or simple caching. That is a pre-data expectation, not an accepted hypothesis. A result favoring the simpler architecture is useful and must remain publishable.

Agent removal and cheaper-model substitution already have close prior art in [[chen-2026-agentslimming]]. Online topology adaptation is also represented by [[huang-2026-manta]]. The remaining candidate contribution is **reversible, agent-proposed specialization of data services and capabilities over a persistent workload**, evaluated against strong engineering baselines with honest lifetime accounting. [Prior-art boundary](PRIOR-ART.md) records what remains unverified.

## Setup

The first workload is a fictional operations desk. Agents answer recurring stock, supplier and delivery questions using versioned local fixture APIs. Jobs differ in their required records, transformations and freshness deadlines. Outputs are structured decisions plus source receipts; a separate deterministic evaluator checks them against protected truth. The fixtures are an instrument, not real business data or paid external API traffic.

S1 starts with six persistent agent identities, eight epochs and six jobs per epoch. Four independent workload roots are paired across four arms. Each agent begins with identical resources in the adaptive arm; job assignments and observed history can subsequently differ. The larger prospective study uses twelve agents, longer horizons and additional controls, after S1 informs feasibility and precision.

The pinned candidate ladder is Haiku 4.5 through Anthropic, Qwen3 8B through Alibaba, and Jev 1.13 through TypeSafe, using provider-specific OpenRouter routes. [Models and tariffs](models.json) record exact requested IDs and catalog backend revisions; these are not yet qualified execution receipts. Jev is eligible only for a separately qualified finite-choice subtask. It is not assumed capable of arbitrary tool use or free-form reasoning.

## Protocol

| Arm | What it can change | Purpose |
| --- | --- | --- |
| A0 Generalists | Nothing structural; full tools and ordinary private memory | Measures the starting architecture |
| A1 Shared cache | A conventional coherent cache with request coalescing; full generalist agents | Tests how much ordinary deduplication explains |
| A2 Static specialists | Roles, services, skill subsets and model routing chosen on development data and then frozen | Strong engineered comparison |
| A3 Poietic | Agents propose costed capability, provider, model and connection changes within a fixed action grammar | Main adaptive treatment |
| A4 Central adaptive | One costed optimizer has the same information and change grammar | Later control for the value of decentralized proposals |
| A5 Learned and frozen | Copy A3 immediately before the change, then disable structural changes | Later paired recovery comparison; shares A3's parent history |
| A6 Single solver | One capable solver with cache, tools and the same total resource ceiling | Later control for whether a swarm helps at all |

In S1, epochs 1–2 acquire experience, 3–4 measure stable operation, and 5–8 face a prescheduled change. Two roots change overlap from high to low; two introduce a documented API schema revision. Provider withdrawal is a later separate stress test, not mixed into those episodes. Every arm sees the same legal API access, workload stream and observable notices for its paired root.

No actor is told to become a server or rewarded for looking heterogeneous. Each gets the same operational objective. A deterministic controller validates proposed changes and enforces budgets; it does not nominate specialist roles. Changes take effect at epoch boundaries. All unsuccessful proposals and their costs remain in the record.

S0-01 made 36 actual generalist calls, then stopped after repeated relay errors. All 144 assigned outcomes are reconciled, including 108 unstarted; USD 0.479232 remains conservatively reserved because the original relay lost usable response/billing details. This is an instrument failure, not evidence of model incompetence. See [post-mortem](reviews/S0-01-post.md).

S0-02 executed once at frozen f362 source after81 runtime checks and complete admission. Its first Haiku response was HTTP 200 but contained fenced, nested JSON; the strict parser stopped after1 call, leaving143 unstarted and 144 terminal. No role qualifies. All12hub artifacts verified. New API costUSD 0.00077; cumulative conservative exposureUSD 0.562186183 including allocation lifetime, under the originalUSD 2cap. Worker, relay and allocation are released. See the [post-mortem](reviews/S0-02-post.md), [trace review](results/S0-02/trace-review.json) and [scientific assessment](reviews/S0-02-scientific.json).

D0-01 executed the owner-approved36-decision screen at frozen38544138 after106runtime checks. It stopped after3calls:Haiku returned the correct flat fetch inside a rejected Markdown fence;Qwen executed a correct fetch then receivedHTTP429;Jev was unstarted. All36outcomes are terminal,33unstarted,9aggregate artifacts verified. No role passes the diagnostic or qualifies. Cumulative conservative exposureUSD0.568560890 ofUSD2; worker/relay and allocation released. See [post-mortem](reviews/D0-01-post.md), [scientific review](reviews/D0-01-scientific.json) and [aggregate evidence](results/D0-01/summary.json). Raw traces remain private. Next work is offline interface/transport diagnosis; no successor is authorized or running andS1/S2 remain closed.

The subsequent [offline repair and cost review](readiness/format-repair/REPORT.md) implements a bounded JSON-fence adapter and safe provider-error metadata; 121 tests pass. The retained Haiku action executes in retrospective replay. No new native call or model substitution has occurred; this source needs fresh qualification.

Read the [full protocol](PROTOCOL.md), [machine-readable design](design.yaml), [agent and context contracts](contracts.json), [visualization mapping](VISUALIZATION.md), [first qualification assessment](reviews/S0-01-pre.md), and [execution handoff](RUNBOOK.md).

## Metrics

The primary efficiency quantity is total deployment cost per assigned job over the whole lifetime, **conditional on meeting prespecified quality, freshness and deadline guardrails**. It is not cheaper execution of only the easiest successful jobs. Report cost per verified success as a secondary quantity, including all failures in its cost numerator.

Record actual model charges, tokens, CPU/GPU time, API fetches, communication bytes, migrations, compilation, probes and repairs. Synthetic API tolls are a separate sensitivity analysis; they never masquerade as a real provider bill. Track the break-even horizon, duplicate requests, loaded skills, model assignments, provider concentration and loss after a change. Analyze independent workload roots, not messages or agents as independent samples.

For a later confirmatory claim, the proposed practical threshold is at least 20% lower lifetime cost than the development-selected strongest baseline, with no more than a two-percentage-point reduction in verified success and at least 95% verified success overall. These are design choices for review, not measured effects or proof of adequate power. S1 cannot establish those claims.

## Current status

The owner selected the project and its name. [Dmarz’s independent review](../../../dmarz/notes/inbox-reviews-2026-10-04-round2/poietic-review.md) is resolved in the [prospective amendment](AMENDMENTS.md): fixed arrivals include adaptation delay; ordinary caches may reuse derived computation; recovery/advance criteria and quotas are explicit. The offline instrument and gated S0 launcher are implemented; [validation](VALIDATION.json) records software checks, not model competence. [Setup status](SETUP.md) and [launch instructions](RUNBOOK.md) name the remaining gates. [Launch state](launch-state.json) distinguishes design publication, independent review, model qualification, spending authorization, dedicated allocation and S2 research acceptance. Public registration of the design creates no queued run. Any successor requires its own approved scope and current execution gates. Researcher sign-off is waived by owner direction; incomplete prior-art work and qualification remain scientific limitations, not extra reviewer gates.

The central decision after development is whether Poietic Agents adds enough beyond caching and static specialization to justify a larger study. If it does not, stop and recommend the simpler system.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.

## Current diagnostic execution

The owner has now directed the prepared D0-01 diagnostic. [Prospective plan](D0-01-PLAN.md) and [pre-run assessment](reviews/D0-01-pre.md) define the unchanged36-decision scope. Public artifacts are aggregates/frames/hashes; full traces stay private.106offline checks pass. One run follows current exclusive allocation, original-ledger and public-plan admission. Approval covers no automatic successor.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
