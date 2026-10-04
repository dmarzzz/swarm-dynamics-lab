# Five decision-model research sketches

Latest: [second-pass variants and revised editorial priorities](REIMAGINING.md). This document preserves the initial shortlist and assessment.

These are exploratory hunches, not accepted hypotheses or preregistered runs. No model calls have been made. Each requires a completed prior-art gate, applicable review, and a separate published run plan before execution.

## DM-01 — Phantom Coast

**Question:** Can a few false local reports create a persistent false coastline in a communicating Jev swarm?

**Rubric score:** 89/100.

Use a fictional archipelago with labelled local observation reports as the primary causal task, plus Earth coordinates as a separate pretrained-knowledge demonstration. Start from paired worlds and freeze the exact truth layer. A false survey bulletin reaches a bounded patch of scouts, then disappears. It may alter only untrusted state, never the governing question, criteria, evaluator or truth map. Ask whether errors cross the exposure boundary and survive after the bulletin is removed.

Use independent predictions, plain neighbor exchange, unique-source exchange, a deterministic evidence accumulator and a single Jev solver with the same union of evidence. Match total calls as well as observation budget; include a same-length benign bulletin and random corruptions with the same initial error count. Fresh-state calls distinguish external-memory persistence from model changes. If a generated world is too hard at baseline, stop at qualification rather than interpreting its failures as persuasion.

The spatial view has synchronized panels for truth, predicted land probability, correctness, uncertainty and source ancestry; animate only measured rounds. Mark directly exposed tiles and missing calls. Score spatially blocked held-out worlds, not thousands of cells as independent samples. On Earth, define coastline resolution, inland water treatment, country boundaries, equal-area weighting and a grid-specific water-only baseline. Report land/water separately from named-country identity.

Biological connection: local sensing and social interaction can produce group-level spatial behavior; our text decisions do not reproduce fish cognition. Closest prior: [[gh-dy-ma-jev-world]], [[hu-2026-jevadvbench]], [[berdahl-2013-emergent]]. The candidate contribution is a spatial exposure–propagation–recovery boundary, not drawing a recognizable continent or showing one flip.

**Disconfirming outcome:** Reject the collective-amplification claim if errors do not spread beyond directly exposed cells or are fully predicted by the single-agent dose response.

**Decision changed:** Tests whether a distributed evidence map needs provenance-aware communication, independent of whether Jev can already recall Earth.

## DM-03 — Stop-Signal Swarm

**Question:** Can evidence-backed inhibitory messages stop a wrong decision cascade without silencing a correct minority?

**Rubric score:** 88/100.

Use the same evidence task as Phantom Coast so treatment effects can be compared without inventing a new benchmark. Each scout can endorse a candidate or send a bounded stop message linked to a specific contradictory observation. A recipient decides whether that observation justifies pausing propagation. The detector receives only available records; evaluator truth never appears in a stop packet.

Compare endorsement-only communication, uniform throttling, random suppression and evidence-linked inhibition. Freeze thresholds on disjoint calibration worlds and match both messages and decision calls. Include bad cascades, equally attractive alternatives, legitimate new evidence, a correct minority, harmless duplicated reports and fabricated stop messages. Add an ablation where code supplies correct contradiction labels, clearly marked as an oracle ceiling rather than the deployed policy.

Measure incorrect cascade area, correct-minority survival, delay, coverage and correct completed decisions. An intervention that stops all action does not succeed. The decisive comparison is whether evidence-linked inhibition improves the error–latency frontier beyond ordinary bandwidth reduction.

Visualization: a network shows endorsements and inhibitory edges separately, with a correctness overlay and a trace from every stop to its cited observation. Biological precedent is honeybee cross-inhibition during nest-site selection [[seeley-2012-stop]]. This transfers a communication mechanism, not a claim of biological equivalence. Jev state sensitivity is the computational starting point [[hu-2026-jevadvbench]]. The idea overlaps the lab’s dissent and immune-response themes; its distinct test is whether a typed, fallible stop channel preserves correct minorities.

**Disconfirming outcome:** Drop the biological-mechanism claim if random throttling or simple rate limits achieve the same tradeoff.

**Decision changed:** Determines whether to implement a distinct evidence-backed stop channel rather than merely slowing communication.

## DM-04 — Panic Queue

**Question:** Can uncertainty spread through a decision swarm and exhaust its ability to review legitimate work?

**Rubric score:** 87/100.

Construct a benign stream of map-report validation or support-triage cases with frozen truth and deadlines. Record Jev decisions under clean and bounded misleading context; then use the identical response tapes to compare review policies. Reviewers have a fixed service rate, known latency and an explicit residual error rate. An ideal reviewer is an upper bound, not the main claimed deployment.

Compare fixed confidence thresholds, calibrated abstention bands, queue-aware admission and reserved capacity for clean independent checks. First hold the input arrival process constant; then vary burstiness at constant average load. Distinguish independent items from a communicating swarm that forwards unresolved cases. Measure whether feedback creates excess overload beyond a queue supplied with the measured single-item escalation rate.

Count every arrival: correct on-time completions, wrong auto-actions, review delays, dropped work and abstentions. Report accepted-answer accuracy alongside total useful throughput. Plot risk–coverage curves at matched capacity. If a policy quietly rejects all difficult work, its missed-deadline count exposes the failure.

Visualization: the queue fills over measured or explicitly simulated logical time while a separate panel shows correctness and available reviewers. Clearly label queue simulations versus live model observations. JevAdvBench already identifies confidence-gate pressure [[hu-2026-jevadvbench]]; selective classification supplies the risk–coverage baseline [[geifman-2017-selective]]. The proposed increment is system-level capacity and feedback. The biological parallel is an alarm system consuming finite response capacity, a mechanism analogy rather than a verified immune model.

**Disconfirming outcome:** Drop the collective contribution if a standard queue fed the measured single-item escalation rates explains the entire effect and no communication-dependent residual remains.

**Decision changed:** Sets review-capacity and admission policies for fast decision services; distinguishes safer predictions from a functioning system.

## DM-02 — Quorum of Mirrors

**Question:** How much independent information does a swarm of identical decision models actually contribute?

**Rubric score:** 86/100.

Give each team a set of grounded, balanced decisions over a synthetic evidence field. Hold the pinned Jev version fixed while independently manipulating prompt wording, overlap between observations and whether peers exchange answers. Agent IDs alone create no independence. Estimate correctness and pairwise error dependence within task-difficulty strata, and retain joint failure patterns rather than relying only on one average correlation.

Compare one call, repeated identical calls, semantics-checked prompt variants, disjoint observations and a pooled-evidence single solver. Every condition receives the same distinct facts and an explicit total compute budget. A simple evidence-counting rule and a calibrated conventional classifier are strong baselines. Separate within-request question packing from separate calls; packing is not a population of autonomous agents.

Primary endpoint is improvement in held-out team correctness per fixed budget, with shared high-confidence failures as the key diagnostic. Bootstrap worlds or task families, not individual agents. Repeat identical requests to estimate service variability. Where an effective-sample-size statistic is shown, label its exchangeability assumptions and show the raw covariance matrix alongside it.

Visualization: rows are models/calls, columns are cases, with red blocks revealing common failures; a second view groups errors by source ancestry. Biology motivates independent sensing versus social dependence, not the false premise that independently named agents are independent organisms. Closest prior: [[rao-2026-jev]], [[sasahara-2026-latent]], [[lorenz-2011-how]]. The opening is which controllable diversity lever improves Jev collectives on a spatial task; generic correlated-model-error claims are already known.

**Disconfirming outcome:** Do not claim useful diversity if gains vanish against a single solver with matched evidence or only arise from more tokens.

**Decision changed:** Decides whether to pay for more copies, more evidence, or an independent measurement.

## DM-05 — Menu Parasites

**Question:** Can harmless-looking changes to a choice menu redirect a collective even when underlying actions and evidence are unchanged?

**Rubric score:** 84/100.

Define a small set of benign latent actions, such as choosing a survey location or a colored target. A menu registry exposes one or more aliases per action. Keep the evidence, legitimate goal and underlying action utilities fixed while adding irrelevant options, duplicating equivalent options, shuffling order or replacing names with neutral identifiers. Manipulations are to this owned test registry, not to someone else’s application.

Separate three phenomena: semantic label bias; mathematically expected probability splitting among aliases; and a caller policy that incorrectly treats an option-dependent confidence statistic as a universal threshold. The currently inspected Choice formula is (p_max − 1/n)/(1 − 1/n). Compute its purely arithmetic menu-size effect before attributing anything to model reasoning. Aggregate mass by latent action and show both raw and aggregated distributions.

Compare raw Choice, canonicalized Choice, binary judgments over fixed actions and an exact utility rule. Calibrate thresholds on held-out menus. Preserve a genuine unknown/unavailable action so removing the answer does not force a bogus success. Evaluate unseen alias families and action sets, not only the strings used during development.

Visualization: a probability river splits across aliases and rejoins at latent actions, beside downstream allocation and correctness. Biological/behavioral connection is competition among alternatives; the connection is weaker than the honeybee stop-signal mechanism and is scored accordingly. [[sun-2026-type]] already studies option semantics; [[typesafe-2026-confidence]] documents the confidence calculation. Our opening is dynamic menu changes affecting collective action and whether canonicalization restores action-level invariance.

**Disconfirming outcome:** If all change is predicted by probability normalization or disappears after aggregating aliases, report a harness arithmetic effect rather than semantic manipulation.

**Decision changed:** Tests whether tool registries and shared action catalogs require canonicalization before decision-model calls.

## Shared measurement contract for any future plan

Freeze questions, criteria, model ID, provider, templates, world seeds, exposure assignment and analysis before calls. Use separate calibration, development and held-out task families; do not retune against held-out failures. Pin the actual returned model snapshot. Randomize paired treatment order and repeat clean calls to measure service drift. Treat invalid responses and timeouts as recorded failures, not neutral votes. Distinguish decision flips, newly wrong decisions, helpful corrections and justified uncertainty. Preserve request hashes, sanitized receipts, usage, latency and each scheduled outcome. A language model must not supply the sole truth label.

Each future run needs its own readable design, immutable registered URL, condition-specific TLDR, preflight, pre-run review, visualization mapping, dedicated allocation and existing budget authorization. None of this research screening grants launch approval or consumes the saved credential.
