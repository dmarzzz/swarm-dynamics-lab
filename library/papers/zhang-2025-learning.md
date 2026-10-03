---
id: zhang-2025-learning
type: paper
title: "Learning vision-based agile flight via differentiable physics"
authors: ["Yuang Zhang", "Yu Hu", "Yunlong Song", "Danping Zou", "Weiyao Lin"]
year: 2025
venue: "Nature Machine Intelligence"
url: https://arxiv.org/html/2407.10648
doi: "10.1038/s42256-025-01048-0"
arxiv: null
cite: "Zhang, Y., Hu, Y., Song, Y., Zou, D., & Lin, W. (2025). Learning vision-based agile flight via differentiable physics. Nature Machine Intelligence, 7(6), 954-966. https://doi.org/10.1038/s42256-025-01048-0 (preprint: arXiv:2407.10648, 'Back to Newton's Laws: Learning Vision-based Agile Flight via Differentiable Physics')."
topics: [swarm-robotics, marl-emergence, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "62 (Crossref, 2026-10-03); 118 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

The authors train a single end-to-end neural policy (depth image + attitude, optionally velocity, to desired thrust acceleration) for quadrotor navigation by backpropagating a hand-written, differentiable loss straight through a deliberately crude simulator: a point-mass model with a calibrated first-order control lag, quadratic drag and a CUDA depth renderer of random planes, cuboids, spheres and cylinders. The same recipe, with other drones rendered as spherical obstacles, yields a decentralised swarm policy. Six real drones swap sides through a narrow gate and fly through clutter with no communication and no global planner, and the authors report emergent waiting, following and giving way although no coordination term appears in the loss. Single-agent flights reach 20 m/s in a forest on a $21 ARM board. I read the arXiv v2 HTML in full; the published Nature Machine Intelligence version carries the shorter title above.

## Contribution

This is the first real-world quadrotor system trained by differentiable physics rather than RL or imitation, and the first to show that one physics-driven objective scales from single-agent agile flight to communication-free swarm navigation. It sits between mapping-and-planning swarm stacks such as EGO-Swarm v2 ("Swarm of micro flying robots in the wild", Science Robotics 2022) and model-free RL swarm controllers such as [[batra-2022-decentralized]] and [[huang-2024-collision]], and it argues that a low-fidelity but differentiable model beats a high-fidelity black box for sample efficiency.

## Key results

- Single agent, simulation benchmark (Flightmare/AirSim, 10 trials per speed, measured): 90% success through complex environments against 60% for the previous state of the art (Agile, Loquercio et al. 2021). Mapping-based EGO-v2 degrades sharply as target speed rises.
- Real world (measured): up to 20 m/s in a forest, which the authors describe as double the speed of the imitation-learning baseline. About 7 m/s with high success through dense urban obstacles. Avoids moving obstacles (a closing gate, swinging objects) although training used only static obstacles.
- Sample efficiency (measured, Fig. 8E): reaches PPO's maximum reward with about 10% of PPO's samples under the same parallel setup.
- Ablations (measured): plain BPTT without temporal gradient decay converges more slowly and reaches lower success. Higher-resolution depth helps in training but hurts at test time, which the authors attribute to overfitting and sim-to-real depth noise.
- Swarm (measured, 6 custom 3-inch FPV quadrotors in two groups of 3 swapping through a gate): all six reached their goals. In simulation, success rate and flight time match the communication-based EGO-v2 while flying faster (Fig. 6F-G). The emergent waiting, following and retreating behaviours are qualitative observations from video, not quantified.
- Odometry-free variant (measured, 10 trials each at 3 speeds): matches VICON-fed policies and beats VIO-fed policies, which fail more often at high speed.

## Methods and models

- Problem: discrete-time dynamics $x_{t+1}=f(x_t,u_t)$, observation $o_t=h(x_t)$, policy $u_t=\pi_\theta(o_t)$, loss $L=\frac{1}{T}\sum_t c(x_t,u_t)$. The policy gradient is computed analytically through the simulator Jacobians, not estimated from rollouts.
- Dynamics: point mass, $v_{t+1}=v_t+a_t\,dt$, $p_{t+1}=p_t+v_t\,dt+\tfrac12 a_t dt^2$, with actual thrust equal to the desired thrust delayed by a fixed latency and passed through an exponential moving average, plus quadratic drag. Delay and drag coefficients are calibrated from real flights (Supplement S1); drag is randomised around the calibrated value during training.
- Loss: smooth-L1 velocity tracking against a 2 s moving-average velocity, an obstacle term equal to approach speed times (truncated quadratic + softplus barrier) on the distance to the nearest obstacle point, and acceleration/jerk smoothness penalties.
- Temporal gradient decay: the state-to-state gradient is multiplied by $e^{-\alpha\,dt}$ at each step backwards (decay rate 0.92 per step), which stops exploding gradients and focuses learning on obstacles inside the sensing horizon.
- Network: small CNN (32-64-128 filters) on a max-pooled, inverted low-resolution depth map, fused with target velocity and attitude into a 192-d feature, then a GRU and a linear head. AdamW, lr 1e-3 with cosine decay, batch of 64 environments, 150 steps at 15 Hz, 50,000 iterations.
- Hardware: 3-inch FPV quadrotor, thrust-to-weight 3.6, BetaFlight, RealSense D435i, Mango Pi (Cortex-A53) companion computer.
- Multi-agent: identical training loop with each other agent rendered as a sphere. At deployment each drone runs the policy independently. Motion capture supplies only each drone's own velocity reference in the gate-swap test.
- Code: the authors' repository is https://github.com/HenryHuYu/DiffPhysDrone (seen on the search results page; not opened in this session).

## Limitations and open questions

- The swarm experiments are small (6 drones) and partly rely on motion capture for each drone's own velocity. Scaling with N, density and speed is not reported. The emergent social behaviours are anecdotal.
- Collaboration comes for free only because neighbours are treated as moving obstacles. There is no alignment or cohesion term, so this is collision-free co-navigation rather than flocking. Whether flocking order parameters emerge was not measured.
- The point-mass simplification works for the agile regime tested. Its limits (aggressive attitude manoeuvres, wind) are not mapped.
- The comparison with EGO-v2 is in simulation. Real-world head-to-head swarm comparisons are absent.

## Relevance to us

This is a strong template for a hackathon experiment: a differentiable point-mass swarm simulator where one designs a local loss and backpropagates. It is cheap, GPU-friendly and has real-world evidence behind it. It pairs with the later quadruped extension [[zhang-2026-asymmetric]], with model-free RL swarms [[huang-2024-collision]] and [[choi-2026-communication]], and with the mixed-fidelity point-mass training of [[mednikov-2026-calibrate]]. An open question we could test: does adding a weak alignment loss to this framework produce a Vicsek-like order-disorder transition, as hand-tuned gains do in [[verdoucq-2025-flocking]]?
