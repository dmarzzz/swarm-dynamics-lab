# Right Dissenter RD5 setup record

**Implemented and checked offline; next-run preparation complete; no native stage admitted or started.** Owner/operator/assessor: vishesh/codex-decision-models. Exploratory scope, tagged dissent and decision models. Follow the [setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [operations guide](../../../../../tooling/agent-experiments/OPERATIONS.md).

Question: when does remembering unresolved evidence and protecting a future check help, and when does it delay an urgent decision? Primary B2 reserve versus B1 memory; secondary B1 versus B0 bounded always-check. [Plan](PLAN.md), [amendment](AMENDMENT-01.md), [ready package](READY.md), [previous cohort](../rd4/REPORT.md).

| Gate | Status | Evidence and next action |
| --- | --- | --- |
| G0 question/prior art | scoped exploratory | RD4 post-mortems, failure decomposition, existing source/Twitter map, Hay/Tan primary references. No completed novelty survey or accepted hypothesis claimed. |
| G1 design before code | complete | Amendment published at `10e6b4d775c8409c1a9817ad633f0f6f84ae3c40` before code. All H5 mechanisms now share one domain. |
| G2 instrument | offline checks passed | 61 development tests; state/resource separation, frozen input adapter, policies, transport and replay. [Validation](validation/VALIDATION.json). |
| G3 admission | prepared; runtime evidence pending | Frozen packet manifest, registration file and pre-assessments. Fresh public hub/page verification, exclusive approved fleet/account claim, route, source/runtime and original budget receipts required immediately before dispatch. |
| G4 qualification | not run | Q5 maximum 24 calls; 12/12 valid/correct cards and 24/24 valid completed requests required. Old Q4 does not qualify this source. |
| G5 closeout | no new run | Zero native calls; no fleet host or worker allocated. |

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

Next authorized execution sequence: register/verify immutable plan and Q5 TLDR; obtain a fresh dedicated allocation from Dmarz's authorized private fleet; verify actual workload/account, source, original ledger, route and runtime; issue fresh private receipts; run Q5 once and assess it before H5. No idle host is held. Researcher sign-off is not required by owner direction. Better native semantic accuracy, independent semantics and adaptive arrival timing remain untested.

Owner decision boundary: the refreshed [agent protocol](../../../../../AGENTS.md) requires approval of the updated next-run plan before allocation or launch. The concrete [proposal](spec/next-run-plan.json) and [evidence-linked RD4 quality review](reviews/RD4-QUALITY-REVIEW.json) are ready for that decision. Existing budget approval remains valid; the disabled template does not invent plan approval.

Operator closeout hook after each stopped native attempt: `python3 scripts/experiment.py finalize right-dissenter --attempt <unique-rd5-attempt> --results <saved-results> --outcome <completed|failed|ambiguous> --worker-stopped`. This generates an operational handoff only; complete the scientific review separately and retain reporting/cost status.
