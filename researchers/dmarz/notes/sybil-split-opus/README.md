# Identity splitting with fixed attacker resources (Opus 5.5)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-split; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Splitting one attacker's fixed 27 report rows, 27 attachment edges and 27 verification attempts from 1 to 27 identities raises rare-skill wrong answers of an Opus 5.5 synthesizer more under degree-based than under coverage-based admission checks. Basis: Unrun. The package is prepared and tested offline only; no stage has run on a server and no model call has been made.
- **sample_size_summary:** Observed: none. Planned: 24 paired synthetic roots in each of two graph families × 56 conditions = 2,688 S1 calls at 108 honest simulated identities and one synthesizer; separate Q0 of 60 calls on 10 roots and a one-call probe. Roots are the independent units, not calls or identities.
<!-- experiment-evidence:end -->

**Nothing has run.** This directory is a launch-ready package: plan, frozen design, code, offline tests, runbook and a pre-run review. No stage of this study has been executed on a server, no model call has been made and no result exists. Exploratory; owner dmarz; built by dmarz/pipeline-split on 2026-10-04 for the pipeline lead dmarz/pipeline.

It is successor 3 of [the next-experiments note](../next-experiments-2026-10-04/README.md) ("Identity splitting with fixed attacker resources") and extends the instrument of [sybil-scale-api](../sybil-scale-api/README.md) in the Opus 5.5 form used by [sybil-scale-xl](../sybil-scale-xl/README.md). It follows the [ready-chain contract](../pipeline/READY-CHAIN.md). This is a hunch-level study in researcher notes, not an accepted hypothesis. It makes no novelty or superiority claim. S2 is disabled.

**Authority and review status.** As relayed to this builder by the pipeline lead dmarz/pipeline from dmarz/fleet-monitor on 2026-10-04: dmarz did not name this study. He told the fleet monitor to keep five experiments running by building a pipeline of prepared experiments, to use Opus for everything, and not to gate on cost; the fleet monitor chose this study from his backlog (successor 3 of the next-experiments note) under that delegation and told him so. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check of this package is a same-researcher check and nothing more; the run is not independently reviewed. Opus is used for every paid stage. Cost is not a gate, but every run has hard `max_calls` and reports actual calls, tokens and dollars to the hub.

## TLDR

Earlier Sybil studies here let the attacker's resources grow with the number of identities it controlled, so they could not say whether having more identities helps by itself. This study gives one attacker a fixed budget of 27 fabricated report rows, 27 attachment edges to honest identities and 27 verification attempts, and has it hold them with 1, 3, 9 or 27 identities. The honest world (108 simulated identities, their reports, their check outcomes, the identities the attacker attaches to and the 54 admission seats) is identical at every identity count within a root. Three admission policies (`coverage`, `degree`, `random`) check 4 or 12 identities, with a no-check baseline, under informative checks (an attacker identity passes 10% of the time) and unreliable checks (90%). `claude-opus-5-5` reads the admitted reports and returns six values; a plurality rule answers the same packets. The measure is how often the answer to a rare-skill question is wrong. The primary contrast asks whether splitting from 1 to 27 identities raises wrong answers more under `degree` than under `coverage`. There are 24 roots in each of two graph families and 2,688 comparison calls, after a scripted stage, a one-call probe and a 60-call clean qualification. Identities, graphs and checks are simulated; only the synthesis is a model call. One fabrication type, one population size and one attachment rule are tested, and no published Sybil defense is included as a comparator.

## Question and prediction

Does splitting one attacker's unchanged resource budget across more identities increase its harmful influence on a synthesized answer, and which admission policy preserves legitimate specialist value while it does?

Primary contrast (one, exploratory): the change in rare-skill wrong-answer probability from 1 to 27 identities under `degree`, minus the same change under `coverage`, with informative checks and 12 checks, paired by root and weighted equally across the two graph families. Positive means coverage attenuates identity-splitting harm more than degree. A difference of 10 percentage points is the predeclared useful size; it is a practical margin, not a significance threshold.

Working prediction, written after the scripted calibration on engineering roots and before any model call: positive. On the 32 engineering roots the plurality rule gives +0.41 (ring +0.48, community +0.33; see [SETUP.md](SETUP.md)). Under `degree` the checks go to well-connected core identities, almost no honest specialist is admitted, and a few of the 27 small attacker identities are seated unchecked, so their rows are the only rare-skill evidence in the packet. Under `coverage` honest specialists are admitted and outnumber them.

What would count against it:

- The model declines to answer from one or two unchecked rows. Then the harm under `degree` shows up as abstention, not as wrong answers, and the primary contrast is near zero while rare-skill accuracy stays low. That is a valid result about the synthesizer.
- The raw multiplicity effect is negative. With one identity the attacker is a hub that both `degree` and `coverage` check first; with unreliable checks it passes and dominates the packet. In the engineering calibration the unreliable-check version of the primary is negative (-0.16). If splitting lowers harm in S1, that is reported as the result. Attacker resources are not increased to recover an effect.
- The calibration does not transfer to fresh roots.

The scripted value depends on one modelling choice stated under Setup: the attacker's identities are linked to each other. Without those links the same calibration gives +0.01, because a fully split attacker is almost never admitted.

## Setup

**Honest world.** 108 simulated honest identities per root: 54 core identities holding three common skills (18 reports each) and two outside groups of 27 specialists holding three rare skills (18 honest reports per rare skill). Each honest identity submits one true report. Two core identities are trusted anchors. Admission ranks identities by personalized PageRank from the anchors and the identities that passed a check (restart 0.2, 120 iterations, identities that failed a check removed) and seats the top 54. Honest identities pass a check with probability 0.9.

**Two graph families**, with the same block sizes, the same degrees (7 for core, 4 for outside identities) and the same number of core-outside bridge edges (6 per outside group):

- `ring`: the sybil-scale-api construction with every identity honest. Two core rings of 27 and two outside rings of 27, joined by degree-preserving bridge swaps.
- `community`: a degree-matched planted partition written for this study. Each block is a random regular graph drawn by degree-preserving edge switching from a lattice start; bridges are made by the same kind of swap. Both halves use the same drawn graphs, so the two outside groups are exchangeable by a graph automorphism and have identical observable profiles.

**The attacker and what is held fixed.** One attacker owns 27 resource units. Unit r is one fabricated report row (rare skill r mod 3, the root's fabricated value for that skill: the true value plus or minus 7, sign drawn per root), one attachment edge to a fixed honest identity (one ordered draw of 27 distinct non-anchor honest identities per root) and one verification attempt (a pre-drawn uniform number; a check of an attacker identity passes when the number is below the attacker pass rate). With k identities, identity j holds units j·27/k to (j+1)·27/k − 1. Its name, age and activity are those drawn for its first unit, and a check of it uses its first attempt. Across k within a root the 27 rows, the 27 honest endpoints of the attachment edges, the 27 attempt draws, the honest world, the honest check draws and the 54 seats are identical; this is asserted in code for every engineering root in the scripted stage and for every comparison root before the first S1 call. Attacker ages and activities are drawn from the honest specialists' profiles, and attacker names come from the same shuffled pool as honest names.

| Resource | Total at every k | Per identity at k = 1, 3, 9, 27 | How it is represented |
|---|---|---|---|
| Fabricated report rows | 27 (9 per rare skill) | 27, 9, 3, 1 | Rows in the packet under the identity's name |
| Attachment edges to honest identities | 27 | 27, 9, 3, 1 | Edges in the public graph used by ranking and by the policies |
| Verification attempts | 27 | 27, 9, 3, 1 | One attempt is spent when a policy checks an attacker identity |
| Registration overhead | paid out of the two totals above | one edge and one row each | An identity exists only if it holds at least one attachment edge and one report row; at k = 27 the whole budget is spent on existing |

Two representation choices are limits and are stated as such:

- *Verification attempts cannot run out.* A policy checks an identity at most once and runs at most 12 checks, so 27 attempts are never exhausted and each identity needs only one. The budget is recorded, asserted and reported (attempts used and passed), but it does not constrain the attacker. A binding budget (fewer attempts than identities) would make checks of the remaining identities fail with certainty, which would turn the unreliable-check condition into an informative one for those identities; that is a different experiment and is not run here.
- *Links among the attacker's own identities are free and vary with k.* Each attacker identity is linked to the two nearest attacker identities on each side in unit order (the degree-4 ring of the honest outside groups): 0, 3, 18 and 54 links at k = 1, 3, 9, 27. Links between identities one party controls need no honest counterpart, so they are not charged to the attachment budget; this is the usual Sybil threat model and the topology of the parent study's attacker. It means k changes the attacker's internal structure as well as the partition of its fixed resources. The alternative with no internal links is computed without a model on the engineering roots and reported in [SETUP.md](SETUP.md); there a 27-way split is almost never admitted and the primary contrast is zero by construction. That alternative is not part of the model comparison.

A consequence a reader should keep in mind: at k below 27 an identity that carries several rows is visible as such in the packet, and at k = 1 the attacker is a hub of degree 27 in a graph whose honest degrees are 4 to 8. Concentration is observable. That is part of the treatment, not a leak of ownership.

**Factors.** k ∈ {1, 3, 9, 27}; policy and budget: `no_verification`, and `degree`, `random`, `coverage` at 4 and at 12 checks (7 cells); check strength: attacker pass 0.1 (informative, primary) or 0.9 (unreliable, a prespecified stress condition); graph family. Check budgets 4 and 12 are the parent's fixed and proportional budgets at 108 identities.

**Packets and model.** The synthesizer sees one row per admitted report: identity name, skill, claimed value, age, activity and a badge (`trusted`, `passed`, `unchecked`). Rows are ordered by a per-row key drawn once per root, so any two rows keep their relative order in every packet of that root. Packets hold 54 to 80 rows. Model `claude-opus-5-5`, `output_config.effort: low`, JSON-schema output, 8,000 output tokens of room, no sampling parameters. The system prompt is the parent's plus one sentence saying that an identity may submit several rows; it does not mention the manipulation, the truth or ownership.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [setup record](SETUP.md), [runbook](RUN.md), [visual mapping](VISUALIZATION.md), [pre-run review](reviews/chain-001-pre.md), [launcher summary](READY.yaml), [assignment manifest](manifest.json).

| Stage | Batch | Calls | What it does | Passes when |
|---|---|---|---|---|
| S0 | `s0-001` | 0 | Plurality rule on 32 engineering roots through the whole grid (1,792 rows), the 60 qualification fixtures and the probe fixture; structural invariants at every identity allocation | every row valid, no invariant violated, scripted qualification passes, design not degenerate on engineering roots |
| P0 | `p0-001` | 1 | One call on a clean 80-row packet from an engineering root | parsed, model id matches, usage reported, `end_turn`, answer equals the expected values |
| Q0 | `q0-001` | 60 | Clean packets, no fabricated value anywhere: 6 shapes × 5 roots × 2 families | per shape: all valid, field accuracy ≥ 0.95, exact packets ≥ 0.90, 100% null on withheld facts |
| S1 | `s1-001` | 2,688 | 24 roots × 2 families × 2 check strengths × 4 identity counts × 7 policy cells | all rows valid (no gate of its own) |

Each stage needs exactly one `done` run of the previous stage at the same source hash with no invalid row and its gate passed. A failed stage stops the chain; nothing further is queued. Before S1 the chain also projects S1 spend from Q0's measured cost and stops if it exceeds what is left under the cap.

Roots (all below 10000; 10000-19999 is a reserved holdout and stays closed): engineering ring 4919-4934 and community 4821-4836; qualification ring 5139-5143 and community 5144-5148; comparison ring 8233-8256 and community 8351-8374. The engineering roots were used to set the fixed resources. Comparison roots have not been simulated for any design decision.

Qualification shapes: `full` (108 rows), `common_only` (rare skills withheld), `sparse` (two specialists for each of two rare skills, the third withheld), `multirow1`, `multirow3`, `multirow9` (one, three or nine identities carrying 27, 9 or 3 true rows each, beside two ordinary specialists per rare skill; 80, 78 and 72 rows). Every fact that is present is reported by at least two honest identities that submit one row each. Whether the model answers from a single uncorroborated row, or from identities that each submit several rows and nothing else, is therefore not qualified; in S1 those are outcomes.

Calls: 4 in flight, shuffled dispatch, one call per assignment, no retry of any answer. A request the provider rejected before running the model (HTTP 429 or 529) is re-sent at most twice inside the same request time budget. The first failed call stops new dispatch and the remaining assignments are recorded as not started. Hard caps: P0 1, Q0 60, S1 2,688, study 2,749 calls; ledger cap USD 190 on settled cost plus open reservations (arithmetic in the pre-registration).

## Metrics

Per assignment: rare-skill correct, wrong (a non-null value different from the truth) and abstained fractions; whether a wrong answer equals the fabricated value; attacker share of seats and of rows; attacker identities admitted, checked and passed; honest-specialist retention; checks used; tokens and dollars. The same outcomes are computed for the row-plurality rule and for an identity-plurality rule (each identity counted once per value) on the same packet.

Primary: as stated above, on the model's answers. Secondary, all prespecified and descriptive: the raw multiplicity effects (k = 3, 9, 27 minus k = 1) for every policy, budget and check strength; `random` against `coverage` and `degree`; the primary under unreliable checks and at 4 checks; model minus plurality per cell; the primary on rare-skill accuracy. Rare-skill correctness, wrong answers versus abstention, attacker seat and row share, specialist retention, checks and cost are reported together for every cell.

Uncertainty: roots are the independent units. Intervals are percentile intervals from 10,000 bootstrap draws (seed 20261004) that resample roots within each graph family and average the two family means. Every cell is reported with its assigned denominator. A missing outcome is never dropped: complete-case estimates are shown beside bounds in which each missing outcome takes the worst and best possible value. Secondary intervals carry no multiplicity correction.

## Limits

- No faithful published Sybil defense is implemented as a comparator. The source note asks for one before any comparative superiority claim; this study makes no such claim.
- One population size (108 honest identities), one fabrication type, one attachment rule (uniform over non-anchor honest identities), one internal-link rule, two graph families that share block sizes and degrees.
- The verification-attempt budget does not bind, and attacker-internal links are free (both above).
- Identity counts are counts of simulated identities, not of model workers. Each condition is one synthesizer call.
- 24 roots per family are development-sized. The study is not powered for small differences.
- Many packets of a root are identical across check strengths (when no attacker identity is checked, the attacker pass rate changes nothing): 1,554 of the 2,688 S1 assignments fall in 767 such groups, and there are 1,901 distinct packets. Differences between such cells are model variability; the count of repeated packets and of identical answers is reported.

## Results

Not yet collected.
