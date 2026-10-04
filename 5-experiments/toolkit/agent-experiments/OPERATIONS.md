# Inspect and operate an experiment

## Default experiment spending authorization

Owner update, 2026-10-04 UTC: Vishesh-owned experiments have a **USD10 cumulative default**, or **USD50 cumulative for a promising experiment**. This replaces the former generic USD2 default. These are per-experiment ceilings, not an aggregate portfolio pool or per-run allowances. Do not request another budget approval for the applicable authorized tier.

Operational interpretation of “promising”: the owning session records a short evidence-linked assessment in the existing setup/next-run record explaining the useful unresolved question, what prior results/traces or offline validation support, and the credible next test whose outcome changes a decision. A valid negative result can support this assessment; positive effects, an arbitrary confidence score, visual appeal and sunk effort are not prerequisites or sufficient evidence. Record the assessor/date, evidence, selected tier and bounded next-stage envelope. This is the owning assessment, not a new independent-review or per-tier owner-sign-off gate. If the case for promising is not established, use the default or existing explicit study cap.

An explicit experiment-specific budget remains the baseline instead of being silently reduced or replaced by the default. The documented promising assessment can use this new standing authorization to raise a lower study ceiling to USD50; an already higher explicit authorization is preserved. Later explicit owner restrictions take precedence. Existing smaller **attempt/stage limits remain in force** until a prospective, appropriately authorized amendment; changing the study ceiling does not enlarge a running or frozen packet.

Both tiers cover all stages, qualification, attempts, retries, coordinator/model/tool charges and incremental infrastructure costs in the same study lineage. Carry actual spend and unresolved reservations forward. USD50 means USD50 total, not USD50 added to USD10. Before dispatch, append the selected authorization to the original ledger, reconcile exposure and reserve the exact next-stage maximum; never reset spend, discard unknown charges or create funds by renaming a continuation, opening a new chat, changing machines or starting a new ledger. Any increase beyond the applicable ceiling needs owner authorization.

This policy supplies budget authority only. It does not start experiments, authorize other researchers’ spending, expand scientific scope, or replace public-plan registration, qualification, source/runtime, credential and approved-account/exclusive-allocation checks. Necessary diagnostics retain their standing scoped authority; broader successors still need the applicable scope decision. Generic shared templates remain disabled until their study-specific budget, assessment where needed, ledger and admission evidence are filled. Existing launcher ceilings are not automatically raised by editing this guidance: reconcile and version the budget contract before the next admitted attempt, preserving historical receipts.


## Researcher review is optional for Vishesh-owned experiments

Owner directive, 2026-10-04 UTC: skip the researcher-review step for Vishesh-owned experiments, including Phantom Coast. No independent researcher, design, dossier or researcher sign-off is required to prepare, qualify or launch these experiments. This supersedes the earlier single-review requirement and conflicting researcher-approval launch gates in study plans and runbooks. The owning agent completes the pre-run assessment, resolves known substantive defects and records limitations; optional feedback must not become a blocking approval step.

Keep prospective plans and public registration, offline checks, bounded native qualification, honest analysis, original spending limits, secure credentials, current exclusive approved-account allocation, and source/runtime verification. Continue prior-art work and record research scope honestly, but do not reintroduce the skipped reviewer as a research-scope sign-off. A waived review is recorded as not required by owner direction, never as passed, independent validation or formal hypothesis acceptance. Preserve historical reviews and immutable plans. Other researchers' policies are unchanged. Update legacy launcher review gates before use rather than supplying a fabricated approval receipt.


Use [the experiment command](../../scripts/experiment.py) to find a study, prepare a bounded iteration and inspect what is still missing. The [registry](operations.json) covers the ten named research areas. Only Swarm of Theseus v2 has a native adapter in this first version. It preserves the native stage-closure guards: a completed historical stage cannot simply be relaunched. An entry, prepared packet or passing offline check is **not current launch admission**.

The [setup runbook](EXPERIMENT-SETUP.md) remains the scientific workflow. Maintain its existing [setup record](templates/experiment-setup.md) in the study directory; link plans, reviews and receipts there instead of copying their contents into another checklist. Local access aliases and private infrastructure records stay outside the public repository.

For an end-to-end iteration, follow [the iteration process](ITERATION.md): review traces and results, fix errors and design gaps, validate and push changes, select the next action, execute an authorized ready scope, then close out. The commands below support that workflow; `iterate` alone only writes a configuration delta.

## Start with inspection

Run from the repository root. These commands do not make provider calls, contact the fleet, claim resources or launch experiments:

```sh
python3 scripts/experiment.py list
python3 scripts/experiment.py inspect swarm-of-theseus-v2
python3 scripts/experiment.py validate --registry-only
python3 scripts/experiment.py validate swarm-of-theseus-v2
```

`list` and `inspect` report inventory, references and adapter coverage. `validate` checks the registry or the selected adapter's offline contract; it does not certify live model routing, funds, public registration or machine access. A null adapter means that the study still uses its own documented workflow. It does not mean that its native launcher is absent or defective.

Each registry entry retains a stable study ID, title, owner, study path, setup and preceding post-mortem paths, adapter, checked revision/time and next action. A null evidence path is a visible documentation gap. The checked revision is inventory provenance, not a claim that budget, review, qualification or allocation remains current. Before continuing, read the linked post-mortem and check for later attempts in the owning study.

## Commands and their boundaries

| Command | What it does | Boundary |
|---|---|---|
| `new ID --owner RESEARCHER --title TITLE` | Creates a design scaffold under an existing researcher's notes | No experimental implementation, registry entry, registration, calls or admission |
| `iterate STUDY --base BASE.json --changes PATCH.json --output CONFIG.json` | Writes a resolved configuration and lineage sidecar with hashes and field differences | Preserves the base; a configuration change is not authorization |
| `prepare STUDY --stage STAGE --attempt ATTEMPT --config CONFIG.json [--qualification SAVED_RESULT_DIRECTORY] [--next-plan NEXT.json] --output PACKET.json` | Freezes the adapter's intended inputs, assignments and cost envelope | Offline preparation only; unsupported study/stage or missing evidence remains blocked |
| `run STUDY --packet PACKET.json --receipt RECEIPT.json [--update-approval APPROVAL.json] --output RUN_DIRECTORY` | Checks a frozen packet and admission receipt before calling the supported adapter | This is the only dispatch operation; existing study gates and authority remain binding |
| `finalize STUDY --attempt ATTEMPT [--results SAVED_DIRECTORY] [--outcome completed\|failed\|blocked\|ambiguous] [--worker-stopped]` | Writes/reconstructs an immutable operational post-mortem and handoff from saved evidence | No model calls; stopped-worker flag is an operator attestation, never a stop command |
| `check-update STUDY --packet PACKET.json --update-approval APPROVAL.json` | Checks that the owner-decision record matches the reviewed next-run proposal and execution contract | Offline record validation; no approval issuance, allocation or native admission |
| `resume STUDY` | Reports the initial adapter's missing recovery support | Does not replay calls or restart a worker |
| `report STUDY --results SAVED_RESULT_DIRECTORY --output REPORT_DIRECTORY` | Uses the adapter's saved-evidence reporting path | No new model calls; output is not a fresh sample or independent replication |

The Theseus adapter supports the native S0, S0-repair and S1 contracts; S1 additionally requires saved qualification evidence. It retains the native plan/review/source/price checks and existing budget ledger. Approved-account evidence in the private admission receipt is an operator attestation, not an independent fleet audit. Vishesh’s researcher-review waiver applies; historical review fields are optional and must remain truthful. The owner’s approval of a successor update is a separate record. Reporting recomputes from saved evidence in scratch space and exports a summary plus context hashes; it does not publish raw prompts or private receipts.

The exact configuration and receipt allowlists are in [the adapter](../../scripts/experiment_ops/theseus.py). The receipt binds the existing ledger and prior reservation floors as well as allocation and review references; it is not generated by `prepare`. Native execution also depends on the deployed Python runtime and authorized `swarm_report` reporting installation. Offline validation reports its own scope and does not provision or install those dependencies.

Paths are repository-relative, contained and nonsymlink. Generated configuration, iteration sidecars, packets, run outputs and reports belong under ignored `data/experiment-operations/`. The command accepts no arbitrary shell command, force option or reset of attempt identity. Use `--help` for the exact arguments; study-specific configuration and receipt requirements belong to the adapter, not to guessed example values.

Attempt claims are kept in `data/experiment-operations/attempts.sqlite`. They prevent duplicate dispatch through this checkout. This is not a distributed lock: two clones must not act as competing authorities. Existing study workers can still have separate entry points; inspect their gates rather than assuming that this wrapper controls all possible launches. Failed or interrupted attempts retain their claim and artifacts. Reconcile them before a separately identified, justified attempt.

## Reuse evidence according to what changed

Keep the full source commit for provenance. Separately identify the qualified instrument by its effective runner, model/configuration, prompt renderer, delivered context policy, tools, memory policy, scenarios, evaluator and dependency hashes. The table is an operator decision rule; it does not grant automatic qualification reuse to every existing launcher.

The first adapter retains Theseus v2's native guards: each prepared packet/configuration and deployment receipt must match the current frozen source, while S1 qualification matches the native instrument hash over `src/*.py` and `PLAN.md`. An unrelated repository edit therefore needs refreshed source/admission evidence but does not inherently require new paid qualification when that instrument hash and the qualification scope are unchanged. The broader dependency policy below is guidance; it does not relax the native checks or certify dependency coverage in every launcher.

| Change | Evidence to renew |
|---|---|
| Prose, navigation or formatting only, with no effective instrument change | Relevant documentation checks; preserve the earlier qualification's exact scope and fingerprint |
| Saved-data analysis or figure repair | Recompute from immutable evidence and validate arithmetic/rendering; retain prior reports and describe the correction |
| Prompt, model, response limits, tools, context order, truncation, memory, scheduler or task semantics | Prospective amendment, affected offline checks and fresh bounded qualification |
| Scoring or denominator change | Audit affected historical conclusions, independent reference calculation where practical, amended analysis; requalify where the qualification endpoint changes |
| New scenario population, treatment, resource regime or hypothesis | Material design revision with applicable research review and fresh qualification |
| Host change or interrupted transfer | Deployment verification, exclusive allocation, single budget authority and pending-call reconciliation; no ledger reset |
| Any new attempt or stage | Current public plan and condition TLDR, pre-assessment, source/dependency match, quota, claim lifetime and applicable account checks |

A completed researcher review can be reused within its stated design scope. For Vishesh's studies, researcher review is optional by owner direction; no design or dossier sign-off blocks launch. A design review is not an independent code or arithmetic audit. Qualification can be reused only when its actual scope and relevant hashes match. A failed competence gate cannot be replaced by a favorable diagnostic.

## Initialize the agent that was specified

Use the existing [agent definition](templates/agent-definition.json), [context/access manifest](templates/context-access.json) and [run configuration](templates/run-config.json). The [lifecycle contract](AGENT-LIFECYCLE.md) specifies the full receipt. Before dispatch, record what was actually loaded: definition and instance IDs, role, parent/checkpoint, model settings, tool schemas, fresh memory namespace or inherited snapshot, ordered delivered-context hash and size, truncation, named random streams and treatment overlay.

Pair corresponding baseline observations across conditions; agents within a world may intentionally have different roles and private evidence. Keep scorer truth and held-out inputs outside actor access. Default to fresh per-episode mutable state, frozen retrieval inputs, explicit context limits and disabled provider fallback unless the protocol defines otherwise. A seeded startup controls initialization; it cannot promise identical hosted-model answers.

Record memory writes, retrieval results and delivered peer messages as the run progresses. Preserve episode, attempt, instance and checkpoint ancestry separately. A retry, checkpoint fork or repeated score does not become another independent world.

## Control cost and recover without hidden repeats

Reserve worst-case call cost before dispatch against the existing cumulative authority. Retain calls, tokens, actual usage, uncertain exposure, provider request IDs when available and failed attempts. Study adapters remain responsible for their existing budget ledgers; the operations attempt database is not a spending ledger. Moving a ledger or host never creates new funds. Reconcile estimated versus actual cost at closeout.

Do not automatically retry an ambiguous send: it may already have executed or incurred cost. Preserve its reservation and request identity, then reconcile. Retry only declared transport classes within the protocol's cap; invalid or adverse answers remain outcomes. A reporting upload can be retried from saved artifacts without rerunning the model. A process restart is safe only when the adapter can resolve pending effects and preserve assignment and budget identity; this first adapter exposes no general resume command.

Use offline fixtures before bounded native qualification, and saved traces for evaluator or visualization repairs. Immutable provider prompt caches may reduce cost; writable shared memory and answer caches change the experiment unless explicitly controlled. Report cached work and fresh calls separately. Never treat replay as new sampling.

## Automatic closeout and the next session

The shared `run` path invokes saved-data closeout after a terminal return, admission block or caught interruption. It preserves the native outcome and writes an immutable `POST-MORTEM.md`, `handoff.json` and completion marker under ignored `data/experiment-operations/closeouts/`. A report-write failure is separate from the native result and makes the command unsuccessful; retry `finalize`, never recollect model outputs just to repair the report. Repeating finalization over unchanged evidence is idempotent. Changed evidence yields a new preserved snapshot.

The generated post-mortem inventories evidence, recomputes available saved Theseus analysis and identifies unresolved [run-quality dimensions](RUN-QUALITY.md). It does **not** invent scientific interpretation or claim that a template is a completed review. The owning session must finish the [scientific post-mortem](templates/post-mortem.md) before marking the attempt reviewed. It may conclude that a valid negative result finishes the study.

`inspect` exposes the latest recorded completion and handoff by journal chronology. Also check the native study history: a missing local journal does not mean no earlier experiment exists. For the existing Theseus study, first wrapper use requires importing/finalizing its most recent native attempt and assessing it. Native launchers for the other study families are still manual; call `finalize` in their operator's terminal/failure closeout. The shared interface does not retrofit their running workers or schedule a new session automatically. Heterogeneous Swarms has no admitted native adapter.

A killed process cannot run its finalizer. Preserve the journal, verify that the old worker has stopped and no descendant worker can continue, reconcile pending calls, then recover with `finalize --worker-stopped`. The flag records an operator assertion; it neither kills nor independently verifies a worker. A live `dispatching` attempt otherwise blocks recovery and successor planning.

### Prepare the update for owner review

1. Read the latest handoff, raw evidence and previous post-mortem. Test the suggested causes and improvements against [RUN-QUALITY.md](RUN-QUALITY.md); distinguish gaps, unknowns and valid findings.
2. Complete [scientific-post-mortem.json](templates/scientific-post-mortem.json) alongside the readable review. Pin the parent handoff and supporting evidence. Each quality dimension needs a reason; a `pass` needs evidence, and a `gap`/`unknown` needs a repair and acceptance check.
3. Draft [the next-run plan](templates/next-run-plan.md) before experimental implementation, then do the approved offline preparation and checks. Resolve [next-run-plan.json](templates/next-run-plan.json): independent sample count/rationale, allocation and analysis; scenario construction/controls/holdouts; records and missingness; code/tests; total resource ceilings and machine needs. Set `allocation_required` explicitly: false only when reusing this experiment’s still-valid allocation; true for a fresh claim or provisioning. Link the same parent and scientific review by hash. `prepare --next-plan` binds that proposal to the actual assignments, effective configuration, instrument, context policy and runtime.
4. Present that concrete update to the owner. Only after an actual approving decision, record [owner-update-approval.json](templates/owner-update-approval.json) privately with the proposal and execution hashes, scoped `launch` and (if needed) `provision` permission, timestamp and decision reference. Keep the owner's exact prompt out of the record. This is an operator attestation, not an authentication mechanism. An existing explicit decision may be referenced again only when it actually covers the same named scope; budget availability and the researcher-review waiver are not approval of an update.
5. Run `check-update` before allocation. Verify or acquire the required dedicated approved-account machine, retain cumulative budget/reservations, satisfy native public-plan/qualification/runtime gates, then `run --update-approval` for the approved packet. Do not hold idle machines while waiting for a proposal decision.

The templates start unresolved/pending and cannot admit a run. New evidence, changed sample assignments, model/context/instrument/runtime or resource contract requires reassessing the proposal and matching approval. Pure source-commit/receipt-URL freshness changes do not alter the scientific contract; native provenance checks still apply. The commands neither allocate machines nor grant new funds. No `approve` command exists.

## Close the attempt

Reconcile assigned, started, terminal, graded and analyzed counts, including partial and unstarted units. Keep execution, response validity, qualification, scientific conclusion, process compliance and artifact delivery separate. Link the post-mortem, durable evidence and actual cost from `SETUP.md`; update the [confidence and sample-size metadata](../../experiments/EVIDENCE-METADATA.md) after analysis. Release only this experiment's resources after artifact readback and the applicable owner workflow.

The next action should name a concrete operation and its missing evidence. For the current portfolio, consult [the consolidated PI next decisions](../../researchers/vishesh/notes/pi-next-decisions-2026-10-04/README.md) and each study’s DESIGN-TRANSFER note; then reconcile later native evidence before acting. Refresh the registry's checked revision/time and links when that decision changes. Neither this registry nor a historic successful run establishes present authority to spend, provision or deploy.

## Troubleshoot from retained evidence

| Symptom | Local check | Next action |
|---|---|---|
| Missing or changed source/configuration pin | Compare packet hashes, resolved configuration and intended frozen checkout | Regenerate preparation after the appropriate amendment/checks; do not edit the saved packet to make it pass |
| No current runtime receipt | Inspect which admission evidence is absent, stale or mismatched | Obtain only the missing verified evidence; a historical successful deployment is not a replacement |
| Budget exhausted or usage unknown | Read the ledger's sanitized reservations and settlement status, including pending calls | Reconcile known charges; retain uncertain exposure and stop dispatch when the bound is unavailable |
| Ambiguous dispatch or duplicate attempt | Inspect the attempt claim and native call-start/response records | Fence the original worker, resolve pending effects and preserve identity; do not retry by deleting the claim |
| Invalid provider response | Compare the retained sanitized response status, requested/served metadata and declared schema | Diagnose transport, route or contract failure without assuming the cause; retain the outcome and requalify relevant repairs |
| Missing report artifact | Check local terminal outcomes, saved traces and upload/readback receipts | Repair or replay reporting from saved evidence; do not recollect model outputs to fix delivery |

Existing [Theseus preflight](../../researchers/vishesh/notes/swarm-of-theseus/v2/src/preflight.py), [Optimal Size reservations](../../researchers/vishesh/notes/optimal-swarm-size/src/budget.py) and [Immune Response interruption post-mortem](../../researchers/vishesh/notes/immune-response-v3/evidence-study/reviews/receipt-a2-post.md) illustrate these distinct evidence checks. Their historical settings and permissions do not transfer to a new attempt.


## Trace evidence coverage

Every shared closeout now reports [trace receipt coverage](TRACE-RECEIPTS.md) independently of native execution status. Native launchers without the manifest remain explicitly uninstrumented for this check; use a retrospective bridge only for bytes actually retained.
