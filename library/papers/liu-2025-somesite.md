---
id: liu-2025-somesite
type: paper
title: "Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers"
authors: ["Enze Liu", "Elisa Luo", "Shawn Shan", "Geoffrey M. Voelker", "Ben Y. Zhao", "Stefan Savage"]
year: 2025
venue: "ACM Internet Measurement Conference (IMC 2025)"
url: https://arxiv.org/abs/2411.15091
doi: "10.1145/3730567.3732913"
arxiv: "2411.15091"
cite: "Liu, E., Luo, E., Shan, S., Voelker, G. M., Zhao, B. Y., & Savage, S. (2025). Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers. In Proceedings of the 2025 ACM Internet Measurement Conference (IMC '25), pp. 78-99. https://doi.org/10.1145/3730567.3732913. arXiv:2411.15091."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "16 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Liu, Luo, Shan, Voelker, Zhao and Savage measure how well content creators, especially artists, can keep AI crawlers off their sites. They combine large-scale measurements of robots.txt and NoAI meta-tag adoption, a user study of 203 professional artists, and tests of reverse-proxy crawler blocking such as Cloudflare's. Artists want robots.txt-style controls but lack the technical access or awareness to deploy them, and robots.txt has limited effect on crawlers that do not honour it; reverse-proxy blockers protect better but are rarely deployed and have their own gaps.

## Contribution

Early systematic measurement of AI-crawler opt-out tools from the publisher side, frequently cited by the 2026 agent-fingerprinting papers ([[fayolle-2026-internet]], [[kang-2026-whose]], [[wang-2026-fp-agent]]) as the baseline that robots.txt is advisory and active blocking is rare.

## Key results

- Measured (abstract): user study of 203 professional artists shows strong demand but low awareness and agency to deploy robots.txt.
- Measured (abstract): robots.txt has limited efficacy against unresponsive crawlers; reverse-proxy blockers offer stronger protection but limited deployment.
- Cited by [[kang-2026-whose]]: active blocking is adopted by only about 2% of the top 10K websites (figure attributed to this paper; not checked here).

## Methods and models

Web measurement of opt-out signals, controlled tests of crawler behaviour, evaluation of reverse-proxy blocking, and a survey of artists. Details not read; abstract only.

## Limitations and open questions

Abstract only. Pre-dates browser agents as a traffic class; focuses on training and assistant crawlers that self-identify.

## Relevance to us

Background for why self-declared identity (User-Agent, robots.txt) cannot anchor swarm detection on the web. Same group later built the canary-token attribution in [[seiden-2026-identifying]].
