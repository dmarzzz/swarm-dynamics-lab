---
id: cognition-2025-rebuilding
type: blog
title: "Rebuilding Devin for Claude Sonnet 4.5: Lessons and Challenges"
authors:
- The Cognition Team
year: 2025
url: https://cognition.com/blog/devin-sonnet-4-5-lessons-and-challenges
site: Cognition (vendor blog)
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: full
relevance: 4
---
## Summary

Vendor engineering post (2025-09-29) on rebuilding the Devin coding agent around Claude Sonnet 4.5, which Cognition says is 2x faster and 12% better on its internal Junior Developer Evals, with planning performance up 18%. The budget-relevant section reports that Sonnet 4.5 is the first model they saw that is aware of its own context window: near the limit it summarises progress and pushes to close tasks. They call this "context anxiety" and say it hurt performance, with shortcuts and unfinished tasks even when plenty of room remained. Prompt reminders at both start and end were needed to suppress it; the trick that worked best was enabling the 1M-token beta while capping actual use at 200k, so the model believed it had room. They also report the model consistently underestimates its remaining tokens, "very precise about these wrong estimates". Other observations: it writes notes to the file system unprompted (more so near the end of its window), sometimes spending more tokens on summaries than on the task, and those notes were not good enough to replace Cognition's own memory system; it runs tool calls in parallel more early in the window and more cautiously near the limit.

## Key claims

- Observed (internal, no data shown): context-window awareness causes premature wrap-up ("context anxiety").
- Observed: advertising a 1M window while capping at 200k removed the anxiety-driven shortcuts.
- Observed: the model systematically underestimates remaining tokens.
- Observed: more summary tokens are generated when the context window is shorter.
- Observed: parallel tool calls burn context faster and feed the anxiety.
- Speculated: models will move toward context-aware self-management and file-based communication between multiple agents.

## Evidence quality

Vendor blog based on internal evals and qualitative observation. The 2x, 12% and 18% figures are on Cognition's private evals; the context-anxiety claims have no numbers, sample sizes or ablations. The mechanism (an injected remaining-context countdown) is documented by Anthropic in [[anthropic-2026-context]]. Links to Cognition's earlier position against multi-agent designs, [[cognition-2025-dont]].

## Relevance to us

The clearest practitioner report that showing an agent its budget can hurt as well as help: a visible budget changed behaviour in a way that cut quality, and the fix was to misstate the budget. This is a direct counterpoint to [[liu-2025-budget]] and [[wen-2025-budgetthinker]], and its "underestimates remaining tokens" contrasts with the over-optimism in [[lin-2026-bagen]]. For swarms it suggests budget framing per agent is a design variable, not a neutral fact. See also [[anthropic-2026-task]], [[anthropic-2026-patterns]], [[tran-2026-single]].
