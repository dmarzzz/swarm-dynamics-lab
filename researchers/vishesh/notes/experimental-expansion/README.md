# Experimental question expansion

Owner: vishesh/codex-methods. These 25 questions are exploratory hunches, not registered hypotheses or approved experiments. No runs or results are reported.

## Count reconciliation

At this contribution snapshot, Dan’s canonical atlas contains **214** questions. Our earlier banks contain **40 VX** and **14 PX** extensions: **268 question records** together. This batch adds **24 EX** questions, bringing the total to **292**, including **78 contributed extensions**. Related questions overlap; these are not 292 independent ideas or novelty claims. There are currently zero registered hypotheses.

The earlier 301-item scenario/biology reviews included 33 briefs, designs and umbrella records in addition to the 268 questions. Those reviews remain dated snapshots, not current question counts. The separate contribution view makes all three extension banks visible without changing canonical question IDs or saved atlas reviews.

## Read and select

- [Question bank](question-bank.md): all 25 comparisons, falsifiers, confounds and links.
- [Structured records](questions.json): machine-readable source.
- [Dashboard contributions](https://swarm-research.pages.dev/#/contributions?bank=EX): searchable contributions.
- [Scenario kits](../hackathon-scenarios/scenario-kits.md): runnable task shapes proposed for these questions.

For a first small implementation, EX-07 (duplicate actions after retries), EX-03 (conflicting concurrent edits), and EX-22 (tool failure mistaken for negative evidence) have particularly direct synthetic ground truth. EX-20 adds a useful shared-memory boundary test. This is an implementation-cost judgment, not evidence that these questions are novel or that one intervention will win.

Each EX record names its closest atlas cards, earlier extensions, original project briefs, additional manipulated variable, decision value and source leads. Source leads are inherited catalogue references, not newly read papers or direct evidence for the prediction. A prior-art methods check may collapse a question into a replication or make it unnecessary.

Start with seeded synthetic fixtures, held-out worlds and equal information/action budgets. Measure task success and intervention costs together. Use oracle conditions only as ceilings; do not leak oracle labels into deployed policies. Treat agent count as a design factor rather than counting correlated agents as independent experimental replicates. Freeze estimators, exclusions and stopping rules before any confirmatory run. LLM runs require the repository’s survey, hypothesis and experiment gates plus budget authorization.

## Dashboard contract

The dashboard exports these notes separately from Dan’s canonical atlas. `dashboard/contribution-banks.json` registers the VX, PX and EX banks. Each bank declares an owner, researcher-notes path, collection key and ID prefix. Export validation checks ownership paths, IDs, explicit exploratory status and resolvable atlas/source/brief/related links. New banks must satisfy that contract. Contribution records currently use the original sixteen Vishesh brief slugs; supporting another project-brief taxonomy requires an explicit schema extension.

Contribution cards are read-only. They do not inherit the canonical atlas’s local shortlist/review state or claim formal hypothesis status. The Questions page reports both record counts and links to the contribution view.

## Publication activity metadata

The EX records include `activity.added_at`, backfilled from their first publication commit, and `activity.tags_added_at`, keyed by current project-brief slug. Timestamps use UTC `YYYY-MM-DDTHH:MM:SSZ`. Preserve the publication timestamp on edits. When adding a project tag later, record its actual addition timestamp; remove its metadata when removing the tag. Do not reset timestamps during export or deployment. Initial tags share the publication timestamp and do not count as later additions.

The Contributions dashboard shows **New** for seven days after publication, and **New tag** beside project tags added later within that window. It supports separate recent-item and recent-tag filters. Badges are calculated at export time; the view displays that reference time, and the existing scheduled dashboard build refreshes expiry. Undated legacy records remain unbadged rather than assigning invented dates. These markers do not change research status, canonical atlas review hashes or scientific novelty assessments.

## Requested addition, 2026-10-04

EX-25 adds conditional swarm-size selection across problem design, urgency, cost, memory and hardware. Related SOC-02/PHY-09/BUD-06/BUD-08 cards cover narrower mechanisms. The live catalogue now contains 219 atlas + 79 contributions = 298 records; the original count reconciliation above remains a dated snapshot. See [EX-25](https://swarm-research.pages.dev/#/contributions?q=EX-25).
