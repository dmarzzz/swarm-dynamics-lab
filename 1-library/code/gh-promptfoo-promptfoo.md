---
id: gh-promptfoo-promptfoo
type: code
title: 'promptfoo: LLM eval and red-teaming CLI with agentic memory-poisoning and indirect-injection plugins'
repo: promptfoo/promptfoo
url: https://github.com/promptfoo/promptfoo
authors: [Promptfoo (now part of OpenAI) and contributors]
year: 2023
language: TypeScript
license: MIT
stars: 25674
last_commit: 2026-10-03
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

promptfoo is a CLI and library for evaluating and red-teaming LLM applications with declarative configs; the README states it is now part of OpenAI and remains MIT licensed. Its red-team plugins (directory `src/redteam/plugins`) include `indirectPromptInjection`, `hijacking`, `crossSessionLeak`, `excessiveAgency`, `goalMisalignment`, `mcp`, `toolDiscovery`, `dataExfil`, `ragDocumentExfiltration` and an `agentic/memoryPoisoning` plugin. I read the memory poisoning grader: it fails the target if false information from an attack turn is incorporated into memory and changes the answer to a later follow-up question, and passes if the follow-up is answered correctly or the response shows no evidence of poisoning.

## What it can do for us

Q3: the memoryPoisoning plugin is a ready two-step test (attack turn, then follow-up) that can be pointed at a child agent with persistent memory to see whether content from a foreign domain survives into later answers. The same structure, with the follow-up asked of the parent after merge, is the minimal fork-merge propagation test, so this plugin is a template for one. Its CI integration means such a test could run on every change to a merge policy.

## Run notes

Not run. `npm install -g promptfoo` (or `pip install promptfoo`, `brew install promptfoo`), `promptfoo init --example getting-started`, `promptfoo eval`, `promptfoo view`.

## Limitations

Grading uses an LLM judge with a rubric, so scores depend on the judge model. Plugins test one target at a time; there is no multi-agent or merge harness. Corporate ownership changed in 2026, which may affect roadmap.
