# Experiment setup record: active-evidence-swarm / revision 2

- Owner: dmarz. Status: **evaluation unresolved; scale recommendation withdrawn**, 2026-10-04.
- Current decision: whether a defensible evaluation exists for this candidate question. There is no recommended experiment scale, model or server layout.
- Runbook: [experiment setup](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).
- Operations: [operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).
- Current assessment: [proposal.json](proposal.json); rendering source: [build_review.py](src/build_review.py).

## Owner correction and disposition

> if we dont have a good eval then we shouldnt even do thiss, please dont take evals so laxily. we cant plan really without knowing what the eval will be

The previous recommendation put models, costs, agent counts and servers ahead of a defined and validated measurement. That was a design error. The phrase “fraction of critical decisions correctly resolved” does not specify the decision, denominator, correctness rule, answerability, or value of abstention versus error. A deterministic scorer would not by itself establish that the task measures useful coordination.

The 64-agent, 192-world, three-server recommendation, five-point useful-effect target and approximately $250 envelope are withdrawn. Revision 1 remains historical; its assumptions are retained under `withdrawnProposal` in proposal.json and in the immutable v1 artifact. None is an active allocation or launch plan.

## Gates

| Gate | Status | Evidence and next action |
|---|---|---|
| G0 Question and applicable research gates | Unresolved | Define the target decision and task population. Earlier portfolio synthesis and adjacent abstracts do not establish evaluation validity or formal acceptance. |
| G1 Prospective design | Blocked: evaluation undefined | Specify concrete cases, actor information, justified reference answers, scoring and denominators, meaningful controls and generalization scope. Assess whether the proposed question can be evaluated usefully at all. |
| G2 Instrument | Unstarted | No simulator, experimental agent, evaluator or model adapter exists. Reporting code is not an experimental instrument. |
| G3 Admission | Unstarted | No immutable run plan, study allocation, provider qualification, claim or deployment. |
| G4 Qualification | Unstarted | No model outputs. A small paid screen is not the next step while evaluation validity remains unresolved. |
| G5 Reconciliation and closeout | No attempt | No experimental spend or active resources. |

## Evidence required before an experiment recommendation

1. A target use case and exact decision contract, with worked cases, justified reference answers and adjudication of ambiguity. Specify score, denominator, time window, errors, abstention, invalid responses and missing outcomes.
2. An observability account showing what actors can learn and when an answer is supported. Distinguish justified correctness from lucky guesses and justified uncertainty from avoidable failure.
3. A task sampling rationale and structurally different challenges, with development/evaluation separation and audits for repeated templates, leakage and shortcuts. Fresh seeds alone are insufficient.
4. Fair information and resource contracts, strong single-controller and simple search/deduplication baselines, and controls that expose trivial or architecture-favoring tasks. Any practical benefit threshold needs a decision-based justification.
5. A defensible attacker model and pairing scheme, plus case and trace review that challenges whether scoring reflects the intended failures. Scorer arithmetic checks and model schema compliance remain separate from evaluation validity.

All five are unresolved. This list is a requirements assessment, not a completed evaluation specification or passing review. A same-session subagent critique helped identify gaps; it does not satisfy independent researcher review.

## Next action and handoff

Produce an evaluation specification with worked cases and a validity assessment. Continue this direction only if that assessment supports a meaningful experiment; otherwise discard it or select an existing defensible evaluation. Do not translate the old arithmetic into a model screen, agent count, sample size or fleet plan.

There is no attempt ID, dispatch command or reserved holdout. No key value, account identifier or private inventory is recorded; the supplied credential was neither used nor stored. The shared dmarz budget is not allocated to this candidate, and this correction authorizes no run.
