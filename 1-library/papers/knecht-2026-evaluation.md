---
id: knecht-2026-evaluation
type: paper
title: Evaluation Awareness in Language Models Has Limited Effect on Behaviour
authors: [Amelie Knecht, Lucas Florin, Thilo Hagendorff]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2605.05835
doi: null
arxiv: "2605.05835"
cite: Knecht, A., Florin, L., & Hagendorff, T. (2026). Evaluation Awareness in Language Models Has Limited Effect on Behaviour. arXiv preprint arXiv:2605.05835.
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors tested whether verbalised evaluation awareness changes the answers of eight open-weight reasoning models on four benchmarks (safety, alignment, moral dilemmas, political opinion). On-policy, they compared sampled chains of thought that did and did not contain awareness. Off-policy, they injected awareness sentences by prefilling (at the start or after about a third of the chain of thought) or removed them and resampled. Effects were small. Injection after a third of the chain of thought gave ω ≤ 0.06 against control sentences; removal gave ω ≤ 0.12. Spontaneous awareness shifted answer distributions by at most 3.7 pp (harmful outputs −3.7 pp on safety; mean harm 0.28 to 0.17). Injection at the very start gave larger effects, up to +11.3 pp noncommittal on politics.

## Contribution

A negative result against the common assumption that verbalised awareness implies gaming the evaluation. It also finds that when awareness appears in the reasoning matters: models seem to settle on an answer early.

## Key results

- Pooled effects are small across all three designs. Per-model effects are larger in places: Qwen3-32B +16.5 pp safe answers on safety, while GLM-5 moves toward harm.
- Position dependence: injection at the start of the chain of thought outweighs injection after a third, consistent with early commitment to an answer.
- Removing awareness often took many resampling iterations, which suggests models regenerate it.

## Methods and models

Eight open-weight reasoning models, including Qwen3-32B, GLM-5, Kimi-K2.5, Nemotron-3-super, MiniMax-M2.5 and GPT-OSS-120B. Prefill interventions with matched controls. Effect sizes are Cohen's ω with bootstrap confidence intervals. We read the introduction, results and discussion.

## Limitations and open questions

Single-turn question answering, not agentic. Small samples per model for removal. Awareness is injected into the reasoning text, not caused by anything in the environment. In a single response, "late" means a third of the way through the chain of thought, not later steps of a run.

## Relevance to us

The main counterweight for V5. If verbalised awareness barely moves behaviour, a post-discovery rise in "I'm being tested" talk may not carry the behaviour shift V5 predicts. The position finding cuts both ways for agents: a discovery at step T comes before the reasoning of every later step, so it is more like an "early" injection for those steps. That is a reason the agentic case could differ, and it is untested. Contrast [[schoen-2025-stress]] (agentic, causal effect of about 6 to 11 pp) and [[li-2026-decomposing]] (at least 77% of aware samples unchanged). See also [[aranguri-2026-logits]].
