---
id: openai-2025-disrupting
type: blog
title: "Disrupting malicious uses of AI: June 2025"
authors: [Ben Nimmo, Albert Zhang, Sophia Farquhar, Max Murphy, Kimo Bumanglag]
year: 2025
url: https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf
site: OpenAI threat intelligence report (PDF, 46 pages)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor threat-intelligence report (June 2025) with ten case studies of ChatGPT accounts OpenAI banned in the three months before publication; four of ten likely had a Chinese origin. Five cases are covert influence operations (IO) that used the model to mass-produce short social media comments posted by networks of inauthentic accounts. The detection signal in every case is the operator's prompt and completion log on OpenAI's side, which investigators then match to posts found on TikTok, X, Facebook, Reddit, Telegram and Bluesky with open-source methods. Impact is graded on Nimmo's IO Breakout Scale (1 to 6); every IO in the report is rated Category 1 to 3.

Measured details from the cases:

- "Sneer Review" (likely China): a "main" account posts, then other network accounts reply to simulate debate. On one TikTok video attacking activist Mahrang Baloch the operation generated 220 comments while the video showed 199, so most visible engagement was AI-generated. The operators also asked ChatGPT to write an internal performance review describing how the operation was run, and the observed account behaviour matched that document.
- "High Five" (Philippines, linked to marketing firm Comm&Sense Inc): five TikTok channels posting the same videos with different captions, plus dozens of commenting accounts that posted no videos, followed nobody and had 0 to 10 followers. Thousands of comments; none got more than single-digit replies, likes or shares. After the ban the actor tried several times to return.
- "Uncle Spam" (China, lead from Meta): generated content on both sides of US tariff debates and asked the model for optimal posting times, which OpenAI reads as adaptation to the old giveaway of posting on China working hours.
- STORM-2035 (Iran, recidivist): batches of about a dozen tweets in Spanish and English, posted by accounts that followed far more accounts than followed them; typical tweet 150 to 350 views and zero engagement.
- A China-linked cyber actor wrote code to drive a fleet of Android phones to post and like on X, Facebook, Instagram and TikTok (a phone-farm controller).
- "ScopeCreep" used throwaway emails and one conversation per account to evade linkage, and was still caught by "scaled cyber abuse detection".

## Key claims

- AI built into every stage of an operation "also increased their exposure": the model provider sees the whole workflow, so provider-side logs are a strong detection vantage point (claim, supported by the cases).
- Most AI-enabled IO in the report failed to gain authentic engagement (measured per case with public view and like counts, which the report itself warns may be inflated by the same networks).
- Classic network signals still identify the accounts: freshly created accounts, follower/following asymmetry, mismatched name scripts and languages, recycled profile photos, and replies only from the same network.

## Evidence quality

Primary vendor report with screenshots and engagement counts; no released data, no indicators beyond screenshots, no false-positive rates. Attribution is hedged ("likely", "consistent with"). The detection method on OpenAI's side (classifiers, "AI as a force multiplier for our expert investigative teams") is not described in detail. Later reports continue the series: [[openai-2025-disrupting-update]].

## Relevance to us

The best public evidence on what LLM-run account swarms look like in the wild in 2025: small (dozens to about a hundred accounts), cheap, low-engagement, and detected mainly from the model provider's side rather than the platform's. The self-reply pattern (main post plus network replies) and the 220-vs-199 comment count are concrete signatures a detector could target. Pairs with [[anthropic-2025-detecting]], which reports an LLM deciding engagement actions for over 100 bot accounts.


## Notes from shadow/sol-g49

Reopened primary PDF text via Exa 2026-10-03. It contains ten selected cases over the preceding three months, not ten sampled operators from a representative population; method combines provider prompts/completions and open-source social-account matching. Confirms high-volume synthetic comments and low/uncertain authentic engagement. Published 2025-06-05. No raw labelled account/session dataset supplied by this report, licence/access of incident prose does not imply access to internal API logs.
