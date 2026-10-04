---
id: kamenica-2011-bayesian
type: paper
title: Bayesian Persuasion
authors:
- Emir Kamenica
- Matthew Gentzkow
year: 2011
venue: American Economic Review 101(6)
url: https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf
doi: 10.1257/aer.101.6.2590
arxiv: null
cite: 'Kamenica, E., & Gentzkow, M. (2011). Bayesian Persuasion. American Economic Review, 101(6), 2590-2615. https://doi.org/10.1257/aer.101.6.2590'
topics:
- meta
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: '1526 (Semantic Scholar) / 2012 (OpenAlex), both 2026-10-03'
code: []
---

## Summary

A Sender commits in advance to a signal, meaning an information structure mapping states of the world to observable realisations; a Receiver sees the realisation, updates by Bayes' rule, and takes an action that both care about. The Sender cannot lie or pay the Receiver, only choose what information exists. The paper's move is to recast the Sender's problem as choosing a distribution over the Receiver's posterior beliefs, constrained only by Bayes plausibility, that the expected posterior equals the prior. Proposition 1 establishes that this reformulation loses nothing and that attention can be restricted to straightforward signals, which recommend an action the Receiver then follows. Corollary 2 then gives the characterisation the paper is known for: the value of an optimal signal is the concave closure of the Sender's indirect value function evaluated at the prior, and the Sender benefits from persuasion exactly when that concave closure exceeds the function itself at the prior.

## Contribution

It establishes that a rational, fully aware Receiver can be systematically moved by a Sender who controls only the information environment, and reduces the whole design problem to a geometric one, concavification, which is why the result became the standard tool for information design.

## Key results

- The motivating example is exact: prior probability of guilt 0.3, a prosecutor who gains from conviction regardless of truth, a judge who wants to match the state. Full disclosure yields conviction 30% of the time. The uniquely optimal binary investigation is pi(i|innocent) = 4/7, pi(g|innocent) = 3/7, pi(i|guilty) = 0, pi(g|guilty) = 1, which makes the judge convict 60% of the time even though she knows 70% of defendants are innocent and knows the investigation was designed to maximise convictions.
- Proposition 1: there exists a signal with value v* if and only if there exists a straightforward signal with that value, if and only if there exists a Bayes-plausible distribution of posteriors whose expected Sender payoff is v*.
- Corollary 2: the value of an optimal signal is V(mu_0), the concave closure of the Sender's indirect value function; the Sender benefits from persuasion if and only if V(mu_0) > v-hat(mu_0).
- Remark 1: if v-hat is concave the Sender never benefits for any prior; if it is convex and not concave the Sender benefits for every prior. No disclosure is optimal when the Sender's payoff is concave in the Receiver's beliefs, full disclosure when it is convex.
- Proposition 2: if there is no information the Sender would share, the Sender does not benefit; if there is such information and the Receiver's preference is discrete at the prior, the Sender does benefit. With a finite action space, the Receiver's preference is discrete at the prior generically.
- Proposition 3: when the Sender's payoff depends only on the expected state, the Sender benefits if and only if the concave closure of that reduced function exceeds it at the prior; the paper gives an explicit counterexample showing that value is only an upper bound, not the value of the optimal signal.
- Propositions 4 and 5: an optimal signal that induces a belief leading to the Sender's worst action makes the Receiver certain of her action there; and at an interior belief, or one leading to a best-attainable action, the Receiver is not strictly preferring, meaning she is indifferent between two actions.
- Preference alignment: more aligned preferences weakly raise the Sender's payoff, but can make the optimal signal either more or less informative, so greater alignment can reduce the amount of information actually communicated. This is the opposite of the standard cheap-talk intuition.

## Methods and models

Pure theory. Finite state space, compact action space, continuous utilities, common prior, Sender-preferred subgame perfect equilibrium as the solution concept. The central assumption is commitment: the Sender picks the signal before seeing its realisation and the realisation is truthfully reported. The paper argues this is reasonable where disclosure is legally mandated (Brady v. Maryland for prosecutors), where a rule must be fixed in advance (grading policies, rating procedures, registered clinical trial designs), or where the test is publicly observable (taste tests, software trials). The online appendix extends the characterisation to compact metric state spaces and shows the Sender's gain here upper-bounds the gain in any alternative communication game. Applications worked in the paper include a lobbyist commissioning a study to influence a benevolent politician, and a seller providing free trials. Read here through the published version hosted on the second author's university page; the publisher landing page at aeaweb.org was also loaded and confirms journal, volume, issue, pages and DOI, while pubs.aeaweb.org returned HTTP 403.

## Limitations and open questions

Commitment is the binding assumption and the authors spend a subsection defending it; without it the results are an upper bound rather than a prediction. One Sender, one Receiver, common prior, no private Receiver information in the main model (extensions are sketched in the final section, including multiple receivers). Nothing here is measured; it is a characterisation theorem, and the prosecutor numbers are an illustration, not data.

## Relevance to us

This is the formal account of the mechanism the LLM attack papers demonstrate empirically. An agent that selects what evidence enters a shared context, without lying, is a Sender choosing a signal, and concavification says exactly when that is worth doing: when the Sender's payoff as a function of the group's belief is not concave at the current prior. For a hackathon project this converts into a predictive test rather than a vocabulary - estimate the collective's payoff-relevant belief, estimate the induced action, and the theory says where influence should and should not pay off, which is a falsifiable prediction to run against a debate harness. Two specific transfers: Proposition 4 and 5 give signatures of an optimal manipulation (the group is made certain where it takes the manipulator's worst action, and indifferent where it takes a good one), which are detectable; and the alignment result warns that making agents more similar can increase rather than decrease how much a manipulator can get away with, which contradicts the obvious defence of homogenising a swarm. Read against the empirical persuasion results in [[kraidia-2026-when]] and the content-selection attacks in [[nestaas-2024-adversarial]], and against the belief-aggregation baselines [[degroot-1974-reaching]] and [[hegselmann-2002-opinion]].
