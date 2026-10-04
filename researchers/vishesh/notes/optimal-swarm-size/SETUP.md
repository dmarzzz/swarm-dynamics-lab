# Optimal swarm size: setup and attempt index

Follow the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [operations guide](../../../../tooling/agent-experiments/OPERATIONS.md). This index is retrospective for earlier attempts and prospective for the schema-contract repair; it does not replace current runtime admission.

Owner/operator: Vishesh / vishesh/codex-idea-scores. Independent design review: Dmarz, 2f5281f. Exploratory synthetic instrument qualification; formal hypothesis/core and transfer remain closed. [Protocol](PROTOCOL.md), [task contracts](TASK-CONTRACTS.md), [prior art](PRIOR-ART-REVIEW.md), [status/history](BUILD-STATUS.md).

## Gate evidence

| Gate | Status | Evidence / next action |
|---|---|---|
| G0 question/research scope | pass for qualification only | Existing Dmarz design review; no formal hypothesis acceptance claimed |
| G1 plan before implementation | pass repair | [Structured-output repair](reviews/structured-output-repair.md), published in 3b75d2c1 before implementation |
| G2 offline instrument | pass | 41 tests; validation.json source hashes; strict parser remains unchanged |
| G3 current admission | pending | Freeze source, verify exact registered plan URL/revision, current claim, canonical ledger, runtime; private receipts required |
| G4 model qualification | fail Q-A1 and Q-A2 | Q-A2 stopped after two fenced-response failures; schema repair still needs live qualification |
| G5 reconciliation | pass Q-A1 and Q-A2 | Q-A2: 2 terminal with acknowledged artifacts, 14 unstarted; q-a2-post.md preserves denominator |

## Current attempt admission

Manual supported entry point: src/run_qualification.py with frozen private runtime config, fresh output, and existing canonical Q1 ledger. Shared experiment-operations adapter does not dispatch this study. Resume is unsupported; preserve failed attempts and require separately authorized identity.

Attempt q-a2; parent Q-A1 per-task IDs; [pre-assessment and plan](reviews/q-a2-plan.md). Revised prompt only, safe parse diagnostics and early stopping; model, fixtures, actor isolation, scheduler and evaluator unchanged. Source snapshot plus validation.json pin the effective instrument. Same 16 repeated fixtures (two families, two structures, four roots) at N=1; not 16 independent replications across earlier/later attempts. No optimal-N inference.

Original SPENDING-AUTHORIZATION.json is historical authority. Owner's latest request authorizes this additional attempt from its remaining funds, not another $20. Canonical ledger retains $0.322112 exposure before Q-A2. $2/episode, 600 seconds/episode, 60 reserved for integration, four service slots, 4096 output tokens and full-context reservations; two consecutive malformed episodes stop the batch. No transport retries or fallback.

Existing claim vishesh-swarm-size-anthropic-q1 on research-01 must be current and exclusive before dispatch. No provisioning. Source/runtime/public receipt and prior-process completion checked before transfer. Exact credential selector swarm-lab-anthropic/account vishesh; [standing credential policy](../../../../tooling/agent-experiments/SWARM-LAB-CREDENTIALS.md), verified SSH stdin, exact single-key payload, separately verified routing metadata, no persistent key or general-key fallback. Private deployment/config/receipt record contains no key.

## Attempt history and closeout

Three transport diagnostics and Q-A1 are retained; [status](BUILD-STATUS.md) distinguishes execution, strict validity, cost, publication and the a3 registration process failure. Q-A1: 16 assigned/started/terminal, zero valid task outcomes, 32 calls, $0.101476 settled; all public artifacts acknowledged. Failures arose before item work; rejected response contents were not retained, so fenced responses are a plausible cause, not an established fact for all Q-A1 cases. Q-A2 adds fixed response-format diagnostics.

Next action: prepare a separately identified bounded qualification of the native schema contract, with a fresh exclusive allocation, exact immutable public plan/source receipt and the original ledger. Q-A2 is closed; the reservation was released in agentops PR173. Do not relaunch its identity or reuse its admission. No new reviewer gate for this routine repair; offline checks are not an independent code audit.

## Current engineering repair

[Investigation and prospective amendment](reviews/structured-output-repair.md) identify prompt-only transport as the interface mismatch. Native phase-specific JSON Schema replaces formatting by prose; local strict parsing/evaluation remains unchanged. Repair feedback identifies parse versus dependency-map failures. No paid requests during this repair; 41 offline experiment checks and 5 credential checks pass. Canonical exposure remains $0.328990. Historical admission paragraphs above describe Q-A2, not current machine authority. No live hosted verification or successful qualification is claimed.

## Proposed next-run redesign

[Next-run design](reviews/next-run-design.md) synthesizes both post-mortems and the schema repair. Proposed first stage: four width-2 N=1 canaries covering both families/structures, with explicit readiness criteria and a $5 sublimit inside the original authority. Requires width-aware identities, canonical-ledger sublimit enforcement and phase-specific stopping/diagnostics before execution. It also records dependency-integrity and slot-capacity controls required before any size-effect claim. Design only; no new run launched.

## Latest completed attempt: Q-A3 canary

[Closeout](reviews/q-a3-canary-post.md): 4/4 end-to-end successes, 16 calls, all artifact hashes and public TLDRs verified. Exact public registration/source admission passed on research-01 under fresh PR207 claim. $0.014038 added; cumulative exposure $0.343028. Earlier pending canary/repair paragraphs are historical. This qualifies only width-2 N=1; next action is separately admitted full-width baseline preparation after correcting the width-dependent progress display. No automatic Q-B escalation.

## Latest iteration: Q-A4 full-width qualification

[Prospective plan](reviews/q-a4-full-width-plan.md), source 69cb6a288d2993cd231f1954519810970dbe5104, 48 passing experiment tests. Sixteen width-16 N=1 cases interleaved across four family/structure cells; strict schema contracts, corrected progress totals, $8 attempt/$2 episode sublimits within the existing original $20 ledger. Fresh claim PR212 and exact immutable public registration verified. Starting exposure $0.343028; no budget reset. Results and promotion decision pending; no automatic larger-N launch.

## PI-driven cycle: Q-A5

Q-A4 closed: 11/16 substantive successes, all 16 schema-valid; all 64 artifact hashes verified. [PI-perspective self-review](reviews/q-a4-pi-review.md) localizes the weak evidence-chain stratum and distinguishes proven observations from integration/propagation hypotheses. This is author critique, not independent review. [Q-A5 plan](reviews/q-a5-evidence-audit-plan.md) published before implementation; source 9b11abb7, 52 offline tests. Eight evidence-only development repeats retain worker artifacts and evaluate stage transitions after termination, without extra calls or actor feedback. Claim PR231 extends the existing exclusive host; exact live plan/source admission verified. $4 attempt sublimit inside the original canonical $20 authority; starting exposure $1.178002. Post-mortem and any further intervention depend on observed stage diagnostics.

## Current cycle: Q-A5 closed; Q-A6 prepared

[Q-A5 post-mortem](reviews/q-a5-post.md) completes scientific self-review: 3/8 successes, all errors already in workers, no integration correctness transitions. 32 public artifact hashes verified; preceding worker stopped. Cumulative original-ledger exposure $1.606634 including $0.220480 historical hold.

[Q-A6 plan](reviews/q-a6-matched-roster-plan.md) was written before implementation. Eight evidence episodes form four N1/N2 pairs but only two independent root seeds. Both arms enforce all supplied dependency edges; evaluator-only audits remain outside actor context. 56 offline checks pass including omitted-edge rejection/one repair, matched task hashes, counterbalanced order, context isolation and parallel-versus-chain service concurrency. The owner's active cycle request authorizes deciding and running these bounded updates; no fresh spending authority or self-issued approval. Researcher review is optional under updated standing policy. Current G3 remains pending until frozen source/public registration, live exclusive claim, ledger and runtime verification; no assertion that implementation tests establish model performance.
