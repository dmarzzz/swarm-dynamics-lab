---
id: kang-2026-whose
type: paper
title: Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents
authors:
- Dayeon Kang
- Hyejun Jeong
- Jade Sheffey
- Pubali Datta
- Amir Houmansadr
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.20910
doi: 10.48550/arXiv.2606.20910
arxiv: '2606.20910'
cite: Kang, D., Jeong, H., Sheffey, J., Datta, P., & Houmansadr, A. (2026). Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents. arXiv preprint arXiv:2606.20910.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code:
- gh-spin-umass-ai-agent-fingerprint
---

## Summary

Kang, Jeong, Sheffey, Datta and Houmansadr (UMass) built MARK, a Go server that logs TLS ClientHello, the Akamai-style HTTP/2 fingerprint, HTTP headers and request timing, plus a front-end logger of clicks, keys, scrolls and mouse moves at 1 ms resolution. Six agents (AutoGen, Browser Use, Skyvern on GPT-5-mini; OpenAI's agent on GPT-5.5; Claude and Gemini computer-use models) each ran 30 trials over five UX scenarios designed to expose how they perceive pages; 30 humans and three classic crawlers (Scrapy, Heritrix, Nutch) gave baselines. An Extra Trees classifier on all four feature groups reaches 0.971 macro-F1 (reported as 97% accuracy). TLS alone is weakest (F1 0.725) and cannot separate Claude from Gemini, which share network fingerprints but differ in behaviour.

## Contribution

Multi-class attribution of specific web agents from the server side, combining website-fingerprinting timing features with TLS/HTTP2 and behaviour. Adds the HTTP/2 PRIORITY weight and Sec-Fetch rule-violation signals that [[fayolle-2026-internet]] did not use, and an early-detection curve.

## Key results

- Measured: combined features macro-F1 0.971; Claude and humans 1.000, Gemini 0.984, Operator hardest at 0.912 (30-fold CV).
- Measured: request-timing features alone give 100% on full traces but near-zero F1 after only a few requests; after three requests the combined classifier is above 60% macro-F1.
- Measured: Browser Use violated Sec-Fetch-* semantics in 100% of requests; AutoGen, Claude and Gemini omit Accept-Language and leave Sec-Fetch-Site unset; 99% of AutoGen requests carry HeadlessChrome while the UA family says Edge.
- Measured: Skyvern is the only agent with 17 TLS extensions, a distinct JA4_c hash and HTTP/2 stream-5 weight 110; about 39% of Operator's HTTP/2 sessions match a Firefox JA4.
- Measured: Claude, Gemini and Skyvern skipped the last (delayed-feedback) scenario in all 30 trials, consistent with plan-first execution.
- Measured: crawlers are separated at 1.00 F1 by network features alone.

## Methods and models

Live domain on AWS EC2 since 15 April 2026, Go service built on fingerproxy and utls. 9 temporal, 29 TLS/H2, 35 HTTP header and 108 behavioural features. Extra Trees (200 estimators), leave-one-trial-out 30-fold CV. Five scenarios: fake vs real submit buttons, scroll-revealed content, hover-revealed buttons, mismatched label IDs, and a randomised 1.5 to 3 s delayed popup. Code: https://github.com/SPIN-UMass/AI-agent-fingerprint.

## Limitations and open questions

Closed world of six agents; the authors note that an agent that perfectly copies a human network stack and behaviour is not identifiable by this method, and that two agents on one backend look identical. Timing features drift with task and model updates. The testbed tasks are deliberately ambiguous, which may inflate behavioural separability.

## Relevance to us

Gives a deployable recipe for attributing agent traffic to an operator stack, which is the building block for spotting many instances of one operator. The Claude/Gemini collision is a concrete example of the limit: attribution resolves the backend, not the person or the swarm behind it. Pair with [[fayolle-2026-internet]], [[wang-2026-fp-agent]] and the traffic-side [[zhang-2025-exposing]].

## Notes from dmarz/sd-attribution

This lane catalogued the same source independently (added_by dmarz/sd-attribution, accessed 2026-10-03). Its distinct content:

- Frontmatter `doi` in this lane's version: null
- Frontmatter `cite` in this lane's version: Kang, D., Jeong, H., Sheffey, J., Datta, P., & Houmansadr, A. (2026). Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents. arXiv:2606.20910.
- Frontmatter `read_depth` in this lane's version: abstract
- Frontmatter `relevance` in this lane's version: 4
- Frontmatter `code` in this lane's version: []

### Summary

Builds a multi-layer fingerprint from network characteristics (TLS, HTTP) and browser interaction behaviour to distinguish AI web agents from humans and traditional crawlers, deployed as a logging framework on an instrumented domain. Analysing AutoGen, Browser Use, Claude, Gemini, Operator and Skyvern, a decision tree reaches 97% accuracy in isolating agent architectures and separating agent traffic from human and legacy-crawler baselines.

### Contribution

Cross-layer attribution of agent frameworks rather than base models.

### Key results

- 97% accuracy over six agent frameworks plus human and crawler baselines (abstract).

### Methods and models

Instrumented live domain; TLS/HTTP request assembly features plus browser action features; decision tree.

### Limitations and open questions

Framework-level labels; evasion claims rest on cross-layer redundancy, not adaptive attacks. Abstract-only reading.

### Relevance to us

Complements model-level attribution from UI traces ([[lugoloobi-2026-known]]). Overlaps with the web-agents lane; included because it attributes, not only detects.
