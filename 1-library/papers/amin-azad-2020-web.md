---
id: amin-azad-2020-web
type: paper
title: "Web Runner 2049: Evaluating Third-Party Anti-bot Services"
authors: ["Babak Amin Azad", "Oleksii Starov", "Pierre Laperdrix", "Nick Nikiforakis"]
year: 2020
venue: "Detection of Intrusions and Malware, and Vulnerability Assessment (DIMVA 2020), LNCS 12223"
url: https://www.semanticscholar.org/paper/5dcf8d90def33a08bf8f60748bb70f87972daad3
doi: "10.1007/978-3-030-52683-2_7"
arxiv: null
cite: "Amin Azad, B., Starov, O., Laperdrix, P., & Nikiforakis, N. (2020). Web Runner 2049: Evaluating Third-Party Anti-bot Services. In Detection of Intrusions and Malware, and Vulnerability Assessment (DIMVA 2020), Lecture Notes in Computer Science, vol. 12223, pp. 135-159. Springer. https://doi.org/10.1007/978-3-030-52683-2_7."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "52 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Amin Azad, Starov, Laperdrix and Nikiforakis analyse the client JavaScript and, through grey-box and black-box tests, the back-end decisions of commercial anti-bot services. Browser fingerprinting lets more than 75% of protected sites stop basic bots built from Python scripts or PhantomJS, but bots that use less-automated browsers such as Safari on Mac or Chrome on Android bypass protection on up to 82% of protected sites.

## Contribution

First independent evaluation of commercial anti-bot vendors; shows protection depends on whether the bot's platform looks unusual.

## Key results

- Measured (abstract): over 75% of protected sites block basic Python/PhantomJS bots.
- Measured (abstract): up to 82% of protected sites bypassed using less common automation platforms.

## Methods and models

Static and dynamic analysis of vendor scripts; simulated bots on several automation tools and browsers. Abstract read from the Semantic Scholar record.

## Limitations and open questions

Abstract only; 2020 vendors and tools.

## Relevance to us

Predicts the finding in [[fayolle-2026-internet]] and [[ousat-2026-broken]] that agents inside a genuine user browser pass commercial checks: detection keys on platform rarity, not on automation itself.
