---
id: anthropic-2026-task
type: blog
title: "Task budgets"
authors:
- Anthropic
year: 2026
url: https://platform.claude.com/docs/en/build-with-claude/task-budgets
site: platform.claude.com (vendor documentation)
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: full
relevance: 5
---
## Summary

Vendor documentation (undated page; beta header `task-budgets-2026-03-13`) for an API parameter, `output_config.task_budget = {type: "tokens", total, remaining?}`, that tells Claude how many tokens it has for a whole agentic loop: thinking, tool calls, tool results and output across all the requests that make up one turn. The server injects a countdown that only the model sees; the API response does not expose it. The budget is advisory: `max_tokens` remains the hard per-request cap, and Claude may overrun the budget to finish an action. The minimum budget is 20,000 tokens. The page warns that a budget clearly too small for the task can make Claude decline, scope down aggressively, or stop early with partial results, and recommends sizing budgets from the measured p99 of per-task spend.

## Key claims

- Stated: the countdown counts what the model newly sees or generates, not resent history; a worked example spends 19,000 of 100,000 tokens over three requests whose payloads total about 20,820 input tokens.
- Stated: server-side compaction does not reset the budget; client-side compaction should pass `remaining` forward.
- Stated: effort controls depth per step and task budgets control total work ("effort tunes depth, task budgets tune breadth"); adaptive thinking shrinks as the budget depletes.
- Stated: decrementing `remaining` client-side breaks prompt caching and can under-report the budget, making Claude wrap up early.
- Stated: supported in beta on Opus 4.7, 4.8, 5, 5.5, Sonnet 5.5 and Fable/Mythos 5.x; not on Sonnet 5, Opus 4.6, Sonnet 4.6, Haiku 4.5, or in Claude Code.

## Evidence quality

Product documentation. The behavioural statements (graceful wrap-up, refusal-like behaviour under too-small budgets) are vendor descriptions with no published numbers on this page. Nothing here was run.

## Relevance to us

The most direct production handle for budget-aware agents: a model-visible, server-tracked token countdown per agentic loop. It makes the visible-versus-hidden budget question testable on frontier models without training ([[liu-2025-budget]], [[wen-2025-budgetthinker]] do it with custom plumbing). For swarms, each agent's loop has its own budget; how an orchestrator should divide a total among subagents is left to the user. The refusal-under-small-budget warning is the opposite failure to the over-optimism in [[lin-2026-bagen]]. Predecessor mechanism: [[anthropic-2026-context]]. Related: [[anthropic-2026-patterns]], [[kim-2025-towards]].
