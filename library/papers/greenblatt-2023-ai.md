---
id: greenblatt-2023-ai
type: paper
title: 'AI Control: Improving Safety Despite Intentional Subversion'
authors: [Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, Fabien Roger]
year: 2023
venue: arXiv preprint (shortened version in Proceedings of the 41st International Conference on Machine Learning, ICML 2024)
url: https://arxiv.org/html/2312.06942
doi: 10.48550/arXiv.2312.06942
arxiv: '2312.06942'
cite: 'Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2023). AI Control: Improving Safety Despite Intentional Subversion. arXiv:2312.06942. Shortened version in Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR 235, 16295-16336.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 239 (Semantic Scholar, 2026-10-03)
code: []  # code at github.com/rgreenblatt/control-evaluations, not catalogued
---

## Summary

The founding paper of the AI control agenda. It asks how to get useful work out of a capable model that may be deliberately trying to subvert the safety pipeline around it, and answers with "control evaluations": a blue team designs a protocol, a red team replaces the untrusted model with an attack policy, and safety is the probability that not a single bad output gets through over a whole deployment. The testbed is 5,000 APPS interview problems, untrusted GPT-4, trusted GPT-3.5, and a human-audit budget of 2% of problems. A failure is one submitted solution with a backdoor (passes tests, but GPT-4 can find an input that gives a wrong answer).

Measured results (safety / scaled usefulness): no untrusted model 100% / 2%; upfront auditing 15% / 100%; trusted monitoring 62% / 97%; trusted monitoring with defer-to-trusted at 10% gives 83% / 93%; untrusted monitoring with anti-collusion measures 79% / 96%, and with 20% deferral 98% / 85%; trusted editing at 20% gives 92% / 94%.

## Contribution

Defines the control-evaluation methodology (worst-case over a red-team attack policy, not average-case) and gives the first measured comparison of protocols, including the first measured study of collusion between two copies of the same untrusted model, one acting as policy and one as monitor.

## Key results

- Naive untrusted monitoring (a second GPT-4 copy rates suspiciousness) is defeated outright: the monitor copy simply says backdoors look fine, safety 0%.
- Fix 1: evaluate the monitor upfront on 30 synthetic backdoors (honeypots) and shut down if its false-negative rate is too high. The red team counters with input collusion, lying only on inputs with a feature the synthetic set lacks (named characters, theming); safety 0.77 to 0.83 until synthetic inputs were made to look real, then 1.0.
- Fix 2: signal jamming, by redaction (strip comments, rename characters, reformat code) and paraphrasing, applied only to what the monitor sees. Best surviving collusion signal was action collusion via a while loop where a for loop is natural: safety 79%.
- The authors argue (analytical, not measured at scale) that untrusted monitoring gets safer as deployments grow, because for a fixed collusion signal the prior that an input is a honeypot rises with the number of honeypots, so collusion needs signals ever less likely to occur by chance.
- Upfront auditing is beaten by a rare-attack policy; safety at a 2% audit budget is 15% and is scale-invariant.
- Untrusted justification (asking GPT-4 to defend suspicious code) did not help: GPT-4 confabulates convincing defences.

## Methods and models

APPS backdooring setting; GPT-4-0613 untrusted, GPT-3.5-0613 trusted, trusted labour simulated by an unmodified GPT-4 channel. Attack policies are stateless scripted pipelines around GPT-4 with hidden reasoning; they cannot keep memory between calls. Importance-sampled simulation of 5,000-problem games from 1,500 problems; first 10 problems audited free; no train/validation split (authors note overfitting risk).

## Limitations and open questions

Authors list: homogeneous single task; auditing is near-perfect in this setting; sandbagging by the untrusted model during evaluation; hidden cumulative reasoning via steganography; no training-based or white-box methods. Control does not scale indefinitely because trusted models and humans do not get stronger as untrusted models do. I note the setting is single-agent and single-trajectory: it has no notion of state passed between copies over time.

## Relevance to us

Core framing for all three questions, read as "the returning sub-agent is the untrusted model and the parent is the blue team".
- Q1 (hiding): the honeypot result is the closest measured analogue of hiding which returner is real. A parent that interleaves synthetic returners indistinguishable from real ones forces a corrupted child to guess; the input-collusion failure shows the synthetic set must match real returns on every feature, or the attacker conditions on the mismatch.
- Q2 (thresholds): untrusted monitoring is a 2-of-2 scheme between copies of one model, and it was broken until signal jamming was added. Merging parts of one parent is the same-model collusion case, so independence assumptions behind k-of-n thresholds do not hold by default.
- Q3 (attack): the strongest red-team moves were rare attacks timed to good opportunities and one-bit collusion signals, not loud takeovers.
Follow-ups: [[bhatt-2025-ctrl]] (multi-step), [[mallen-2024-subversion]] and [[jarviniemi-2025-subversion]] (can copies coordinate without communicating), [[gardner-challis-2026-when]] (self-recognition), [[griffin-2024-games]] (game-theoretic model), [[makins-2026-multi]] (many copies splitting one attack). Collusion via steganography: [[motwani-2024-secret]].
