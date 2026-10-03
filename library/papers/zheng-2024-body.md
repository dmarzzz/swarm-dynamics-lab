---
id: zheng-2024-body
type: paper
title: "Body orientation change of neighbors leads to scale-free correlation in collective motion"
authors: ["Zhicheng Zheng", "Yuan Tao", "Yalun Xiang", "Xiaokang Lei", "Xingguang Peng"]
year: 2024
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-024-53361-8
doi: "10.1038/s41467-024-53361-8"
arxiv: null
cite: "Zheng, Z., Tao, Y., Xiang, Y., Lei, X., & Peng, X. (2024). Body orientation change of neighbors leads to scale-free correlation in collective motion. Nature Communications, 15(1), 8968."
topics: [collective-motion, swarm-robotics, criticality-measurement]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "22 (OpenAlex W4403510590, 2026-10-03)"
code: []
---
## Summary

The authors propose that the change in a neighbour's apparent body orientation (BOC), measured from the focal animal's own view as the rate of change of the angular width of the neighbour's silhouette (with a frontal weighting term), is the visual cue animals use to pick whom to follow. In 444 spontaneous U-turns of rummy-nose tetra groups (44 with 10 fish, 400 with 8 fish; public data of Lecheval et al.), a fish's BOC-based motion salience correlates with its leadership in a time-lagged leader-follower network (Spearman rho peaks near 1 when a frontal preference is included), much more than distance or bearing change do. They then build a model where each agent aligns only with the visible neighbour of largest BOC, and test it in pybullet simulations (collective spin, collective turn) and on 50 real SwarmBang robots. BOC-based selection gives fast information transfer whose speed grows with group size and a correlation length that grows linearly with group size (scale-free correlation); a random-neighbour baseline does neither.

## Contribution

A first-person, vision-computable cue for selective interaction that links empirical leadership in fish, scale-free correlations (as in starlings) and a practical robot controller. Extends the motion-salience line of [[xiao-2024-perception]] from birds to fish and robots.

## Key results

- Measured (fish): BOC salience positively correlated with leadership during U-turns when frontal preference alpha >= 1; with alpha = 0 the correlation peak is near 0; frontal preference alone gives rho peak only 0.3-0.5.
- Measured (fish): distance-based and bearing-change-based salience correlate much more weakly with leadership.
- Simulation: correlation length r0 proportional to group spatial size for BOC interaction, roughly constant for random interaction; information transfer speed increases with N (avalanche-like) only for BOC.
- Robots (50, plus 20 and 30): BOC swarm follows successive 90 degree turns of an informed robot; random baseline and a Vicsek-average baseline respond worse; correlation length grows with swarm size.

## Methods and models

Ellipse bodies with occlusion; BOC g_ij(T, tau) = sum over a window of |beta_j(t) - beta_j(t-1)|/dt times fp(t), fp = ((1 + v_i . x_ij)/2)^alpha. Leadership from the directional alignment function (time lag maximising heading correlation) and normalised out-degree. Swarm model: constant speed, v_i(t+1) = v_i(t) + k_a v_j(t) for the neighbour j with max BOC within R_visual, plus soft repulsion. Robots are tracked by a NOKOV motion capture system; vision is simulated on the server with a pinhole camera model (bounding-box area change as the BOC proxy), so the robots do not use onboard cameras. Code: https://github.com/DerekZhengEvosil/Body_orientation_change_of_neighbors_leads_to_scale_free_correlation ; fish data at Dryad 10.5061/dryad.9m6d2.

## Limitations and open questions

The robots' "vision" is simulated centrally from motion capture, not onboard. Agents are assumed to know the chosen neighbour's velocity. One neighbour only. The correlation length is defined as the first zero of C(r), which for finite groups is partly forced by the zero-sum of fluctuations, so "scale-free" here should be read cautiously (the same caveat applies to starling analyses). Fish analysis rests on assuming a leader exists in each U-turn.

## Relevance to us

Directly usable selective-attention rule for a hackathon swarm sim and a benchmark (collective turn responsiveness, correlation length vs size). Compare with [[xiao-2024-perception]], [[puy-2024-selective]] (fish attend to faster neighbours), [[mezey-2025-purely]] (onboard vision robots), and [[hang-2026-self]] (loss of scale-free correlation before fragmentation).
