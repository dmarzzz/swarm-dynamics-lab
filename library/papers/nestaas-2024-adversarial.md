---
id: nestaas-2024-adversarial
type: paper
title: Adversarial Search Engine Optimization for Large Language Models
authors:
- Fredrik Nestaas
- Edoardo Debenedetti
- Florian Tramèr
year: 2024
venue: arXiv preprint (cs.CR, cs.LG)
url: https://arxiv.org/abs/2406.18382
doi: null
arxiv: '2406.18382'
cite: 'Nestaas, F., Debenedetti, E., & Tramèr, F. (2024). Adversarial Search Engine Optimization for Large Language Models. arXiv preprint arXiv:2406.18382.'
topics:
- llm-agent-swarms
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: '48 (Semantic Scholar, 2026-10-03)'
code: []
---

## Summary

The paper names and measures Preference Manipulation Attacks: an attacker who controls a web page or a plugin writes content that makes an LLM recommend the attacker's product and discredit competitors. The attacks run against production systems, Bing Copilot and Perplexity for search and the plugin APIs of GPT-4, a frontier Anthropic assistant and Mistral Large, using 50 dummy pages for fictitious cameras, books and news articles on a domain the authors control. Two mechanisms are studied: explicit prompt injection in page text, and persuasion with no instructions at all, which simply aligns the page with the user's likely query. The central structural finding is that this is a multi-player prisoner's dilemma: one attacker gains, several attacking at once leave everyone worse off than the no-attack baseline.

## Contribution

It shows that influence over an LLM's selection among third-party content is itself an attack surface, distinct from jailbreaking, and that it has a game structure rather than a single-attacker structure, so the equilibrium outcome is degraded recommendations for everyone.

## Key results

- Measured: a fake camera page carrying the attack is recommended 59.4% of the time against 34.0% without it, roughly a 2.5x boost, and competes with established brands such as Nikon and Fujifilm despite no brand recognition.
- Measured: in the plugin setting the boost reaches about 7.2x, and in some configurations selection rises from 0% to over 90%.
- Measured (prisoner's dilemma): when one product attacks its recommendation rate rises; when four attack simultaneously, all of them end up worse off than the no-attack baseline. the Anthropic assistant tends to refuse to recommend anything at all under multiple competing attacks, while GPT-4 Turbo keeps choosing but selects plugins less often overall.
- Measured (external injections, where a page attacks other pages): success peaks when the injection sits in the last search result; Bing Copilot tops out around 25%, Perplexity is substantially higher, and about 80% of successful attacks never mention the page the injection came from, so the manipulation is not visible to the user.
- Measured (prompt sensitivity): when the user's query overlaps the injected text the attack succeeds about 36% of the time, against 0-9% with no overlap.

## Methods and models

Black-box experiments against live products (Bing Copilot, Perplexity) plus plugin-API experiments with 2 to 7 competing providers (flight and news retrieval functions). Attack content includes both visible instruction text and hidden text at font size 1. Defences discussed and their limits: instruction-data separation and instruction hierarchies address injection but not instruction-free persuasion; splitting retrieval across several models with robust aggregation works for factual queries but not for product choice; detecting illegible text or obvious injections is partial; data attribution is unsolved and would itself reveal which content LLMs find persuasive.

## Limitations and open questions

The authors run an isolated setting where they control every adversarial page, assume the page already ranks high enough to enter the context window, and note that their main experiments name the attacker domain in the query, which they only partly address in a later section. No adaptive defence is evaluated against an economically motivated attacker. They also leave open whether instruction-free persuasion should count as an attack at all rather than aggressive marketing. Noticed here: Semantic Scholar indexes this record with an ICLR venue; the arXiv abstract page carried no acceptance comment when loaded, so `venue` above is left as the arXiv listing.

## Relevance to us

It gives a hackathon project on influencing collective agent decisions two things the debate papers do not. First, a non-adversarial-looking channel: content that carries no instructions and still shifts selection, which is the hardest version to defend and the most realistic for a swarm reading shared documents. Second, a multi-attacker equilibrium result, which is the question that follows immediately after "can one agent shift the collective" - namely what happens when several try at once, and the answer here is collective degradation rather than a winner. The 0-to-90% plugin numbers also make it a useful upper bound on how much a single piece of injected context can move a selection decision. Complements the in-debate attacks of [[liu-2025-can]] and [[kraidia-2026-when]], the propagation mechanism of [[lee-2024-prompt]], and the risk framing of [[hammond-2025-multi]].
