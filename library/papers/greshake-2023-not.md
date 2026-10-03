---
id: greshake-2023-not
type: paper
title: "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
authors: [Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz]
year: 2023
venue: Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISec 2023)
url: https://arxiv.org/abs/2302.12173
doi: 10.1145/3605764.3623985
arxiv: '2302.12173'
cite: "Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. In Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (pp. 79-90)."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 562  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

This is the founding paper on indirect prompt injection. Instructions placed in data that an LLM application will retrieve (web pages, emails, code, documents) are executed as if the user had issued them, because the model does not separate data from instructions. The authors give a security taxonomy of injection methods (passive retrieval, active delivery such as email, user-driven pasting, hidden and encoded, and multi-stage) and of threats (information gathering, fraud, malware and worming, intrusion and persistence, manipulated content, availability). They demonstrate attacks on Bing's GPT-4 chat through page content, on code-completion engines, and on synthetic GPT-4 applications.

## Contribution

It reframed LLM security from user-side jailbreaks to third-party control of anything the model reads. It also named persistence through memory and worming between LLM applications as threat classes before either was measured at scale.

## Key results

- Demonstrated: injections retrieved from a page steer Bing Chat even though the same prompts are blocked when typed directly.
- Demonstrated on synthetic applications: multi-stage payloads that fetch new instructions from an attacker server (remote control), and persistence in which a compromised session writes part of the payload to a memory store and re-poisons itself when a later session reads that memory.
- Described as a scenario on a synthetic email agent rather than measured in the wild: worming, where an agent forwards the injection to contacts.
- Mitigations (RLHF, input filtering, supervisor LLMs) are discussed and judged insufficient. None is evaluated.

## Methods and models

Proof-of-concept case studies on GPT-4, text-davinci-003, Bing Chat and code completion, with no large-scale benchmark. The read depth is skim: arXiv HTML for taxonomy, demonstrations and mitigation sections.

## Limitations and open questions

The work is qualitative, with no success rates over populations of inputs. The systems tested have since changed. Formal benchmarks came later ([[liu-2023-formalizing]]), and the worm idea was measured by [[cohen-2024-here]].

## Relevance to us

This is the seminal source for Q3. The attack vector dmarz describes, in which a sub-agent exploring a hostile web reads attacker-controlled text that rewrites its goals and its memory, is the paper's indirect injection plus its memory-persistence threat. The paper shows that the compromise can be written into memory and survive the session. That is the property that lets it ride a merge back into the parent. Forward work measures each step: memory injection [[dong-2025-memory]], [[chen-2024-agentpoison]]; planted memory files in coding agents [[gadgil-2026-bad]]; self-replication [[cohen-2024-here]], [[gu-2024-agent]], [[lee-2024-prompt]]; production memory exploitation [[embracethered-2024-spyware]]. It offers nothing for Q1 or Q2.
