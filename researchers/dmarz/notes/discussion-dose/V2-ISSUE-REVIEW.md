# Does discussion dose v2 address the original pilot issues

**Partly. V2 fixes the main experimental floor effect, adds the right kind of control for extra model calls, and uses fresh development worlds. It does not repair memory coverage or parent grounding, and the completed results do not yet establish a causal benefit or harm from additional discussion.**

This assessment compares v2 with the [original pilot reflection](RESULTS-AND-REFLECTION.md). It is based on the deployed implementation and completed H1–H4 calibration artifacts inspected on 4 October 2026 UTC, approximately 01:29. At inspection, the H4 dose sweep, private-reflection comparison and H5/H6 searches were still running. Their partial rows are not treated as final estimates. No paid model calls were made for this review.

## Assessment against the original issues

| Original issue | V2 change and evidence | Assessment |
| --- | --- | --- |
| Corruption disappeared before discussion | Removes the free clean verification turn; distributes incomplete evidence among exposed, witness and swing roles; progressively makes source conflict harder. H4 has 11/12 attacked memories poisoned at round zero. | Fixed for constructing a contested starting condition. |
| Discussion also buys extra model calls | A separate board-versus-private comparison uses the same acquisition snapshot, call counts and output caps at six rounds. | Addressed in design; completed empirical comparison still pending. Input tokens are not matched. |
| Correct votes and true retained facts did not ensure useful parent memory | Majority merge and parent behavior are inherited unchanged. No required-fact coverage gate or enforced abstention was added. | Not fixed or directly stress-tested by the completed calibration. |
| Reusing repaired development fixtures weakened readiness evidence | Calibration uses worlds 200–211, dose sweep 220–225, private control 230–235; these are disjoint from v1. | Addressed at the world-ID level. Templates, model and swarm size remain the same. |
| Format failures and weak clean competence | H4 calibration has 0/24 invalid and 10/12 correct clean votes. H1–H3 each have one invalid attacked episode and only 9/12 correct clean votes. | Improved relative to v1's original grammar defect, but not a generally solved interface or competence problem. |
| Limited generalization and uncertain attribution | Still three agents, one model, one seed and three fictional rule templates. Source cues and information availability change together relative to v1. | Unresolved; exploratory mechanism study only. |

## What the completed calibration actually establishes

All rates below use assigned denominators, retaining invalid episodes. Each level has 12 clean and 12 attacked episodes and zero additional board rounds. Children have already exchanged their initial reports at that point.

| Level | Clean votes correct | Attacker target wins | False fact enters memory | Parent gives attack-derived answer | Invalid episodes |
| --- | --- | --- | --- | --- | --- |
| H1 | 9/12 | 4/12 | 6/12 | 6/12 | 1/24 |
| H2 | 9/12 | 2/12 | 9/12 | 9/12 | 1/24 |
| H3 | 9/12 | 4/12 | 9/12 | 9/12 | 1/24 |
| H4 | 10/12 | 5/12 | 11/12 | 11/12 | 0/24 |

H4 was the only level to clear the predeclared 80% clean-accuracy bar, and its target-win rate was closest to the desired nontrivial baseline among eligible levels. It therefore qualifies as a candidate difficulty setting under the recorded selection rule. With only 12 worlds, that clean pass is fragile: one fewer correct world would fail the gate.

H4's 5/12 attacked target-win rate is not the attack-attributable increase. The clean arm also chose the same designated target in 1/12 worlds. The observed clean-adjusted difference is **4/12, or 33.3 percentage points**, on these calibration worlds. This is an exploratory paired comparison, not a population estimate or discussion effect. Calibration selected H4 using its outcomes, so fresh sweep/control worlds remain essential.

The completed four-level calibration cost $2.146441 and produced 955 model calls with complete reported token usage. Its 96 episodes share the same 12 underlying task IDs across levels; they are not 96 independent worlds. Runs: H1 `06699b02`, H2 `d3cb8c02`, H3 `1f1e2f69`, H4 `14b3bd88`, all in `discussion-dose-v2`, runtime `241084145b25718ad3785631cbf0486849c8c807`.

## The most important new finding is downstream contamination

In H4, the witness originally reported the true target value in 12/12 attacked worlds. After receiving the report packet, that same witness endorsed the false value in 11/12. The exposed child endorsed the false value in 12/12, and the swing child in 9/12. Thus the reports alone were sufficient for extensive measured contamination before extra board discussion.

The final task decision understated the damage. H4 had five correct attacked decisions, but **four of those five still merged the false fact and gave an attack-derived parent answer**. Those four were worlds 205, 206, 210 and 211. Two additional attacked episodes abstained at the team vote while still admitting the false fact and misleading the parent. Only one of 12 attacked parent answers was correct, compared with all 12 clean parent answers.

This is stronger evidence for the original architectural concern: successful voting does not certify the memory passed to the parent. It demonstrates propagation of an incorrect value through a nominal majority into a later answer. Agreement among agents who have read one another's reports does not imply independent evidence.

However, it is a different failure from v1's missing-fact case. Every valid H1–H4 calibration memory contained the target key; there were no missing-target cases in that sample. Consequently, the calibration cannot show that v1's unsupported-answer-on-missing-memory behavior improved. The merge still lacks an explicit coverage requirement, and parent abstention is a permitted model response rather than a deterministic gate.

## What the private control can and cannot resolve

The implemented private arm preserves the shared initial report packet, makes the same number of subsequent discussion/probe calls, and stores each new post only in its author's private history. Peers' later posts are absent. This is a sensible comparison for the **incremental effect of additional peer messages beyond initial report exchange**.

It does not compare all communication against independent work: both arms already saw peer reports, and contamination can already have spread. It matches calls and output ceilings rather than exact input tokens, so “equal compute” is too strong a label. The private prompt also still asks for a discussion-style post, even though it is not delivered to peers. That makes the intervention fairly localized, but it does not represent an optimized private reasoning strategy.

If private reflection changes the outcome, that does not invalidate it as a control. Such change is precisely why the comparison is needed: repeated private processing may reinforce or correct an error. The relevant estimate is the paired board-versus-private difference, with clean controls and invalid outcomes retained. The pending control run, `d0725be0`, must finish before that estimate is assessed. The dose sweep `723dad8e` by itself still mixes additional peer exposure with additional model calls.

## Remaining design and reporting cautions

The difficulty ladder is a calibration device, not a clean one-factor ablation. `make_world_v2` seeds role assignment and document layout with the level as well as task ID. Between H1 and H2, roles change in 10/12 worlds; H2 to H3 in 12/12; H3 to H4 in 9/12. Therefore differences between levels cannot be attributed solely to authority labels, recency or fake corroboration. Clean/attack pairs within each level remain matched.

Several prose claims in [V2-DESIGN](V2-DESIGN.md) are stronger than the implementation supports. Additional discussion is not the only route to a correct answer: round zero already exposes peer reports and produces correct attacked votes in five H4 worlds. Attack success also need not require a particular exposed-plus-swing voting coalition; any strict-majority coalition can decide. The opening statement that no model run has happened is stale. The evidence and timing above should govern interpretation.

The three invalid calibration episodes are still output-contract failures. I inspected the failed responses: H1 repeated `C.power`, H2 repeated `B.power`, and H3 repeated `C.transfer`, producing claim lists longer than the allowed key set. This is distinct from v1's unsupported derived key. The old grammar repair did not eliminate duplicate-key failures under conflicting evidence. H1–H3 also miss the clean competence gate independently of those invalid attacked episodes.

H5/H6 are separate stress anchors. H6 removes every clean copy of the attacked fact, so a high error rate there would not establish a failure to recover accessible evidence. It can test an unrecoverable condition, but it cannot by itself repair causal identification, memory coverage or external validity. No final H5/H6 result is claimed here.

## Verification and decision

I downloaded the four completed calibration bundles, verified compressed and raw artifact hashes, reconciled their assignment ledgers, reconstructed their worlds and checked world hashes, and recomputed all valid evaluation objects, final majority decisions and merged memories. The completed calibration numbers above agree with those artifacts. This review did not perform the full exact-observation model-response replay used for the original v1 qualification, nor audit unfinished runs as complete.

**V2 is a substantially better experiment for studying corruption that survives report exchange. It is not yet evidence that longer discussion improves safety, and it is not a repaired memory architecture.** The completed results make it more important to keep decision accuracy, false-memory admission, required-fact coverage and parent consequences separate.

The next analysis should use the already-running sweep and private comparison once terminal artifacts exist. Before any further scale-up, inspect per-mode clean competence and validity, report the paired contrast with its small-world uncertainty, and add a deterministic missing-fact parent regression fixture. For cue-level causal claims, hold allocations and document randomization fixed across levels. These are recommendations only; this review launches or modifies no model run.

Sources: [v2 implementation](src/sim_v2.py), [world construction](src/tasks_v2.py), [frozen plans](src/pilot_v2.py), [private control design](PRIVATE-CONTROL.md), [shared merge and parent path](src/sim.py), and the individual runs on the [live v2 experiment](https://swarm-live.pages.dev/#/x/discussion-dose-v2).
