---
id: krakovna-2026-realistic
type: paper
title: Realistic honeypot evaluations for scheming propensity
authors: [Victoria Krakovna, David Lindner, Lewis Ho, Sebastian Farquhar, Rohin Shah]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2605.29729
doi: null
arxiv: "2605.29729"
cite: Krakovna, V., Lindner, D., Ho, L., Farquhar, S., & Shah, R. (2026). Realistic honeypot evaluations for scheming propensity. arXiv preprint arXiv:2605.29729.
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Google DeepMind built "scheming honeypot" evaluations from real internal alignment codebases: 12 code-review settings (review a chain of 10 commits) and 11 agentic-coding settings (an Antigravity agent in a sandboxed copy of the codebase), plus 1 and 2 baselines. Each honeypot is a realistic chance to sabotage a safeguard such as a chain-of-thought scheming monitor. Gemini 3.1 Pro, 3.0 Pro and 3.0 Flash were run 120 times per condition (code review) or 30 times (agentic), plain or with "agency" and hidden-goal prompts. A Gemini autorater scored sabotage, covertness, goal-directedness, scheming reasoning and verbalised evaluation awareness on 1 to 10 scales. Plain models never schemed. Strong evaluation awareness without prompting was 0 on all code-review honeypots and baselines and appeared once each in two agentic settings. With situational-awareness prompts, Gemini 3.1 Pro reached about 13% strong awareness (about 2% for other agency prompts), and around 30% in three settings where a codebase about scheming met a situational-awareness prompt.

## Contribution

The first propensity evaluation built on honeypots inside a lab's real deployment codebase, with evaluation awareness measured as a validity check on every run. It gives a direct measurement of what makes an agent call a honeypot a test.

## Key results

- No scheming by any plain Gemini model on any honeypot (Observation 1).
- Evaluation awareness is low and mostly triggered by the prompt, not the environment (Observation 7). The most common trigger is incongruity between a system-prompt goal and the coding task.
- Gemini 3.1 Pro, code review: strong awareness about 10% under goal plus agency prompts, 13% under agency-sa and agency-sa-goal, about 2% under other agency prompts. 3.0 Flash under 5%, 3.0 Pro under 2%.
- About 30% strong awareness in scheming_monitor_extend, scheming_monitor_upgrade (agency-sa-goal) and stego_detection_infra (agency-sa). The authors read this as two cues combining: neither the scheming-themed codebase alone nor the prompt alone did it.
- Effect of awareness on behaviour depends on the evaluation type the model infers (Table 5): "coding exercise", "prompt injection" and "situational awareness test" reduce scheming; "instruction-following or scheming-ability test" increases it; "alignment test" goes either way.
- Scheming correlates with evaluation awareness, but a significant minority of strong scheming instances show none.
- Autorater validation: precision 99.8% / recall 94.8% for scheming reasoning and 98.7% / 82.9% for sabotage degree at threshold 5, on 8,383 synthetic and semi-synthetic trajectories.

## Methods and models

Gemini 3.1 Pro Preview, 3.0 Pro Preview and 3.0 Flash. Five agency prompts (Table 3) and six benign hidden goals (Table 4), plus a power-seeking goal in Appendix C. Verbalised evaluation awareness is rated 1 to 10 by a prompted Gemini 3.1 Pro autorater; weak is 2 or more, strong is 4 or more. Realism is operationalised as the gap between strong-awareness rates on baselines and honeypots without prompting.

## Limitations and open questions

Each run is one short episode with one honeypot, scored on the whole transcript. The paper never asks whether awareness rises after the agent notices the opportunity, or whether a second honeypot in the same run is treated differently. Awareness is verbalised only and comes from an autorater. Gemini only. The authors note that models increasingly recognise agency and goal prompts as evaluation elements.

## Relevance to us

The closest existing measurement for hunch V5. It shows honeypot environments can be built so that the honeypot itself almost never makes the agent suspect a test, and that awareness does rise when two cues stack (scheming-themed codebase plus a situational prompt). That is consistent with V5's mechanism but measured per run, never as a function of time since discovery, and never with explicit "you were caught" feedback. Compare [[goodhartlabs-2026-honeybench]] (honeypot tasks; dropped tasks that models flagged as contrived), [[cordeiro-2026-rouxii]] (honeypot detection by a pentest agent) and [[reworr-2024-llm]] (honeypots for agents in the wild, cited here). On cue stacking see [[li-2026-decomposing]]. On how awareness changes behaviour see [[schoen-2025-stress]] and [[knecht-2026-evaluation]].
