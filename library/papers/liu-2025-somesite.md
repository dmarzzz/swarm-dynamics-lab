---
id: liu-2025-somesite
type: paper
title: 'Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers'
authors:
- Enze Liu
- Elisa Luo
- Shawn Shan
- Geoffrey M. Voelker
- Ben Y. Zhao
- Stefan Savage
year: 2025
venue: ACM Internet Measurement Conference (IMC 2025)
url: https://arxiv.org/abs/2411.15091
doi: 10.1145/3730567.3732913
arxiv: '2411.15091'
cite: 'Liu, E., Luo, E., Shan, S., Voelker, G. M., Zhao, B. Y., & Savage, S. (2025). Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers. In Proceedings of the 2025 ACM Internet Measurement Conference (IMC ''25), pp. 78-99. https://doi.org/10.1145/3730567.3732913. arXiv:2411.15091.'
topics:
- swarm-detection
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 16 (Semantic Scholar, 2026-10-03)
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

## Notes from dmarz/sd-honeypots

Folded in by dmarz/sd-merge from the duplicate entry `liu-2024-somesite` (added_by dmarz/sd-honeypots, accessed 2026-10-03, read_depth abstract, relevance 3). Same source (same arXiv id and DOI); the kept id uses the year of the published version given in cite.

- Frontmatter `year` in the folded entry: 2024
- Frontmatter `venue` in the folded entry: ACM Internet Measurement Conference (IMC 2025); arXiv preprint 2024
- Frontmatter `cite` in the folded entry: 'Liu, E., Luo, E., Shan, S., Voelker, G. M., Zhao, B. Y., & Savage, S. (2025). Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers. In Proceedings of the ACM Internet Measurement Conference (IMC 2025), pp. 78–99. https://doi.org/10.1145/3730567.3732913'
- Frontmatter `relevance` in the folded entry: 3

### Summary

Large-scale measurement plus a user study of 203 professional artists on whether creators can keep AI crawlers away using robots.txt, NoAI meta tags and reverse-proxy crawler blocking. Artists want such tools but face hurdles in awareness and in the ability to deploy them (hosting restrictions), and robots.txt has limited efficacy against crawlers that do not respond to it. Network-level blockers in reverse proxies give stronger protection but are not widely deployed and have their own limits.

### Contribution

Establishes that self-declared crawler identity plus voluntary compliance is a weak basis for controlling AI agents on the web. This motivates identity inference from behaviour or traps ([[seiden-2026-identifying]], [[fayolle-2026-internet]]).

### Key results

- 203 professional artists surveyed; strong demand but low awareness and agency (abstract).
- robots.txt has limited efficacy against unresponsive crawlers; reverse-proxy blockers are stronger (abstract).

### Methods and models

Web measurement of robots.txt and blocker deployment; active crawler tests; user study. Abstract-level read. Note: arXiv year 2024, conference version IMC 2025 (authors ask to cite the conference version).

### Relevance to us

Background for the web-crawler slice of swarm detection: declared identity fails, so traps and fingerprints are needed. Shares an author (Enze Liu) with [[seiden-2026-identifying]]. Related: [[hoetzlein-2025-protecting]].
