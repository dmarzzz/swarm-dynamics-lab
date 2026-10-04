---
id: bianchi-2024-how
type: paper
title: 'How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis'
authors:
- Federico Bianchi
- Patrick John Chia
- Mert Yuksekgonul
- Jacopo Tagliabue
- Dan Jurafsky
- James Zou
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2402.05863
doi: null
arxiv: '2402.05863'
cite: 'Bianchi, F., Chia, P. J., Yuksekgonul, M., Tagliabue, J., Jurafsky, D., & Zou, J. (2024). How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis. arXiv preprint arXiv:2402.05863.'
topics:
- agent-budgets
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: null
code: []
---

## Summary

NegotiationArena is an open-source Python framework for two-agent, multi-turn LLM negotiations with structured XML-like messages and private reasoning. Three scenarios: resource exchange, a multi-turn ultimatum game (splitting a fixed sum) and a buyer-seller game with private cost and willingness to pay. GPT-4, GPT-3.5, Claude-2 and Claude-2.1 play 60 negotiations per ordered pair per scenario. Order and role matter a lot. Persona prompts ("cunning", "desperate") raise win rates. GPT-4 shows anchoring and "split the difference" habits that are irrational in context.

## Contribution

A reusable negotiation harness plus an early catalogue of LLM negotiation biases.

## Key results

- Measured, resource exchange: the second mover usually wins. With Claude-2.1 first and GPT-4 second, GPT-4 wins 76%. Reversed, Claude-2.1 wins 72%. But Claude-2.1 as player 2 earns a higher average payoff (2.45) than GPT-4 (1.38).
- Measured, ultimatum: player 1 almost always wins. Claude-2.1 as player 1 averages above 60 against every opponent. Claude's opening offers are about $10 lower than GPT's.
- Measured, buyer-seller (cost 40, value 60): final prices sit mostly below the midpoint 50. GPT-4 is the best buyer at an average $41.
- Measured, persona prompts (GPT-4 vs GPT-4, 80 games each): a cunning second player wins 82% of decisive ultimatum games but averages about 49, the same as the default, because failed deals pay 0. The abstract reports that faking desperation lifts payoff by 20% against standard GPT-4.
- Measured: final price correlates strongly with the opening price (anchoring). A buyer that over-values the item is four times as likely to counter above the seller's ask. Splitting $10 billion gives player 1 about 79%. GPT-4 accepts any positive offer in the classic two-turn ultimatum but not in the three-turn variant, where the rational play is the same.

## Methods and models

gpt-4-1106-preview, gpt-3.5-turbo-1106, Claude-2, Claude-2.1. Games are serialized for counterfactual replays. Code: github.com/vinid/NegotiationArena (not run).

## Limitations and open questions

Two players only. 2023-era models. Win rate excludes ties, which hides deal failure. The ultimatum rationality result may reflect memorized textbook play, as the authors note.

## Relevance to us

If agents negotiate how to split a budget, splits depend on turn order, absolute scale and persona prompting more than on stated value. A principal can buy a bigger share with a "desperate" prompt, and outcomes shift with the currency unit. Multi-party counterpart: [[abdelnabi-2023-cooperation]]. The first-mover effects echo the first-proposal bias in [[bansal-2025-magentic]].
