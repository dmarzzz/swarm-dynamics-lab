# Setup record: right-dissenter / RD-3

Operator vishesh/codex-decision-models. This index is retrospective for Q0 and prospective for Q1; it does not replace the original timestamped plan and receipts. [Required setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

Question: can evidence-backed dissent earn a bounded check and recover after withdrawal? Exploratory instrument; formal survey/hypothesis/independent review incomplete. [Sources](SOURCES.md), [RD-2](LIVE-PLAN.md), [Q1 amendment](Q1-PLAN.md), [Q0 post-mortem](reviews/Q0-A1-POST.md).

| Gate | Status / evidence | Next action |
|---|---|---|
| G0 research | Owner-authorized exploratory work; formal review pending | S2 stays closed |
| G1 plan | RD-2 prospective for Q0; Q1-PLAN prospective for repair | Publish immutable Q1 URL |
| G2 instrument | 50 checks for Q0; Q1 tests pending | Validate paired inputs and controls |
| G3 admission | AUTHORIZATION.json approved; Q0-LAUNCH.json historical | Bind Q1 source, public receipt and existing exclusive claim |
| G4 qualification | Q0 failed 12/18 | Q1 diagnostic, unchanged clean threshold plus uncertainty controls |
| G5 closeout | Q0 all 18 retained, post-mortem written | Verify public artifacts, then close Q1 and S1 separately |

Study artifacts remain under this directory and public Swarm Live. Q0 source and model versions, allocation, executable command and output are in results/q0-a1/configuration.json and manifest.json. Keys are locally consumed through approved protected aliases; never in published artifacts. The same ledger enforces $1 API/500 calls across attempts; host cap is $1/six hours. Deployment uses the original owner infrastructure state and may modify only this host. Workers stop and claim releases only after durable upload, followed by authorized teardown.

Issue ledger: Q0 sufficient-evidence ambiguity is suspected, not proven; Q1 paired intervention and six uncertainty controls test it. Missing SETUP index at Q0 is a process deviation, documented here retrospectively. The original public-plan preflight did pass. Current action: implement and qualify RD-3 within the approved cap after prospective publication.
