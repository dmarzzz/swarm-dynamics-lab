---
id: blanchard-2017-byzantine
type: paper
title: Byzantine-Tolerant Machine Learning
authors:
- Peva Blanchard
- El Mahdi El Mhamdi
- Rachid Guerraoui
- Julien Stainer
year: 2017
venue: arXiv preprint
url: https://arxiv.org/pdf/1703.02757
doi: null
arxiv: '1703.02757'
cite: 'Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. (2017). Byzantine-Tolerant Machine Learning. arXiv preprint arXiv:1703.02757.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Founding paper of Byzantine machine learning (arXiv v1, all sections read, proof algebra skimmed; the conference version appeared under a different title and was not opened). A parameter server aggregates gradient vectors from n workers, up to f of which are Byzantine with full knowledge and collusion. Lemma 1: any aggregation that is a linear combination with non-zero weights, including averaging, can be steered to any vector by a single Byzantine worker. Choosing the vector closest to all others also fails for f >= 2, because colluders can drag the barycenter. Krum instead scores each vector by the sum of squared distances to its n - f - 2 nearest neighbours and picks the lowest score. If 2f + 2 < n and gradient noise is small relative to the gradient, Krum satisfies (alpha, f)-Byzantine resilience and SGD reaches a region where the gradient is small, in O(n^2 (d + log n)) time.

## Contribution

Defines the first resilience property for aggregation under Byzantine workers and gives a rule (Krum, and m-Krum) that meets it, establishing the n > 2f + 2 regime for robust aggregation by a trusted aggregator.

## Key results

- Proved: averaging tolerates zero Byzantine workers (Lemma 1).
- Proved: Krum is (alpha, f)-Byzantine resilient for 2f + 2 < n with sin(alpha) = eta(n, f) sqrt(d) sigma / ||g||, where eta(n, f) = O(n) when f = O(n).
- Proved: almost-sure convergence of the gradient norm to zero under standard SGD assumptions (Proposition 2).
- Open (stated by the authors): whether 2f + 2 < n is tight; tolerance of asynchrony; reducing the O(n) factor.

## Methods and models

Synchronous rounds, reliable parameter server, i.i.d. unbiased honest gradients with bounded moments. Resilience defined by an angle condition on E[F] versus the true gradient plus moment bounds. Convergence by a quasi-martingale argument. The v1 has no experiments.

## Limitations and open questions

The guarantee needs honest vectors to be i.i.d. and tightly clustered relative to the signal; [[el-mhamdi-2018-hidden]] and [[baruch-2019-little]] show attacks that stay within the honest spread in high dimension, and [[karimireddy-2020-byzantine]] shows failure under heterogeneous (non-i.i.d.) honest data.

## Relevance to us

Q2. The cleanest statement that plain merging (averaging) of sub-agent contributions gives an attacker total control with one corrupted part, and that distance-based selection can raise the bar to roughly f < n/2 under independence assumptions. For fork-merge the key assumption to examine is i.i.d. honest contributions: sub-agents sent to different domains return deliberately non-identical updates, which is the heterogeneous case where these rules weaken. Survey context: [[guerraoui-2024-byzantine]]. LLM transfers: [[jo-2025-byzantine]], [[lee-2026-robust]].
