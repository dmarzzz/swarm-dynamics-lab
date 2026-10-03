# Research questions for human selection

Owner: dmarz/question-atlas, holding `synthesis-question-atlas-update`. Updated 2026-10-03.

This bank contains **214 candidates supported by 319 distinct source records**, prepared for the team's human review: research questions, tentative predictions and ways to test them across all 15 research areas. **Every item is an unreviewed hunch.** The user explicitly requested hypothesis brainstorming before selecting projects. These working notes do not create formal hypotheses, approve protocols, pass survey gates, or report experimental findings.

**[Read the full candidate bank](../researchers/dmarz/notes/question-atlas/README.md).** The [review browser](../researchers/dmarz/notes/question-atlas/review.html) supports search, topic and feasibility filters, shortlisting, comments, and review export/import. Download/open the HTML locally; GitHub's code view will not execute it. [Structured data](../researchers/dmarz/notes/question-atlas/candidates.json) supports other review tools. The [scope record](../researchers/dmarz/notes/question-atlas/scope.md) states what was inspected and what remains uncertain.

## Swarm factory questions (MKT-01 to MKT-12)

Twelve questions added 2026-10-03 for a proposed Factorio-like environment where LLM firms build production chains and sell into shared Cournot markets. They cover tacit market division with sunk capacity, firm-to-good ratios, one principal running several firms, telling Sybil firms from tacit colluders, communication channels, forks and mergers, mixed models, public ledgers, competitive entrants, regulators, and whether a small simulator predicts the full game. Like every item here they are unreviewed hunches. The idea brief is [swarm-factory.md](../researchers/dmarz/notes/swarm-factory.md); the cards are in `markets.json`.

## What changed in this update

The update adds **59 questions**, revises **36 originals**, and retains **107 originals unchanged**. All 143 earlier IDs survive. New research has expanded the bank and changed several test designs. [The update guide](../researchers/dmarz/notes/question-atlas/update-v2.md) lists the new and revised IDs, maps B1–B5 to budget questions, and records the research cutoff. Use **New in this update**, **Revised in this update** or **Needs review again** in the browser to focus your review. Existing IDs, local decisions and notes are preserved. A changed candidate keeps its previous choice but asks you to review it again; editing notes alone does not clear that flag.

The additions cover shared budgets and truthful metering; false-name allocation and scheduling; containment, reintegration and recovery; dataset validity and evaluator leakage; and the distinction between fresh model generation and replay. The newly revised LLM survey also narrows claims about effective team size, capture, diversity and belief change. These are proposed comparisons, not new empirical findings.

## What is in the bank

The bank covers collective motion, biological decisions, active matter, physical robot swarms, synchronization and consensus, crowds and traffic, swarm optimization, learned coordination, LLM societies, Sybil resistance, fork-and-merge security, swarm detection, measurement and research methods, and agent budgets and resource allocation.

Each entry has a stable ID, a question, a directional candidate hypothesis, a test sketch, comparators, measurements, evidence that would count against it, confounds, closest-prior relationships, and a prerequisite for promotion. Entries link back to the team's original briefs where relevant. The closing section of the full bank maps all sixteen original briefs to candidates; the external-influence direction is also included.

The framing labels mean:

- **Replication:** recover or challenge a previously studied result in a clearly specified setting.
- **Boundary test:** identify where an established explanation or method stops working.
- **Extension:** a candidate modification or comparison whose added value remains to be established.
- **Measurement:** test whether an observation or evaluation procedure measures what we think it does.
- **Speculative:** an interesting possibility with a weaker evidential bridge.

These are editorial labels, not verified novelty judgments. Several apparently new ideas already have close predecessors. A useful replication or negative result can justify a project without an originality claim. Source depths shown in the bank are inherited catalogue metadata; they are not fresh full-read claims by this pass, and the team's [read-depth audit](https://github.com/dmarzzz/swarm-lab/issues/76) remains open.

## Connections worth discussing together

The IDs below are discussion bundles, not a ranking or an experiment selection.

- **How many independent observations does a swarm really have?** SOC-01/02/08 distinguish information diversity, effective team size and stopping rules; PHY-09 tests shared evidence in collective decisions; SEC-03/13 connect evidence counts to returning forks and cheap identities. Shared premise: more agents or messages need not mean more independent observations. These domains need distinct models and should not be pooled as replications of one theorem.
- **Can useful state survive change?** SOC-21–25 address compression, rare knowledge, removal, turnover and obsolete conventions. SEC-05–07 isolate uncertainty loss, incomplete dependency graphs and stale children. MTH-05 concerns execution replay, while PHY-17/24 concern physical recovery. Knowledge repair, replay and physical regrowth have different success criteria.
- **When does communication help?** SOC-04/05/13–19, PHY-07/20/25/26/30, RL-03/05 and OPT-02 test routing, attention, scheduling, topology and bottlenecks. Count attempted, admitted, delivered and used messages where the mechanism requires it; equal message counts need not imply equal information or inference budgets.
- **What does consensus accomplish?** SOC-06–12, PHY-08/10–12 and MTH-02 separate convergence, accuracy, responsiveness and decision value. Compare against task truth or another independent evaluator, not a judge that simply rewards agreement.
- **Are we seeing interaction or a shared cause?** SOC-06/33–35, SEC-25–29, MET-05/07 and SIM-01 distinguish common exposure, prompt or scaffold similarity, actual peer effects and narrator leakage. A model-family fingerprint does not identify an operator. Correlation alone does not establish influence. [[shalizi-2011-homophily]]
- **Are impressive patterns doing useful work?** PHY-03/13/16–18/28/34, MET-01/02/04/06, RL-06/07 and OPT-03 compare order, shape, synchrony, synergy or complexity with task outcomes. An evocative visualization is a reason to investigate, not an outcome measure.
- **How should a society spend its limited budget?** BUD-01–22 connect budget signals, hard enforcement, allocation rules, delegation, common pools and service floors. SOC-15/16/27/28 provide coordination and verification complements; SEC-13/37–44 distinguish resource quotas from false-name incentive guarantees.
- **Which new data actually support a comparison?** MTH-07–15 and SIM-05–07 separate label quality, independent sequences, legal information, translation, failed attempts, true collaboration, coverage changes and deployable comparators. The [dataset audit](../researchers/dmarz/notes/question-atlas/datasets-scope.md) maps all 33 new dataset records to uses or limits.
- **Can we trust the experimental platform?** MTH-01/03–06 and SIM-01–04 test sample dependence, version changes, variance allocation, replay, selection bias, private-state leakage, activation order, blind-policy shortcuts and agreement between engines. These can become shared validity checks for whatever projects humans select.

## A practical human review

First skim by area and mark **Shortlist**, **Discuss** or **Park**, adding a short reason. Leave enough variety to compare an ambitious mechanism question with a cheaper replication or measurement project. The list has no automatic priority score and no preselected winners.

For each shortlisted idea, answer five questions:

1. **Decision value:** What would we do differently if the prediction is supported, contradicted or unresolved?
2. **Prior-art difference:** Which closest result might already answer it? Is the difference a new mechanism, boundary, task, measurement, or replication?
3. **Observability:** Can we actually observe the required state, exposure, identity or outcome without giving the method privileged labels?
4. **Interpretability:** Would the proposed comparison distinguish the mechanism from a simpler explanation?
5. **Feasibility:** Is there an accessible environment, independent evaluator, realistic resource budget and a smallest useful study?

Existing review exports remain importable. Per-candidate fingerprints on new decisions let later versions flag changed content; legacy reviews without fingerprints are flagged on revised cards. The browser and canvas have separate local stores, so export before moving between them. Export individual reviews before combining them. The HTML browser saves choices locally, not to a shared team database. Importing a review replaces overlapping candidate choices in that browser, so preserve separate reviewer exports when disagreements matter. Discuss disagreement rather than averaging it into a spurious precise ranking.

After human selection, audit the few load-bearing methods in full and finish the relevant survey/review work. Then write the formal hypothesis with at least three closest prior entries, a primary outcome, smallest effect worth pursuing, independent sampling unit and uncertainty-aware kill rule. Most cards currently name two or three sources: they are starting anchors, not complete novelty reviews. A noisy estimate near zero is inconclusive, not a refutation. Choose confirmatory sample sizes from a precision or power analysis and keep pilot/tuning cases separate.

## Reuse infrastructure after selecting questions

Many candidates can share small, transparent test substrates without requiring one giant simulator:

- A distributed-evidence decision task for information, dissent, attention, routing and external-influence comparisons.
- A reversible shared-state task for compression, recovery, turnover and fork-return studies.
- A local identity and contribution simulator for rate limits, entry, reputation and coalition mechanisms.
- A fully labeled trace generator for common-exposure, attribution, missing-data and detector-validity tests.
- Existing particle, robot, traffic and learned-policy environments for physical and MARL questions.
- A fixed-budget optimizer harness for component, coordinate, topology and noise tests.

These are possible reuse groups, not instructions to start building them. The now-merged [simulator survey](../surveys/sim-environments.md) reports many candidate environments and twelve teammate CPU smoke tests. This update incorporates its source records and practical test routes without repeating those runs. The survey remains in progress; its broad absence claims and speed comparisons across different workloads are not established novelty or performance claims. A particular question may need only a tiny reference implementation rather than a new platform. Existing code availability does not establish suitability or license compatibility for the chosen study.

Vishesh's [agent-experiment toolkit](../tooling/agent-experiments/README.md) remains the shared methods starting point. Its [integration guide](../tooling/agent-experiments/INTEGRATION.md), manifests, protocol template and offline demonstration are the starting point for shared bookkeeping after selection. The demonstration uses scripted policies; it does not establish an LLM effect or supply a production provider adapter. Reuse these methods rather than duplicating them inside this candidate bank.

## Readiness at this snapshot

The LLM-agent survey passes the mechanical gate and now includes a response to the citation and interpretation corrections. Its existing review is still **revise**, with a new re-review task open; this atlas does not approve that response. Fork-merge and Sybil surveys remain in progress. The contagion scan is now complete, which changes the evidence available for those questions without completing their surveys. The simulation-environment survey is merged and meets mechanical floors but deliberately remains in progress because paper coverage is not saturated. Agent budgets has an open survey task and no completed survey. Other topic catalogues are broad, but most lack completed surveys.

The immediate next action is human selection from the bank. Formal promotion still needs the repository's focused prior-art and review process. No experiment, model-training job, hardware run, deployment or paid simulation was launched in producing this list.
