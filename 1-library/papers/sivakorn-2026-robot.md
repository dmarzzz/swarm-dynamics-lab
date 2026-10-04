---
id: sivakorn-2026-robot
type: paper
title: "Robot Visions: Breaking reCAPTCHA at Zero Cost and Zero Shot"
authors: ["Suphannee Sivakorn", "Samantha Gottlieb"]
year: 2026
venue: "Information Security Conference (ISC 2026), accepted; arXiv preprint"
url: https://arxiv.org/abs/2609.18518
doi: "10.48550/arXiv.2609.18518"
arxiv: "2609.18518"
cite: "Sivakorn, S., & Gottlieb, S. (2026). Robot Visions: Breaking reCAPTCHA at Zero Cost and Zero Shot. Accepted for publication in the Proceedings of the 29th Information Security Conference (ISC 2026). arXiv preprint arXiv:2609.18518."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Sivakorn and Gottlieb build zero-shot, zero-cost reCAPTCHA solvers on free local models with no training: CLIP for independent-tile challenges (58% per-challenge accuracy) and OWLv2 for single-image 4x4 grids (43.5%). End to end, their solver passes 92.6% of 500 real reCAPTCHA sessions. They also show a non-technical user can defeat reCAPTCHA by instructing a commodity AI assistant in natural language.

## Contribution

Removes the remaining cost and skill barriers to breaking reCAPTCHA's visual fallback; concludes challenge-based visual CAPTCHAs may have reached the end of their useful life.

## Key results

- Measured (abstract): 92.6% per-session success over 500 real reCAPTCHA sessions.
- Measured (abstract): CLIP 58% per challenge on Type A; OWLv2 43.5% on Type B.
- Demonstrated (abstract): a commodity AI assistant solves reCAPTCHA from natural-language instructions.

## Methods and models

Taxonomy of reCAPTCHA challenge types; zero-shot open-source vision models; automated end-to-end solver. Abstract only.

## Limitations and open questions

Abstract only. reCAPTCHA increasingly relies on reputation, which this does not address.

## Relevance to us

With [[plesner-2024-breaking]], establishes that visual challenges add no Sybil cost for agent swarms; the remaining signal is reputation and environment ([[ousat-2026-broken]]).
