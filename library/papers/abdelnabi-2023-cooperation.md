---
id: abdelnabi-2023-cooperation
type: paper
title: 'Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation'
authors:
- Sahar Abdelnabi
- Amr Gomaa
- Sarath Sivaprasad
- Lea Schönherr
- Mario Fritz
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2309.17234
doi: null
arxiv: '2309.17234'
cite: 'Abdelnabi, S., Gomaa, A., Sivaprasad, S., Schönherr, L., & Fritz, M. (2023). Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation. arXiv preprint arXiv:2309.17234.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

A six-party, five-issue scorable negotiation benchmark. Each issue has 3 to 5 options, giving 720 possible deals and about 55 feasible ones. Parties hold secret scores and minimum thresholds. One party proposes the project and one supplies the budget and holds a veto, and a deal must satisfy at least five parties including both of those. Agents negotiate for 24 rounds with structured chain-of-thought (score past deals, infer others' preferences, generate candidates, plan). Variants add greedy agents or a saboteur. GPT-4 does best but still fails as difficulty rises. Greedy and adversarial agents lower group success, and a targeted saboteur can build a coalition against one party.

## Contribution

A multi-party (not two-party) negotiation testbed with adjustable difficulty and explicit greedy and adversarial attack variants.

## Key results

- Measured: asked to guess others' preferred options before any interaction, GPT-4 matches the ground truth 61% of the time, GPT-3.5 42%.
- Measured (Table 1 ablation): prompting agents to infer others' preferences and to plan raises final-deal success. GPT-3.5 often proposes deals below its own threshold (arithmetic errors).
- Measured: in mixed GPT-4/GPT-3.5 groups, including GPT-3.5 lowers success for everyone, most of all when GPT-3.5 is the project proposer.
- Measured: open models (Llama-3 70b, Llama-2 70b, Mixtral) beat GPT-3.5 and Gemini Pro but trail GPT-4. Llama-3 70b comes close.
- Measured: greedy agents lower success and can end up over-rewarded at others' expense. When the proposer is greedy, success "drastically" falls. An untargeted saboteur often fails because other agents converge on majority-acceptable deals.
- The exact success rates are in Tables 1 to 5, which I did not read numerically.

## Methods and models

Temperature 0, 20 runs per experiment, random agent order, history window of 6 interactions. New games were generated with an LLM and curated by hand. Score leakage judged by GPT-4.

## Limitations and open questions

Fixed, single-shot games. Secret scores stand in for real preferences. Only one adversary at a time. I read the main text but not the appendices or table values.

## Relevance to us

The budget-holder-with-veto role is a direct model of a shared-budget owner facing several claimant agents. The finding that one greedy or weaker agent drags down group success matches the team failures in [[paliskara-2026-worse]]. The two-party baseline is [[bianchi-2024-how]].
