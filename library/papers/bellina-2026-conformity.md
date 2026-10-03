---
id: bellina-2026-conformity
type: paper
title: "Conformity and Social Impact on AI Agents"
authors:
- "Alessandro Bellina"
- "Giordano De Marzo"
- "David Garcia"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.05384
doi: null
arxiv: "2601.05384"
cite: "Bellina, A., De Marzo, G., & Garcia, D. (2026). Conformity and social impact on AI agents. arXiv preprint arXiv:2601.05384."
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: "0 (OpenAlex W7123246623, arXiv record, 2026-10-03); Semantic Scholar 10 same day"
code: []
---

## Summary

Runs Asch-style conformity experiments on open multimodal LLMs. The model sees a simple visual task (line-length judgment, colour recognition, dot estimation) that it solves correctly alone, plus N "confederate" answers that are wrong. Conformity is measured as the token probability of the wrong answer, p_wrong(N), read from logits. All models conform; the effect follows Social Impact Theory: it grows with group size, collapses when unanimity breaks, rises with task difficulty and depends on the strength and immediacy of the sources.

## Contribution

A quantitative, logit-level measurement of the microscopic social-influence response of AI agents, i.e. the response function that collective models such as [[de-marzo-2024-ai]] assume, from the same group. It separates task difficulty from model competence as the driver of conformity.

## Key results

- p_wrong(N) rises with the number of confederates; some models approach p_wrong close to 1; some rise monotonically up to N = 10, others saturate near N = 3-4 as in human Asch experiments. Measured.
- Breaking unanimity strongly suppresses conformity: even 20% correct confederate answers markedly reduce it, and 50% almost removes it. Measured (Qwen2.5-VL-32B, colour task).
- Conformity (area under p_wrong(N)) correlates with task difficulty (Spearman rho = 0.97, p < 1e-10); in a multivariate regression difficulty is significant (beta = 0.657, p < 1e-9) and model performance is not (p = 0.46). Measured.
- Public answers raise conformity relative to private ones for most models (normative effect). Measured.

## Methods and models

13 open models: Qwen2-VL-7B, Qwen2.5-VL-3B/7B/32B, Gemma-3 4B/12B/27B, Mistral-Small-3.1-24B, Ovis2 4B/8B/16B/34B. Synthetic images with controlled difficulty; binary A/B answers; logit-based probabilities. Skimmed results, discussion and methods.

## Limitations and open questions

Single-shot prompts with fictitious confederates, not interacting agents; open models only; visual tasks. Open: whether the measured response function, inserted into a population model, predicts the collective dynamics seen in [[de-marzo-2024-ai]] or [[flint-2026-group]].

## Relevance to us

Supplies the individual-level social response curve needed to build or validate a mean-field model of an LLM swarm. Compare [[weng-2025-do]] (BenchForm), [[cho-2025-herd]], [[han-2026-conformity]] and [[li-2025-systematic]].
