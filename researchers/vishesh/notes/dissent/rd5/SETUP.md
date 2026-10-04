# Right Dissenter RD5 setup record

**RD5 is complete and scientifically reviewed: Q5 passed; H5 returned a valid adverse result. See [current status](RUN-STATUS.md) and [report](REPORT.md). This remains the authoritative Right Dissenter setup record.** Owner/operator/assessor: vishesh/codex-decision-models. Exploratory scope, tagged dissent and decision models. Follow the [setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [operations guide](../../../../../tooling/agent-experiments/OPERATIONS.md).

Question: when does remembering unresolved evidence and protecting a future check help, and when does it delay an urgent decision? Primary B2 reserve versus B1 memory; secondary B1 versus B0 bounded always-check. [Plan](PLAN.md), [amendment](AMENDMENT-01.md), [ready package](READY.md), [previous cohort](../rd4/REPORT.md).

| Gate | Status | Evidence and next action |
| --- | --- | --- |
| G0 question/prior art | scoped exploratory | RD4 post-mortems, failure decomposition, existing source/Twitter map, Hay/Tan primary references. No completed novelty survey or accepted hypothesis claimed. |
| G1 design before code | complete | Amendment published at `10e6b4d775c8409c1a9817ad633f0f6f84ae3c40` before code. All H5 mechanisms now share one domain. |
| G2 instrument | offline checks passed | 61 development tests; state/resource separation, frozen input adapter, policies, transport and replay. [Validation](validation/VALIDATION.json). |
| G3 admission | completed for both stages | Scoped direct directive, central fence, current approved-account claim, native source/route/plan/ledger receipts and real relay health verified before each dispatch. |
| G4 qualification | native Q5-A2 passed | 24/24valid complete,12/12correct cards and all6uncertainty controls; source-bound seven-file audit and post-mortem complete. |
| G5 closeout | both stages reviewed; allocation released | Complete native records, post-mortems, eleven-dimension assessments, exact replay, verified artifacts and worker/relay shutdown. Valid adverse H5 result retained; no successor scheduled. |

## Definitions and access

H5: six authored roots (three mechanisms × stop/resume), three policies, four epochs: 72 dependent outcomes, 24 per arm. Q5: 12 disjoint authored packets in two representations. Development ID 51901; Q5 52000-series; H5 53000-series; ordering seed 51004. IDs do not establish semantic independence. Ordinary tests never construct Q5; explicit preparation does.

Actors receive only current task, supplied ballots, own historical/current state and acquired source text/card. No evaluator truth, arm, mechanism, future frames, peer results or operating-assistant context enters the request. Each arm starts fresh; no cross-arm answer cache. The finite parser preserves text, matched spans and unknown/conflicting fields. Jev resolves actions; no oracle substitute.

The canonical ledger is now488lifetime calls, including all60approved RD5calls. Committed API exposure is USD 0.022699069, including historical USD0.004032unresolved. Original USD 1 API/USD1infrastructure authority remains unchanged; the conservative full-allocation combined envelope stays below USD0.821. Twelve historical unallocated slots are not launch authority. See [final accounting](results/h5-a1/resources.json).

## Operations

- Offline: `python3 -m unittest discover -s researchers/vishesh/notes/dissent/rd5/tests -v`.
- Prepare: `src/rd5_cli.py prepare`; committed source only, no dispatch. Public hashes in [preparation manifest](spec/preparation-manifest.json).
- Run: `src/rd5_supervise.py`; strict native admission in both relay and worker, actual remote health probe, supervised transport. See READY.md.
- Report: `src/rd5_cli.py report --results <saved directory>`; no model calls.
- Resume: deliberately unsupported. Preserve partials/reservations; separately assess any never-started trajectory continuation. Never delete identities to retry.
- Shared operations CLI: this study uses its documented manual workflow; no new `scripts/experiment.py` adapter is claimed.

No next execution is scheduled. The approved Q5/H5 sequence is complete. Read [the native post-mortem](reviews/H5-A1-POST.md) and [candidate next question](NEXT-QUESTION.md) before any separate proposal; a changed scientific scope needs its corresponding owner decision.

Owner decision boundary: the refreshed [agent protocol](../../../../../AGENTS.md) requires approval of the updated next-run plan before allocation or launch. The concrete [proposal](spec/next-run-plan.json) and [evidence-linked RD4 quality review](reviews/RD4-QUALITY-REVIEW.json) are covered by the recorded approval in [RUN-STATUS.md](RUN-STATUS.md) for unchanged Q5/conditional H5. Do not request that approval again; materially different scope requires a new decision. Existing budget approval remains valid; the disabled template does not invent plan approval.

Operator closeout hook after each stopped native attempt: `python3 scripts/experiment.py finalize right-dissenter --attempt <unique-rd5-attempt> --results <saved-results> --outcome <completed|failed|ambiguous> --worker-stopped`. This generates an operational handoff only; complete the scientific review separately and retain reporting/cost status.


## RD6 reopening revision and native closeout

RD5 remains a completed, reviewed adverse result. The separate [RD6 diagnostic](../reopening/README.md) preserves that scientific ancestor and asks about contextual interpretation. Its 18 Q0 / conditional 144 D0 scope and 650 lifetime ceiling were approved under the unchanged USD 2 split cap. The plan was public before implementation.

Q0-A1 stopped before any model request; its [post-mortem](../reopening/reviews/Q0-A1-POST.md), original ledger fence and allocation estimates remain intact. The owner directly approved its narrowly defined one-time zero-dispatch replacement. Fresh account, exclusive allocation, public plan, source/runtime, budget and exact receipt admission passed for Q0-A2 at source `ab7a92c944f882e85c70abd28feea87602bbd324`.

**Q0-A2 completed 18 valid native requests and failed qualification at 15/18. D0 was not run.** All clean controls scored 12/12 and conflicts 3/3; expired evidence scored 0/3. Read the [result](../reopening/REPORT.md), [post-mortem](../reopening/reviews/Q0-A2-POST.md), [eleven-dimension assessment](../reopening/reviews/Q0-A2-QUALITY.json) and [resources](../reopening/results/q0-a2/resources.json). These are authored development controls, not a causal context comparison or field-rate estimate.

Current gates: G0 scoped exploratory; G1 prospectively published; G2 passed 88 offline checks locally/remotely; G3 admitted; G4 qualification failed; G5 operational and scientific closeout complete; G6 **FINISH / PARK**. The closeout wrapper path defect was corrected offline and the saved-data finalize hook verified. Researcher review was not required and is not represented as independent validation.

The sole original ledger has 506 calls and USD 0.023434447 committed API, retaining historical uncertainty. Combined committed API and infrastructure allocation estimate is USD 0.778524856 within the original split cap; estimates are not invoices. Worker and relay stopped and the exclusive claim was released. No D0 calls, retry, new allowance or automatic successor occurred.

The actual latest operational handoff is `a5493a765b57b14270a6e3a4ea893162fe5809e5cbcf6f12bc79fbf4c90316a9`; its owning scientific assessment is separate. This file remains the single authoritative setup. Registry entries are navigation, not live admission. Preserve the valid negative qualification and do not rerun this consumed attempt or substitute an older handoff.
