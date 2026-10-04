# Experiment setup record: Poietic Agents v0.2

Status: offline instrument and qualification package prepared; no native calls authorized or executed. Follow the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Updated 2026-10-04 UTC by vishesh/codex-heterogeneous.

## Ownership and question

Owner: vishesh. Operator/author: vishesh/codex-heterogeneous. Independent design reviewer: dmarz/inbox-design-feedback, [review](../../../dmarz/notes/inbox-reviews-2026-10-04-round2/poietic-review.md). This is one different-researcher design review, not an independent code audit or a formal hypothesis pass.

Question: does reversible, locally proposed specialization lower complete deployment cost per assigned, fresh, correct and on-time job beyond competent caching/static specialization? Research status: exploratory instrument. [Prior art](PRIOR-ART.md) leaves formal research gates open. No previous Poietic attempt or post-mortem exists.

Current gate: G3 for S0-01. G2 offline preparation passed 54 checks. Next action: resolve explicit confirmation of the proposed $2 cumulative cap, verify credential provenance, then resolve the dedicated allocation task and deployment evidence. G3 awaits explicit confirmation of the proposed $2 cumulative budget and still needs the approved credential selector plus a fresh exclusive approved-fleet allocation. The reduced $2 proposal is sufficient for initial S0; explicit confirmation is pending and the earlier $7 increase is not presumed approved.

## Gate evidence

| Gate | Status | Evidence and assessor | Next action |
|---|---|---|---|
| G0 question / research gates | partial | [PRIOR-ART.md](PRIOR-ART.md), author; independent focused overlap review linked above | Full survey/hypothesis acceptance before formal research |
| G1 prospective design | pass for offline implementation | Published v0.1 at `4a373dad56aab6a7129f16748a2edf312ce6d048`; [v0.2 amendment](AMENDMENTS.md) resolves P1–P3 before code | Bind executable definitions |
| G2 instrument | pass for S0 preparation | [VALIDATION.json](VALIDATION.json), author; 54 checks; [review resolution](REVIEW-RESOLUTION.md) | Native interface behavior remains unobserved |
| G3 S0 admission | blocked | [S0 pre-assessment](reviews/S0-01-pre.md) | Budget, exclusive allocation, source/plan freeze, public verification |
| G4 qualification | not run | 0 native responses | Only after G3 |
| G5 closeout | not applicable yet | No experimental assignments started | Reconcile and post-mortem every future attempt |

## Design and instrument index

- [Protocol](PROTOCOL.md), [amendments](AMENDMENTS.md), [design](design.yaml), [contracts](contracts.json), [visualization](VISUALIZATION.md), [handoff](RUNBOOK.md).
- S1: four paired roots, six agents per arm, four arms, eight epochs, six jobs per epoch: 768 assigned jobs, not 768 independent samples. Four roots support feasibility only.
- Development roots 0–99; S0 namespace roots 100–147; S1 200–203. S2 10000–19999 stays unopened and unassigned.
- Startup must verify effective definitions, empty state, paired exogenous inputs, immutable plan, unique attempt, authorization and current dedicated allocation before dispatch. Model contracts and source definitions are implemented. [Validation](VALIDATION.json) pins exact hashes and checks. Native/deployment evidence remains pending, not implied by this checklist.

## Current attempt admission

S0-01 is blocked on credential/allocation admission, with budget authority pending. Existing [registration](registration.json) publishes design only. A newly frozen immutable plan, condition TLDR, public receipt/page check, model/source hashes, durable assigned manifest, shared budget reservation, deployment/credential status and exclusive claim must be checked before any native request. Missing evidence cannot be replaced by operator booleans or another study's receipts. No host is claimed while approval is pending.

## Attempt and repair history

No attempts. Independent P1–P3 measurement clarifications are prospective design changes, not repairs of measured outcomes. They are tracked in AMENDMENTS.md.

## Closeout

Execution: not started. Response validity: unobserved. Qualification: untested. Scientific conclusion: none. Process compliance: preparation only. Reporting: previously verified public design with zero runs. Evidence confidence remains 0/4 for the claimed adaptive benefit. Exact next action is G3 S0 admission; the $2 proposal is recorded as unapproved in AUTHORIZATION.json, [allocation task](../../../../tasks/allocate-poietic-agents-s0.md) is open, credential provenance must be verified, and S2 remains closed.

## Completed preparation evidence

`src/prepare.py` wrote 144 assignment IDs without opening reserved source fixtures. `src/launch.py check` rejected the candidate with `study_budget_not_authorized` before network/credential/model work. No allocation is held. Official route metadata fixed Haiku/Anthropic, Qwen/Alibaba and Jev/TypeSafe; worst-case API reservation for all 288 physical calls is $1.447723008. The proposed amount is $2 cumulative, allocated as $1.50 API plus $0.50 infrastructure; the approved amount remains zero pending explicit confirmation. PNG layout and interactive replay transitions were inspected locally. The latter remains visibly scripted. A1 serializes requests in the one-worker instrument, so shared-cache hits coalesce repeated work without a separately claimed concurrent-cache benchmark.

The historical independent review and its useful corrections remain in place; no waiver is needed. The candidate refuses dispatch without explicit budget confirmation and current host/credential/deadline evidence. Continue via [qualification task](../../../../tasks/qualify-poietic-agents-s0.md).
