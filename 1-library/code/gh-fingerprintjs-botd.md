---
id: gh-fingerprintjs-botd
type: code
title: "BotD: open-source in-browser detector of automation frameworks (Selenium, Puppeteer, Playwright, headless browsers)"
repo: fingerprintjs/BotD
url: https://github.com/fingerprintjs/BotD
authors: ["FingerprintJS"]
year: 2021
language: TypeScript
license: "MIT"
stars: 1478
last_commit: 2026-06-17
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Client-side JavaScript library that inspects browser properties for traces of automation tools and headless browsers and returns `{bot: true|false, botKind}`. Maintained in stability-only mode; the vendor's commercial Fingerprint Pro product handles more advanced bots.

## What it can do for us

Baseline for detecting browser-driving AI agents (Operator, browser-use, Playwright-based agents) by their automation stack. Testing which agent frameworks it flags would be a cheap experiment.

## Run notes

Not run (requires a browser page).

## Limitations

Detects 'basic bots' by its own description; stealth patches (for example the many 'anti-detection browser for AI agents' repos with thousands of stars, such as jo-inc/camofox-browser at 11.4k stars) are built to defeat exactly these checks. No new features planned.
