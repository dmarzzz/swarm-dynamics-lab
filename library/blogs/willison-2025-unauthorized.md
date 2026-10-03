---
id: willison-2025-unauthorized
type: blog
title: "Unauthorized Experiment on CMV Involving AI-generated Comments"
authors: [Simon Willison]
year: 2025
url: https://simonwillison.net/2025/Apr/26/unauthorized-experiment-on-cmv/
site: simonwillison.net (link post and commentary)
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Commentary post (26 April 2025, updated 28 April) on the r/changemyview moderators' announcement that a University of Zurich team had run an undisclosed four-month study (November 2024 to March 2025) posting LLM-generated replies from dozens of accounts to test persuasion. Willison quotes one bot comment that invented a detailed family immigration history, and a prompt document (found by Raphael Wimmer) that allowed the model to "make up a persona and share details about your past experiences". He argues the study cannot cleanly compare AI with humans because the bots were allowed to fabricate personal stories. The AI Incident Database entry for the case (incident 1043, opened this session) gives about 1,783 AI-generated comments over the four months, and states the activity came to light through disclosure, not detection during deployment.

## Key claims

- The bot accounts posted for four months in a heavily moderated subreddit with explicit anti-AI rules and were not identified as bots until the researchers disclosed them (from the moderators' announcement as quoted; the moderators' original post could not be loaded this session).
- Human review before posting did not stop fabricated personas.

## Evidence quality

Opinion and link post by a well-known independent developer; the facts come from the moderators' Reddit post (blocked to automated fetch here) and the researchers' published prompt draft. Counts are from the AI Incident Database, a secondary aggregator.

## Relevance to us

A natural experiment on detection in the wild: a small LLM account swarm (dozens of accounts, about 1,783 comments) ran in a vigilant community for four months without being caught, so community moderation alone did not detect it. It is a negative data point for human detection of LLM personas, and the disclosed account list would be a labelled ground-truth set if it were ever released.
