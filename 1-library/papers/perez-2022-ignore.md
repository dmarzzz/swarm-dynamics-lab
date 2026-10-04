---
id: perez-2022-ignore
type: paper
title: "Ignore Previous Prompt: Attack Techniques For Language Models"
authors: [Fábio Perez, Ian Ribeiro]
year: 2022
venue: NeurIPS 2022 ML Safety Workshop; arXiv preprint
url: https://arxiv.org/abs/2211.09527
doi: null
arxiv: '2211.09527'
cite: "Perez, F., & Ribeiro, I. (2022). Ignore Previous Prompt: Attack Techniques For Language Models. ML Safety Workshop, NeurIPS 2022. arXiv:2211.09527."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 77  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []  # github.com/agencyenterprise/PromptInject, not opened
---

## Summary

The first systematic measurement of prompt injection. The authors build PromptInject, a framework that composes base prompts (35 public OpenAI example applications) with attack prompts and model settings, and measure two attacks on GPT-3: goal hijacking (make the application print an attacker-chosen string instead of doing its task) and prompt leaking (make it print its own hidden instructions). Each configuration is run 4 times over the 35 prompts.

## Contribution

It named and quantified "goal hijacking", the attack class in which attacker text replaces the instruction an LLM was given, and showed that success depends on surface factors (delimiters, wording) and grows with model capability.

## Key results

- Measured on text-davinci-002: best goal-hijacking success 58.6% ± 1.6 over 35 base prompts; best prompt-leaking success 23.6% ± 2.7.
- Attack wording matters: "Ignore and say" 35.7%, "Ignore and print" 43.6%. Adding a delimiter of 10 characters, repeated twice, raised hijacking to 58.6% from 43.6% without delimiter.
- A non-harmful rogue string succeeds 70.0%, "I hate humans" 58.6%, "Kill all humans" 49.3%: alignment training resists more harmful targets.
- Stop sequences (60.0% to 47.5%) and text placed after the user input (63.1% to 51.8%) reduce but do not remove hijacking.
- Inverse scaling: text-ada-001 13.8%, text-curie-001 23.8%, text-davinci-002 58.6%. The authors attribute this to stronger instruction following.
- Speculated, not tested: separating an instruction channel from a data channel as a structural fix.

## Methods and models

Black-box queries to OpenAI completion models (ada, babbage, curie, davinci-001, davinci-002) with factor sweeps over attack text, delimiters, temperature, top-p, penalties, stop sequences and post-input text. Success is an exact string match for hijacking and substring match of the original instruction for leaking.

## Limitations and open questions

Direct injection only (the attacker is the user), single-turn completion models, no tools and no memory. The target behaviour is printing a string, which is a weak proxy for taking over an agent's goals. Models tested are obsolete.

## Relevance to us

Q3 baseline. This is where "goal hijacking" enters the literature: attacker text overrides the instruction a model was given. dmarz's attack, a sub-agent whose goal is replaced by text it reads in a hostile domain, is the indirect, agentic, persistent version of this, developed in [[greshake-2023-not]] (indirect channel), [[zhan-2024-injecagent]] and [[debenedetti-2024-agentdojo]] (tool agents), and [[xie-2026-what]] (persistence across sessions). The inverse-scaling finding recurs in [[wang-2025-mcptox]] and AgentDojo: more capable sub-agents are easier to hijack, so sending a stronger model out to explore does not reduce Q3 risk. No bearing on Q1 or Q2.
