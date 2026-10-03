---
id: openai-2024-covert
type: blog
title: "AI and Covert Influence Operations: Latest Trends"
authors: [Ben Nimmo]
year: 2024
url: https://downloads.ctfassets.net/kftzwdyauwt9/5IMxzTmUclSOAcWUXbkVrK/3cfab518e6b10789ab8843bcca18b633/Threat_Intel_Report.pdf
site: OpenAI threat intelligence report (PDF, 39 pages)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

OpenAI's first public report on covert influence operations (May 2024), covering five networks banned in the prior three months: "Bad Grammar" (new, Russia, Telegram), Doppelganger (Russia), Spamouflage (China), the International Union of Virtual Media (Iran) and "Zero Zeno", run by the Israeli commercial firm STOIC. None scored above Category 2 on the Breakout Scale (Bad Grammar stayed at 1); OpenAI concludes AI increased volume and polish but not authentic engagement. Cross-case trends: all used the model for content, none exclusively (AI text was mixed with human-written posts and copied memes); several faked engagement by generating both a post and the replies to it (Zero Zeno on Instagram and X; Spamouflage threads attacking Cai Xia where every reply was generated); Bad Grammar used the model to debug a Telegram auto-posting pipeline and posted from at least a dozen Telegram accounts. Human error exposed operations: Bad Grammar posted the model's refusal messages, IUVM auto-generated website tags that included model messages, Doppelganger captioned Gaza footage with a Ukraine comment. OpenAI says its own AI tools cut some investigative workflows from hours or days to minutes, and it published domains and shared indicators with peers.

## Key claims

- "Evolution, not revolution": AI improves operator productivity but does not solve distribution.
- Self-reply threads (post plus generated replies) are a common way AI-enabled IO fakes engagement.
- Leaked refusal and error text is a recurring exposure route.

## Evidence quality

Vendor report building on prior platform and open-source research (EU DisinfoLab, Meta, Microsoft, Mandiant, Graphika, ASPI, DFRLab). Skimmed: read the introduction, trends and defender sections and the start of the Bad Grammar case; did not read the remaining case studies in full. No false-positive rates.

## Relevance to us

The baseline for the later series ([[openai-2025-disrupting]], [[openai-2025-disrupting-update]]) and the source of two detection signals that recur in every later report: leaked model text and network self-replies. The same STOIC network appears on the platform side in [[meta-2024-adversarial]], which lets the two vantage points be compared on one operation.
