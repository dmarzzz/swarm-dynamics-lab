# Right Dissenter RD5 setup record

**Reviewed operational non-dispatch; approved scientific scope unchanged; Q5 qualification passed, conditional H5 admission next. See [current status](RUN-STATUS.md) and [renewal plan](ACTIVATION-02.md).** Owner/operator/assessor: vishesh/codex-decision-models. Exploratory scope, tagged dissent and decision models. Follow the [setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [operations guide](../../../../../tooling/agent-experiments/OPERATIONS.md).

Question: when does remembering unresolved evidence and protecting a future check help, and when does it delay an urgent decision? Primary B2 reserve versus B1 memory; secondary B1 versus B0 bounded always-check. [Plan](PLAN.md), [amendment](AMENDMENT-01.md), [ready package](READY.md), [previous cohort](../rd4/REPORT.md).

| Gate | Status | Evidence and next action |
| --- | --- | --- |
| G0 question/prior art | scoped exploratory | RD4 post-mortems, failure decomposition, existing source/Twitter map, Hay/Tan primary references. No completed novelty survey or accepted hypothesis claimed. |
| G1 design before code | complete | Amendment published at `10e6b4d775c8409c1a9817ad633f0f6f84ae3c40` before code. All H5 mechanisms now share one domain. |
| G2 instrument | offline checks passed | 61 development tests; state/resource separation, frozen input adapter, policies, transport and replay. [Validation](validation/VALIDATION.json). |
| G3 admission | refreshing before direct dispatch | Scoped owner directive and central fence verified; new exclusive approved-account allocation merged. Fresh source/runtime, public plan, route, receipts and normal platform launch review remain. See DIRECT-ACTIVATION.md. |
| G4 qualification | native Q5-A2 passed | 24/24valid complete,12/12correct cards and all6uncertainty controls; source-bound seven-file audit and post-mortem complete. |
| G5 closeout | Q5-A2 reviewed | Worker/relay stopped; expected artifacts read back; operational finalize plus scientific assessment complete. Current allocation retained for conditional H5. Historical A1 non-dispatch preserved. |

## Definitions and access

H5: six authored roots (three mechanisms × stop/resume), three policies, four epochs: 72 dependent outcomes, 24 per arm. Q5: 12 disjoint authored packets in two representations. Development ID 51901; Q5 52000-series; H5 53000-series; ordering seed 51004. IDs do not establish semantic independence. Ordinary tests never construct Q5; explicit preparation does.

Actors receive only current task, supplied ballots, own historical/current state and acquired source text/card. No evaluator truth, arm, mechanism, future frames, peer results or operating-assistant context enters the request. Each arm starts fresh; no cross-arm answer cache. The finite parser preserves text, matched spans and unknown/conflicting fields. Jev resolves actions; no oracle substitute.

The original ledger remains 428/500 calls, $0.01662045 settled plus $0.004032 historically unresolved, $0.02065245 committed API. Q5+H5 allow at most 60 new calls, lifetime stop 488; 12 remain unallocated. Preserve $1 API/$1 infrastructure, including historical estimated compute $0.011643. Prior existing-fleet invoice is unavailable; bound incremental infrastructure before launch. No budget reset or redundant approval.

## Operations

- Offline: `python3 -m unittest discover -s researchers/vishesh/notes/dissent/rd5/tests -v`.
- Prepare: `src/rd5_cli.py prepare`; committed source only, no dispatch. Public hashes in [preparation manifest](spec/preparation-manifest.json).
- Run: `src/rd5_supervise.py`; strict native admission in both relay and worker, actual remote health probe, supervised transport. See READY.md.
- Report: `src/rd5_cli.py report --results <saved directory>`; no model calls.
- Resume: deliberately unsupported. Preserve partials/reservations; separately assess any never-started trajectory continuation. Never delete identities to retry.
- Shared operations CLI: this study uses its documented manual workflow; no new `scripts/experiment.py` adapter is claimed.

Next authorized execution sequence: register/verify immutable plan and Q5 TLDR; obtain a fresh dedicated allocation from Dmarz's authorized private fleet; verify actual workload/account, source, original ledger, route and runtime; issue fresh private receipts; run Q5 once and assess it before H5. Allocation and relay status here are historical; use the dated RUN-STATUS and fresh private receipts to establish whether any claim remains active. Researcher sign-off is not required by owner direction. Better native semantic accuracy, independent semantics and adaptive arrival timing remain untested.

Owner decision boundary: the refreshed [agent protocol](../../../../../AGENTS.md) requires approval of the updated next-run plan before allocation or launch. The concrete [proposal](spec/next-run-plan.json) and [evidence-linked RD4 quality review](reviews/RD4-QUALITY-REVIEW.json) are covered by the recorded approval in [RUN-STATUS.md](RUN-STATUS.md) for unchanged Q5/conditional H5. Do not request that approval again; materially different scope requires a new decision. Existing budget approval remains valid; the disabled template does not invent plan approval.

Operator closeout hook after each stopped native attempt: `python3 scripts/experiment.py finalize right-dissenter --attempt <unique-rd5-attempt> --results <saved-results> --outcome <completed|failed|ambiguous> --worker-stopped`. This generates an operational handoff only; complete the scientific review separately and retain reporting/cost status.
