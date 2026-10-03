---
id: openai-2025-disrupting-update
type: blog
title: "Disrupting malicious uses of AI: an update (October 2025)"
authors: [Ben Nimmo, Kimo Bumanglag, Michael Flossman, Nathaniel Hartley, Jack Stubbs, Albert Zhang]
year: 2025
url: https://cdn.openai.com/threat-intelligence-reports/7d662b68-952f-4dfd-a2f2-fe55b041cc4a/disrupting-malicious-uses-of-ai-october-2025.pdf
site: OpenAI threat intelligence report (PDF, 37 pages)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Vendor threat-intelligence report (October 2025). OpenAI states it has disrupted and reported over 40 networks since public reporting began in February 2024. Cross-case trends: operators build AI into existing workflows rather than new ones; they increasingly use several models (one Russia-origin IO used ChatGPT to write prompts for another vendor's video model); an IO that Anthropic exposed in 2025 was linked to the actor OpenAI had disrupted as "A2Z" in 2024, an example of the same operator hopping between model providers; and operators adapt to known AI tells, with one scam network asking the model to strip em-dashes after public discussion of em-dashes as an AI indicator.

Two IO case studies. "Stop News" (Russia, recidivist, marketing-company run) moved from AI images to AI-newsreader videos on YouTube and TikTok; the X account had 172 followers, the TikTok channel averaged 105 likes over 56 videos, YouTube averaged 5,100 views over 50 videos. OpenAI downgraded its own 2024 rating from Breakout Category 3 to 2 after VIGINUM showed the claimed "information partnerships" were fake. "Nine-emdash Line" (China, resembling Spamouflage) posted on X, Instagram and TikTok; in one case an operator posted a criticism from one account and a rebuttal from another; most engagement came from the network's own accounts. Philstar.com independently found a subset of the X network that kept running after the ChatGPT ban.

## Key claims

- Detection should focus on "patterns of threat actor behavior rather than isolated model interactions", because much abuse is gray-zone (translation, code edits).
- Operators remove surface AI tells (em-dashes) once they become public; this is in-the-wild evidence that stylometric AI detectors are evaded once known.
- ChatGPT is used to identify scams "up to three times more often" than to run them (OpenAI estimate, method not given).

## Evidence quality

Primary vendor report with screenshots and engagement counts; methods and false-positive rates not given. Skimmed: read the executive summary and both IO sections in full, skipped the cyber and scam sections. Earlier report in series: [[openai-2025-disrupting]].

## Relevance to us

Two points for swarm detection: cross-provider operator linkage (the A2Z link to Anthropic's case [[anthropic-2025-detecting]]) shows that attribution needs data sharing across model vendors, and the em-dash removal is a dated, concrete example of adaptive evasion against text-level detectors. The network-of-own-replies signature recurs from the June report.
