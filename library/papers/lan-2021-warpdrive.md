---
id: lan-2021-warpdrive
type: paper
title: "WarpDrive: Extremely Fast End-to-End Deep Multi-Agent Reinforcement Learning on a GPU"
authors: [Tian Lan, Sunil Srinivasa, Huan Wang, Stephan Zheng]
year: 2021
venue: arXiv preprint (repository describes a JMLR 2022 version; not checked)
url: https://arxiv.org/abs/2108.13976
doi: null
arxiv: '2108.13976'
cite: "Lan, T., Srinivasa, S., Wang, H., & Zheng, S. (2021). WarpDrive: Extremely fast end-to-end deep multi-agent reinforcement learning on a GPU. arXiv:2108.13976."
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: [gh-salesforce-warp-drive]
---

## Summary

Introduces WarpDrive, a PyCUDA and PyTorch framework that runs both multi-agent simulation and RL training on one GPU, with environment replicas and agents executed in parallel, a single in-place GPU data store and no CPU-GPU copying. Reports 2.9 million environment steps per second with 2000 environments and 1000 agents in a Tag pursuit benchmark, at least 100x a CPU implementation, with near-linear scaling in agents and environments.

## Contribution

Early demonstration that the CPU-simulation plus GPU-model split is the bottleneck for many-agent RL and that moving the simulator onto the GPU removes it; precursor in spirit to Madrona [[shacklett-2023-extensible]] and JAX suites such as [[gh-bold-lab-ai-jaxmarl]].

## Key results

- 2.9M env steps/s, 2000 envs x 1000 agents, Tag (abstract).
- The README adds about 10x faster training than a 16-CPU node for Tag with 100 runners and 5 taggers at 60 replicas.

## Methods and models

CUDA C (later Numba) environment step kernels, one block per environment and one thread per agent; PyTorch policy updates on the same device.

## Limitations and open questions

Environments must be rewritten as CUDA kernels; NVIDIA-only. Repository now archived. Only the abstract and README were read.

## Relevance to us

Historical reference for vectorisation design choices. Code: [[gh-salesforce-warp-drive]].
