# Experiment setup record: compositional-safety / interface diagnostic v1

Exploratory instrument repair, not the scaled study. Follow the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). This record incorporates the workflow added upstream during preparation of i0-003; it does not retrospectively register older attempts.

## Ownership and question

- Owner/operator/author reviewer: dmarz/patchwork-hypotheses. The user's explicit instruction replaces independent review with clearly labeled author research/mechanism critiques; no institutional review is claimed.
- Diagnostic question: does explicitly stating the existing host execution/history contract improve productive action selection on retained failed states, with model and task unchanged?
- Main research question and prior work: [SEC-54 plan](../compositional-safety-plan/README.md). Formal survey/hypothesis acceptance and S1/S2 remain closed; this is bounded engineering diagnosis under the user's shipping/repair instruction.
- Previous evidence: [q0-004 post-mortem](reviews/q0-004-post.md), all previous reviews and immutable result summaries. Twelve stalls and two refusals remain failed outcomes.
- Current stage: i0-004, sixteen paired atomic diagnostic requests after the reconciled i0-003 failure. Next action: finish current-source public registration and launch only after all runtime checks pass.

## Gate evidence

| Gate | Status | Evidence / assessor | Next action |
|---|---|---|---|
| G0 Question and applicable research gates | Pass for authorized engineering diagnosis only | Existing plan, explicit review override, internal-design-review.md / author | No formal hypothesis promotion or scaled claim |
| G1 Prospective design | Pass | i0-003-pre.md and fixed case list committed at 29b52a30 before any diagnostic data / author | Preserve original and clarified outcomes |
| G2 Instrument and offline checks | Pass for diagnostic preparation | Fourteen offline checks passed locally and on sim-dmarz; eight exact parent packets reconstructed / author | Check additional admission regression before launch |
| G3 Current attempt admission | Pending until runtime receipt | common.frozen invokes admission.check before dispatch; immutable URL/content/source and live registration must agree | Save registration/i0-003.json after actual page verification; capture it in result artifacts |
| G4 Qualification before escalation | Failed | q0-004: 10/24 safe, twelve incomplete, two refused | Atomic success cannot replace fresh Q0 |
| G5 Prior reconciliation and closeout | Pass for prior attempts | q0-004 post-mortem, 53 hashes, thirteen complete hub runs, empty spool, original claim released | New attempt requires its own post-mortem and closeout |

## Design and instrument index

- Plan/amendments: [i0-003 assessment](reviews/i0-003-pre.md), [preregistration amendments](preregistration.md), [design](design.yaml).
- Eight deliberately selected previously failed states, two conditions per state; not eight independent task structures or sixteen full episodes. No significance or generalization claim.
- The expected-action sets are evaluator-only; provider bodies contain original policy/menu/history plus the declared static contract in the clarified condition. No hidden state or expected answer is supplied.
- Definitions: src/engine.py, src/prompt.txt, src/provider.py, src/contract.py. Diagnostic driver: src/diagnose.py through src/probe.py. Source/design hashes cover every Python file and the prompt.
- Model: pinned claude-sonnet-5; disabled thinking, high effort, default sampling. Python 3.12.3, PyYAML 6.0.2, Pillow 11.3.0. No automatic retries or model fallback.
- Startup: common.frozen verifies committed protocol plus current public-plan admission; unique result directory; parent artifact hash; fixed shuffled assignments; transactional call IDs and spending reservations.
- Offline tests cover simulator/evaluator controls, history boundaries, 4,200 reference fixtures, costs/failures, static-contract nonmutation and public-admission fault cases. This remains same-author verification.
- Visualization: diagnostic-v1 in the pre-run assessment. Eight rows × original/clarified columns; every observed response retained in PNG/GIF and exact request/result JSON.

## Current attempt admission

- Attempt/parent/stage: i0-003 / q0-004 / I0. Command: python src/probe.py i0-003.
- Immutable plan URL: the deployed full revision's GitHub blob URL for reviews/i0-003-pre.md. The exact URL, expected SHA-256, runtime hashes, registered TLDR and verification timestamp are required in registration/i0-003.json and copied into the run's public-plan-receipt.json before run_start.
- TLDR: compare original vs explicit execution-contract inputs on eight saved failed decision states with the same model. Measure validity and advancing actions. Selected-state diagnostic only; not qualification.
- Run: compositional-safety/i0-003-diagnostic, seed i0-003-paired-order, sixteen frozen condition assignments. The run retains its immutable plan link even if the experiment's latest link changes.
- Existing authority: researchers/dmarz/README.md grants $500 shared API spend and directs continued bounded repair. The existing study ledger has 1,610 calls, $5.340097 reported actual and $28.033098 retained reservations; remaining local ceilings are 7,606 calls and $156.966902 reserved. This diagnostic adds at most sixteen calls/$0.699072 reserved, not a fresh $185 allocation. The local ledger is not an account-wide billing authority; cross-study reports must not be represented as a complete balance.
- One process; 350 output tokens/16,000 serialized input bytes per request; 90-second request timeout; 1,800-second stage ceiling plus one in-flight request/reporting; no retries. No further stage is automatically launched.
- Exclusive server: sim-dmarz, claim dmarz-compositional-repair, merged agentops PR 105, expires 2026-10-04 07:09:09 UTC. Original worker exited; clean retained checkout and ledger verified. No provisioning or billing-account change.
- Credentials: SWARM_MODEL_API_KEY and SWARM_MODEL_WORKSPACE_ID from the existing approved encrypted source; host-provided hub configuration. Values remain in process memory.
- Runtime receipt and actual public-page verification are launch requirements, not inferred from this document. No model request may precede them.

## Attempt and repair history

| Attempt | Disposition / evidence |
|---|---|
| s0-001 | 84/84 scripted completions; implementation evidence only |
| q0-001 | 21/24 safe; two invalid and one violation |
| q0-002 | 20/24 safe; four incomplete |
| q0-003 | 16/24 safe; eight nonterminal outputs |
| i0-001 / i0-002 | Refusal reproduction / one-call fallback compatibility; not qualification |
| q0-004 | 10/24 safe; twelve incomplete and two refusals; fully reconciled |
| i0-003 | 16/16 reconciled; original 0/8 and clarified 3/8 advancing, diagnostic failed; post-mortem published |
| i0-004 | Prepared model/configuration diagnostic using the same fixed states |

The interface hypothesis is open until observed diagnostic evidence and a fresh full qualification support it. Provider refusals remain a separate unresolved suitability issue. Earlier valid negative outcomes and thresholds remain unchanged.

## Closeout and handoff

After i0-003, reconcile sixteen assignments, exact request bodies, answers/failures, costs, hashes and every visual cell/frame. Save the post-mortem before choosing the next run. If the clarified condition is clean, apply the same static contract consistently, run offline regression and fresh disjoint Q0. If it fails, diagnose its actual failure before any new amendment. P1 and formal S1/S2 remain blocked until their own gates pass. Keep the claim only through active repair/execution and verified uploads; release it while blocked.

## i0-004 admission update

Read i0-003-post.md and i0-004-pre.md. The latter is the current prospective plan, bound to the deployed immutable revision and verified again by the same runtime admission gate. Use registration/i0-004.json and run compositional-safety/i0-004-diagnostic. The prior run had 24 verified hub artifacts, 23 checked file hashes, sixteen exact request/response pairs, 17 decoded GIF frames, an empty spool and an exited worker. Remaining study ceilings before this follow-up: 7,590 calls and $156.606526 reserved. This attempt adds at most sixteen calls/$0.349536 reserved. Same exclusive server claim and expiry; no new infrastructure. A read-only hub snapshot around 04:17 UTC summed $42.221204 across recognized cost fields in 1,220 runs; it can double-count stage summaries and omit unreported costs, so it is not an account balance. The standing shared $500 authority and cumulative local guard remain unchanged.

## d0-001 admission update (supersedes prior current-attempt sections)

Current stage: bounded closed-loop I0, parent i0-004. Read i0-004-post.md and d0-001-pre.md. Seventeen offline checks cover actual delivered packet/trace identity, unchanged world transitions and complete paired assignment. Pinned Haiku 4.5, temperature zero. Eight episodes, four cases with original/clarified contracts, at most 320 calls/$6.99072 reservations and 1,800 seconds. Existing cumulative ledger before run: 1,642 calls/$5.432886 actual/$28.573278 reserved. Same exclusive claim and 07:09:09 UTC expiry; no new machine. Runtime admission requires registration/d0-001.json bound to the newly deployed full revision and actual verified public page. G3 remains pending until that receipt; G4 remains failed. All four clarified episodes must finish safely and validly before considering adoption/fresh Q0. Original atomic 8/8 screens remain failed. After run, reconcile all eight episodes, traces, plots/replays, costs and hub uploads, then write the post-mortem. Normal Q0/P1 inputs are not changed by this diagnostic.

## d0-002 admission update (current)

d0-001 was registered but withdrawn before dispatch, with zero calls, after code/trace review identified single-controller instructions implying nonexistent other actors. Current plan is d0-002-pre.md, paired contract-v2 diagnostic; parent remains i0-004. Contract v2 states sole-controller versus round-robin scheduling, active actor count, and abstract D1 fact representation, without changing actions or exposing hidden truth. Same eight assignments and limits as the withdrawn plan. Public receipt is registration/d0-002.json at the final deployed revision. Same budget/claim; G4 still failed and no normal-worker adoption yet. Same-team reviewers checked behavior and pending code; this is not independent researcher or institutional review. Next action: local/remote checks, final current-revision public registration, then finite diagnostic.

## q0-005 admission update (current)

d0-002 passed 4/4 clarified and was fully reconciled; see d0-002-post.md. Candidate contract v2 is adopted through explicit shared Q0/P1 configuration. Fresh qualification roots 240–242, 24 episodes, five structural fingerprints. Before launch: 1,742 calls / $5.572021 actual / $29.646810 reserved; maximum 960 new calls / $20.97216 reservations; same 07:09:09 UTC claim expiry. Current plan q0-005-pre.md and receipt registration/q0-005.json must bind final frozen source/design and actual public page. G3 pending runtime receipt; G4 still pending fresh qualification, not granted by the diagnostic. Next action: finish shared-transform regression, deploy/publish/register/verify, then run finite Q0. Preserve all source hashes unchanged for any later P1.
