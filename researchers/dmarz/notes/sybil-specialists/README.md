# Sybil defense and useful specialist teams

## Question

Can graph-based admission keep adversarial identities out without excluding useful specialist teams, and where should a limited verification budget be spent? This is the SEC-19 and SEC-43 exploratory instrument, owned by dmarz/sybil-specialists. The user requested an experiment plan, a visual in the live UI, scripted qualification before API use, and deployment through swarm-labs-agentops.

The first deployed version is a **scripted engineering rehearsal**. It tests the environment, comparisons, scoring, failure handling, deployment and measured replay. It does not establish a finding about LLM behavior or a general Sybil-resistance guarantee. The survey remains in progress; formal hypotheses and S2 stay blocked. The experiment-worker template explicitly permits S0/S1 instruments in researcher notes before those gates pass.

## Prediction and decision

The working prediction is that spending verification on currently uncovered graph neighborhoods will recover more rare-specialist task accuracy than selecting high-degree nodes, at equal check budgets. It may also admit more adversarial identities. Adoption would require a useful accuracy increase without an unacceptable increase in malicious admission; showing more admitted nodes alone is insufficient.

A valid adverse result is that coverage merely moves trust to attackers, especially when attackers can obtain passing checks cheaply. With equally informative checks for both populations, topology cannot be assumed to identify ownership. We include that condition explicitly.

## Setup

Each independently generated world has 36 identities: an 18-node established core, a nine-member honest specialist community and nine identities controlled by one simulated adversary. Clean controls make both outside communities honest. Two core nodes are initially trusted. The outside communities have identical internal structure and matched degrees, age, activity and claimed skills. Labels are randomized, and which outside community is honest is randomized per world. The graph is deliberately symmetric between outside communities; ownership is not encoded in topology.

The two halves of the core are nine-node ring lattices with three neighbor offsets and matching cross-half edges. Outside groups are nine-node lattices with two neighbor offsets. One or three symmetric edge swaps connect each outside group to the core while preserving every node degree. This is a small synthetic graph family, not an empirical model of real agent traffic. A second independently implemented graph family and realistic edge-acquisition processes are requirements for formal promotion.

The world contains six objectively scored task facts, three common and three rare. Each identity reports one fact. Honest reports are correct; adversarial reports use a fixed wrong value. The common downstream solver takes the strict plurality for each skill and abstains on a tie or missing evidence. Six facts are equally weighted. This task makes the effect of losing rare expertise visible; it does not simulate sophisticated work or strategic adaptation.

A verification probe returns only pass/fail. Honest pass probability is 0.90; attacker pass probability is 0.10, 0.50 or 0.90. Potential outcomes are fixed per world and node before policies run, so policies checking the same node see the same result. This is a **modeled external verification service**, not an implemented ownership detector. A passing service check can be earned by an attacker; it never proves independent ownership. No real identities, payments or public endpoints are used.

Policies see only the graph, public profiles, fixed trusted seeds and checks already purchased. They cannot read honest/malicious labels, true owner groups, correct answers, future check outcomes or visualization coordinates. Evaluator truth is passed only to scoring and rendering functions after admission decisions.

## Protocol

All arms use the same personalized random-walk ranking, restart probability 0.20, 120 iterations and 18 admission seats. Initial seeds and newly passed nodes receive equal restart mass. Failed checks remove the checked node; they do not reveal other nodes' ownership. Ranking is recomputed after each check.

- **No verification:** graph-only reference, zero checks. This is an uncharged diagnostic baseline.
- **Degree:** verify the highest-degree unchecked node outside the initial seed set.
- **Random:** verify uniformly using a precommitted per-world tie stream.
- **Coverage:** verify the node whose closed one-hop neighborhood adds the most vertices not already covered by initial or passed seeds. Ties use the same precommitted stream.

Degree, random and coverage buy exactly the same number of checks. Coverage is a defined greedy heuristic. It is not SybilShield, a vertex-cut proof, or a new false-name-proof mechanism. The current common ranking is a simple graph baseline; audited implementations of SybilShield and trusted-seed vertex-cut admission must be added before comparative claims about published defenses.

Run S0 first, then S1 only after every exact-source S0 cell has finished with zero invalid episodes and artifacts are durably acknowledged. S2 is disabled in configuration and code. Follow [the run instructions](RUN.md), [design.yaml](design.yaml), [pre-registration boundary](preregistration.md) and [visualization mapping](VISUALIZATION.md).

S0 has four world seeds (100–103), two bridge levels, two attacker-pass levels, two check budgets (0/4), and clean/attack worlds: 16 cell runs and 256 arm episodes. S1 uses 12 fresh world seeds (200–211), two bridge levels, three attacker-pass levels and three check budgets (2/4/8): 18 cell runs and 864 arm episodes. The same seed across parameter cells remains a dependent world cluster; 864 is not 864 independent samples. Holdout seeds 10000–19999 are untouched.

## Metrics

Primary development contrast: coverage minus degree in rare-task accuracy, at one bridge swap, attacker-pass probability 0.10, budget four, attack worlds. Rare accuracy is correctly resolved rare facts / 3. Overall task accuracy is correctly resolved facts / 6; abstentions are incorrect for completion. Honest rejection is excluded honest identities / all honest identities. Malicious admission is admitted adversarial identities / all adversarial identities, and is null in clean worlds. Also report specialist rejection, malicious share of admitted seats, verified checks and invalid episodes.

Compare whole paired worlds. Report the 12 per-world differences, mean and task-cluster bootstrap interval as exploratory descriptions. Never treat agents, checks, frames or parameter cells sharing a seed as independent replicates. Report the complete useful-output versus malicious-admission tradeoff; fixed seat count is not a guarantee of matched malicious risk. Suggested practical targets for a later preregistration are +10 percentage points rare accuracy with no more than +5 points malicious admission, but these are proposed decision margins, not powered acceptance thresholds for this pilot.

## Qualification and failure policy

Offline checks cover deterministic paired worlds, degree-preserving rewiring, matched outside profiles, public-observation schemas, equal zero-budget behavior, conserved seats, unique checks, clean all-admitted correctness, tie abstention, rejected-node removal, the uninformative-verifier control, visual history fidelity, retained failures and blocked holdout access. Qualification must not require a favorable treatment effect.

Every assigned arm receives a record. An engine exception produces invalid records for all affected arms; it does not silently retry. Invalid outputs remain in the assigned denominator and prevent escalation. Artifact failure preserves raw data and blocks completion until upload is repaired. Deployment is pinned to a full source commit and design digest; results record both. Local output directories and server run-attempt directories refuse overwrite.

## Visual in the live UI

Each cell uploads an initial view, final 1800 × 1180 PNG and, when checks occur, an animated GIF showing all four policies side by side. The replay follows the first assigned world, declared before seeing results. It is not a representative result selected afterward. A fixed layout shows admitted and excluded nodes, verification outcomes, rare-task accuracy and malicious admission at each logical check step. Honest/malicious shapes and colors are explicitly marked evaluator-only.

Full JSONL traces and replay source are retained in the authenticated hub. Only supported PNG/GIF images appear on the public live page. The experiment's plan URL and stage/cell metadata let the UI connect each visual to its run. The existing spatial flock frame format is unsuitable for this graph, so the supported image/replay path is used. See VISUALIZATION.md for semantics and checks.

## Model-backed follow-up

The graph question is meaningful without model calls. An API extension should first qualify a downstream model solver on clean admitted report packets, with correct answers kept outside its context. It would test whether admission effects carry through model synthesis; it would not turn the verification service into a real identity detector. Freeze model, prompt, packet ordering, output schema, total calls, pricing and an explicit spending cap before execution. Keep this extension separately labeled and never pool scripted and model outcomes. No API backend or credential access is enabled by this rehearsal.

## Prior work and limits

Viswanath et al. analyze graph defenses through local community structure; their findings motivate measuring honest outsiders' exclusion. Their paper also emphasizes ranking/cutoff tradeoffs. [[viswanath-2010-analysis]]

SybilShield explicitly addresses multiple honest communities, so multi-community admission is established prior art. Its random-route and agent-voting protocol is a required future comparator, not a name for the heuristic here. [[shi-2013-sybilshield]]

Conitzer et al. connect trusted verification and vertex-cut admission to false-name-resistant mechanism composition under bounded-coalition assumptions. This instrument does not implement that composition or claim its guarantee. [[conitzer-2010-false-name-proofness]]

Primary papers were opened during planning on 2026-10-04; this bounded review is not a complete prior-art survey or a new full-read claim. Formal promotion requires completion and independent review of the Sybil survey, an accepted hypothesis, faithful comparator audits, a broader graph family, a defensible verification model and sample sizing from separate development data.

## Results

The deployed scripted rehearsal completed on 2026-10-04 UTC: 16 S0 cells (256 arm outcomes) and 18 S1 cells (864 arm outcomes), all valid. All 230 run-artifact checksums reconcile; 68 PNG frames and 26 measured GIF replays are available. Fifteen offline controls now pass locally and on sim-dmarz-4, including the subsequently strengthened stop-after-failure control. No provider was called and API spend is zero.

[Live experiment](https://swarm-live.pages.dev/#/x/sybil-specialists) · [Summary chart and analysis](https://swarm-live.pages.dev/#/r/sybil-specialists%2Fanalysis-scripted-001) · [Fleet post-mortem](reviews/fleet-s1-001-post.md) · [Reconciled results](results-summary.json) · [Deployment record](deployment.json).

At the prespecified development cell (one bridge, attacker check-pass 0.10, four checks), the 12-world means are:

| Policy | Rare-task accuracy | Adversarial identities admitted |
|---|---:|---:|
| No checks | 0.0% | 0.0% |
| Highest degree | 2.8% | 3.7% |
| Random | 44.4% | 6.5% |
| Uncovered neighborhoods | 86.1% | 12.0% |

Coverage minus degree is +83.3 percentage points rare accuracy (descriptive paired-world bootstrap interval +58.3 to +100.0 points) and +8.3 points malicious admission. The latter exceeds the plan's suggested +5-point risk margin; this pilot does not justify adoption. When attacker check-pass rises to 0.90 in the same cell, coverage yields 22.2% rare accuracy and admits 76.9% of attackers. All 18 S1 conditions and four arms appear in the summary chart. These are conditional synthetic outcomes, not measured LLM behavior or a general defense guarantee.

Overview scalar metrics describe coverage. Compare all arms through the summary chart, per-world four-panel replays and saved arm summaries. Simulation source stays frozen at e3caaf3; the installed post-run revision adds failure-stop enforcement without changing simulation/scoring or rerunning observations.

## Analysis

The initial implementation tests whether the planned measurements discriminate the known fixture states and whether the UI renders their actual history. Any policy difference is conditional on the synthetic generator, fixed adversarial reports and externally supplied probe reliability.
