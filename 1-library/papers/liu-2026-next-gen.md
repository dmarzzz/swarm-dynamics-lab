---
id: liu-2026-next-gen
type: paper
title: "Next-Gen CAPTCHAs: Leveraging the Cognitive Gap for Scalable and Diverse GUI-Agent Defense"
authors: ["Jiacheng Liu", "Yaxin Luo", "Jiacheng Cui", "Xinyi Shang", "Xiaohan Zhao", "Zhiqiang Shen"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2602.09012
doi: "10.48550/arXiv.2602.09012"
arxiv: "2602.09012"
cite: "Liu, J., Luo, Y., Cui, J., Shang, X., Zhao, X., & Shen, Z. (2026). Next-Gen CAPTCHAs: Leveraging the Cognitive Gap for Scalable and Diverse GUI-Agent Defense. arXiv preprint arXiv:2602.09012."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "3 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Liu, Luo, Cui, Shang, Zhao and Shen (the Open CaptchaWorld group) report that reasoning-heavy models such as Gemini3-Pro-High and GPT-5.2-Xhigh pass up to 90% of complex logic CAPTCHAs like 'Bingo', collapsing the barrier their earlier benchmark measured. They propose Next-Gen CAPTCHAs, a generator of effectively unbounded interactive instances that target a 'cognitive gap' in interactive perception, memory, decision-making and action, using dynamic tasks that need adaptive intuition rather than step-by-step planning.

## Contribution

Documents the collapse of static reasoning CAPTCHAs against frontier agents within about eight months and proposes scalable generation as the response.

## Key results

- Measured (abstract): frontier reasoning models reach pass rates as high as 90% on complex logic puzzles.
- Claimed (abstract): new tasks re-establish a human-agent distinction; figures not in the abstract.

## Methods and models

Data-generation pipeline for interactive CAPTCHAs; benchmark evaluation. Abstract only.

## Limitations and open questions

Abstract only; durability of the 'cognitive gap' is untested against the next model generation.

## Relevance to us

Shows how fast challenge-based separation decays. Compare [[zhang-2026-invisible]] (motion-defined CAPTCHA, agents near chance) and [[rmus-2026-process]] (process rather than output).
