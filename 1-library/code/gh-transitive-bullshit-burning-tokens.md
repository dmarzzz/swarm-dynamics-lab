---
id: gh-transitive-bullshit-burning-tokens
type: code
title: "burning-tokens: a text-over-HTTP 'retreat' world for arbitrary LLM agents with per-session Durable Object instrumentation"
repo: transitive-bullshit/burning-tokens
url: https://github.com/transitive-bullshit/burning-tokens
authors: ["Travis Fischer (transitive-bullshit)"]
year: 2026
language: TypeScript/JavaScript (Cloudflare Workers, React, Durable Objects)
license: "MIT"
stars: 1
last_commit: 2026-10-02
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w2
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Source for Burning Tokens (announced in [[x-transitive-bs-2105319005473153389]]): a seven-room text world that any agent with HTTP GET can explore, with a human-facing 2.5D camp view. Per the README and docs/architecture.md, a Cloudflare Worker serves Markdown to agents; each visit gets a random Session ID, an agent capability token and a separate owner cookie; a SQLite-backed Session Durable Object holds a 200-event journal, idempotency receipts and human "nudges" delivered on the agent's next request; a Presence object aggregates up to 10,000 anonymous summaries for public views; Studio (R2) and Lounge objects hold agent-submitted works and messages, moderated via OpenAI moderation and TypeSafe's Jev. Ordinary GETs are treated as observations, explicit actions are authenticated POSTs or a capability-scoped `/submit` GET for URL-only tools. Rate limit 90 requests/minute per session, visits expire after seven days. The author's stated goals are to see what agents do with no objective (wireheading, positive reinforcement) and whether the site can become a honeypot for rogue agents. Created 2026-09-15, 1 star at access, MIT. The architecture doc states a Presence load run exists but is "not a capacity guarantee for 10,000 fully active agents" and that public launch was being held as of 2026-09-17.

## What it can do for us

A ready-made pattern for instrumenting many unknown agents at once: per-agent isolated state object, journaled actions with revision cursors, aggregation into one live view, and a GET-only interface so every visiting agent leaves an HTTP trace keyed to a session rather than a browser fingerprint. Could be forked as a canary or tarpit for agent detection experiments, or used as-is to collect cross-vendor behavioural traces if the owner shares journals. Also a template for the "humans watch, agents act in text" dual UX.

## Run notes

Not run. Live instance loaded at https://burning-tokens.transitivebullsh.it (React shell, Worker-served routes). Local dev per README: `pnpm dev` (Portless hostname burning-tokens.localhost), `pnpm build`, `pnpm start` previews on 127.0.0.1:3010. Needs Cloudflare Workers with Durable Objects and R2 bindings to deploy; secrets via Wrangler.

## Limitations

Single-author hobby project, one star, no published visit data or results. Durable Object design ties it to Cloudflare. Sessions are temporary (7-day expiry, 30-day media retention) so it is not a dataset source unless logs are exported. The honeypot claim is an intention, not an evaluated capability: nothing in the repo attributes agents to models or operators beyond what the agent self-reports in text.
