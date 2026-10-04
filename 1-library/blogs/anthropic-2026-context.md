---
id: anthropic-2026-context
type: blog
title: "Context windows"
authors:
- Anthropic
year: 2026
url: https://platform.claude.com/docs/en/build-with-claude/context-windows
site: platform.claude.com (vendor documentation)
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: full
relevance: 4
---
## Summary

Vendor documentation (undated page; year is the access year) for how Claude's context window is counted and managed. Its budget-relevant section, "Context awareness", says that Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5 and Haiku 4.5 are told their total context in the system prompt (`<budget:token_budget>200000</budget:token_budget>`) and, after every tool call, receive an injected line such as `Token usage: 35000/200000; 165000 remaining`. The API injects these automatically. Claude Opus 4.7 and later Opus models, Sonnet 5.5 and the Fable and Mythos 5.x models do not receive these tags; for them the page points to task budgets ([[anthropic-2026-task]]). The rest of the page covers what counts toward the window (system prompt, messages, tool definitions, output and thinking), 1M-token versus 200k windows by model, thinking-block retention rules, compaction, and overflow behaviour.

## Key claims

- Stated: some Claude models get a model-visible remaining-context countdown after each tool call; it cannot be turned off or sent by the user.
- Stated: the countdown is removed on newer Opus and Sonnet 5.5 models, replaced by the opt-in task budget.
- Stated: accuracy and recall degrade as token count grows ("context rot"), so less context can be better.
- Stated: 1M-token context is the default on listed newer models; others, including Sonnet 4.5, have 200k.

## Evidence quality

Product documentation, not a study. It describes the mechanism but gives no measurements of how the countdown changes behaviour. The only behavioural report on it we have is third-party and anecdotal: [[cognition-2025-rebuilding]] describes "context anxiety" in Sonnet 4.5. That the countdown was dropped on later models is a fact on the page; why it was dropped is not stated (inferred link to context anxiety is ours, not Anthropic's).

## Relevance to us

A production instance of the in-band remaining-budget signal studied in [[wen-2025-budgetthinker]] and [[liu-2025-budget]], and the mechanism behind the behaviour reported in [[cognition-2025-rebuilding]]. Any experiment on budget visibility with Claude must record which model was used, because the default visibility differs by model. See also [[anthropic-2026-patterns]].
