---
id: gh-in-toto-in-toto
type: code
title: "in-toto: reference implementation of the in-toto supply chain integrity framework"
repo: in-toto/in-toto
url: https://github.com/in-toto/in-toto
authors: ["in-toto project contributors"]
year: 2016
language: Python
license: "Apache-2.0 (LICENSE file: Copyright 2018 New York University, Apache License 2.0)"
stars: 1049
last_commit: 2026-08-27
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [torres-arias-2019-in-toto]
---

## Summary

Python reference implementation of [[torres-arias-2019-in-toto]]. A project owner signs a layout listing supply chain steps, the functionaries authorised for each, and artifact rules (CREATE, DELETE, MODIFY, ALLOW, DISALLOW, REQUIRE, MATCH ... FROM step) that chain the products of one step to the materials of the next. Functionaries run steps through the in-toto tools, which record the command and the hashes of materials and products in signed link metadata. Verification checks the layout signature, the links against per-step thresholds and keys, the artifact rules, and runs inspections. Installable with pip install in-toto; repository created May 2016, actively maintained (last commit 2026-08-27), 1,049 stars at access.

## What it can do for us

A ready policy language and verifier for "which part may produce which artifact, and how many independent parts must agree". It could be used almost unchanged to make sub-agent reports into signed link files over the hashes of inputs read and outputs produced, with a threshold per merge step.

## Run notes

Not run. I read the README, the repository file listing and the LICENSE header.

## Limitations

Assumes deterministic artifacts so that hashes from different functionaries match; LLM outputs would need canonicalisation or a semantic comparison inspection. The GitHub API reports the licence as Other, but the LICENSE file is Apache 2.0.
