---
id: huttenrauch-2019-deep
type: paper
title: Deep Reinforcement Learning for Swarm Systems
authors: [Maximilian Hüttenrauch, Adrian Šošić, Gerhard Neumann]
year: 2019
venue: Journal of Machine Learning Research
url: https://jmlr.org/papers/v20/18-476.html
doi: null
arxiv: '1807.06613'
cite: Hüttenrauch, M., Šošić, A., & Neumann, G. (2019). Deep reinforcement learning for swarm systems. Journal of Machine Learning Research, 20(54), 1–31.
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "152 for the arXiv record plus 120 for the JMLR record (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The paper asks how a decentralised policy for a swarm of identical agents should represent what it sees of its
neighbours, given that the neighbours are interchangeable and their number changes. Concatenating neighbour
observations (as MADDPG-style methods do) breaks permutation invariance and fixes the input size. The authors
treat each neighbour observation as a sample from a distribution and feed the policy the empirical mean
embedding of those samples, with the feature map either a histogram, a radial basis function grid, or a small
neural network trained end to end. With parameter-shared TRPO (centralised learning, decentralised execution)
on unicycle agents, the learned neural mean embedding learns faster and reaches better policies than
histogram, RBF, concatenation, softmax pooling or max pooling, on rendezvous and pursuit-evasion tasks, and the
policies transfer to swarm sizes not seen in training.

## Contribution

It is the standard reference for permutation-invariant, size-invariant observation encoders in swarm RL, the
"mean embedding" counterpart of Deep Sets (Zaheer et al. 2017) applied inside deep MARL. It sits between
mean-field MARL [[yang-2018-mean]], which averages neighbours' actions inside the Q-function, and the
centralised critics of [[lowe-2017-multi]], which scale poorly with agent number. It builds on the swarm MDP
formalism of Šošić et al. (2017).

## Key results

- Rendezvous, 20 agents, global observability, double-integrator unicycles: all encodings eventually succeed;
  the neural mean embedding of the extended feature set (distance, bearing, relative orientation, relative
  velocity) is about 10% better in average return than NN or RBF embeddings of distance and bearing alone, and
  roughly halves steady-state mean inter-agent distance (about 4e-2 versus 8e-2), reaching a given distance
  about 25% sooner (measured). Histogram and RBF encodings of the extended set failed to learn at all, because
  their input dimension grows exponentially with feature dimension.
- A policy trained with 20 agents still performs rendezvous with 100 agents; the NN embedding is again fastest.
  The hand-tuned consensus PD controller eventually drives distance to zero while the learned policies leave a
  small residual, but the learned policies contract faster and score higher return.
- Local observability (cut-off radius 40 in a 100x100 world): adding a simple communication channel (each agent
  broadcasts its neighbourhood size) raises return; policies trained with 20 agents still work, worse, with 10.
- Pursuit-evasion with an evader twice as fast as the pursuers on a torus: the learned strategy first spreads
  pursuers to stop the evader enlarging its Voronoi cell, then encircles and closes in. Policies trained with
  10 pursuers capture faster with 20 and 50, but all methods struggle with 5 because the ring has gaps.
- 50 pursuers versus 5 evaders: concatenation becomes unlearnable; the NN mean embedding beats RBF and beats
  hand-built moment features (mean, standard deviation, skew, kurtosis).
- Pooling comparison: mean embedding found the capturing solution in 10 of 16 seeds, softmax pooling 6/16,
  max pooling 4/16.
- Compute: 4 to 6 hours of training for 20 agents on a 10-core machine; about 1 ms per forward pass.

## Methods and models

Swarm MDP (a homogeneous Dec-POMDP). Agents are unicycles with single- or double-integrator dynamics
(x' = v cos phi, y' = v sin phi, phi' = omega). Agent i receives a set O_i = {o_ij} of neighbour features over
a fully connected graph (global) or a Delta-disk proximity graph (local), and the policy input is
mu_i = (1/|O_i|) sum_j phi(o_ij) concatenated with local features (distance and bearing to the nearest wall,
own neighbourhood size). phi is one 64-unit ReLU layer for the NN variant. Optimisation is parameter-shared
TRPO (OpenAI baselines), 10 MPI workers x 2048 steps, subsampling 8 agents' data per iteration (163,840
samples per update). Baselines: consensus protocol x_i' = -sum_j (x_i - x_j) with a PD wrapper, and the
Voronoi-minimising pursuit strategy of Zhou et al. (2016). Code: https://github.com/LCAS/deep_rl_for_swarms

## Limitations and open questions

Rewards are global and hand-shaped; agents are identical; only cooperative tasks are tested, with a fixed,
scripted evader. Learning curves report the median of the top five of 16 seeds, which flatters stability. No
physical robots. The paper does not study what collective order the policies produce (no order parameters),
only task return. Whether mean pooling loses information that matters for larger or denser swarms (it
discards neighbour count unless that is fed separately) is open.

## Relevance to us

This is the default observation architecture to copy for any learned-swarm experiment at the hackathon:
permutation-invariant mean embedding plus parameter sharing gives size transfer for free. Pair with
[[yang-2018-mean]] for the mean-field view, [[durve-2020-learning]] for a physics reading of what a learned
swarm policy is, and [[lowe-2017-multi]] as the concatenation baseline it beats.
