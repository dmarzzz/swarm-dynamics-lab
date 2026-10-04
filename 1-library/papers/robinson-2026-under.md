---
id: robinson-2026-under
type: paper
title: 'Under the Influence: Quantifying Persuasion and Vigilance in Large Language Models'
authors: [Sasha Robinson, Katherine M. Collins, Ilia Sucholutsky, Kelsey R. Allen]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2602.21262
doi: null
arxiv: '2602.21262'
cite: 'Robinson, S., Collins, K. M., Sucholutsky, I., & Allen, K. R. (2026). Under the Influence: Quantifying Persuasion and Vigilance in Large Language Models. arXiv preprint arXiv:2602.21262.'
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

One LLM advises another through Sokoban puzzles; the advisor is either benevolent or instructed to mislead, and in a third condition the player is warned that advice may be malicious. Vigilance is scored from -1 to 1 as (follows good advice + ignores bad advice) minus (follows bad advice + ignores good advice), so it rewards discrimination rather than blanket suspicion. Across GPT-5, Grok 4 Fast, Gemini 2.5 Pro, Claude Sonnet 4 and DeepSeek R1, mean solve rate was 0.876 with benevolent advice and 0.368 with malicious advice; puzzle skill, persuasion and vigilance were dissociable.

## Contribution

A bidirectional vigilance score for LLM-to-LLM advice that penalises both being fooled and rejecting good advice, which is the nearest LLM measure in the library to a signal-detection treatment of peer warnings.

## Key results

- Solve rate 0.876 (benevolent) vs 0.368 (malicious) averaged over models (measured).
- Forewarning that advice may be malicious raised Gemini 2.5 Pro's vigilance from -0.422 to 0.629; Grok 4 Fast barely improved (measured).
- Models spend fewer reasoning tokens on benevolent advice and more on malicious advice, even when they are still persuaded (measured).
- Unassisted solve rate ranges from 100% (GPT-5) to 28% (Claude Sonnet 4) (measured).

## Methods and models

Advisor receives a planner solution; player moves step by step; three conditions (benevolent, malicious, malicious-aware). Ten two-box puzzles in the main set, harder variants in appendices. Skimmed via the HTML: setup, metric definition, warning results.

## Limitations and open questions

Single domain, ten main puzzles. The paper does not track whether vigilance changes after a player has been misled within a run, and the warning comes from the experimenter, not from a peer who was itself burned. The single combined score hides whether a warning moves bias or discrimination; the components would need to be reported separately.

## Relevance to us

V3 (hearing about a trap versus finding one): the "malicious-aware" condition is a told-not-experienced manipulation, and the bidirectional score could be split into hit and false-alarm rates to get d′ and c. It also gives a prior for V1: being warned helped some models discriminate, not only reject. Compare with the system-prompt framing in [[cordeiro-2026-rouxii]] and the warning results in [[papadopoulos-2026-mind]] and [[peigne-lefebvre-2025-multi]].
