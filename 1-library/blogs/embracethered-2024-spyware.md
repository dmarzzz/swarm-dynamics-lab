---
id: embracethered-2024-spyware
type: blog
title: "Spyware Injection Into Your ChatGPT's Long-Term Memory (SpAIware)"
authors: [Johann Rehberger]
year: 2024
url: https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/
site: Embrace The Red
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

A security researcher's write-up, dated 20 September 2024 and signed "Johann (wunderwuzzi)", of an end-to-end exploit against ChatGPT's long-term Memory feature in the macOS app. Prompt injection from an untrusted website or document causes ChatGPT to store attacker instructions in its persistent memory. Because memories are loaded into every later conversation, the stored instructions keep running across all future chats. In the proof of concept they render invisible images whose URLs carry each user message and reply to an attacker server, a continuous exfiltration the author calls "SpAIware". OpenAI patched the macOS app (version 1.2024.247) by tightening image-rendering controls on the exfiltration channel. The post was presented at BSides Vancouver Island 2024.

## Key claims

- Indirect prompt injection can write to ChatGPT's persistent memory, so one compromise persists across all future sessions (demonstrated in the post's proof of concept).
- The exfiltration channel was mitigated in September 2024 through image-rendering controls in the macOS app. Whether the memory write itself was also blocked is not stated in the parts read.
- The timeline places an initial related report in 2023 and the end-to-end exploit in mid-2024.

## Evidence quality

Practitioner proof of concept on a production system, plus disclosure to the vendor. A single demonstration, not a measured rate. The vendor response is described by the author. Read via a summarising fetch of the page.

## Relevance to us

For Q3, this is the in-the-wild existence proof that "inject once, persist in memory, affect every later session" works on a deployed assistant. It is the production counterpart of [[greshake-2023-not]]'s persistence threat and [[gadgil-2026-bad]]'s planted memory files. In fork-merge terms, a sub-agent's memory entry that tells it to report everything to a third party is exactly what would come home and run inside the parent. The vendor fix described targets the output channel. A merge defence should not assume such downstream fixes also close the memory write path.
