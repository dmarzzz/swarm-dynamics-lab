---
id: yokoo-2005-coalitional
type: paper
title: "Coalitional Games in Open Anonymous Environments"
authors: [Makoto Yokoo, Vincent Conitzer, Tuomas Sandholm, Naoki Ohta, Atsushi Iwasaki]
year: 2005
venue: Proceedings of the 20th National Conference on Artificial Intelligence (AAAI-05), Pittsburgh, pp. 509-514 (also IJCAI-05 poster)
url: https://users.cs.duke.edu/~conitzer/coalitionalAAAI05.pdf
doi: null
arxiv: null
cite: "Yokoo, M., Conitzer, V., Sandholm, T., Ohta, N., & Iwasaki, A. (2005). Coalitional Games in Open Anonymous Environments. In Proceedings of the 20th National Conference on Artificial Intelligence (AAAI-05), pp. 509-514. AAAI Press."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not available (no DOI; AAAI proceedings; OpenAlex rate-limited at access time; batch metadata lists 6 for the CiteSeerX record, Google Scholar is far higher)"
code: []
---

## Summary

Brings false-name analysis to cooperative game theory. In open anonymous environments an agent in a coalition-formation setting can (i) submit false names, splitting its skills across several identifiers (one acting as many), (ii) collude, several agents pooling skills under one identifier (many acting as one), (iii) hide skills, or combine these. Modelling agents as holders of skills with a characteristic function over skill sets, the paper shows by examples that the Shapley value, core, least core and nucleolus are all manipulable by these moves; Theorem 2 proves no payoff division can simultaneously treat symmetric agents equally, distribute all value and be false-name-proof (since such a rule must agree with Shapley on the examples). Theorem 3: applying any solution concept to the declared skills directly, rather than to agents, is automatically robust to false names, collusion and their combinations, because the rule cannot see who declared what. Building on that, they define the anonymity-proof core by six axioms (Theorems 4-5 characterise it: a payoff function is in the anonymity-proof core iff it satisfies the axioms) and show it can be empty even when every sub-coalition's ordinary core is non-empty (Theorem 6, four-skill counterexample; no three-skill counterexamples exist). Relaxing with an epsilon gives the least anonymity-proof core, which always exists (Theorem 7). Theorem 8: with the Shapley value over agents, deciding whether an agent benefits from false names is NP-complete (reduction from SAT). Read: abstract, introduction and examples, Theorems 2-8 statements with proof sketches, conclusions; omitted proofs not available in the 6-page version.

## Contribution

Shows that standard cooperative solution concepts are false-name and collusion manipulable, that skill-based (identity-blind) accounting fixes this by construction, and defines the (least) anonymity-proof core as the stable, manipulation-robust division concept, with existence and hardness results.

## Key results

- Impossibility: equal treatment + full distribution + false-name-proofness cannot coexist (Theorem 2).
- Identity-blind, skill-based solution concepts are robust to false names and collusion (Theorem 3).
- Anonymity-proof core characterised axiomatically; may be empty (Theorem 6); least anonymity-proof core always exists (Theorem 7).
- Checking profitable false-name splits under Shapley is NP-complete (Theorem 8).

## Methods and models

Characteristic-function games over skills, axiomatic characterisation, counterexamples, NP-completeness reduction.

## Limitations and open questions

Transferable utility only; skills must be verifiable (the rule rewards declared skills, so unverifiable skill claims reopen manipulation); the least anonymity-proof core sacrifices stability by epsilon; proofs omitted in the conference version (fuller treatment in the authors' later Artificial Intelligence journal paper).

## Relevance to us

Directly applicable to any scheme that divides rewards among cooperating agents (task bounties split across a swarm, contribution-based payouts): the result says pay for verifiable contributions (skills), not for identities, and that Shapley-style attribution is both manipulable and hard to audit. Pairs with the voting result [[bachrach-2008-divide]] / [[aziz-2011-false]] (same "identity splitting under Shapley" theme), the auction line [[yokoo-2000-effect]], [[yokoo-2003-characterization]], and the merge/split impossibility in scheduling [[moulin-2007-scheduling]]. Root: [[douceur-2002-sybil]].
