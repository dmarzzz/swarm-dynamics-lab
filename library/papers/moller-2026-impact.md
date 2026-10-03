---
id: moller-2026-impact
type: paper
title: "The impact of generative AI on social media: an experimental study"
authors: [Anders Giovanni Møller, Daniel M. Romero, David Jurgens, Luca Maria Aiello]
year: 2026
venue: Scientific Reports
url: https://www.nature.com/articles/s41598-026-40110-8
doi: 10.1038/s41598-026-40110-8
arxiv: null
cite: "Møller, A. G., Romero, D. M., Jurgens, D., & Aiello, L. M. (2026). The impact of generative AI on social media: an experimental study. Scientific Reports. https://doi.org/10.1038/s41598-026-40110-8"
topics: [swarm-detection, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Controlled experiment on a custom chat-room platform resembling a social media forum. A representative sample of 680 US participants was split into groups of five and randomly assigned to one control and four AI-assistance conditions: open-ended Chat with an assistant, AI reply Suggestions with agreeing, neutral and disagreeing stances, AI Feedback on drafts, and AI Conversation Starters. The four tools span two design axes: initiative (reactive Chat and Feedback versus proactive Suggestions and Starters) and task orientation (generating new content versus refining user text). Each group discussed three topics in random order (cats versus dogs, health benefits of oats, universal basic income), ten minutes each, with questionnaires before and after and full interaction logs. Producer-side results: Chat and Suggestions raised self-reported willingness to participate; every AI tool significantly lengthened comments; Conversation Starter improved participation equality (normalised Shannon entropy) and was the only tool that raised the chance of receiving a reply (beta 0.300, p = 0.021). Consumer-side results: no AI condition improved perceived quality; Chat and Conversation Starter made comments seem less informative and lower quality; replies to one's own comments were rated lower in all conditions except Suggestions (weakly positive); all AI treatments increased Dislikes; free text called AI-assisted content "robotic" and "generic". Demographic moderators were not significant at 130 to 140 per condition. We read the introduction and main results; the usage-pattern and methods sections were not read.

## Contribution

First platform-integrated randomised experiment separating producer and consumer effects of AI writing assistance in group discussion, showing that no single intervention helps both sides and that AI-assisted threads are perceived as lower quality even as volume and participation rise.

## Key results

- n = 680, five conditions, groups of five, three topics.
- All AI tools increased comment length (p < 0.05 or better); Chat and Suggestions increased stated willingness to participate.
- Conversation Starter: higher participation equality and higher reply likelihood (beta = 0.300, p = 0.021).
- Perceived informativeness and quality fell under Chat and Conversation Starter; reply ratings fell in all but Suggestions; Dislikes rose in every AI condition.

## Methods and models

Between-subjects randomised experiment on a purpose-built forum; pre and post questionnaires on Likert scales; platform logs of comments, reactions and AI use; bootstrapped tests and Cohen's d reported in a table; post-hoc regressions on reply likelihood and demographics (supplementary).

## Limitations and open questions

Short (10-minute) synthetic discussions among strangers; one platform design and one model configuration; participants knew AI tools were present, so perception effects may partly reflect labelling. The paper is about humans using AI assistance, not autonomous agents, so inferences about agent populations are indirect.

## Relevance to us

Indirect for swarm detection but gives a measured human-side signature: when AI-shaped text enters a thread, readers rate it as generic and downvote it even without knowing which messages were assisted, which suggests reaction patterns (Dislike rates, reply ratings) as population-level indicators of machine participation. Also a clean experimental template (groups of five, randomised tools, producer versus consumer metrics) that could be adapted to measure how a few agents change a mostly human discussion. Related: [[lloyd-2025-there]] on moderators' heuristic detection; [[x-himanshiet-2103730840144633924]] on platforms preparing for agent traffic.
