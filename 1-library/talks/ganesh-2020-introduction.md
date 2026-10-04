---
id: ganesh-2020-introduction
type: talk
title: "Lecture 8: Introduction to consensus, and the de Groot model"
authors: [Ayalvadi Ganesh]
year: 2020
url: https://www.youtube.com/watch?v=qeL1zN3AajQ
venue: "Recorded university lecture (stochastic processes on networks unit, level 3/4 and MSc), posted on the lecturer's YouTube channel 26 October 2020, 50 min"
topics: [sync-consensus, collective-decision]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

A clean one-lecture treatment of the DeGroot averaging model and exactly when it reaches consensus, from a course on stochastic processes on networks (the previous lecture covered rumour spreading, the next one discrete-valued voter-type consensus). Read from the full auto-generated transcript; the channel name gives the lecturer, the institution is not stated on the page. Timestamps approximate.

- 00:03 to 15:35: motivation. Galton's ox-weighing crowd (the average of guesses close to the true weight), honeybee nest-site choice without a leader, bacterial quorum sensing, flocking and schooling without follow-the-leader, and engineering uses: sensor networks fusing noisy readings, consistency of replicated databases and blockchains. He explicitly sets polarisation and fake-news persistence aside as phenomena the averaging model does not capture (11:12).
- 15:35 to 22:10: the model (attributed to DeGroot, a social scientist). Discrete time, continuous opinions, x(t+1) = P x(t) with P row-stochastic and non-negative: each agent has a "fixed budget of trust of total one" split over neighbours, typically keeping substantial self-weight. Trust is never negative in this model.
- 22:10 to 39:46: analysis via Perron-Frobenius. Solution x(t) = P^t x(0); consensus requires the all-ones vector to be the unique principal eigenvector with a spectral gap. He states the Perron-Frobenius theorem for primitive non-negative matrices (eigenvalue 1 simple, positive eigenvector, strict spectral gap), and shows the primitivity condition is equivalent to the Markov chain with transition matrix P being irreducible and aperiodic; a periodic chain of period m has all m-th roots of unity as eigenvalues and opinions cycle instead of converging (37:33).
- 39:46 to 45:05: rate and limit. Distance to consensus decays like |lambda_2|^t (modulo Jordan-block subtleties). Since pi P = pi for the stationary distribution, pi . x(t) is conserved, so the consensus value is pi . x(0): a weighted average with weights given by the stationary distribution.
- 45:05 to 48:44: interpretation. Influence of agent i on the final opinion is pi_i. For uniform weights 1/deg(i) on an undirected graph, pi is proportional to degree, so "popular nodes have more influence". Open directions flagged for student presentations: time-varying weight matrices, random switching, and an adversary rewiring the weights to prevent consensus (48:44).

Everything here is standard textbook material presented carefully; no original claims. The lecture does not cite papers by name on the audio apart from DeGroot and Galton.

## Relevance to us

Short, correct reference for the linear consensus baseline that every richer model (bounded confidence, Kuramoto, Byzantine agreement) is measured against. Two points transfer directly to agent swarms: (1) the final collective answer is pi . x(0), so whoever holds stationary-distribution mass controls the outcome, which is the quantitative version of a Sybil or influence attack on an averaging swarm (an attacker needs weight in pi, not head count); (2) consensus can fail purely for structural reasons (reducible or periodic interaction graphs) even with fully honest agents. The flagged adversarial-rewiring setting is exactly the fork-merge / corrupted-sub-agent threat in linear form. Primary sources: [[degroot-1974-reaching]]; the networked-control continuous-time analogue is [[olfati-saber-2004-consensus]] and [[olfati-saber-2007-consensus]], discrete-time switching topologies [[jadbabaie-2003-coordination]], [[moreau-2005-stability]], [[ren-2005-consensus]]; bounded-confidence departure from this model [[hegselmann-2002-opinion]].
