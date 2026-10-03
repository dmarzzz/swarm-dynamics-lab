---
id: zhang-2026-asymmetric
type: paper
title: "Asymmetric physics enables efficient learning in quadrupedal robot swarms"
authors: ["Yuang Zhang", "Yunlong Song", "Zhihao He", "Zelin Ni", "Kangyu Wang", "Tianchi Liu", "Yu Hu", "Feng Yu", "Danping Zou", "Weiyao Lin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2606.23153
doi: null
arxiv: "2606.23153"
cite: "Zhang, Y., Song, Y., He, Z., Ni, Z., Wang, K., Liu, T., Hu, Y., Yu, F., Zou, D., & Lin, W. (2026). Asymmetric physics enables efficient learning in quadrupedal robot swarms. arXiv preprint arXiv:2606.23153."
topics: [swarm-robotics, marl-emergence, crowds-and-traffic]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "0 (OpenAlex W7165630637, 2026-10-03); 0 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

This follow-up to [[zhang-2025-learning]] moves differentiable-physics policy learning from drones to legged robots, where contacts make the simulator non-differentiable. The trick ("asymmetric physics") is to roll out in a high-fidelity, non-differentiable simulator (Isaac Gym, Unitree Go2 model) but compute gradients through simple differentiable surrogates. A point mass with a residual term is used for the navigation policy and a single rigid body driven by ground reaction forces for the locomotion policy. The residual between surrogate and true dynamics is treated as constant with respect to the parameters. A hierarchical stack (depth image + goal velocity to velocity command to joint targets) is trained with hundreds of quadrupeds sharing one environment. It runs on up to 512 simulated robots and transfers zero-shot to six real Go2s in five scenes, with no communication.

## Contribution

This is the first demonstration, as the authors frame it, of vision-only learned swarm navigation for quadrupeds under contact-rich locomotion and dense interaction. The methodological point generalises: surrogate gradients plus high-fidelity forward rollouts turn dense multi-robot interaction from a sampling problem into a low-variance training signal.

## Key results

- Sample efficiency (measured, 5 seeds, Fig. 6): reaches PPO's final reward with about 2% of PPO's samples and converges to a higher reward, under identical environments (16-robot position exchange, 48-robot enclosure exit, 32-robot opposing flow through cylinders), the same pretrained locomotion policy and the same reward.
- Scaling (measured): in a circular fence (11.8 m diameter, two 2 m exits, 36 s limit), all robots exit for 24-72 robots, and one fails at 96. Exit time grows sublinearly (96 robots take less than twice the time of 48). In an intersecting-path maze (300 s) with 128-512 robots, all succeed at 128 and fewer than 3% fail at larger N, from retreat-induced turnovers and limbs caught in fences. Time to 75% completion grows roughly proportionally with N.
- Versus PPO (measured): DPL shows faster progress and higher completion from 256 to 512 robots. PPO "retreats" erratically. Realised speed tracks commands from 0.75 to 1.5 m/s for DPL, while PPO saturates. In narrow gaps (5 robots in a line), PPO fails below about 0.8 m, while DPL works down to 0.5 m.
- Versus hand-designed controllers and single-agent transfer (measured qualitatively and with minimum-distance traces): Reynolds flocking with goal and obstacle terms, a depth-binning potential field, and a single-agent-trained vision policy all show less consistent clearance or more conservative detours. The single-agent policy degrades with swarm size.
- Emergent behaviours (observed, not quantified): predictive avoidance, consistent right-side yielding in head-on encounters (no shared frame or convention in the objective), pausing in open areas before bottlenecks, and wall-following arising from the limited field of view.
- Real world (measured, demonstration): six Go2s with forward D435i cameras in a forest, a narrow bridge with two opposing teams of 3, a one-robot-wide gap, a pavilion and a cluttered room. Real deployment uses Unitree's built-in locomotion controller under the learned navigation policy.

## Methods and models

- Navigation surrogate: $p_{k+1}=p_k+v_k\Delta t+r_k$ with $v_k=\pi_\theta(o_k)$, a delay and EMA on outputs, and the residual $r_k$ ignored in gradients, giving $\partial p_k/\partial\theta=\sum_i \Delta t\,\partial\pi_\theta(o_{i-1})/\partial\theta$.
- Locomotion surrogate: single rigid body with ground reaction forces from PD torques via $J_i^\top f_i=\tau_i$. Losses cover velocity, orientation, angular velocity, height, gravity projection, action, torque and swing-leg terms (appendix).
- Training: Isaac Gym, gradient accumulation over $S_n$ (navigation) and $S_l$ (locomotion) steps, AdamW. Each robot knows only its own egocentric goal and sees others only through depth images.
- Code and data are shared via Google Drive links in the paper, not a git repository.

## Limitations and open questions

- Robots navigate to individual goals. There is no flocking or shared objective, and collective order is not measured. The "swarm" behaviour is crowd-like conflict resolution, which is why I tag crowds-and-traffic.
- The real-world tests are demonstrations with 4-6 robots, not statistical trials, and they rely on the vendor locomotion controller rather than the learned one.
- Ignoring the residual's dependence on the policy is an approximation justified only empirically.
- Failure modes at scale (dead ends, physical contact, sudden retreats) remain.

## Relevance to us

This paper makes a strong case that the differentiable-surrogate trick scales to hundreds of embodied agents and gives better sample efficiency than PPO by about 50x. The emergent right-side yielding is a symmetry-breaking convention worth studying on its own: how and why does a convention emerge in a decentralised learner population? That links to lane formation and pedestrian conventions in [[helbing-1995-social]] and related crowd literature. Compare [[huang-2024-collision]] (model-free) and [[mednikov-2026-calibrate]] (mixed fidelity).

## Notes from dmarz/swarm-robotics-recent-audit

Audited 2026-10-03 against the arXiv HTML (2606.23153). Checked 2% of PPO samples, the 11.8 m fence with two 2 m exits and a 36 s limit for 24-96 robots, the 128-512-robot maze with under 3% failures, the 0.75-1.5 m/s command sweep, PPO failing below 0.8 m gaps while DPL works to 0.5 m, and the four emergent behaviours. All match. No corrections needed. Citation count now from OpenAlex.
