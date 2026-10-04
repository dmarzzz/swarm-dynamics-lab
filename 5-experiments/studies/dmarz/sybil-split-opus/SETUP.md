# Experiment setup record: sybil-split-opus v1

Status: prepared, not launched. This record follows [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. Nothing has run on a server and no model call has been made.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-split (Claude Code, offline on dmarz's Mac), working for the pipeline lead dmarz/pipeline. Operator: whoever takes the queued request; the server is a launcher parameter. Review independence: none. As relayed to this builder by the pipeline lead dmarz/pipeline from dmarz/fleet-monitor on 2026-10-04: dmarz did not name this study. He told the fleet monitor to keep five experiments running by building a pipeline of prepared experiments, to use Opus for everything, and not to gate on cost; the fleet monitor chose this study from his backlog (successor 3 of the next-experiments note) under that delegation and told him so. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check of this package is a same-researcher check and nothing more; the run is not independently reviewed. Nothing here is an independent review.
- Question: does splitting one attacker's unchanged resources across 1, 3, 9 or 27 identities increase harmful influence, and which admission policy preserves legitimate specialist value? Primary contrast: (wrong answers at k = 27 minus k = 1 under `degree`) minus (the same under `coverage`), informative checks, 12 checks, paired by root, two graph families weighted equally. Claim boundary: simulated identities and checks, one population size, exploratory, no superiority claim.
- Research status: hunch-level exploratory study in researcher notes. Survey and hypothesis gates are not met; S2 is disabled.
- Prior art and gates: the idea is successor 3 of [the next-experiments note](../next-experiments-2026-10-04/README.md). No survey gate was run for it. A faithful published-defense comparator is out of scope and listed as a limit.
- Previous studies and lessons used: [sybil-scale-api results](../sybil-scale-api/RESULTS.md) (random checking matched coverage at equal budget; plurality is a strong comparator; attacker resources grew with population, so it could not answer this question), its [prospective amendment](../sybil-scale-api/README.md) (central controls: equal-budget random and same-packet plurality; counterbalance the fabricated direction; qualify each packet-load regime), [sybil-scale-xl A1](../sybil-scale-xl/AMENDMENT-A1.md) (Opus request shape, settled-cost ledger, 48 input tokens per report row) and [the pipeline lessons](../pipeline/LESSONS.md) items 1 to 3 (size caps and timeouts before qualification; settled-cost accounting; drop redacted thinking blocks).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | README and preregistration, 2026-10-04T08:35Z, dmarz/pipeline-split | Formal survey and hypothesis gates not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, preregistration, design.yaml, experiment.yaml and this record committed (f3e294c5) before the study code (88fcf92a, 0b8a444a); the simulator existed only as uncommitted working files used for the calibration below. One plan change after that and before any run: qualification fixtures corroborate every present fact with two single-row honest identities (88fcf92a); the retry rule and the dollar-cap arithmetic were in the first plan commit | none |
| G2 Instrument and offline checks | pass (offline, builder's own checks) | 2026-10-04T09:18Z, dmarz/pipeline-split, on commit 0b8a444a (source hash 95889bea...): selftest 55 tests OK; offline S0 1,853/1,853 valid, 0 violations, 0 calls; manifest check current (digest 2a4b2166...); rehearsal against a throwaway local hub with a stubbed model endpoint passes both chains; simulator output identical under Python 3.9, 3.12 and 3.14; details in [the pre-run review](reviews/chain-001-pre.md) | the full suite has not run under Python 3.12 with numpy and Pillow; the launcher's setup step does that on the server |
| G3 Current attempt admission | pass | [reviews/chain-001-pre.md](reviews/chain-001-pre.md); claim `dmarz-sybil-split-opus` on sim-dmarz-13 (agentops #253) by dmarz/orchestrator-2; `run-ready-chain.py setup` 55/55 selftests, source hash 95889bea… matched, 2026-10-04T09:34Z; chain started 10:11:59Z | none |
| G4 Qualification before scientific escalation | pass | S0 1,853/1,853 valid, 0 invariant violations; P0 1/1 (parsed, model id matched, end_turn); Q0 60/60, every shape at 1.0; software gate admitted S1 at the same source hash, 2026-10-04T10:14Z | none |
| G5 Reconciliation and closeout | pass | 2,749/2,749 valid, USD 45.38592; `verify` ok for every stage; [RESULTS.md](RESULTS.md), [reviews/chain-001-post.md](reviews/chain-001-post.md); claim released 10:51:57Z; dmarz/orchestrator-2, 2026-10-04T11:00Z | none |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml); history in git.
- Independent units: 24 roots per graph family for S1 (48 roots), 5 per family for Q0, 16 per family for engineering. Per root: 2 check strengths × 4 identity counts × 7 policy cells = 56 paired assignments.
- Sample size: 24 roots per family follows the source note's proposal for development roots. Not powered for small differences; the useful difference is 10 points and intervals are descriptive.
- Splits: engineering ring 4919-4934, community 4821-4836; qualification ring 5139-5143, community 5144-5148; comparison ring 8233-8256, community 8351-8374; probe: engineering root 4919. Holdout 10000-19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; prompt and schema in `src/provider.py`.
- Versions: `claude-opus-5-5`, effort low; requirements.txt pinned; the runtime source hash covers design.yaml, experiment.yaml, requirements.txt and `src/*.py`.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md), mapping v1.
- Offline checks: `src/selftest.py` (55 tests: graph generators and parent equality, structural invariants at every identity allocation and a tampered-world control, blind packets and policies, fixtures and gates, request shape, thinking blocks, refusal, transport retry rule, ledger caps, worker failure accounting, coordinator gates, chain stop and projection gate, analysis sign, weighting and missing-outcome bounds, frames and replay).
- Launcher gate integration: `coordinator.check` and `coordinator.enqueue` are the only way a stage is queued; `worker.py` has no hub entry point of its own (its command line runs the scripted stage offline only); `chain.py` executes only the run it queued itself, at attempt 1.

### Root-range scan (2026-10-04T08:20Z)

Every text file under `researchers/`, `experiments/`, `hypotheses/`, `tooling/`, `templates/`, `src/`, `scripts/`, `tasks/`, `synthesis/`, `surveys/` and `reviews/` with extension yaml, yml, json, md, py, txt, csv or sh (files over 5 MB skipped) was searched for every four-digit number as a standalone token. A range was accepted only if none of its numbers occurs anywhere.

- The draft ranges were rejected. 8200-8223 collides with seeds of `researchers/vishesh/notes/adaptive-quorum-v2/repair-v3` (8200-8212) and `healing-helping-hands` (8201-8203); 5100-5104 and 4950-4965 contain numbers that occur in other studies' records.
- Chosen ranges, zero occurrences each: 4821-4836, 4919-4934, 5139-5148, 8233-8256, 8351-8374.
- Ranges used by the dmarz Sybil family, for reference: 4900-4901, 5000-5003, 6000-6023 (scale), 6800-6801, 6900-6903, 7000-7023 (budget), 6900-6901, 7000-7005, 7100-7123 (newcomer), 7790-7791, 7800-7823, 7900-7907 (scarcity). No overlap.
- The scan was repeated at 09:05Z and at the pinned commit after pulling `main`: still no occurrence outside this directory.

### Engineering calibration of the fixed resources (2026-10-04, no model call)

The source note fixes the identity counts and asks for fixed attacker resources; the amounts and the attachment rule had to be chosen. They were chosen on the engineering roots only, with the plurality rule, using one criterion stated before looking: the two ends of the primary contrast (k = 1 and k = 27 under `degree` and `coverage`, informative checks, 12 checks) must not sit at a floor or ceiling by construction, that is, the attacker must be admitted in some engineering roots at both ends in both families.

Two exploratory passes in a scratch directory (roots 4950-4965, not used anywhere in this study) compared, without internal links, 27, 54 and 81 attachment edges, and, with internal links, 27 and 9 attachment edges. Without internal links a 27-way split is seated in almost no root under `degree` at 12 checks with 27 edges and in no root under `coverage` with 27, 54 or 81 edges, so that end of the primary is fixed at zero and the contrast only measures how often the single hub passes its check. The frozen design therefore uses 27 units with internal links. The reasons are the criterion above and the threat model (links among one party's identities cost nothing; the parent's attacker was a ring of 27), not the sign of the contrast.

Reproduce with `python3 src/analyze.py calibration` and `python3 src/analyze.py calibration --internal-links none`. Each cell is the mean over 16 engineering roots; columns are k = 1, 3, 9, 27.

Frozen design (internal links `ring2`), informative checks (attacker pass 0.1):

| Family | Policy, checks | Plurality wrong-answer rate | Rare-skill accuracy | Attacker identities admitted | Honest specialists retained |
|---|---|---|---|---|---|
| ring | no_verification, 0 | 1.00 1.00 0.83 0.65 | 0.00 0.00 0.17 0.31 | 1.00 3.00 7.38 7.88 | 0.12 0.11 0.09 0.10 |
| ring | degree, 4 | 0.12 0.04 1.00 0.65 | 0.35 0.38 0.00 0.06 | 0.12 0.25 5.31 4.88 | 0.05 0.11 0.03 0.03 |
| ring | degree, 12 | 0.12 0.19 1.00 0.54 | 0.27 0.29 0.00 0.00 | 0.12 0.25 5.06 2.19 | 0.02 0.03 0.00 0.00 |
| ring | random, 4 | 0.83 0.96 0.33 0.17 | 0.12 0.02 0.56 0.71 | 0.88 2.75 3.75 3.75 | 0.25 0.24 0.23 0.21 |
| ring | random, 12 | 0.62 0.62 0.04 0.00 | 0.29 0.27 0.94 1.00 | 0.81 2.62 2.06 2.31 | 0.38 0.37 0.37 0.36 |
| ring | coverage, 4 | 0.12 0.31 0.96 0.48 | 0.25 0.27 0.00 0.12 | 0.12 0.50 3.69 2.31 | 0.02 0.06 0.02 0.02 |
| ring | coverage, 12 | 0.06 0.00 0.21 0.00 | 0.92 0.96 0.67 0.98 | 0.12 0.44 4.00 2.06 | 0.44 0.35 0.31 0.27 |
| community | no_verification, 0 | 1.00 1.00 0.85 0.10 | 0.00 0.00 0.08 0.17 | 1.00 2.75 2.12 0.38 | 0.02 0.02 0.02 0.02 |
| community | degree, 4 | 0.00 0.00 1.00 0.60 | 0.35 0.19 0.00 0.10 | 0.00 0.00 3.81 3.00 | 0.03 0.02 0.02 0.02 |
| community | degree, 12 | 0.00 0.00 1.00 0.46 | 0.29 0.23 0.00 0.00 | 0.00 0.00 4.19 1.38 | 0.02 0.02 0.00 0.00 |
| community | random, 4 | 0.85 0.85 0.25 0.06 | 0.06 0.06 0.52 0.83 | 1.00 2.88 3.00 1.88 | 0.26 0.25 0.24 0.25 |
| community | random, 12 | 0.73 0.62 0.06 0.02 | 0.23 0.31 0.83 0.94 | 0.94 2.62 2.50 2.44 | 0.36 0.36 0.34 0.35 |
| community | coverage, 4 | 0.00 0.06 0.96 0.21 | 0.19 0.21 0.00 0.15 | 0.00 0.06 2.19 1.12 | 0.01 0.02 0.01 0.02 |
| community | coverage, 12 | 0.00 0.00 0.33 0.12 | 1.00 0.98 0.54 0.81 | 0.00 0.06 3.38 2.38 | 0.42 0.28 0.20 0.19 |

Unreliable checks (attacker pass 0.9), the cells that differ most:

| Family | Policy, checks | Plurality wrong-answer rate | Attacker identities admitted |
|---|---|---|---|
| ring | degree, 12 | 1.00 1.00 1.00 0.54 | 1.00 2.69 5.06 2.19 |
| ring | random, 12 | 0.81 0.73 0.25 0.04 | 1.00 2.88 4.38 7.94 |
| ring | coverage, 12 | 0.69 0.65 0.44 0.29 | 1.00 2.75 6.62 8.38 |
| community | degree, 12 | 0.88 1.00 1.00 0.46 | 0.88 2.62 4.19 1.38 |
| community | random, 12 | 0.73 0.73 0.29 0.21 | 1.00 3.00 4.62 9.56 |
| community | coverage, 12 | 0.71 0.75 0.81 0.54 | 0.88 2.69 7.88 11.00 |

Plurality value of the primary contrast on the engineering roots: informative checks ring +0.479, community +0.333, mean +0.406; unreliable checks ring −0.062, community −0.250, mean −0.156.

What the table shows about floors and ceilings:

- At k = 1 the attacker is a hub that `degree` and `coverage` check first, so its fate is its first verification attempt: admitted in 2 of 16 ring engineering roots and 0 of 16 community roots under informative checks (expected rate 0.1), in 16 and 14 of 16 under unreliable checks. This end is low but not fixed.
- At k = 27 the attacker is seated in part in both families under both policies (1.4 to 2.4 identities on average at 12 checks). Under `degree` no honest specialist is retained, so those rows decide the plurality answer; under `coverage` honest specialists outnumber them.
- `degree` at k = 9 is at the ceiling (1.00) in both families. It is a secondary cell.
- `no_verification` and `random` are far from `degree` and `coverage` at k = 1: without a check aimed at the hub the single identity is admitted and dominates.

Sensitivity, internal links removed (same engineering roots, not part of the model comparison), informative checks, 12 checks: plurality wrong-answer rate under `degree` 0.12 0.19 0.81 0.04 (ring) and 0.00 0.00 0.88 0.04 (community); under `coverage` 0.06 0.15 0.00 0.00 and 0.00 0.08 0.00 0.00; attacker identities admitted at k = 27: 0.12 and 0.12 under `degree`, 0.00 and 0.00 under `coverage`. Plurality value of the primary: +0.010 (informative), −0.198 (unreliable). The direction of the scripted primary therefore depends on the internal-link assumption, and the README says so.

Under plurality the model cannot change who is admitted. What S1 adds is what the synthesizer does with the admitted rows: whether it answers from one or two unchecked rows or abstains, and whether it discounts many rows from one identity.

## Current attempt admission

Operations entry: manual, through the generic private launcher `scripts/run-ready-chain.py` in the agentops repository (commands in [RUN.md](RUN.md)). [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all pass on 0b8a444a (builder, offline) |
| Prepare named stage | `python3 scripts/run-ready-chain.py sybil-split-opus <commit> setup --host <server>` | pending |
| Dispatch named stage | `python3 scripts/run-ready-chain.py sybil-split-opus <commit> chain --host <server> --confirm-paid` | pending |
| Resume interrupted execution | unsupported by design: a batch name cannot be queued twice; a repair is a new attempt with its own pre-run review | not applicable |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>`; `python3 src/analyze.py rows <episodes.jsonl.gz>` | pending |
| Stop this study and close out | stop the chain process, verify uploads, release claim `dmarz-sybil-split-opus` | pending |

- Attempt: chain-001 (S0, P0, Q0, S1); no parent attempt; pre-run assessment [reviews/chain-001-pre.md](reviews/chain-001-pre.md), status ready, not launched.
- Frozen assigned manifest: [manifest.json](manifest.json), digest 2a4b21669c9301a440c3f59d0c1cbe8439a981507e2649203b1c1a0275fc6b75; execution command in the runbook.
- Budget authority: as relayed (see Ownership): Opus for everything and no gate on cost; hard call caps P0 1, Q0 60, S1 2,688, total 2,749; ledger cap USD 190 on settled cost plus open reservations.
- Allocation: none yet. The operator takes the exclusive claim `dmarz-sybil-split-opus` at launch.
- Credentials: `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` supplied in memory by the launcher; never written to a file, an argument or a log. No credential was used to prepare this package.
- Go/no-go: not decided. This builder does not launch.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| none yet | | | | |

## Closeout

Pending. Nothing has run.
