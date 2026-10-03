# Experimental question expansion

Owner: vishesh/codex-methods. These 24 questions are exploratory hunches, not registered hypotheses or approved experiments. No runs or results are reported.

## Count reconciliation

At this contribution snapshot, Dan’s canonical atlas contains **214** questions. Our earlier banks contain **40 VX** and **14 PX** extensions: **268 question records** together. This batch adds **24 EX** questions, bringing the total to **292**, including **78 contributed extensions**. Related questions overlap; these are not 292 independent ideas or novelty claims. There are currently zero registered hypotheses.

The earlier 301-item scenario/biology reviews included 33 briefs, designs and umbrella records in addition to the 268 questions. Those reviews remain dated snapshots, not current question counts. The separate contribution view makes all three extension banks visible without changing canonical question IDs or saved atlas reviews.

## Read and select

- [Question bank](question-bank.md): all 24 comparisons, falsifiers, confounds and links.
- [Structured records](questions.json): machine-readable source.
- [Dashboard contributions](https://swarm-research.pages.dev/#/contributions?bank=EX): searchable contributions.
- [Scenario kits](../hackathon-scenarios/scenario-kits.md): runnable task shapes proposed for these questions.

For a first small implementation, EX-07 (duplicate actions after retries), EX-03 (conflicting concurrent edits), and EX-22 (tool failure mistaken for negative evidence) have particularly direct synthetic ground truth. EX-20 adds a useful shared-memory boundary test. This is an implementation-cost judgment, not evidence that these questions are novel or that one intervention will win.

Each EX record names its closest atlas cards, earlier extensions, original project briefs, additional manipulated variable, decision value and source leads. Source leads are inherited catalogue references, not newly read papers or direct evidence for the prediction. A prior-art methods check may collapse a question into a replication or make it unnecessary.

Start with seeded synthetic fixtures, held-out worlds and equal information/action budgets. Measure task success and intervention costs together. Use oracle conditions only as ceilings; do not leak oracle labels into deployed policies. Treat agent count as a design factor rather than counting correlated agents as independent experimental replicates. Freeze estimators, exclusions and stopping rules before any confirmatory run. LLM runs require the repository’s survey, hypothesis and experiment gates plus budget authorization.

## Dashboard contract

The dashboard exports these notes separately from Dan’s canonical atlas. `dashboard/contribution-banks.json` registers the VX, PX and EX banks. Each bank declares an owner, researcher-notes path, collection key and ID prefix. Export validation checks ownership paths, IDs, explicit exploratory status and resolvable atlas/source/brief/related links. New banks must satisfy that contract. Contribution records currently use the original sixteen Vishesh brief slugs; supporting another project-brief taxonomy requires an explicit schema extension.

Contribution cards are read-only. They do not inherit the canonical atlas’s local shortlist/review state or claim formal hypothesis status. The Questions page reports both record counts and links to the contribution view.
