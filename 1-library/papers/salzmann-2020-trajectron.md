---
id: salzmann-2020-trajectron
type: paper
title: 'Trajectron++: Dynamically-Feasible Trajectory Forecasting with Heterogeneous Data'
authors:
- Tim Salzmann
- Boris Ivanovic
- Punarjay Chakravarty
- Marco Pavone
year: 2020
venue: Computer Vision – ECCV 2020 (Lecture Notes in Computer Science)
url: https://arxiv.org/abs/2001.03093
doi: 10.1007/978-3-030-58523-5_40
arxiv: '2001.03093'
cite: 'Salzmann, T., Ivanovic, B., Chakravarty, P., & Pavone, M. (2020). Trajectron++: Dynamically-Feasible Trajectory Forecasting with Heterogeneous Data. In Computer Vision – ECCV 2020, Lecture Notes in Computer Science, 683–700. Springer. https://doi.org/10.1007/978-3-030-58523-5_40'
topics:
- crowds-and-traffic
- swarm-robotics
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 927 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

A graph-structured recurrent conditional VAE that forecasts the future trajectories of a variable number of heterogeneous agents (pedestrians, vehicles) in a scene. Each agent is a node; edges encode interactions aggregated per semantic class; a discrete latent variable captures high-level behaviour modes. Instead of outputting positions directly, the decoder outputs control inputs that are integrated through agent-specific dynamics models (single integrator for pedestrians, unicycle for vehicles), so samples are dynamically feasible. Optional inputs are semantic maps and the ego robot's planned motion. It reports large gains over earlier deterministic and generative predictors on ETH/UCY and nuScenes.

## Contribution

Brings dynamics constraints, heterogeneous agent types and planner conditioning into learned multi-agent prediction, making it usable inside robot planners. Successor to [[gupta-2018-social]] and [[alahi-2016-social]] on the same benchmarks, and the standard learned baseline for crowd forecasting in robotics.

## Key results

Measured on ETH/UCY (8 observed, 12 predicted steps, leave-one-scene-out):
- Most-likely single output: average ADE/FDE 0.38/0.93 m (0.37/0.91 with dynamics integration), versus 0.72/1.54 for Social LSTM and 0.79/1.59 for linear; the authors cite a 33% improvement in mean FDE over prior approaches.
- Best of 20 samples: average ADE/FDE 0.19/0.41 m (versus Social LSTM 0.47/0.92 in this table).
- KDE-based NLL (2000 samples): average −0.74 (−1.14 with integration) versus 1.79 for the next-best generative baseline listed.
- nuScenes vehicles: FDE at 1, 2, 3, 4 s of 0.18, 0.57, 1.25, 2.24 m (most likely) versus constant velocity 0.32, 0.89, 1.70, 2.73 m; with maps and ego conditioning 0.07, 0.45, 1.14, 2.20 m. Road-boundary violation rate rises from 0.2% at 1 s to 6.9% at 4 s without maps.
- The authors note that a competing method (Social Attention) has suspiciously high FDE/ADE ratios, a caution about benchmark reporting.

## Methods and models

Spatiotemporal graph; node history encoded with LSTM; edge influence aggregated by element-wise sum per neighbour class then attention; CVAE with discrete latent z (Gaussian mixture output over controls); dynamics integration through known agent models to produce positions; optional CNN map encoding and future ego-motion encoding. Metrics: ADE, FDE, KDE NLL, best-of-N. Code: https://github.com/StanfordASL/Trajectron-plus-plus (MIT, 834 stars, last push 2023-08-17, per GitHub API).

## Limitations and open questions

- ETH/UCY are sparse scenes; nothing is shown at the densities where crowd physics dominates ([[gu-2025-emergence]], [[helbing-2007-dynamics]]).
- Interaction modelling is a learned aggregation with no interpretable law; compare the interpretable time-to-collision law of [[karamouzas-2014-universal]].
- I read the abstract, method overview and results tables, not the full ablations.

## Relevance to us

The standard learned interaction model for heterogeneous agent collectives, and a ready code base for "predict the swarm, then plan" experiments, for instance a robot moving through a simulated crowd ([[chen-2019-crowd]]). The dynamics-integration trick (predict controls, integrate physics) is a cheap way to keep learned swarm models physically consistent. Review context: [[korbmacher-2022-review]].
