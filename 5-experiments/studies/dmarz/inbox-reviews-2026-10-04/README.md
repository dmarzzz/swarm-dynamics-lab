# Inbox reviews — 2026-10-04

Reviewer: dmarz/inbox-design-feedback. User request: “review it all”. All reviews are completed; pass/revise is specific to the stated review scope and is not automatic launch permission.

| Item | Verdict | Main feedback |
| --- | --- | --- |
| [LLM-agent-swarms survey](../../../../2-surveys/reviews/llm-agent-swarms--dmarz-inbox.md) | REVISE | Separate qualitative evidence from replication of a scaling law; restore attention-theorem assumptions; reconcile Flag Game catalogue numbers. |
| [Influence Q4 dossiers](influence-q4-review.md) | PASS, case review | Four independent answers agree. The chair contrast removes ballot fields, not recommendations embedded in shared prose. |
| [Right Dissenter RD-1](right-dissenter-review.md) | REVISE | Alias multiplicity can consume checks; supported repeats restore old votes. Split reserved qualification fixtures out of ordinary offline discovery. |
| [Optimal swarm-size Q-A](swarm-size-review.md) | PASS, offline package only | Earlier E1–E3 fixes verified. Runtime/reporting preflight remains; chain scheduling needs resolution before Q-B. |

Validation: 24 Influence tests, 49 Dissenter tests, and 31 swarm-size tests on Python 3.12 pass. The Python 3.9 swarm-size run had one mocked HTTPError cleanup failure; its log is retained. Independent scripts check arithmetic, actor inputs, evidence duplicates, scoring mutations and concurrent reservations. Zero model calls or spending. The full Dissenter author suite constructs reserved Q0 fixtures internally; this exposure is disclosed rather than claiming a fully blind audit. No confirmatory holdout or transfer corpus was inspected.

## V3 follow-up

Re-scored the saved v3-q0-a1 swarm episodes with the existing reviewer-recommended script. All 48 world hashes and fully valid vote metrics agree with the pinned record: zero invalid final ballots and zero changed vote scores. Both quorum and unidentified schemes reproduce those vote metrics. [Full secondary analysis](v3-rescore.json) includes the original episode-file hash. This does not rescue the failed clean-competence qualification or change the original post-mortem.

F1/F2 repairs are already in 6563e28. The owner still needs to link this rescore beside the original post-mortem and pin that repair or later equivalent hashes in any next launch manifest. The review did not create or start a successor run.

## Evidence and ownership

[Package source receipt](package-receipt.json) and [survey receipt](survey-receipt.json) pin reviewed inputs. Scripts and compact outputs here are reviewer-owned internal audit records. Source packages were not edited. Findings were routed to the authors through their inboxes; the original review records remain intact.
