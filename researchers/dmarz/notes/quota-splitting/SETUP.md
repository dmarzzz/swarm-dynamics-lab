# Experiment setup record: quota-splitting v1

Status: plan written, package not built yet. This record follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. Nothing has run on a server and no model call has been made.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-quota (Claude Code, offline on dmarz's Mac), working for the pipeline lead dmarz/pipeline. Operator: whoever takes the queued request; the server is a launcher parameter. Review independence: none. As relayed to this builder by the pipeline lead dmarz/pipeline on 2026-10-04: dmarz did not name this study. He told the fleet monitor to keep five experiments running by building a pipeline of prepared experiments, to use Opus for everything, and not to gate on cost; the fleet monitor chose this study from his backlog (agent-budgets hunch B2) under that delegation. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed.
- Question: when a quota is enforced per identity and an agent can spawn subagents, does an Opus 5.5 agent create more identities than the task needs and take more than its share of a shared pool, and do a lineage quota or a spawn fee remove that? Primary contrast: subagents created in `B` minus `N` at pressure 3.0, paired by root. Claim boundary: abstract units stated in a prompt, scripted subagents and scripted other teams, one model and effort level, exploratory, no novelty claim.
- Research status: hunch-level exploratory study in researcher notes (hunch B2 of [the agent-budgets note](../agent-budgets-hunches.md)). The `agent-budgets` survey has not passed the prior-art gate; there is no hypothesis file; S2 is disabled.
- Prior art named by the hunch: false-name manipulation theory [[yokoo-2004-effect]] [[yokoo-2007-making]] [[hu-2026-dissociative]]; over-spawning by lead agents without a quota incentive [[anthropic-2025-how]]. This builder did not run a new search.
- Previous studies and lessons used: no earlier attempt of this study. The chain, ledger, adapter, rehearsal and manifest machinery is taken from [sybil-split-opus](../sybil-split-opus/README.md) and [sybil-scarcity-opus](../sybil-scarcity-opus/README.md) and adapted to multi-turn episodes. From [the pipeline lessons](../pipeline/LESSONS.md): caps and timeouts sized for the whole chain before qualification (item 1); the Opus 5.5 request shape and a one-call probe (item 3); read failing answers before changing anything (item 6); a written near-miss rule and what a 14-of-16 gate misclassifies (item 7); an upper bound on the control as well as a lower one (item 9).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | README and preregistration, 2026-10-04T09:55Z, dmarz/pipeline-quota | Formal survey and hypothesis gates not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, preregistration, design.yaml, experiment.yaml and this record are committed before any study code exists | none |
| G2 Instrument and offline checks | pending | not built | implement; selftest, offline S0, rehearsal, manifest check |
| G3 Current attempt admission | pending | none | pre-run review, READY.yaml, fleet monitor's same-researcher check, run-queue request |
| G4 Qualification before scientific escalation | pending | P0 and Q0 are stages of the chain; the software gate admits S1 only after Q0 passes at the same source hash | run |
| G5 Reconciliation and closeout | pending | none | run |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml); history in git.
- Independent units: 24 roots for S1, 8 for Q0, 2 for engineering. Per S1 root: 8 conditions × 3 pressures = 24 paired episodes of at most 6 model calls.
- Sample size: 24 roots is the size the source brief asks for. Not powered for small differences; the useful difference is 1 identity and intervals are descriptive.
- Splits: engineering 9281-9282 (also the probe root 9281), qualification 9271-9278, comparison 9245-9268. Holdout 10000-19999 unopened.
- Agent definition: one lead agent per episode; each turn is one stateless call whose input is the fixed system prompt of the condition and the current state; subagents and the three other teams are scripts. Prompt, schema and adapter will be in `src/provider.py`.
- Versions: `claude-opus-5-5`, effort medium; requirements.txt pinned; the runtime source hash will cover design.yaml, experiment.yaml, requirements.txt and `src/*.py`.

### Root-range scan (2026-10-04T09:40Z)

Every text file under `researchers/`, `experiments/`, `hypotheses/`, `tooling/`, `templates/`, `src/`, `scripts/`, `tasks/`, `synthesis/`, `surveys/` and `reviews/` with extension yaml, yml, json, md, py, txt, csv or sh (files over 5 MB skipped; 3,550 files) was searched for every four-digit number as a standalone token. A range was accepted only if none of its numbers occurs anywhere.

- Chosen ranges, zero occurrences each: 9245-9268 (comparison), 9271-9278 (qualification), 9281-9282 (engineering). They lie inside the unused run 9245-9289.
- Ranges used by other dmarz studies built tonight, for reference: 4821-4836, 4919-4934, 5139-5148, 8233-8256, 8351-8374 (sybil-split-opus), 7790-7907 (sybil-scarcity-opus), 8400 upward (false-alarm-cascade). No overlap.

## Current attempt admission

Not prepared yet. Commands, manifest and the admission record are added when the package is built.

## Attempt and repair history

None.

## Closeout

Nothing has run.
