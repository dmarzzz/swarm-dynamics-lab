---
id: seiden-2026-identifying
type: paper
title: Identifying AI Web Scrapers Using Canary Tokens
authors:
- Steven Seiden
- Triss Ren
- Caroline Zhang
- Taein Kim
- Enze Liu
- Emily Wenger
year: 2026
venue: ACM CCS 2026 (arXiv preprint)
url: https://arxiv.org/html/2605.13706
doi: null
arxiv: '2605.13706'
cite: Seiden, S., Ren, T., Zhang, C., Kim, T., Liu, E., & Wenger, E. (2026). Identifying AI Web Scrapers Using Canary Tokens. In Proceedings of the 2026 ACM SIGSAC Conference on Computer and Communications Security (CCS). arXiv:2605.13706.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

The authors bought 20 fresh .com domains and served each distinct visitor (unique User-Agent plus ASN pair) its own version of every page, with 10 placeholders filled by visitor-specific canary values (names, places, numbers). After two months they asked production AI chatbots with web search about each fictitious person or company and matched canary values in the answers back to the visitor that had been served them. This links an opaque chatbot to the scraper identity that fed it, without cooperation from the provider.

## Contribution

Turns per-visitor content differentiation (a honeytoken per crawler) into an attribution side channel for AI systems. It is the cleanest published template for "serve every unknown agent a unique bait, watch where the bait resurfaces".

## Key results

- Sites saw 313 to 674 unique (User-Agent, ASN) visitors each; 4,042 across all 20 sites (measured).
- Of 22 chatbots identified, 18 returned site content and could be mapped; DeepSeek, Hunyuan, GLM and Liquid returned nothing (measured, v2 of the paper; the v1 abstract says 22 systems).
- 10 first-party declared User-Agents recovered, confirming the method; 6 of 18 systems fetched with generic browser User-Agents (ERNIE, Grok, Solar, Qwen, Kimi among them), and Kimi appears to rotate through many User-Agent strings (measured, last point inferred).
- 10 of 18 systems surfaced content first served to Googlebot, Bingbot or Bravebot, some undisclosed (e.g. Qwen and Perplexity via Googlebot); ASN checks showed these were real search-engine crawlers, so chatbots relay search indexes (measured).
- After sites went offline, 7 of 8 search-backed chatbots still returned the content a week later; 12 of 18 kept returning content under both offline and robots.txt-disallow conditions; only Duck.ai stopped (measured).
- False positives are bounded by token-space size: smallest canary space 4,761 values; single-token, single-site matches discarded.

## Methods and models

Human-written fictitious site templates; tokens from Python Faker and RNG; sites indexed via Google/Bing webmaster tools and Brave; two-prompt elicitation per chatbot per site (March to April 2026); match score combines token count and number of distinct interactions; three conditions (online, offline, robots.txt disallow-all).

## Limitations and open questions

20 sites, one U.S. university vantage point, scraper identity defined coarsely (User-Agent plus ASN; TLS or browser fingerprints suggested as extensions). Adversaries who detect differentiated content or strip specifics evade it. Faker caused some token collisions that had to be discarded.

## Relevance to us

Directly reusable for swarm detection: give each visiting agent a unique canary and observe where it reappears (another agent's post, a chatbot answer, a marketplace listing). The same match-scoring handles multi-source contamination. Pairs with [[fayolle-2026-internet]] (fingerprints at the visit) and [[liu-2024-somesite]] (robots.txt efficacy). The statistical framing echoes [[rao-2025-detecting]]. Classic honeytoken lineage: [[farooqi-2020-canarytrap]].

## Notes from dmarz/sd-web-agents

This lane catalogued the same source independently (added_by dmarz/sd-web-agents, accessed 2026-10-03). Its distinct content:

- Frontmatter `url` in this lane's version: https://arxiv.org/abs/2605.13706
- Frontmatter `doi` in this lane's version: 10.48550/arXiv.2605.13706
- Frontmatter `cite` in this lane's version: Seiden, S., Ren, T., Zhang, C., Kim, T., Liu, E., & Wenger, E. (2026). Identifying AI Web Scrapers Using Canary Tokens. In Proceedings of the 2026 ACM SIGSAC Conference on Computer and Communications Security (CCS 2026), to appear. arXiv preprint arXiv:2605.13706.
- Frontmatter `read_depth` in this lane's version: skim

### Summary

Seiden, Ren, Zhang, Kim, Liu and Wenger host 20 fictitious websites that serve every distinct scraper (unique User-Agent plus ASN pair) its own set of ten canary values, then ask 22 production chatbots about those sites and match canaries in the answers back to the scraper that was served them. After two months online (313 to 674 unique visitors per site), canaries were elicited from 18 chatbots. They recovered 10 self-declared first-party crawler User-Agents, found 6 of 18 systems feeding on generic browser User-Agents (Kimi appears to rotate through many), and found 10 of 18 relaying content only served to Googlebot, Bingbot or Bravebot, several undisclosed. Seven of eight search-backed chatbots kept returning canaries a week after the sites went offline.

### Contribution

A canary-token honeypot that attributes scrapers to downstream AI systems through the model's own output, without needing the scraper to identify itself. This is attribution by content side channel rather than by traffic fingerprint.

### Key results

- Measured: canary tokens elicited from 18 of 22 chatbots; none from DeepSeek, Hunyuan, GLM, Liquid.
- Measured: 10 first-party declared crawler User-Agents matched; 6 of 18 systems linked to generic browser User-Agents.
- Measured: 10 of 18 systems returned content served only to third-party search crawlers; ASN checks (15169 for Googlebot) indicate the crawlers were genuine, so the chatbots read search indexes.
- Measured: 7 of 8 search-backed chatbots still returned canaries one week after sites went offline; robots.txt blocking is largely ineffective once content is indexed.
- Design: per-token collision probability is small; the smallest canary space was 4,761 values.

### Methods and models

Twenty .com domains on Google Cloud, submitted to Google, Bing and Brave indexes; canaries from Python Faker; scraper identity = (User-Agent, ASN); two-prompt elicitation per site per chatbot, via API or Selenium/nodriver; matching thresholds on token count and number of interactions; three stages (online, offline vs robots.txt, back online), March to April 2026.

### Limitations and open questions

I read the method and RQ1 to RQ2 results, not the robots.txt-condition results or discussion in full. Identity granularity is coarse (UA plus ASN), so many agents behind one cloud ASN with one generic UA collapse together. False negatives are likely when chatbots truncate or paraphrase.

### Relevance to us

Strong template for a swarm honeypot: serve each visitor class a unique fact, then watch where those facts surface (in model outputs, posts, or market actions). It turns downstream behaviour into an attribution channel that survives User-Agent spoofing, which [[fayolle-2026-internet]] and [[kang-2026-whose]] cannot handle when agents run from residential browsers. Same group as [[kim-2025-scrapers]] and [[liu-2025-somesite]].
