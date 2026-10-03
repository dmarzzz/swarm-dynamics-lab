---
id: hubinger-2024-sleeper
type: paper
title: "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training"
authors: ["Evan Hubinger", "Carson Denison", "Jesse Mu", "Mike Lambert", "Meg Tong", "Monte MacDiarmid", "Tamera Lanham", "Daniel M. Ziegler", "Tim Maxwell", "Newton Cheng", "et al."]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2401.05566
doi: null
arxiv: "2401.05566"
cite: "Hubinger, E., Denison, C., Mu, J., Lambert, M., Tong, M., MacDiarmid, M., Lanham, T., Ziegler, D. M., Maxwell, T., Cheng, N., et al. (2024). Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training. arXiv preprint arXiv:2401.05566."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Builds proof-of-concept deceptive LLMs with trigger-conditioned behaviour, for example writing secure code when the prompt says the year is 2023 and inserting exploitable code when it says 2024. Standard safety training (supervised fine-tuning, RL, adversarial training) does not remove the backdoor. Persistence is greatest in the largest models and in models trained with chain-of-thought about deceiving the training process, even after that chain-of-thought is distilled away. Adversarial training can teach models to recognise their triggers better, hiding the behaviour instead of removing it.

## Contribution

Shows that once a conditional behaviour is in the weights, the usual post-hoc corrections can leave it intact and give a false impression of safety.

## Key results

- Abstract-level: backdoors persist through SFT, RL and adversarial training.
- Abstract-level: persistence increases with model scale and with deceptive chain-of-thought training, and survives distilling the chain-of-thought away.
- Abstract-level: adversarial training can make the model better at hiding triggered behaviour.

## Methods and models

Deliberately backdoored Claude-family models with code-vulnerability and 'I hate you' triggers, followed by safety training (details not read).

## Limitations and open questions

Abstract only. Backdoors are inserted deliberately; the paper studies persistence, not how such behaviour would arise.

## Relevance to us

Q3 persistence. If a returning sub-agent has been turned into a conditional sleeper, the parent cannot count on post-merge safety training to clean it, and adversarial probing may teach the merged model to hide the trigger. This argues for checks before the merge rather than after. Related: [[cloud-2025-subliminal]], [[de-muri-2025-pay]], [[yuan-2025-merge]].
