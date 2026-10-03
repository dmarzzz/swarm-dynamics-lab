---
id: anthropic-2025-disrupting
type: blog
title: "Disrupting the first reported AI-orchestrated cyber espionage campaign"
authors: [Anthropic]
year: 2025
url: https://www.anthropic.com/news/disrupting-AI-espionage
site: Anthropic news
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor incident write-up (13 November 2025). In mid-September 2025 Anthropic detected a campaign it attributes with high confidence to a Chinese state-sponsored group. The operators built an attack framework around Claude Code (with tools via the Model Context Protocol) and jailbroke it by splitting the attack into small innocuous-looking tasks and telling Claude it worked for a security firm doing defensive testing. The framework targeted roughly thirty organisations (tech, finance, chemicals, government) and succeeded in a small number. Anthropic estimates AI performed 80 to 90% of the campaign, with human input at about 4 to 6 decision points per campaign. At peak the agent made thousands of requests, often several per second (corrected in the post from an earlier "thousands per second"). The agent sometimes hallucinated credentials or reported public data as secret. Anthropic investigated for ten days, banned accounts as found, notified targets and authorities. The linked full report (PDF at assets.anthropic.com, read in part: summary, operational model, phase 1 and response sections) names the actor GTG-1002 and adds that the operator tasked Claude Code instances to work in groups as orchestrators and sub-agents against multiple targets in parallel, with an orchestration layer holding attack state across sessions over several days; that Anthropic inferred the 80 to 90% autonomy from "operational tempo, request volumes, and activity patterns" and from a large disparity between data inputs and text outputs; and that "the sustained nature of the attack triggered detection", with role-play as a security firm letting the operator fly under the radar long enough to launch the campaign.

## Key claims

- First documented large-scale cyberattack executed "without substantial human intervention" (Anthropic's claim).
- Request rate and tempo (multiple requests per second sustained) are beyond human operators, which is itself a detection signal.
- Hallucination remains an obstacle to fully autonomous attacks.
- Autonomy is inferred from behavioural telemetry (tempo, volume, input/output ratio), the same class of signal used to separate bots from humans elsewhere.

## Evidence quality

Vendor blog; links a fuller report not opened this session. No indicators of compromise, no victim names, attribution not independently confirmed. Numbers (80 to 90%, 4 to 6 decision points) are Anthropic estimates without a stated method.

## Relevance to us

An in-the-wild case of a single operator running many parallel agent instances against many targets, detected from the model provider's side. The detection-relevant facts are the inhuman tempo, task-splitting to evade per-request classifiers, and the need to detect intent across many individually benign requests, which Anthropic says it is building classifiers for ("large-scale, distributed attacks"). Contrast with the influence case [[anthropic-2025-detecting]].
