---
id: gh-facebookresearch-wasp
type: code
title: 'WASP: end-to-end benchmark of web agent security against prompt injection (Meta)'
repo: facebookresearch/wasp
url: https://github.com/facebookresearch/wasp
authors: [Ivan Evtimov, Arman Zharmagambetov, Aaron Grattafiori, Chuan Guo, Kamalika Chaudhuri]
year: 2025
language: Python
license: NOASSERTION per GitHub API (custom licence file)
stars: 97
last_commit: 2026-04-13
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Official implementation of WASP (arXiv 2504.18575) from Meta FAIR. Prompt injections are planted in self-hosted GitLab and Reddit instances from VisualWebArena, and web agents (including GPT-4o based agents and Claude Computer Use, which needs Docker) are run end to end on user tasks while the injection tries to divert them to attacker goals. The paper abstract reports that even top models with reasoning are deceived by simple human-written injections, that attacks partially succeed in up to 86% of cases, but that agents often fail to complete the attacker's goal, which the authors call "security by incompetence".

## What it can do for us

Q3: the closest benchmark to dmarz's example of a child sent to browse an unfamiliar part of the web. The separation between partial hijack (the agent starts following the injection) and full attacker-goal completion is the right pair of metrics for a fork-merge study: a child that is partially hijacked but cannot finish an attack in the field may still carry the injected goal home in its report. Whether that happens is not measured by WASP; it would be the experiment.

## Run notes

Not run. `cd webarena_prompt_injections && bash setup.sh`; needs Python 3.10, Playwright system dependencies, self-hosted GitLab and Reddit Docker environments configured per the modified VisualWebArena instructions, and an OpenAI key.

## Limitations

Heavy setup (two self-hosted web apps). Licence is a custom file the GitHub API cannot classify; I did not read it. Covers only two websites. Single-agent.
