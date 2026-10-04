---
id: tan-2024-wolf
type: paper
title: "The Wolf Within: Covert Injection of Malice into MLLM Societies via an MLLM Operative"
authors: [Zhen Tan, Chengshuai Zhao, Raha Moraffah, Yifan Li, Yu Kong, Tianlong Chen, Huan Liu]
year: 2024
venue: ReGenAI Workshop at CVPR 2024; arXiv preprint
url: https://arxiv.org/abs/2402.14859
doi: null
arxiv: '2402.14859'
cite: "Tan, Z., Zhao, C., Moraffah, R., Li, Y., Kong, Y., Chen, T., & Liu, H. (2024). The Wolf Within: Covert Injection of Malice into MLLM Societies via an MLLM Operative. ReGenAI Workshop at CVPR 2024. arXiv:2402.14859."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

The authors manipulate one multimodal LLM agent (through an adversarial image perturbation optimised with white-box access) so that it generates prompts which, when sent to other agents in a society of multimodal LLMs, induce those agents to produce harmful content. The compromised agent is not itself made to output harm directly; it becomes a covert operative that infects its peers through ordinary inter-agent messages.

## Contribution

Early demonstration of indirect propagation: a single compromised agent as a vector that makes other agents misbehave, with generated prompts that transfer across agents.

## Key results

- Demonstrated (abstract): a manipulated agent's generated prompts induce other agents to output dangerous instructions or misinformation.
- Demonstrated (abstract): the generated prompts transfer, so the infection is not tied to a single recipient model.
- Detailed success rates not checked at this read depth.

## Methods and models

White-box attacker. A noise perturbation on an image is optimised with projected gradient descent so that the wolf agent's generated prompt, fed with the image to a sheep agent, yields a chosen malicious target (cross-entropy loss through both models). Transfer is then tested by applying the image and prompt to other agents untouched during optimisation (the paper cites LLaVA, PandaGPT and Shikra as openly available models; which ones were used in experiments was not checked). Read: abstract, method and conclusion.

## Limitations and open questions

Workshop paper; small setting; white-box gradient access to the wolf and sheep models is assumed; the paper says transfer works only sometimes, and rates were not checked here.

## Relevance to us

Q3. Directly models the "operative" pattern in dmarz's question: the corrupted part need not carry an obvious payload, it only needs to emit messages that steer whoever reads them, which after merge is the parent. Later and larger measurements of the same pattern: [[gu-2024-agent]] (exponential spread), [[lee-2024-prompt]] (self-replicating LLM-to-LLM injection), [[ju-2024-flooding]], [[torpmann-hagen-2026-memetic]].
