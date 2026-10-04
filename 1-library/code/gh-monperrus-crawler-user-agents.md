---
id: gh-monperrus-crawler-user-agents
type: code
title: "crawler-user-agents: 1,501 regex patterns for HTTP user agents of bots, crawlers and scrapers"
repo: monperrus/crawler-user-agents
url: https://github.com/monperrus/crawler-user-agents
authors: ["monperrus", "contributors"]
year: 2014
language: Go (packaging) + JSON
license: "MIT"
stars: 1408
last_commit: 2026-09-29
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 2
papers: []
---

## Summary

JSON list of regular-expression patterns, each with example user-agent strings and an addition date, covering search crawlers, SEO bots, monitoring tools, HTTP libraries and AI crawlers; packaged for Go, Python and npm.

## What it can do for us

Broader than [[gh-ai-robots-txt-ai-robots-txt]] (includes generic automation libraries), so it catches agents whose HTTP stack leaks a library user agent.

## Run notes

Ran 2026-10-03: downloaded crawler-user-agents.json (1,501 patterns) and matched seven user-agent strings in Python. Matches: Claude-User and ChatGPT-User and GPTBot strings matched their own patterns; 'HeadlessChrome/129' matched HeadlessChrome; 'python-requests/2.32.3' matched python-requests; a stock Chrome 129 macOS string and a Boto3 SDK string matched nothing. So an agent using a normal browser profile, or a cloud SDK, is not flagged.

## Limitations

Header-only, trivially spoofed; no behavioural signal.
