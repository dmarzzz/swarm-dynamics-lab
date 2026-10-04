---
id: dwarkesh-2025-what
type: blog
title: What fully automated firms will look like
authors: [Dwarkesh Patel]
year: 2025
url: https://www.dwarkesh.com/p/ai-firm
site: Dwarkesh Podcast (Substack blog), 2025-01-31
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Speculative essay, developed with Ege Erdil and Tamay Besiroglu, with a stated epistemic status of "Shooting-the-shit; 25% sure". It argues that AI firms will gain collective advantages because AI workers "can be copied, distilled, merged, scaled, and evolved". The "Merge" section describes "mega-Sundar", a central AI that "will constantly be spawning specialized distilled copies and reabsorbing what they've learned on their own", absorbing knowledge "through explicit summaries, shared latent representations, or even surgical modification of the weights". It claims this yields "approximately no miscommunication, ever again" and compares the parent and copies to speculative decoding, where a larger model verifies a smaller one's guesses. A narrated video version ("What will automated firms look like?") is the video Sutton says he watched before raising the corruption objection in [[sutton-2025-father]].

## Key claims

- Copying collapses training cost per worker and lets one mind micromanage a firm; the essay says there is "no principal-agent problem" inside such a firm (footnote 1 concedes one remains between the AI CEO and shareholders).
- A central model can learn from everything its distilled copies see, the way a driving model learns from a fleet.
- Merge channels named: summaries, latent representations, direct weight edits.
- Firms become evolvable because the whole configuration can be replicated; markets remain the outer loss function that keeps internal planning grounded (citing Gwern).

## Evidence quality

Opinion and analogy. No experiments, no threat model. The essay treats merging as a pure efficiency gain and does not consider adversarial content in what copies bring back; the word "corrupt" does not appear. Its speculative-decoding analogy does contain a verification step (the large model checks the small one), but the essay does not develop it as a security control.

## Relevance to us

This is the "view" that Sutton explicitly says he is adding corruption to, so it fixes the baseline architecture for Q1 to Q3: one root (mega-Sundar), many specialised distilled children, and three merge channels of different bandwidth. For Q3, the channel matters: summaries are a narrow, inspectable text channel (prompt-injection class), latent exchange and "surgical modification of the weights" are wide channels where a backdoor can ride in the update itself (model-merging and federated-poisoning class). For Q2, the speculative-decoding analogy suggests verifying a child's contribution against the parent before acceptance, the cheapest form of a merge gate. The essay's claim of no principal-agent problem is exactly what Sutton's objection attacks: once a child is corrupted, it is a principal-agent problem inside the firm.
