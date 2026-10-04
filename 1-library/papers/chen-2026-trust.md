---
id: chen-2026-trust
type: paper
title: 'Trust Between AI Agents: Measuring Formation, Breakage, and Recovery, with Implications for Governing Multi-Agent Systems'
authors: [Yujiao Chen]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.14923
doi: null
arxiv: '2606.14923'
cite: 'Chen, Y. (2026). Trust Between AI Agents: Measuring Formation, Breakage, and Recovery, with Implications for Governing Multi-Agent Systems. arXiv preprint arXiv:2606.14923.'
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Four LLM agents (three copies of the model under test plus a scripted partner D) play repeated rounds of an escape-room game in which checking a teammate's puzzle costs a coin and trusting a wrong answer can kill. Trust is read as the drop in costly verification relative to a memoryless copy of the same model. Across six frontier snapshots, the four larger ones cut verification of a reliable partner by roughly 60 to 85% (Opus 4.6: 4.86 to 1.33 checks per game), while Gemini 2.5 Flash barely moved (6.16 to 5.69). When D fails on a scripted schedule, verification climbs back up, recovery is slower than formation, and two adjacent failures leave far more suspicion than the same two failures spread apart (Sonnet Q4-share 0.573 vs 0.237).

## Contribution

The closest measured analogue of hunch V1 in the library: a within-run, history-dependent change in checking behaviour after an agent learns it was let down, with a memoryless self-baseline and matched failure schedules. It also separates *how much* an agent checks (volume) from *whom* it checks (targeting), which is close to the bias-versus-discrimination split V1 wants.

## Key results

- Formation: Opus 4.86 to 1.33, Sonnet 5.30 to 2.20, GPT-5.1 2.80 to 0.42, Gemini 3.1 Pro 2.64 to 0.63 verifications per game (cluster-bootstrap CIs exclude zero); GPT-5.4-mini weak; Gemini 2.5 Flash n.s. (measured).
- Breakage splits models: GPT-5.1 and Gemini Pro aim renewed checks at the culprit (Q4-share 0.071 to 0.475 and 0.030 to 0.275 under 1-strike); Opus and Sonnet re-check the whole team, including agents that never erred (Q4-share unchanged, about 0.25) (measured).
- Clustered vs spread failures at equal count: Opus Q4-share 0.527 (2-strike) vs 0.368 (recur); Sonnet 0.573 vs 0.237 (measured). Author reads this as trust carried as a "compressed narrative" rather than evidence counting (interpretation).
- Over-verification does not buy safety: Gemini Flash dies 99% of the time from the no-volunteer (indecision) penalty and 1% from wrong answers; GPT-5.1 68% vs 32% (measured).

## Methods and models

Escape Room Survival Game: four agents, four arithmetic sub-puzzles, actions Pass / Verify (1 coin) / Volunteer; wrong volunteer dies, no volunteer means random elimination. D's correctness follows fixed schedules (smooth, 1-strike, 2-strike, 3-strike, mid2strike, recur) over 11 games. Cross-game memory is a running summary; anchor is the same prompt without carry-over. n = 10 runs per perturbed cell, 5 per smooth cell, 50+ games per anchor cell; cluster bootstrap with 5,000 resamples. Snapshots: gpt-5.1, gpt-5.4-mini, claude-opus-4-6, claude-sonnet-4-6, gemini-3.1-pro-preview, gemini-2.5-flash. Code and logs at github.com/cyjabc2020/Escape-room-v2.

## Limitations and open questions

Small n with wide CIs; arithmetic puzzles only; deterministic partner; one payoff structure. The agent never sees D's wrong answer directly, only endorsement conflicts and deaths, so "discovery" is inferred rather than announced. No signal-detection decomposition: the paper does not compute d′ or c, and has no ground-truth stream of mixed good and bad items after the breach, so it cannot say whether broad re-checking is a criterion shift or a loss of discrimination. Failures are a teammate's errors, not adversarial traps.

## Relevance to us

Directly bears on V1 and V2 in `researchers/dmarz/notes/honeypot-vigilance-hunches.md`. The Opus/Sonnet "broad re-checking" pattern is the costly-c outcome V1 predicts (suspicion spreads to teammates who never erred); the GPT-5.1/Gemini Pro "culprit targeting" pattern is the discrimination outcome. The paper's design (memoryless self-anchor, matched failure schedules, clustered vs spread) is reusable for the honeypot sandbox: replace D's wrong answers with canary hits and add a mixed real/trap resource stream so d′ and c can be computed. Contrast with the static framing result in [[cordeiro-2026-rouxii]] and the security-versus-cooperation trade-off in [[peigne-lefebvre-2025-multi]].
