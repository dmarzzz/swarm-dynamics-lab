---
id: horgan-2018-distributed
type: paper
title: Distributed Prioritized Experience Replay
authors:
- Dan Horgan
- John Quan
- David Budden
- Gabriel Barth-Maron
- Matteo Hessel
- Hado van Hasselt
- David Silver
year: 2018
venue: International Conference on Learning Representations (ICLR 2018)
url: https://arxiv.org/abs/1803.00933
doi: null
arxiv: '1803.00933'
cite: Horgan, D., Quan, J., Budden, D., Barth-Maron, G., Hessel, M., van Hasselt, H., & Silver, D. (2018). Distributed Prioritized Experience Replay. International Conference on Learning Representations (ICLR 2018). arXiv:1803.00933.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Ape-X decouples acting from learning in deep RL: hundreds of actors, each running its own copy of the environment with its own exploration rate, add transitions to one shared, centralised replay memory, and a single learner samples from that memory by priority and updates the network, which actors periodically copy. A key design choice is that actors compute the initial priorities of the transitions they submit, using their local copy of the network, instead of the learner assigning maximum priority to new data. Applied to DQN (Atari) and DDPG (continuous control). Read: abstract, introduction, architecture section, the Atari results and table, the scaling and replay-capacity analyses.

## Contribution

Shows that distributing experience generation and prioritising which experience is learned from, rather than distributing gradient computation, is enough to set the state of the art on Atari with a single learner.

## Key results

- Median human-normalised Atari-57 score of 434% (no-op starts) and 358% (human starts), higher than every baseline in Table 1, as I read that table (measured).
- With 360 actors; performance rose consistently from 8 to 256 actors on six games while learner update rate stayed fixed, which the authors attribute to more diverse exploration (measured, hypothesis for cause).
- Larger replay capacity gave a small benefit; replay was soft-limited to 2 million transitions with FIFO removal (measured).
- The authors note experience goes stale more slowly than gradients and can be shared across data centres if the learner is robust to off-policy data (argument).

## Methods and models

Per-actor epsilon-greedy exploration with different epsilons; n-step returns; double Q-learning and dueling networks for the DQN variant. ICLR 2018 (per the PDF header).

## Limitations and open questions

No faulty or adversarial actors considered. The priority of submitted data is computed by the submitting actor and trusted by the learner.

## Relevance to us

Q3: Ape-X is the clearest example of the attack surface the gap brief points to. Each part both contributes experience and declares how important it is; a corrupted actor that reports high priority for its own poisoned transitions gets them replayed disproportionately often, which multiplies the effect of reward poisoning ([[ma-2019-policy]], [[zhang-2020-adaptive]]) beyond its share of actors (inference from the design; not tested). Q2: nothing in the architecture bounds one actor's influence; a k-of-n guarantee would need either learner-side recomputation of priorities or a robust aggregation step like [[fan-2021-fault-tolerant]]. The finding that diverse exploration is what drives the gains is the same reason a parent forks parts into distinct domains, and is what removes the overlap a majority check needs. Related: [[espeholt-2018-impala]], [[nair-2015-massively]].
