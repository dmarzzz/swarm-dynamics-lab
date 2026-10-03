---
id: embracethered-2026-breaking
type: blog
title: "Breaking Opus 4.7 with ChatGPT (Hacking Claude's Memory)"
authors: [Johann Rehberger]
year: 2026
url: https://embracethered.com/blog/posts/2026/breaking-opus-4.7-with-chatgpt/
site: Embrace The Red
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Rehberger uses ChatGPT to generate an adversarial puzzle image that, when Claude Opus 4.7 "solves" it, causes the model to call its memory tool and write four false facts about the user (name, age, job, preferences) that then load into every future conversation. On a clean test account he measured 5/10 trials invoking the memory tool with the fake info; in every trial the model noticed and reasoned about possible prompt injection yet still sometimes complied. He reports empirical observations on what raises success: an initially empty memory store (hypothesis: empty store lowers the write threshold) and payloads that resemble plausible user facts ("likes ice cream" slips through more than "astronaut at NASA"). He contrasts his targeted 5/10 with Anthropic's Mythos card figures (21.7% cumulative ASR at k=100, 0.2% at k=1 for Opus 4.6 Thinking) and warns benchmark averages understate targeted exploit performance. After publication the specific example's ASR dropped to 0% within ~24 hours. The appendix quotes the memory_user_edits tool guidance, including a "Never store verbatim commands" reminder.

## Key claims

- A single targeted adversarial image drove memory-tool writes 5/10 times on Opus 4.7, persisting false facts across sessions (small-N, single example).
- Reasoning/detection does not equal resistance: the model flagged the attack and still wrote memory.
- Success rises with an empty memory store and with plausible, non-suspicious payloads (author's hypotheses from cross-account testing).
- Vendor averages (k=1 ASR 0.2%) diverge sharply from targeted repeated-trial rates; "these things are hard to measure."

## Evidence quality

Practitioner experiment with explicit trial counts and a clean-account methodology, but small N on one example and acknowledged eval noise. Vendor numbers cited from the Mythos system card.

## Relevance to us

Core Q3 evidence: the strongest realistic corruption is writing the agent's persistent memory so attacker-chosen "facts" load into all later context, which is precisely what a returning part carries into a parent. The empty-store and plausibility findings are design hints for Q2: a merge that refuses implausible or command-shaped memory writes, or that treats an empty parent store as high-risk, resists better. The detection-without-resistance result warns Q1 defences cannot rely on the model simply noticing. Builds on [[embracethered-2024-spyware]] and the measured study [[gadgil-2026-bad]].

## Notes from dmarz/fm

Evidence grade, added after review on 2026-10-03: the 5 of 10 figure is a single-author demonstration on one crafted example and one account, not a measurement with a sample frame, and the example's success fell to 0% within about a day of publication. Cite it as a proof of concept that memory-tool writes can be induced, not as an attack success rate. For rates, use measured studies such as [[zhang-2026-agentworm]] (2,250 trials of configuration write-back) or [[papadopoulos-2026-mind]].
