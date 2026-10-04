# Qualification build and launch status

Updated 2026-10-04 UTC by vishesh/codex-idea-scores.

## Implemented

- `src/tasks.py`: deterministic 16-item evidence/repository fixtures, strict JSON parsing, restricted-AST repair evaluation, operational scoring and an 80-assignment manifest. Transfer generation is deliberately unavailable.
- `src/engine.py`: stateful contexts, one planning-repair allowance for malformed model plans, dependency scheduling, charged-context interfaces and final integration. Ready jobs use the least-used idle actor (ties by actor ID), so a four-slot limit does not silently make N=16 use only the same four contexts. Model-call transport failures are not retried as planning repairs.
- `src/budget.py`: durable SQLite reservations at episode and shared-stage scope; unfinished provider charges retain their reservation. Concurrent reservation tests exercise overspend prevention. This is single-host accounting; do not copy its database to independent hosts.
- `src/provider.py`: an isolated-process OpenRouter transport, parent-enforced request deadline, no credential logging, no route fallback, conservative full-context reservations and actual-cost settlement. Provider execution has not been tested with a real call; served model/provider fields remain unset.
- `src/run_qualification.py`: Q-A-only execution entry point, source/public-plan checks, assigned manifest, local condition-specific TLDRs and durable event/outcome files. It uses `reporting.py` to register each run with a condition-specific TLDR and verify that TLDR through the public proxy before actor calls. `register.py` publishes experiment-plan metadata separately. Local JSON events/outcomes and a standalone interval replay are uploaded through the installed hub client. It does not allocate a machine or manufacture a review verdict. Reporting/transport integration still needs validation on the selected host. Q-B requires the Q-A assessment and frozen calibration configuration; it is not automatically launched.

The actual first implementation narrows repository repair to an explicitly described arithmetic expression grammar. It is a qualification benchmark, not a general software repair study. All actors receive the complete small public task at context initialization; replicated prompt tokens must be charged. This avoids unequal information access but does not implement the large-corpus retrieval extension yet. Dependencies are explicitly visible in these fixtures; latent-structure inference is not being tested.

## Offline verification

Command from repository root:

```
python3 -m unittest discover -s 5-experiments/studies/vishesh/optimal-swarm-size/src -p 'test_*.py' -v
```

Twenty-one test methods cover 80 reference-task variations, all five rosters under scripted transport, malformed and adversarial submissions, equivalent valid repairs, split/input invariants, concurrency/overspending, operational boundaries and refusal of the incomplete launch configuration. Scripted reference answers prove plumbing only; they are not model performance observations. No experimental/model run has occurred.

Read [PRIOR-ART-REVIEW.md](PRIOR-ART-REVIEW.md) for the completed focused author review and its limits. The independent review is requested in `lab/tasks/review-swarm-size-qualification.md` for Shadow; no passing verdict has been received. The focused review does not complete the formal survey/hypothesis gates for a confirmatory study.

## Remaining launch work

1. **Resolved:** the user authorized $20 total for the first qualification attempt, shared across Q-A/Q-B and failed calls. SPENDING-AUTHORIZATION.json records the authorization. The config uses a $2 per-episode sublimit. Reopening the same ledger preserves usage; config changes cannot enlarge the recorded authorization. No model spend has occurred.
2. Review and pin the served model/provider route and the price/accounting bound. Public OpenRouter model metadata on 2026-10-04 listed `openai/gpt-4.1-mini` with input $0.40/M tokens and output $1.60/M tokens. These are observed quotes, not a contract or spending authorization. The draft conservatively reserves 1,047,576 context tokens plus 4,096 output tokens per call: $0.425585 rounded upward. Nineteen calls per episode gives a very loose upper bound of $8.086115 per episode, $129.37784 for Q-A and $646.8892 for all 80. Actual prompt/output usage would normally be much smaller, but it is unmeasured. A smaller authorized cap may stop execution early; tighter reservations need verified tokenization rather than optimistic guesses.
3. Obtain independent package review and address findings. Confirm the permitted exploratory S0/S1 route; keep core/transfer locked behind the research gates.
4. Validate the implemented hub reporting/transport and standalone replay on the selected host; register and verify an immutable public plan and condition-specific TLDR before model execution. Existing public proxy problems must not be treated as a successful public preflight.
5. Verify a fresh exclusive eligible fleet allocation and non-secret credential availability. No machine was claimed or provisioned during this build.
6. Freeze source/config, verify every launch requirement, start Q-A, reconcile all 16 assignments, assess qualification and calibration, then freeze Q-B. Keep failed/cancelled/not-started records visible and retain unknown billing reservations.

The launch check currently exits 2 with missing fields. This is an explicit not-ready result, not an attempted model run or a successful launch.

## Visualization delivery

Live qualification uses textual progress and measured item counts. Final `replay.html` displays recorded service intervals with a scrubber and static table; it is a downloadable hub artifact because the public proxy does not serve arbitrary HTML. `trace.jsonl` preserves event history. There is no flock animation or manufactured physical trajectory, and no claim that an interval plot measures provider GPU activity. Browser validation and transport integration are outstanding review checks; offline replay checks cover interval lengths, missing ends and HTML escaping.

## Authorization update

The $20 cap is now authorized, not pending. Provider requests include price ceilings matching the reviewed quote and disallow per-request charges and fallback routes. Budget tests verify exhaustion at exactly $20, retention across Q-A/Q-B and rejection of cap resets. Route pinning, live integration/public preflight and independent review remain incomplete; the Shadow review task was still open and unclaimed at this check. No machine is reserved while these prerequisites remain unresolved.

## Live setup update — 2026-10-04 UTC

The public plan is now registered and verified; see reviews/q1-public-plan-receipt.json. Source 1002752 passed 23 offline checks on sim-test-01, and the synthetic replay passed browser inspection. Fixed public run requests to use the documented preflight user agent after reproducing HTTP 403 with the Python default. No model calls or spend occurred. Credential availability and independent package review remain unresolved. The temporary allocation is released while blocked; see reviews/q1-setup-post.md for exact resume steps. Earlier lists of unverified reporting/replay checks are superseded only to this extent: real per-run reporting and provider integration remain untested.

## Engineering review repairs — 2026-10-04 UTC

Review 273e35ed returned REVISE for error categories, reporting and batch reconciliation. Those repairs are implemented with 31 passing offline tests; see reviews/q1-engineering-response.md and the exact source hashes in validation.json. Re-review and a new bounded synthetic host reporting check remain pending. No model calls or spend. Formal cross-researcher review is now assigned to dmarz, superseding earlier Shadow references.

## Reporting diagnostic passed — 2026-10-04 UTC

E1–E3 re-review passed at 19fa527d. Live synthetic reporting-q0-a1 passed on exclusively allocated sim-vishesh: public TLDR/terminal state, all acknowledgments, four downloaded artifact hashes and installed-client hash verified. Local child timeout passed at 30.024 seconds. See reviews/reporting-diagnostic-post.md and evidence.json. Zero model calls; full $20 cap remains. Credential/served-route qualification and formal dmarz review remain pending. Diagnostic allocation released after evidence preservation.

## Shared Anthropic selected and prepared — 2026-10-04 UTC

The user explicitly selected the shared Anthropic setup. Pinned native Haiku 4.5 adapter and prospective amendment published at 59a7c45f. All 32 tests pass locally and on research-01 with Python 3.12.3. Fresh exclusive claim vishesh-swarm-size-anthropic-q1 (agentops PR126) covers the batch; public registration/preflight passed. The existing Keychain lookup succeeded locally without revealing the credential. The original authority ledger belonging to other experiments is untouched; this newly authorized $20 scope uses its own single canonical Q1 ledger shared by transport/Q-A/Q-B, never copied/reset.

Automatic approval review rejected transferring the shared credential to research-01 over SSH, requiring explicit user approval for that destination. Credential-free preparation subsequently completed with an empty secrets payload and no Anthropic request. No credential was transferred and no paid call occurred. See reviews/anthropic-preparation.json. The concrete remaining approval is encrypted transfer to this already claimed host, consumed only in process memory by the approved native Anthropic adapter.

Dmarz review 2f5281f is recorded in the config. The root owner's single-researcher-review clarification supersedes duplicate review gates for routine repairs; the new adapter has author regression evidence, not an independent adapter audit. An optional engineering re-review handoff was rejected as unconfirmed scope in the other task and must not be represented as completed. Before Q-A, run the registered one-call transport diagnostic and require valid served route/usage/response, then use the same canonical ledger for the 16 assignments. Full $20 authorization remains available.

## Credential policy and live transport — 2026-10-04 UTC

The owner's standing instruction resolves the earlier one-off destination authorization: only Keychain service swarm-lab-anthropic/account vishesh may transfer to admitted, inventoried and exclusively claimed Swarm Lab hosts. The shared runbook, root instructions, exact-selector helper and five passing credential tests implement that scope. No general Anthropic credential or environment fallback is used. Required workspace routing is separately verified metadata bound to the same selector. The launcher uses verified SSH stdin, disables agent forwarding/core dumps and persists no API key. Private credential-transfer evidence is saved on research-01.

Three diagnostic attempts are preserved in the original canonical Q1 ledger: a1 HTTP400 retains a $0.220480 unknown-charge hold; a2 matched the pinned native route but returned fenced JSON, settling $0.000084; a3 passed strict JSON, route/usage and acknowledged artifact checks, settling $0.000072. Total diagnostic exposure is $0.220636, of which $0.000156 is settled. These are engineering outcomes, not task competence or size-effect evidence. No refund, reset, new authority or higher cap.

Process compliance is separate: a3's pre-call receipt unexpectedly still identified the a2 plan during public metadata propagation. Its execution passed, but a3 is **not process-compliant**; later confirmation cannot make that preregistration. The frozen a3 plan was published before the call, but exact current registration was not verified at dispatch. Preserve both receipts and do not erase this failure. Q-A's source/receipt check caught the same stale reference and stopped its first launcher before any assignment or task call. Its startup record/log are retained. A fresh receipt subsequently verified the current public immutable plan and source c99e0c623d33d3226edecff02ab9728da9cf6374 before relaunch. Future preparation must require exact expected plan URL/revision, not merely a generic preflight success.

## Q-A2 dispatched — 2026-10-04 UTC

The owner requested another run. Prospective plan reviews/q-a2-plan.md was published before implementation; frozen source 056718f7a86b2807b05b6f952e34f4b1218393ed passes 34 offline checks locally and on Python 3.12.3. Changes: explicit raw JSON/no-fences prompts, safe format diagnostics, isolated attempt IDs with unchanged parent task identities, and stop after two consecutive malformed episodes. Strict evaluation is unchanged. All 16 Q-A1 failures remain retained and published.

Exact public plan URL/revision was verified against frozen source before dispatch. The first launch check held because the remaining allocation was shorter than the bounded run; zero task calls occurred. Existing exclusive research-01 claim was extended through agentops PR172, merged. Original and renewed runtime configs are both preserved. Q-A2 then dispatched with only the dedicated Swarm Lab credential under standing policy, fresh output/process records and the same original $20 ledger. Starting cumulative exposure $0.322112; no replenishment. This is a repeated-fixture repair qualification, not an independent replication or swarm-size result. Q-B/core remain closed.

Q-A2 closed with its preregistered early stop: 2/16 terminal, both malformed output; 14 unstarted. All four planning/repair responses were fenced, confirmed by the new trace flags. Both executed cases' publication receipts passed. New spend $0.006878; cumulative exposure $0.328990. Worker exited; see reviews/q-a2-post.md. A successful dispatch is not successful qualification.

## Schema-contract repair implemented — 2026-10-04 UTC

Investigation and prospective plan published in 3b75d2c1 before implementation: reviews/structured-output-repair.md. The native request builder previously omitted output_config.format, so prompt-only wording could not enforce the strict parser's contract. Added explicit closed JSON Schema for plan/repair, family-specific work and final artifacts, using only public field names. Added explicit contract version, pre-reservation configuration/phase checks, full-payload byte bounds, schema hash receipts and safe refusal classification. Existing parser, evaluator, route checks, charge settlement and response-completion gates remain enforced. No fence stripping or retrospective scoring. Plan-repair feedback now distinguishes invalid JSON from invalid dependency maps.

41 offline experiment tests and 5 credential-policy tests pass, including intercepted outbound HTTP payloads, all task-family/phase schemas, refusal/truncation accounting and unchanged rejection of invalid content. Native provider live behavior is not yet requalified. No model calls, credential transfer, allocation or spend during this repair; cumulative exposure remains $0.328990. Q-A2 allocation is released (agentops PR173). Next paid attempt needs a new identity, current exact public admission and exclusive claim while retaining the original ledger.

## Q-A3 canary passed — 2026-10-04 UTC

Four width-2 N=1 cases passed end to end at frozen source c2655e66. All four correct/on-time final artifacts, eight completed work items, 16 model calls, zero repairs. Every uploaded artifact (16 files) matched local hashes on download; public TLDRs and terminal statuses verified. Added spend $0.014038; canonical cumulative exposure $0.343028 of the unchanged $20 cap. Full closeout: reviews/q-a3-canary-post.md. Full-width qualification and any size comparison remain unrun. Legacy live progress total=16 is a documented display defect for width-2 runs; final artifacts and scores are correct.

## Q-A4 full-width build and admission — 2026-10-04 UTC

Prospective plan q-a4-full-width-plan.md published in c12ac6af before implementation. Frozen implementation 69cb6a288d2993cd231f1954519810970dbe5104 passes 48 experiment tests locally and on research-01/Python 3.12.3. Full-width manifest interleaves 16 width-16 N=1 cases, records width/hash/parent identity, uses strict phase-schema checks and enforces an $8 attempt/$2 episode sublimit in the original $20 canonical ledger. Fixed live progress totals to use assignment width, with width-2 and width-16 regression coverage.

Fresh exclusive claim vishesh-swarm-size-full-q4, agentops PR212. Prior canary completion/readback and exited worker verified; exact new immutable plan URL/commit verified on the public API before dispatch. Starting canonical exposure $0.343028 across 55 previous calls, including the unresolved original hold. Dedicated Swarm Lab credential policy remains binding. This is full-width single-agent qualification; no matched-N or core stage was opened. Runtime outcome and closeout remain pending.

## Q-A4 reviewed; Q-A5 stage audit admitted — 2026-10-04 UTC

Q-A4: 11/16 final successes (repository 8/8, evidence parallel 3/4, evidence chain 0/4), all outputs schema-valid, all supplied prerequisite edges present. 288 calls added $0.834974; cumulative exposure $1.178002. All 64 artifact hashes and public TLDRs/terminal states verified. See q-a4-pi-review.md for the retrospective self-critique and failure localization limits.

Q-A5 keeps prompts/model/protocol unchanged while retaining work artifacts and computing evaluator-only per-item transitions after termination. Eight evidence fixtures, new namespace, $4 attempt cap in the existing ledger. Source 9b11abb7 passes 52 offline checks. Existing dedicated host claim extended via PR231; prior worker exit/readback and exact public plan/source verified. All commits now use Cytonomy's explicitly configured identity. No larger-N stage is opened.

## Q-A5/Q-A6 PI cycle closeout — 2026-10-04 UTC

The latest evidence supersedes earlier pending-launch status, without rewriting historical attempts. Q-A5 localized incorrect evidence values to worker outputs (3/8 successes, zero integration correctness transitions). Q-A6 tested matched N1/N2 with required dependencies on two fresh development roots, 8/8 complete, 0 full successes. Parallel N2 was 32–45% faster and about15% cheaper, with lower quality; chain quality was unchanged near zero, timing mixed. See [Q-A6 post-mortem](reviews/q-a6-post.md). This is exploratory evidence, not an optimal-size rule. All 32 original and 8 repaired replay artifacts verified; presentation-only repair used saved traces, zero fresh calls. 56 experiment tests plus 11 evidence-metadata tests pass. Cumulative exposure $2.031320 of original $20; worker exited, no successor queued. Policy/transfer remain untested.

## Q-A7 one-cycle preparation

[Plan](reviews/q-a7-input-binding-plan.md) and [queue operator packet](Q-A7-OPERATOR.md): fixed-N1 full versus redundant public bindings; two fresh roots, eight planned episodes, prospective futility stop after four. 63 offline tests pass. No paid/native execution or qualification claimed. Current ledger unchanged, $2.031320 exposure of original $20; $2 attempt sublimit. Admission blocked on dedicated queue allocation, approved credential delivery and canonical single-writer ledger continuity. Existing research-01 allocation belongs to another experiment. See SETUP for authoritative current state.
