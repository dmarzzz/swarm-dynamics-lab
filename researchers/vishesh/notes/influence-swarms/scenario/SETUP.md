# Experiment setup record: influence-swarms / iteration 3

Exploratory diagnostic, owner/operator vishesh/codex-experiments, 2026-10-04. Follow the [setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). This is a bounded repair study, not formal hypothesis acceptance.

Question: does targeted candidate approval checking outperform an equally budgeted general second look? Decision: retain or reject that proposed workflow repair. [Plan](ITERATION-03.md); previous [Q4](reviews/native-Q4-01-post.md) and [D1](reviews/native-D1-01-post.md) post-mortems. Independent reviewer dmarz/inbox-design-feedback: [Q4 answerability PASS](../../../../dmarz/notes/inbox-reviews-2026-10-04/influence-q4-review.md). Owner's single-review rule applies; this is not an audit of the new diagnostic cases.

| Gate | Status | Evidence / next action |
|---|---|---|
| G0 | diagnostic-only | Existing reviewed procurement scope; main influence claim unqualified. |
| G1 | pass | ITERATION-03.md written before implementation. |
| G2 | pass | 27 tests; scripted-D2-02 30/30; deadline fault 30 invalid/zero dispatch; fixture grid reviewed. |
| G3 | conditional-ready | PR134 exclusive sim-test-01; unreplenished grant has USD7.226604 remaining; entrypoint verifies >=USD5.972 and exact published plan before dispatch. Runtime receipt/manifest bind source and quota. |
| G4 | fail for S1 | Q4 10/12; D2 cannot unlock S1. |
| G5 | pending | Reconcile all 30 assignments, complete post-mortem, upload and release. |

Six fresh authored dossiers, five workflow outcomes each. Two review interventions share the same prior evidence but fresh isolated calls; six case clusters. Existing provider and model-config-native.json, no credential values. Credentials consumed from approved Keychain alias swarm-lab-anthropic only by the launch process. No evaluator input to actors. Raw traces and frozen manifest required. Visualization and stop rules are in ITERATION-03.md. Operator fills admission receipt and current pre-run assessment before dispatch; no machine is held while required authority is missing.
