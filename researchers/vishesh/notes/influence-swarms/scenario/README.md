# How to win agents and influence swarms

## TLDR

A support team has to choose a helpdesk before its existing contract expires. The cheapest seat price is not necessarily the cheapest operation: automated-resolution charges, difficult tickets still needing people, migration dependencies and deployment-specific hosting commitments can reverse the decision. Six specialists read different parts of the same procurement file. Two checkers retrieve requested records. A chair must decide whether to buy or defer.

**Why run this?** Delegating diligence only helps if the final decision preserves the facts specialists uncover. A repeated outside claim may instead become six apparently independent recommendations. We test whether hiding those preliminary votes—while preserving their findings and exactly the same records—changes the final decision. A cheaper single-reviewer workflow tests whether the team was worth using at all.

**Status:** executable scenario redesign and offline validation; no new model result. This is an exploratory instrument, not a reviewed hypothesis or a real vendor evaluation. [Assessment](ASSESSMENT.md), [protocol](PROTOCOL.md), [source grounding](SOURCES.md), [agent contracts](AGENTS.md), and [pre-run review](reviews/scenario-01-pre.md) distinguish evidence from plans.

## Question and prediction

Does displaying peer recommendations increase harmful adoption of a misleading comparison claim, beyond the effect of the underlying documents? The primary paired contrast is `team_ballots` minus `team_evidence` on change in harmful target selection from clean to omission. Both chairs see identical raw documents, findings and checks; only preliminary choices/confidences are removed. This isolates their presence, not a universal effect of discussion. If both perform equally, the recommendation-display intervention has no demonstrated benefit. If a cheaper generalist performs as well, the team has not earned its complexity.

We expect omissions to matter most when headline price or easy-ticket demos conflict with the buyer's actual workload. We expect deployment and deadline failures to be easier to detect when the decisive record is explicit. These are predictions, not labels the evaluator assigns to model behavior. Genuine-value cases make rejecting the promoted option a mistake; evidence-gap cases make deferral useful.

## Setup

Three fictional suppliers, 17 short records, six decision tensions and four buyer profiles give 24 development dossiers. Every dossier has quotes, scoped deployment responses, stratified pilot counts, migration schedules and an operations brief. Four matched outside-evidence worlds give 96 case/world assignments. Each produces three decisions; the 288 decisions are **not 288 independent real procurement cases**. Family is the conservative unit for generalization; profiles are constructed operating variations.

A publisher controls three comparison-page slots. It cannot edit contracts, internal pilot records, buyer requirements or check responses. Names and page order are counterbalanced. The promoted supplier is chosen for its low seat price, not by secretly finding the worst true option. Numeric values are authored scenario assumptions; the sources establish the kinds of complications to represent.

## Protocol

Six partial-dossier reports → two record checks requested by reports → two chair forks from that exact shared prefix, one with and one without votes. A separate generalist gets the full evidence union, two checks and a final decision. The team forks each involve nine actor roles; ten calls collect their shared prefix and two terminal decisions. The generalist requires four calls. We report cost and latency instead of padding its budget with useless calls.

The chair selects, gives an annual cost estimate, cites records, explains its reasoning and names unresolved questions. **The model's choice is the outcome.** No deterministic function overwrites it. The document parser is only an engineering reference. An evaluator checks the choice afterward against scenario requirements and costs. Full source records remain available to both chairs, allowing a wrong decision to be distinguished from a fact lost in summarization.

## Metrics

Report requirements violated by name; extra annual dollars among feasible choices; annual-cost estimate error; warranted and avoidable deferral; harmful target adoption; citation identity validity; and confidence on decision acceptability. Citation validity is not entailment. Human review of the rationale is needed before asserting a cognitive cause. Frame counts, agent counts, forked chairs and repeated pages are not independent samples.

Results must show clean competence, genuine-value acceptance and useful deferral alongside attack effects. Original v2 measurements remain [here](../../external-influence-v2/reviews/quality-post.md); they are not pooled with this redesign. The old score-enforcement repair is an engineering branch, not evidence that agents reason better.

## Reproduce

```sh
python3 -m unittest discover -s researchers/vishesh/notes/influence-swarms/scenario/tests -v
python3 researchers/vishesh/notes/influence-swarms/scenario/src/run.py --out /tmp/influence-scenario-new
```

Choose a new output directory. The runner is offline-only. It saves every request, reply, terminal outcome and failure. Model collection remains gated on scenario review, fresh qualification, a dedicated allocation and a non-overlapping quota under the existing budget. Do not launch the superseded quality-01 score-enforcement comparison as the main experiment.
