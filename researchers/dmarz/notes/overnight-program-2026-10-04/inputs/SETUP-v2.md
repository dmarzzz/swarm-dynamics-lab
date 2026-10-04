# Setup record: 200-agent overnight program, proposed v2

Status: prospective plan. No experiment implementation, qualification, paid calls, server claims or session loops started by this task. This revision supersedes the v1 small-world design; the immutable v1 artifacts and inputs remain available.

## Owner, scope and question

Owner: dmarz. Target: 200 persistent model-backed identities in one shared world, 100 per host, managed by five Claude Code sessions. Ten logical communities of twenty are each split evenly between hosts. Candidate hosts sim-dmarz-2 and sim-dmarz-3 were online/unclaimed at the approximately 08:49 UTC audit; refresh claims before use. Exact IP constraint remains unresolved, so no extra quota is assumed from the second host.

Question: in this one world, how does a source-aware continuation differ from an ordinary continuation after a shared checkpoint? This is a descriptive case study. The interacting agents and communities are not independent worlds. No earlier 48-root uncertainty or efficacy threshold carries forward.

## Gates and next work

| Gate | Status | Required next step |
|---|---|---|
| Research and current directives | Pending | Verify applicable runbook/research gates for this named successor; do not inherit prior waivers automatically |
| Evaluator | Pending | Freeze a checkable task and independent scorer by T+30; the other task's evaluation shortlist is not an integration receipt |
| Instrument | Unbuilt | Implement bounded communication, checkpoint restoration and cross-host reservation authority by T+60 |
| Admission | Pending | Pin model/provider, available cumulative budget, actual quotas, exact manifest and current two-host claims |
| Qualification | Unrun | At most 400 small-fixture calls plus one 200-call max-context operational check; pass by T+90 or fall back |
| Main collection | Unrun | 1,000 prefix + 3,000 ordinary + 3,000 source-aware calls, sequential branches |
| Closeout | Future | Stop dispatch T+300, reconcile T+330, deliver T+420 |

## Manifest and limits

- 200 identities, twenty scientific rounds per branch with five shared prefix rounds; 35 executed rounds total. At most 200 active identities, not 400 simultaneous fork agents.
- Four local and one cross-community neighbor; previous-round messages only. Input cap 8,000 total tokens, billed output cap 1,000, public message cap 160 and retained private summary cap 800. Solvability under these ceilings must be demonstrated.
- Initial concurrency two requests per host/four globally; ceiling four per host/eight globally only within verified limits. One authority coordinates global rate, budget and unique assignment reservations.
- Main ceiling 7,000 calls; qualification ceiling 600; total 7,600. Proposed $25 cap requires verified remaining owner authority. No funds allocated here.
- A failed full-scale qualification ends launch; the cap contains no second scale attempt. Measured maximum-context round latency and queue tails must support the schedule; nominal 0.75 calls/s alone is insufficient evidence.
- Full checkpoint equality includes world, all agent state, random streams, messages and schedule. Branch-qualified call IDs prevent cache collisions. Ordinary-first order and model randomness remain limitations.

## Implementation and artifact index

Current plan: program.json and program.html. Generator: src/build_program_200.py; it uses the historical display renderer in src/build_program.py. Rebuild the plan with the new generator only; neither is an experiment launcher. Original v1 data/setup are frozen in inputs/program-v1.json and inputs/SETUP-v1.md.

Exact task IDs, source catalog, prompts, scorer, graph, manifests, provider settings, runtime hashes, cross-host authority and native launcher remain future implementation. A Codex subagent reviewed v2's arithmetic and integrity requirements. This same-researcher review is not an independent implementation audit or different-researcher approval.

## Fallback and handoff

Retain the timestamped 21-entry evidence review. If readiness fails, produce the saved-data explorer and audit, preserving all qualification/operational failures. Do not represent a partial or mocked run as a successful 200-agent experiment. Future execution records every assignment, actual cost, uncertainty, failure and post-mortem. This record is an operational design, not a measured result.
