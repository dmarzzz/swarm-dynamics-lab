---
id: becker-2026-misinformation
type: paper
title: Misinformation Propagation in Benign Multi-Agent Systems
authors:
- Jonas Becker
- Jan Philip Wahle
- Terry Ruas
- Bela Gipp
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.16710
doi: null
arxiv: '2606.16710'
cite: Becker, J., Wahle, J. P., Ruas, T., & Gipp, B. (2026). Misinformation Propagation in Benign Multi-Agent Systems. arXiv preprint. arXiv:2606.16710.
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Injects machine-generated, topic-relevant misinformation (the MINT data set, nine intent categories such as hoax, rumour, propaganda, framing) into the context of some agents in a benign multi-agent debate, where no agent intends to deceive, and measures task accuracy, persistence of misinformed answers across turns, and the effect of how many agents are misinformed and whether the group decides by voting or by consensus. Tasks: WinoGrande (reasoning), Complex Web Questions (knowledge) and an ethics data set (alignment); models Llama-3.3 and GLM-4.7. Read: abstract, introduction, setup, all of section 4's reported results, conclusion and limitations.

## Contribution

Separates the effect of misinformation from that of adversarial persuasion, and measures a majority threshold for self-correction in debate.

## Key results

- Single agents: relevant misinformation cut Llama-3.3 accuracy on CWQ from 0.49 to 0.36 (-26.75% relative), Ethics -25.71%, WinoGrande -19.51%; irrelevant misinformation had much smaller effects (measured).
- Debate reduced the damage: -2.2% to -10.3% in multi-agent setups versus -12.9% to -17.2% for single agents (measured).
- Answers introduced by misinformed agents persisted more than those from uninformed agents on CWQ (-10.4 points) and WinoGrande (-7.7 points) (measured, Llama-3.3).
- A misinformed agent's chance of switching to the correct answer by turn 5 rose from 8.0% with 2 uninformed peers to 20.5% with 3, i.e. once correct agents formed a majority (measured, WinoGrande, Figure 5).
- Voting accuracy fell from 0.938 with no misinformed agents to 0.857 with five; consensus was more stable under peer pressure (measured, Figure 4).

## Methods and models

Five-agent debates with fixed turns; voting versus consensus protocols; human audit of MINT with only fair agreement on categories (stated). Code, prompts and data released by the authors.

## Limitations and open questions

Two open-weight models; generated rather than human or adversarially optimised misinformation; no tool use or long-term memory (stated).

## Relevance to us

Q2: a measured, non-gradual majority effect: correction of a misinformed agent jumped when uninformed agents became the majority, which is the empirical shape of a k-of-n threshold in LLM groups, though the absolute correction rate stayed low (about one in five). It applies when the correct agents saw the same question; it does not cover facts only the misinformed part observed, which [[yan-2026-when]] shows fail much worse. Q3: misinformation that arrives through context (a tool call, a web page in a hostile domain) is enough; no adversarial agent is needed for the returning part to carry it home. Related: [[yu-2024-netsafe]], [[ebrahimi-2025-adversary]].
