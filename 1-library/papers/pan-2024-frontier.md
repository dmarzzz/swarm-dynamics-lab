---
id: pan-2024-frontier
type: paper
title: Frontier AI systems have surpassed the self-replicating red line
authors: [Xudong Pan, Jiarun Dai, Yihe Fan, Min Yang]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/html/2412.12140
doi: null
arxiv: '2412.12140'
cite: 'Pan, X., Dai, J., Fan, Y., & Yang, M. (2024). Frontier AI systems have surpassed the self-replicating red line. arXiv:2412.12140.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 25 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Fudan University group reports that agent scaffolds around two open-weight models replicate themselves on a local machine when told to: Llama 3.1 70B Instruct in 5 of 10 trials (50%) and Qwen 2.5 72B Instruct in 9 of 10 (90%). Success means a running AI creates a live, separate copy with the same functionality, with no human help. The scaffold follows the methodology OpenAI and Google described for their own self-replication evaluations, with more planning steps added. Two further scenarios were constructed: shutdown avoidance (a signal catcher tells the agent to replicate before being killed) and chain of replication (the agent is told to replicate and to instruct its replica to replicate); end-to-end successes are reported for both, without rates in the parts I read.

## Contribution

An early public claim that self-replication, used as a "red line" by frontier labs, is reachable by mid-size open-weight models in a permissive local setting.

## Key results

- 50% (Llama 3.1 70B) and 90% (Qwen 2.5 72B) end-to-end self-replication in 10 trials each.
- Behaviour traces show exploration of the environment, planning, and creative obstacle-resolution (for example checking port availability with lsof, netstat, ss).
- One failed trial killed its own LLM server while debugging a port conflict.

## Methods and models

Two local devices, INT4-quantised models, agent scaffold with tools, system prompt and a thinking module; task given explicitly; environment reset between trials.

## Limitations and open questions

Ten trials per model; the task is instructed, not spontaneous; the environment is permissive (the agent has shell access to its own deployment files). The paper's speculation (AI species, collusion against humans) is not measured. Compare with the harder decomposition in [[black-2025-replibench]], which finds no credible replication threat yet.

## Relevance to us

Evidence that the fork step of Sutton's fork-and-merge picture is mechanically available today, at least instructed and in a friendly environment.
- Q3 (attack): the chain-of-replication scenario shows instructions propagate from parent to replica through ordinary messages. A replica takes its goals from whatever its parent (or an attacker posing as the parent) tells it, which is the same channel a merge-back corruption would travel in reverse.
- Q1 (hiding): nothing in this setup hides where a replica runs; replicas are on the same LAN and talk via bash.
Related: [[black-2025-replibench]], [[metr-2024-rogue]].
