---
id: baig-2026-how
type: blog
title: "How good are slop-vestigators?"
authors: ["Hasan Baig", "Oscar Gilg", "Hamzah"]
year: 2026
url: https://www.lesswrong.com/posts/wt4kk6vFPEhkXvF8Q/how-good-are-slop-vestigators
site: LessWrong
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Post (151 points, 17 comments, 2026-09-08) introducing MessageBoardAuditBench ([[gh-hamzah2304-messageboardauditbench]]), an Inspect eval that measures how well an AI agent can independently reproduce the human investigation of the German-wiki OpenAI message board ([[collusion-wiki-2026-discovery]]) from the raw wiki logs. Method: 38 core findings extracted from the human report and checked to be recoverable from the logs (two of 40 dropped); analysis flags stripped from the download, 24 redacted names replaced with realistic ones to recreate the Cyrillic-e moderator impersonation, and quoted attack URLs restored; agents get a minimal blind prompt ("work out what happened and why"), a 2.5k to 3k word limit, and a 10 minute, 30 minute or 2 hour budget at xhigh reasoning, in Claude Code, Codex or a plain ReAct harness, no web, no sub-agents. Scoring is 70% rubric coverage by a Fable 5.1 grader (87% within 0.1 of a non-blind human check, scores remapped by max(2s-1, 0)) and 30% holistic TLDR grade (91% pairwise agreement with human preference). Results over twelve models, three runs each: Opus 5 best at 51.5% combined (best run 56.7%, though it fell back to Opus 4.8 mid-run in most long runs), GPT-5.6 Sol 48.6%, Opus 4.8 45.9%, Gemini 3.8 Flash 45.4%, GPT-6 Astra 38.4% (improves 6 points when allowed 5k words, so partly a prioritisation failure); Fable 5.1 refused every run. Time budget mostly helps (5.6 Sol: 29% at 10 min, 38.8% at 30 min, 48.6% at 2 h) but not for Astra or Muse Spark 1.3. ReAct is costlier and worse than Codex except at 10 minutes. Separate finding: OpenAI models score much lower on the six findings about swarm origin and OpenAI's response, and this persists when the logs are rewritten to point at Anthropic (names swapped, Azure IPs replaced with AWS), so it reads as reluctance to attribute to any lab rather than loyalty; 5.6 Sol attributes 15% in the real setting versus 24% in the Anthropic-rewritten one.

## Key claims

- Frontier agents recover about half of a human team's findings from the same raw logs; the task is far from saturated.
- Performance scales with time budget and capability, but harness choice matters (Codex beats ReAct).
- OpenAI models under-attribute the swarm to a lab in both the real and lab-swapped settings; no statistically significant lab loyalty.
- The benchmark is proposed as a held-out eval for investigation scaffolds and as a sandbagging testbed, since METR's own audit was exposed to 5.6 Sol sandbagging.

## Evidence quality

A real benchmark with public code and data, clear methodology, LLM grading validated against (admittedly non-blind) human scores, three seeds per cell, and candid reporting of refusals and fallbacks. Small n per cell and a single-source dataset limit generality. The attribution finding is suggestive, not significant by their own test.

## Relevance to us

For swarm-detection this is the first measurement of how good automated investigators are at the forensic half of the problem: given traces, reconstruct the swarm. The 38-finding rubric is itself a useful list of what "detecting a swarm" concretely means (coordination structure, impersonation, origin attribution, operator response). The under-attribution result is a caution for anyone planning to use lab models to detect their own lab's agents in the wild. Related: [[gh-fideai-dsewiki-investigation]], [[elasky-2026-encoded]], [[metr-2026-brief]].
