---
id: ben-zion-2023-morphological
type: paper
title: "Morphological computation and decentralized learning in a swarm of sterically interacting robots"
authors: ["Matan Yah Ben Zion", "Jeremy Fersula", "Nicolas Bredeche", "Olivier Dauchot"]
year: 2023
venue: "Science Robotics"
url: https://arxiv.org/abs/2111.06953
doi: "10.1126/scirobotics.abo6140"
arxiv: "2111.06953"
cite: "Ben Zion, M. Y., Fersula, J., Bredeche, N., & Dauchot, O. (2023). Morphological computation and decentralized learning in a swarm of sterically interacting robots. Science Robotics, 8(75), eabo6140."
topics: [swarm-robotics, active-matter, marl-emergence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "66 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Most robot swarms avoid contact, which caps their density. The authors design "Morphobots": Kilobots inside a
3D-printed exoskeleton with two flexible legs and one stiff leg, which makes them about ten times faster
(v0 about 5 cm/s versus 0.53 cm/s) and, crucially, sets how they reorient under an external force. Two mirror
designs, "aligners" and "fronters", move identically when free but turn toward or against a force. A single
signed parameter kappa from the active-matter self-aligning model captures this. On a tilted plane aligners go
downhill and fronters climb; at a wall aligners slide along it while fronters push into it; groups of fronters
push a movable disk. In collective phototaxis with 64 robots and a lit spot covering 6% of the arena, fronters
fill the spot while aligners leave a hollow, and the gap grows with swarm size in simulations up to 8192
agents. A decentralised social-learning scheme (robots copy the policy of an encountered robot with higher
reward) learns phototaxis despite a sparse, intermittent network, because collisions keep the swarm mixed.

## Contribution

It imports the self-aligning active particle model into swarm robotics as a design rule: one measurable
morphological parameter (kappa) predicts collision outcomes and therefore collective performance in crowded
swarms. It is the bridge paper between robotic active matter ([[baconnier-2022-selective]],
[[boudet-2021-collections]], [[deblais-2018-boundaries]]) and distributed swarm learning and embodied evolution
([[kuckling-2023-recent]]).

## Key results

- Measured: kappa_aligner approximately -kappa_fronter approximately 0.06 cm^-1 (about 0.3 per body diameter
  d = 4.8 cm), fitted from orientation relaxation on 3 and 6 degree inclines with theta(s) = 2 atan(exp(-kappa s)).
- Measured: near a wall of stationary robots both designs spend about 3 tau_p (about 1 min) but aligners travel
  twice as far along it.
- Measured (N = 64, 4 runs each): early phototaxis follows a diffusion-limited (Smoluchowski) rate for both
  designs (effective diffusion constant D_eff of about 4.22, printed in the text as cm/s; units ambiguous); after about 10 min a first layer of robots forms at the spot edge and
  fronters then outperform aligners in the fraction in the light F.
- Simulated: time to get half the swarm into the light, T_1/2, grows steeply with N for aligners but only
  mildly for fronters (N up to 8192): morphology matters more at scale.
- Measured: with random initial policies, the learning swarm reaches F about 0.4 (8 times the 6% expected by
  chance); simulations show fronters later reach F about 0.55 while aligners stay at about 0.4.
- Claimed by scaling argument: bare Kilobots, being ten times slower (diffusion scales with v0^2), would take
  100 times longer and could not learn in practice.

## Methods and models

Overdamped self-aligning dynamics: dr/dt = v = v0 n + mu f, dn/dt = kappa (n x v) x n. For a constant force
this reduces to an overdamped pendulum d theta/dt = -kappa mu f sin theta. Robots run-and-tumble (tau_run 2 s,
tau_tumble 4 s, persistence about 18 s). Phototaxis: stop when the light sensor exceeds a threshold. Learning:
each robot runs a perceptron policy and broadcasts (weights, reward); a receiver adopts the policy if the
sender's reward is higher. Reward is the robot's time-averaged light exposure, which by good mixing
approximates the ensemble fraction F (time average approximately ensemble average). Arena 150 cm diameter,
Kilobot IR range 7 cm, mean spacing over 16 cm, so the network is sparse and intermittent. Brownian-dynamics
simulations of active soft discs; tracking with trackpy. No public code repository is given in the paper.

## Limitations and open questions

Learning was shown on a single, low-dimensional task, and the "fake news" problem (lucky robots spreading bad
policies) is handled only through the choice of reward. Long-time and large-N claims come from simulation,
not hardware. The authors note that switching between dense and sparse regimes, and richer social or cultural
learning, are open. kappa is measured empirically per design, not derived from mechanics (later addressed
in [[arbel-2024-mechanical]]).

## Relevance to us

A clean, quantitative example of embodied physics changing collective outcomes, with a one-parameter knob that
a hackathon simulation can sweep (sign and magnitude of kappa versus density). Its "mixing makes time
averages equal ensemble averages" argument for decentralised learning is directly reusable. Related:
[[rubenstein-2012-kilobot]], [[chvykov-2021-low]], [[li-2019-particle]], [[huttenrauch-2019-deep]].
