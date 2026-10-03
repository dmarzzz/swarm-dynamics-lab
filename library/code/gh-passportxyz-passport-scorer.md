---
id: gh-passportxyz-passport-scorer
type: code
title: "Passport Scorer: API that turns Passport stamps into a weighted humanity score, plus model-based scoring"
repo: passportxyz/passport-scorer
url: https://github.com/passportxyz/passport-scorer
authors: ["Passport XYZ (formerly Gitcoin)"]
year: 2022
language: "Python (Django) and Rust"
license: "AGPL-3.0 (LICENSE file; README says MIT; API reports NOASSERTION)"
stars: 181
last_commit: 2026-10-02
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Server side of [[gh-passportxyz-passport]]: a Django API (with a newer `rust-scorer`) that reads a holder's stamps and returns a score. In `api/scorer_weighted/computation.py`, the weighted scorer sums a per-provider weight for each distinct stamp provider (duplicates count zero), lets a community override weights through a customisation table, and sets the score's expiry to the earliest stamp expiry. Other folders include `trusta_labs`, `stake`, `cgrants` (Gitcoin grants contribution data), an `indexer` and a `verifier`. The README calls it a centralised service run by Passport XYZ.

## What it can do for us

Concrete, inspectable code for the simplest Sybil-resistance score: an additive weighted sum over independent credentials with expiry. That is a direct template for an agent-admission score in a swarm, and its weakness (weights are hand-set and an attacker optimises against the published weights) is a hypothesis we could test.

## Run notes

Not run. Setup is in `SETUP.md` (Postgres, Redis, Pipenv). Code read via the GitHub API on 2026-10-03.

## Limitations

Licence inconsistency: README says MIT, LICENSE file is AGPL-3.0 with a Passport XYZ copyright header. Weights and thresholds are policy, not learned in the weighted scorer. Model-based scoring components reference external data we did not inspect.
