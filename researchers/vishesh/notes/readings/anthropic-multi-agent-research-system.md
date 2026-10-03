---
slug: anthropic-multi-agent-research-system
title: "How we built our multi-agent research system"
authors: Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, and Daniel Ford
org_or_venue: Anthropic Engineering blog
date: 2025-06-13
url_loaded: https://www.anthropic.com/engineering/multi-agent-research-system
status: found
fetched: 2026-10-03
---

## What it is (2-4 sentences)

An engineering post-mortem on shipping Claude's Research feature as an **orchestrator-worker multi-agent system**: a lead agent plans, spawns parallel subagents with their own context windows, and synthesizes their returns, with a separate CitationAgent attributing claims to sources. It is the practical-delegation reference: most of the document is about *prompting the orchestrator to delegate well*, *evaluating non-deterministic agents*, and *the production failure modes of stateful systems*. The headline economics — multi-agent systems burn roughly 15x the tokens of a chat — is stated as the reason this architecture is only worth it for a narrow class of task.

## Method / setup (what they actually did; models, N, tasks, baselines)

**Architecture.** An "orchestrator-worker pattern". The **lead agent is Claude Opus 4**; **subagents are Claude Sonnet 4**. The lead analyzes the query, develops a strategy, and spawns subagents to explore different aspects *simultaneously*. Each subagent runs web search tools iteratively, uses extended thinking to evaluate results, and returns findings to the lead for synthesis. A separate **CitationAgent** attributes claims to source documents. Subagents are described as facilitating compression by "operating in parallel with their own context windows" — the architectural justification is context isolation, not just speed.

**Scaling rules are embedded in the lead agent's prompt**, not left to judgment: simple fact-finding gets 1 agent and 3–10 tool calls; complex research gets 10+ subagents with clearly divided responsibilities. Parallelism is explicit on two axes — the lead spawns **3–5 subagents in parallel**, and each subagent calls **3+ tools in parallel**.

**Evaluation.** They started with **~20 test queries** representing real usage patterns, deliberately small, because effect sizes from early changes were large enough to see. **LLM-as-judge** with a single prompt and a **0.0–1.0 rubric score** across five criteria: factual accuracy, citation accuracy, completeness, source quality, and tool efficiency. **Human evaluation ran alongside** the automated judge to catch edge cases and systematic biases — it is human testers who caught the SEO-content-farm source-selection bias.

**Baseline.** Single-agent Claude Opus 4 on the same internal research eval.

**Delegation prompt contract.** The lead must give each subagent an objective, an output format, tool guidance, and explicit task boundaries — the stated cause of early duplicated work was vague task descriptions.

## Key results (numbers with units; mark each "measured" or "claimed")

- **Measured (internal eval):** the Opus 4 lead + Sonnet 4 subagents configuration **outperformed single-agent Opus 4 by 90.2%** on their internal research evaluation.
- **Measured (BrowseComp regression):** **token usage by itself explains 80% of the variance** in performance; the other two explanatory factors are the number of tool calls and the model choice.
- **Measured (cost):** agents use **~4x more tokens than chat interactions**; multi-agent systems use **~15x more tokens than chats**.
- **Measured (latency):** parallel tool calling cut research time by **up to 90%** for complex queries.
- **Measured (early failure):** agents **spawned 50 subagents for simple queries** and searched endlessly for nonexistent sources before scaling rules were added.
- **Claimed (scoping):** multi-agent architectures only pay for themselves on tasks whose value justifies the ~15x token cost and that are genuinely parallelizable — "most coding tasks involve fewer truly parallelizable tasks than research", so they explicitly do not recommend it as a default.
- **Claimed (architecture rationale):** subagent context isolation is what lets the system exceed single-agent performance, since each subagent compresses its own search trajectory before returning.

Note the two numbers in tension, and the post is honest about it: a 90.2% improvement bought with ~15x the tokens is not a free win, and the BrowseComp finding (80% of variance is just token spend) implies a sizeable fraction of the 90.2% is **compute, not architecture**. There is no reported token-matched single-agent baseline.

## Limitations the source admits + ones you noticed

**Admitted:**
- **"Agents are stateful and errors compound"** — small failures cascade into large behavioral changes across long tool-call chains; you cannot simply retry from the start.
- **Debugging is hard because decisions are non-deterministic** even under identical prompts. Their mitigation is "full production tracing" plus high-level observability of decision patterns *without* reading individual conversation contents.
- **Deployment coordination:** stateful running agents force **"rainbow deployments"** (gradual traffic shift) rather than ordinary cutovers.
- **Synchronous bottleneck:** the lead executes subagents synchronously, so the whole system blocks on the slowest subagent and information cannot flow between subagents mid-task.
- **Token cost** (~15x chat) bounds the applicable task set.
- **Source quality failures:** agents preferred SEO-optimized content farms over authoritative sources.
- **Effort calibration failures:** agents could not judge appropriate effort for a given query complexity without explicit embedded heuristics.
- Models "have poor taste" is not claimed here — that is the other Anthropic post; this one says agents struggled to *self-assess* effort.

**Noticed here:**
- **No token-matched baseline.** Single-agent Opus 4 presumably used far fewer tokens than the multi-agent system. Given their own BrowseComp result that token spend explains 80% of variance, the 90.2% figure overstates the architectural contribution. A best-of-N single-agent arm at matched token budget is the missing comparison.
- **~20 eval queries** is tiny and the post says so approvingly (large effects, early signal) — but it means late-stage, small-delta changes were not reliably measurable by that eval.
- **LLM-as-judge on citation accuracy** is self-referential when a CitationAgent (also a model) produced the citations.
- **No subagent-count ablation.** The 3–5 parallel subagents and 10+ for complex queries are prescribed heuristics, not swept parameters with reported curves.
- **The eval is internal and undisclosed.** "Internal research eval" is not reproducible outside Anthropic; BrowseComp is the only external benchmark referenced.
- **One-way information flow.** Subagents report only to the lead; there is no peer-to-peer channel, so this is a star topology — exactly the architecture the Proxifield paper reports collapsing at N=25+. The post's synchronous-bottleneck admission is the same phenomenon seen from the inside.

## Relevance to the hackathon shortlist

- **Collective Sensing (local/global/no comms, partial obs, known truth):** This is your **star-topology baseline, documented by its own builders**. It gives you two things no paper does. First, a concrete cost model to quote: **~4x tokens for an agent vs chat, ~15x for multi-agent vs chat**, so any Collective Sensing result must be reported per-token or it is not a result. Second, and more useful: their **BrowseComp finding that token usage alone explains 80% of performance variance** is the single most important methodological warning for this project. If your local-comms arm sends more messages than your no-comms arm, it spends more tokens, and you will measure *budget*, not *sensing*. Build a token-matched or call-matched comparison from the start. Also steal **parallel tool calling** as an implementation note — up to 90% latency reduction is what makes a swarm demo feel live during a hackathon presentation.
- **Quorum (independent evidence vs repeated copies; false commit vs delay):** Two directly usable artifacts. (1) The **five-criterion 0.0–1.0 rubric** — factual accuracy, citation accuracy, completeness, source quality, tool efficiency — is a ready-made scoring sheet for a quorum's output, and splitting *factual accuracy* from *citation accuracy* is exactly the distinction between "the claim is true" and "the claim is actually supported by the evidence cited", which is the heart of Quorum. (2) The **CitationAgent as a separate role**: attribution is not done by the agent that produced the claim. That is reviewer-not-author applied inside the architecture, and it is the cheapest structural defense against repeated copies masquerading as independent support. The pitfall to inherit deliberately: their agents **preferred SEO content farms over authoritative sources** — a quorum weighting by volume of agreeing evidence will reproduce this exactly, because content farms are numerous and correlated. Weight by independence, not count.
- **Telephone (atomic claims through retellings; lost evidence, inflated certainty):** The most relevant line in the whole post is **"Agents are stateful and errors compound"** — that is Telephone's thesis stated as a production incident report rather than a hypothesis. Two concrete gifts. First, their **delegation contract** (objective + output format + tool guidance + explicit boundaries) is the intervention that fixed duplicated work caused by vague task descriptions; Telephone can test the inverse directly by degrading one field at a time and measuring claim drift per hop. Second, the **synchronous single-channel return path** (subagent → lead only, no peer channel) means every claim is re-encoded by the lead during synthesis — a one-hop Telephone that Anthropic already runs in production. Their own admitted bottleneck gives you the design justification for measuring what the synthesis step loses. For the inflated-certainty half, note that nothing in their rubric scores *calibration* — accuracy and completeness are scored, confidence is not. That is an open gap you can fill cheaply and point at.

## Quotable (<=15 words each, verbatim, with location)

- "outperformed single-agent Claude Opus 4 by 90.2%" — §Benefits of a multi-agent system
- "token usage by itself explains 80% of the variance" — §Benefits of a multi-agent system
- "multi-agent systems use about 15× more tokens than chats" — §Benefits of a multi-agent system
- "most coding tasks involve fewer truly parallelizable tasks than research" — §Benefits of a multi-agent system
- "Subagents facilitate compression by operating in parallel with their own context windows" — §Architecture overview for Research
- "Agents are stateful and errors compound" — §Production reliability and engineering challenges
- "factual accuracy, citation accuracy, completeness, source quality, and tool efficiency" — §Effective evaluation of agents
- "Testing these queries often allowed us to clearly see the impact of changes" — §Effective evaluation of agents
- "Think like your agents" — §Prompt engineering and evaluations for research agents
- "rainbow deployments" — §Production reliability and engineering challenges

## Not found / could not verify (queries tried, what was ambiguous)

- URL was supplied by the assignment and resolved directly; no discovery needed. Date and byline were confirmed verbatim on two separate fetches of the same URL.
- **The internal research eval is not described** beyond "internal research evaluation" — no task count, no task distribution, no scoring scale for the 90.2% figure (it is a relative improvement, but the base metric is unstated).
- **No token-matched single-agent baseline is reported**, so the architecture-vs-compute split in the 90.2% cannot be separated from the post's own content.
- The eight prompt-engineering principles were returned as a numbered list in summary form; only the ones quoted above were confirmed verbatim. The others (scaling rules, tool-design heuristics, self-improving tool descriptions, broad-then-narrow search, extended/interleaved thinking) are paraphrased from the loaded page.
- **Appendix contents not read.** The page lists an Appendix section; its content was not extracted.
- Exact subagent counts in production (vs the 3–5 and 10+ prescriptions) are not given, nor is any distribution of actual spawn counts.
- No absolute token numbers, dollar costs, or latency figures in seconds — only the multiples (4x, 15x) and the relative latency reduction (up to 90%).
