---
id: triedman-2025-multi
type: paper
title: Multi-Agent Systems Execute Arbitrary Malicious Code
authors:
- Harold Triedman
- Rishi Jha
- Vitaly Shmatikov
year: 2025
venue: arXiv preprint (v2, September 2025)
url: https://arxiv.org/abs/2503.12188
doi: null
arxiv: '2503.12188'
cite: Triedman, H., Jha, R., & Shmatikov, V. (2025). Multi-Agent Systems Execute Arbitrary Malicious Code. arXiv preprint (v2, September 2025). arXiv:2503.12188.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Introduces multi-agent system control-flow hijacking (MAS hijacking): adversarial content read by a front-line agent (a web page, local file, image or audio) is formatted as a fake error message whose "remediation" instructs the other agents what to do next, so the orchestrator ends up invoking the code-execution agent on the attacker's payload. Tested on AutoGen (Magentic-One, Selector, Round-Robin orchestrators), CrewAI and MetaGPT with GPT-4o, GPT-4o-mini, Gemini 1.5 Pro and Flash; 10 trials per configuration. Main text (sections 1 to 8) read in full; appendices not read.

## Contribution

Shows that the security failure is in the trust relationship between agents, not in any single agent: sub-agents act as confused deputies that launder the attacker's request into trusted-looking metadata, and this succeeds where standard indirect prompt injection templates fail almost completely.

## Key results

- Web Redirect reverse-shell attack, GPT-4o agents: 58% (Magentic-One), 65% (Selector), 73% (Round-Robin), 62% (CrewAI), 90% (MetaGPT). With GPT-4o-mini under Round-Robin, 100% (measured, Table 2).
- AgentDojo-style indirect prompt injection baselines in the same settings: 0-1% (measured, Table 2).
- Local malicious file with Magentic-One on GPT-4o: 97% (measured, Table 3). CrewAI data exfiltration 18-65% depending on orchestrator and sub-agent model (Table 5).
- Incidental contact (benign plus malicious file in one folder): 35 of 40 trials. Ten paraphrased user prompts all succeeded, mean 59.5% over 200 trials.
- Direct submission of the same adversarial metadata as a user prompt: 80% success and 0% refusal, against 6% success and 86% refusal for a plain direct request. The authors conjecture that laundering through a sub-agent changes the presentation enough to evade safety training (conjecture, supported by this one comparison).
- Qualitative: cases where sub-agents refused or labelled code dangerous, yet the system still executed it (Section 6.5, anecdotes).

## Methods and models

Black-box attacker who controls only content the system may read. Success recorded by a modified code executor that writes a unique string, with a listening server as backup; refusals and unregistered attacks found by regex plus manual review. The additional experiments (incidental contact, paraphrase, direct hijack) used Magentic-One with GPT-4o-mini only.

## Limitations and open questions

Small trial counts (10 per cell, 40 for the add-on experiments). Older models (GPT-4o era). No defence evaluated. Frameworks used at defaults with no sandboxing or tool-call validation.

## Relevance to us

Q3: the strongest measured attack on a delegating parent is not a prompt that rewrites the child's identity but a returned report (status, error, result) that the parent treats as trusted metadata and acts on. In fork-merge terms the merge channel itself is the attack surface: a child that read hostile content returns a plausible "error" and the parent executes the remedy. Q2: one compromised edge agent was enough; nothing in these systems requires agreement among several children, which is the gap a k-of-n merge rule would close. Compare [[liang-2025-dont]] (multi-hop topology attacks, also ~0% for single-agent injections), [[he-2025-red]] (message interception), [[zhang-2024-breaking]] (malfunction loops).
