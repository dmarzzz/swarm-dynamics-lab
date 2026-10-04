# Runbook: from a new question to an auditable experiment

## Researcher review is optional for Vishesh-owned experiments

Owner directive, 2026-10-04 UTC: skip the researcher-review step for Vishesh-owned experiments, including Phantom Coast. No independent researcher, design, dossier or researcher sign-off is required to prepare, qualify or launch these experiments. This supersedes the earlier single-review requirement and conflicting researcher-approval launch gates in study plans and runbooks. The owning agent completes the pre-run assessment, resolves known substantive defects and records limitations; optional feedback must not become a blocking approval step.

Keep prospective plans and public registration, offline checks, bounded native qualification, honest analysis, original spending limits, secure credentials, current exclusive approved-account allocation, and source/runtime verification. Continue prior-art work and record research scope honestly, but do not reintroduce the skipped reviewer as a research-scope sign-off. A waived review is recorded as not required by owner direction, never as passed, independent validation or formal hypothesis acceptance. Preserve historical reviews and immutable plans. Other researchers' policies are unchanged. Update legacy launcher review gates before use rather than supplying a fabricated approval receipt.


Shared experiment setup workflow for Swarm Lab, established 2026-10-04 UTC from the existing Swarm Lab workflows. Start here for a new topic, thesis, experiment version or follow-up. Use the [methods guide](GUIDE.md) for statistical detail and the [agent lifecycle contract](AGENT-LIFECYCLE.md) for initialization and memory. This document consolidates the process; it does not retrofit enforcement into existing launchers or authorize spending.

## Start a setup record

Copy [the setup record](templates/experiment-setup.md) into the study's owned directory as `SETUP.md`. Assign a study owner, stable study ID, version and intended decision. Record evidence links and a named next action at every gate. A blank, unknown, stale or failed required check blocks the corresponding transition; a checked box alone is not evidence.

For formal work in the shared repository, follow its [agent protocol](../../AGENTS.md), ownership rules and task tools. Formal experiments belong under `experiments/<id>/`; exploratory hunches stay in the owner's notes with their status explicit. Exploratory status does not waive public registration, review, qualification, budget or resource rules. It also does not confer an exemption from formal survey/hypothesis gates. Local documentation and offline unit fixtures can be prepared without provisioning a host or launching an experiment.

Recommended study layout (references to existing files are preferable to duplicate copies):

```text
SETUP.md                    gate evidence and next action
PLAN.md                     readable prospective design
spec/                       agent, context, run and scenario definitions
src/ and tests/             instrument, evaluator and offline checks
reviews/<attempt>-pre.md    assessment before each attempt
reviews/<attempt>-post.md   reconciliation and repair decisions
results/<attempt>/          assignments, receipts, raw events, outcomes, usage
RESULTS.md                  interpretation with limits and evidence links
```

## Gates and responsible roles

The study owner prepares the evidence and remains responsible for admission. A reviewer assesses design and stage readiness; a separate scoring implementation is useful but is not an independent researcher review. The operator verifies runtime and resources. One person can hold multiple operational roles, but cannot claim independence or satisfy the shared repository's different-researcher review requirement by self-review. Budget and infrastructure authority remain with the authorized owner/provisioner.

| Gate | Required evidence | May proceed to |
|---|---|---|
| G0 — question and prior art | Question, decision value, closest work, status of applicable survey/hypothesis review | Design, within research-gate rules |
| G1 — prospective design | Written plan, scenario contracts, contrasts, metrics, analysis and stage limits | Experimental implementation |
| G2 — instrument readiness | Frozen definitions, offline checks, evaluator controls, trace/replay checks | Bounded qualification preparation |
| G3 — stage admission | Committed pre-run assessment, immutable public plan registration, verified page, current resource/budget/source checks | Only the named registered stage |
| G4 — qualification | S0 outcomes reconciled, controls pass predeclared thresholds, qualified hashes match intended study | S1 preparation; repeat G3 for S1 |
| G5 — review and closeout | All assignments accounted for, analysis/visual audit, post-mortem, durable artifacts and resource release | Finish, or a separately assessed next attempt |

S0 means a bounded competence/qualification screen; S1 means the exploratory comparison; S2 denotes a separately authorized confirmatory or replication stage if planned. Names do not determine evidential strength. Never advance automatically because a process exited successfully.

## 1. Turn the topic into a testable decision

Write one question and one primary contrast: “For [population/tasks], does [intervention] improve [endpoint] over [comparator], under [resource constraint]?” State what a favorable, null or adverse result would change. Separate a useful replication from a novelty claim.

Read the nearest prior work and preceding local post-mortems before designing. Record search scope, what was actually read, competing explanations and unresolved gaps. The shared repository's survey, hypothesis and different-researcher review gates still govern formal work; run its current gate/check tools rather than assuming a local bibliography satisfies them. Do not label an unreviewed hunch an accepted hypothesis.

## 2. Write the plan before implementation

Use [the protocol template](templates/protocol.md). For the public plan, include exactly the readable sections `## TLDR`, `## Question and prediction`, `## Setup`, `## Protocol` and `## Metrics`; detailed appendices may follow. The TLDR explains question, treatment, comparator, success measurement and limitations. Do not invent a directional prediction after seeing outcomes.

Create a scenario contract for each candidate: practical task, hidden world state, actor-visible information, actions, truth/scoring rule, intervention timing, useful baseline, positive and negative controls, and what would make the task uninformative. Select scenarios for different mechanisms and failure modes, not merely different stories. Explain finite feature reuse: new IDs do not imply new reasoning problems.

Freeze these decisions:

- Primary endpoint, denominator, time window, practical effect threshold and claim boundaries. Keep secondary/exploratory endpoints separate.
- Treatment overlays and strongest relevant comparators: clean competence ceiling, no intervention, single controller or budget-matched alternative where needed. If a baseline is omitted, narrow the claim explicitly.
- Independent unit, pairing/blocking, scenario weights and randomization. Agents, calls, cases and frames inside the same world are generally dependent; count independent worlds separately.
- Agent counts, worlds per scenario/arm and maximum attempts. Use pilot variance and power/precision reasoning for inference; if resources support only a tiny pilot, declare feasibility evidence and weak precision. Do not copy Theseus's sample counts as a universal standard.
- Disjoint development, qualification, repair and scientific seeds/tasks; sealed holdout; fixed stopping and failure/missing-data handling. Declare any sequential rules and multiple-comparison policy in advance.
- Calls, tokens, dollars, wall time, concurrency and bounded repair allowance across all stages, including failed attempts and provider probes. No automatic expansion into S2.

## 3. Specify and build a reproducible instrument

Complete the [agent definition](templates/agent-definition.json), [context/access manifest](templates/context-access.json) and [run configuration](templates/run-config.json). Pin model/provider revision, prompts, tools, response schema, agent identities/roles, memory limits, communication, scheduler, evaluator and runtime dependencies. Record source/config/input hashes and exact commands.

Implement a single scripted startup path: verify definitions and snapshots; allocate a fresh run namespace; initialize the seeded world and role state; assemble ordered context; apply only the declared treatment overlay; record effective input/context hashes; then admit dispatch. Compare actual delivered inputs, not just configuration labels. Pair baseline information across corresponding conditions, while preserving intentional private observations and roles within a world.

Specify reset, resume, replacement and checkpoint-fork semantics. Theseus v2's useful pattern is to fork one exact acquisition checkpoint into conditions, retain archive ancestry, and explicitly control feedback timing. Do not reintroduce founder context into descendants by accident. Seeds control supported randomness; hosted model output is not guaranteed deterministic, even at temperature zero.

Keep evaluator truth, future cases and protected labels out of actor inputs. Record access eligibility, retrieved content and actual visible context separately. Define parse failures, abstentions, timeouts, retries and terminal status before execution. Never silently replace a native-model response with an oracle or scripted policy.

## 4. Pass offline checks before paying for qualification

Use known-answer fixtures and deliberately wrong policies to verify that the task and evaluator discriminate the intended behavior. Check treatment masks, paired inputs, timing boundaries, lineage/reset, case-ID alignment, duplicates, missing votes, assigned denominators and budget/stop behavior. Recompute scores from saved raw decisions through an independent reference calculation where practical; identify same-author audits honestly.

Fault-check the launch path: missing/stale plan, mismatched source/model/config, expired/conflicting claim, missing budget authority and duplicate attempt must prevent dispatch. Inspect the actual launcher: an available helper does not prove every entry point invokes it. Do not use a separate CLI smoke path to bypass gates.

Define the [visualization mapping](RUN-VISUALIZATION.md) before collecting data. Bind fields, units, denominators, event markers, time origin and missing states to run/arm/seed IDs. Validate initial, transition, failure and final fixture views. Retain history for replay; the latest uploaded frame is insufficient. Fixtures must say **SCRIPTED — NOT MODEL EVIDENCE**. Rendering should not consume experimental RNG or change agent behavior.

Offline unit fixtures are software checks. Scripted experimental sweeps and model/provider probes are runs and need the applicable admission gates; calling them “tests” does not exempt them.

## 5. Admit each attempt with current evidence

Read the previous post-mortem, then fill the existing [pre-run assessment](templates/pre-run.md). Use `ready`, `diagnostic-only` or `blocked`; name unresolved issues and acceptance checks. Commit the plan, amendments and assessment before execution. Do not hold an idle fleet claim while waiting for missing authority.

Before queueing, loading a model or dispatching any condition:

1. Publish the readable plan at an immutable revision and register its exact URL and experiment TLDR. Bind each run's condition-specific TLDR to stage, treatment, comparator, endpoint and limitation. Preserve the original link per run when the experiment's latest registration changes.
2. Run `public_plan.py` or an equivalent fail-closed check. Require the expected URL/revision/content hash and current assessment, not merely any valid historical plan. Verify the actual public page displays the intended design. A network failure blocks launch. Save the receipt before `run_start`; a local hash alone is not preregistration.
3. Reserve authorized calls/spend through the existing shared transactional authority or non-overlapping allocations. Verify remaining quota and the shared deadline immediately before launch. Copying a ledger onto another host cannot create new budget; another study's funds are not this study's authority.
4. For vishesh-owned studies, follow the [machine workflow](../../researchers/vishesh/notes/experiment-machine-workflow.md): refresh private inventory, check actual workload, obtain a fresh exclusive allocation for this experiment, verify the merged claim and expiry, and deploy frozen source. A container on another study's busy host is not a dedicated allocation. Stages of this same experiment may retain their allocation.
5. For new machines under that owner directive, use **Dmarz's established DigitalOcean account/team and provisioner**. Before create/apply, match the credential's account/team against the explicit approved identity, and verify infrastructure state/project plus exact resource plan. Fail closed if unavailable. Never fall back to a personal/default account or infer permission from a token, fleet label or hostname. Store private verification evidence; publish only verification status.
6. Verify deployed source, dependencies, credential availability by safe status, output destination, exclusive claim and quota. Write a current deployment receipt and assigned manifest. Pin the actual qualified instrument hashes for S1; relevant drift requires requalification.

For shared Anthropic access, follow the owner-authorized [Swarm Lab credential-transfer policy](SWARM-LAB-CREDENTIALS.md): select only Keychain service `swarm-lab-anthropic`, account `vishesh`, and transfer only its API key to the currently admitted Swarm Lab host over verified SSH stdin. This is standing transfer authorization within that scope, not permission to use general Anthropic credentials or increase the budget. Record the policy/alias and destination validation in the deployment receipt.

Credential values never enter chat, command arguments, logs, screenshots or artifacts. Authorized local processes consume them securely. Keep account IDs and private inventory in private configuration. Other researchers follow their applicable allocation directives; this runbook does not change their resource authority. Do not reuse the wrong-account Immune Response provisioning helper or relaunch that deployment without the required verification; preserve its incident and spend record.

Swarm Live UI changes may be pushed to its shared repository, but DMars/CD owns deployment. Do not use the user's Cloudflare account or start its authorization flow. Verify current supported artifact capabilities before promising embedded replay; use a supported fallback if necessary.

## 6. Qualify, review, then compare

Run S0 only under its own completed G3 admission. Measure clean competence per scenario/checkpoint, schema validity, manipulation fidelity and evaluator correctness against thresholds declared before responses. A failed clean ceiling blocks interpreting the treatment comparison. Transport/schema problems and inability to do the task are distinct diagnoses.

Preserve every qualification attempt. Diagnose on development fixtures; repair with a dated amendment, a new attempt ID/output directory and fresh reserved qualification tasks. Keep thresholds fixed unless explicitly redesigning and qualifying a new instrument; never lower them to relabel a failed attempt. Continue justified repairs within authorized bounds. If budget/access is exhausted, record the blocker and exact resume condition.

After S0 passes, reconcile its outcomes and issue an S1 pre-run assessment. Verify that scientific source/provider/model/config hashes match the qualified instrument and scientific seeds remain untouched. Repeat all current admission checks. Passing S0 establishes readiness for the declared comparison, not its scientific result.

## 7. Execute and reconcile the entire assignment set

Write durable assignment and call-start records before dispatch. Preserve raw sanitized decisions, context/provenance, events, terminal outcomes, usage, intervention history and receipt links. Observe actual caps, claim lifetime and systemic-failure stops. Each assigned unit ends in a recorded status, including not-started, interrupted, invalid or missing; no invisible replacement runs.

After every attempt, reconcile **assigned → started → terminal → graded → analyzed**, explain differences, audit scored records and plots, and compare cost estimates with actual usage. Analyze at the declared independent unit with pairing/clustering and stated weights. Report effect sizes, uncertainty, scenario differences and missingness sensitivity. Conservative failure-as-incorrect scoring does not mean that an unobserved paired effect is known to be zero.

Keep separate statuses for execution, response validity, qualification, scientific interpretation, process compliance and artifact/reporting delivery. A green dashboard is not scientific qualification; an unavailable replay is not a scientific null.

## 8. Close the cycle or open a justified repair

Complete [the post-mortem](templates/post-mortem.md), including controls, limitations, visual checks and a failure ledger. Classify each issue before taking action:

| Finding | Next action |
|---|---|
| Execution/reporting defect | Preserve evidence, repair, regression-check, then a bounded new attempt if needed |
| Design/scoring defect | Amend the design, audit affected conclusions, validate and requalify |
| Capability failure | Diagnose, repair or change an authorized model/config, then fresh qualification |
| Valid null, adverse result or ceiling | Report it; do not rerun to obtain a preferred effect |
| Missing authority/access | Record exact blocker, preserve state, continue independent work |

An issue closes only with passing acceptance evidence, not a proposed fix. Freeze the release inventory, verify durable artifacts including failures and resource usage, then stop only this experiment's workers and release its claim after transport completes. Authorized fleet owners handle teardown. Record the next decision as `advance`, `repair-and-rerun`, `diagnostic`, `blocked` or `complete-valid-result`.

A follow-up that changes hypothesis, mechanism, source/model or scenario scope needs a versioned prospective plan and appropriate requalification. Never rewrite old plans/outcomes. Missing historical registration stays a process failure; later documentation is explicitly retrospective.

## Where these practices came from

This is an audit of local records, not a new literature survey or certification of every launcher. “Swarm of DCS” is interpreted here as Swarm of Theseus, the matching recorded study; no separately named DCS study was identified in the inspected records.

| Local evidence | Practice retained |
|---|---|
| [Theseus v1 design and amendments](../../researchers/vishesh/notes/swarm-of-theseus/README.md) | Scenario contracts, paired worlds, clean ceiling, fixed thresholds, disjoint repairs, retained failed screens |
| [Theseus S1 pre-assessment](../../researchers/vishesh/notes/swarm-of-theseus/reviews/S1-a1-pre.md) and [post-mortem](../../researchers/vishesh/notes/swarm-of-theseus/reviews/S1-a1-post.md) | Exact qualified hashes, six worlds distinguished from 36 trajectories, reconciliation, condition TLDRs and bounded claims |
| [Theseus v2 plan](../../researchers/vishesh/notes/swarm-of-theseus/v2/PLAN.md) and [blocked pre-assessment](../../researchers/vishesh/notes/swarm-of-theseus/v2/reviews/S0-pre.md) | Scenario redesign, acquisition checkpoint forks, two replacement waves, controlled feedback, real resource blockers |
| [Regrowth registration failure](../../researchers/vishesh/notes/regrowth-200/REGISTRATION-FAILURE.md) | Public-plan verification before launch; retrospective repair never becomes preregistration |
| [Shared review cycle](RUN-REVIEW.md) | Pre/post review for each attempt, repair classification, evidence-based closure |
| [Workspace rules](../../AGENTS.md) and [machine workflow](../../researchers/vishesh/notes/experiment-machine-workflow.md) | Account identity checks, exclusive allocation, preserved shared budgets and deployment ownership |

Theseus v1's local public-plan helper checks immutable URL shape and sections but alone does not bind the expected current plan revision or guarantee visual verification. New launchers must supply those additional checks. Existing documentation or a copied template is not proof that the production gate is wired. The setup record tracks that evidence explicitly.
