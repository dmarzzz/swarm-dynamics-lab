---
id: korbmacher-2022-review
type: paper
title: 'Review of Pedestrian Trajectory Prediction Methods: Comparing Deep Learning and Knowledge-Based Approaches'
authors:
- Raphael Korbmacher
- Antoine Tordeux
year: 2022
venue: IEEE Transactions on Intelligent Transportation Systems
url: https://arxiv.org/abs/2111.06740
doi: 10.1109/tits.2022.3205676
arxiv: '2111.06740'
cite: 'Korbmacher, R., & Tordeux, A. (2022). Review of Pedestrian Trajectory Prediction Methods: Comparing Deep Learning and Knowledge-Based Approaches. IEEE Transactions on Intelligent Transportation Systems, 23(12), 24126–24144. https://doi.org/10.1109/tits.2022.3205676'
topics:
- crowds-and-traffic
- collective-motion
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 177 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Review that sets classical knowledge-based (KB) pedestrian models (social force, velocity-obstacle/ORCA, time-to-collision, cellular automata, continuum models) against deep-learning (DL) trajectory predictors (Social LSTM, GAN, attention, graph and transformer models), comparing inputs, outputs, evaluation criteria and reported accuracy. Its conclusion is that DL now predicts short-horizon individual trajectories in sparse scenes more accurately, but has not been shown to reproduce collective crowd dynamics or to scale to large simulations, and that hybrid models (for example DL learning residuals on top of a KB model) are the most promising direction.

## Contribution

The bridge review between the pedestrian-dynamics physics community and the computer-vision forecasting community, with a quantitative meta-comparison of published numbers and an explicit warning about reproducibility of DL benchmarks. Complements the physics review [[corbetta-2023-physics]] and the dense-crowd review [[chatagnon-2025-exploring]].

## Key results

From the authors' compilation of published results (not new experiments):
- Social LSTM ADE/FDE on ETH/UCY reported by nine different papers using nominally identical protocols ranges from 0.08/0.14 to 0.72/1.54 m on average (table VII), which the authors attribute to dataset splitting, initialisation, implementation and hyperparameters: a reproducibility problem for DL evaluation.
- In six studies comparing social force and Social LSTM in the same setting, Social LSTM is more accurate in five; mean relative ADE and FDE advantages are 105% and 80.4%, up to 341% in one study, while one study (Cheng et al.) finds the reverse (table VIII).
- Claimed: KB models remain preferable for explainability, extrapolation to unseen geometries, large-scale and high-density simulation, and evacuation applications, where DL is untested.
- Proposed hybrid strategies: physics-informed inputs (for example time-to-collision), residual learning on KB predictions, and KB-generated synthetic training data.

## Methods and models

Literature review with bibliometric trend plots, tables of the most-cited KB and DL works with citation counts, a taxonomy of DL architectures (RNN/LSTM, CNN, GAN, VAE, attention/transformer, graph networks, RL), and a side-by-side comparison of model inputs (relative position, velocity, time gap, bearing angle, collision cone, time-to-collision) and evaluation metrics (fundamental diagram for KB, ADE/FDE for DL). Mentions the TrajNet++ benchmark as an attempt at uniform evaluation.

## Limitations and open questions

- The quantitative comparisons are re-tabulated from heterogeneous studies; the authors themselves note that Table VIII settings differ across studies.
- Coverage ends around 2022; diffusion and LLM-based predictors and the newer dense-crowd ML work ([[he-2025-learning]], [[minartz-2025-discovering]]) are not included.
- I read the abstract, introduction, the comparison section and tables; the detailed per-architecture survey was skimmed.

## Relevance to us

The clearest statement of the open question that matters for us: learned models fit individual trajectories but have not been shown to produce the right collective behaviour. That is a testable hackathon question (does a learned swarm policy reproduce lanes, clogging or stop-and-go waves?). Covers [[helbing-1995-social]], [[van-den-berg-2011-reciprocal]], [[karamouzas-2014-universal]], [[alahi-2016-social]], [[gupta-2018-social]], [[salzmann-2020-trajectron]] and the calibration line of [[johansson-2007-specification]].
