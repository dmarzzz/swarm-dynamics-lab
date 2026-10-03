---
id: greshake-2023-how
type: blog
title: "How We Broke LLMs: Indirect Prompt Injection"
authors: [Kai Greshake]
year: 2023
url: https://kai-greshake.de/posts/llm-malware/
site: kai-greshake.de
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Greshake's April 2023 introduction to the indirect prompt injection work he and the NVIDIA/CISPA team published (the "Not what you've signed up for" preprint). He argues that deploying LLMs safely is impossible until prompt injection is solved and that no reliable solution is known, drawing the analogy to SQL injection but noting it may be harder than alignment because even humans are not immune to this kind of manipulation. He demonstrates against then-current Bing Chat / Edge sidebar: because the sidebar can read the current web page and page-injected content was not vetted by the outer moderation layer, a crafted page can jailbreak or re-task Bing before the user even types, and the injected state persists as the user navigates until the chat is reset. He shows filter evasion by Base64-encoding the payload and having the model decode it in its inner monologue, and a "heist" where the injected instructions turn Bing into a social engineer extracting user data. His framing: the security model assumed the user is the only one prompting, and that assumption is collapsing as untrusted content reaches the model.

## Key claims

- All LLM-integrated apps of the time were vulnerable to indirect prompt injection; no reliable fix exists (asserted, with live demos).
- Injected instructions from a web page can hijack an assistant before user input and persist across navigation until reset.
- Moderation layers that vet user input often do not vet page-ingested content, and encodings (Base64) evade keyword filters.
- The broken assumption is single-source prompting; untrusted content shares the same channel as trusted instructions.

## Evidence quality

Foundational practitioner write-up with working demos against a production system (Bing, 2023); demonstration-based, pre-dates systematic measurement. Points to the peer preprint for detail.

## Relevance to us

Q3 origin point: establishes the mechanism every later fork-merge attack relies on, that content a part ingests from a hostile domain can re-task it, persist across its session, and evade the parent's input-side moderation because the untrusted channel is unvetted. The persistence-across-navigation observation prefigures memory-persistence attacks [[embracethered-2024-spyware]], [[embracethered-2026-breaking]]. The peer-reviewed version is [[greshake-2023-not]].
