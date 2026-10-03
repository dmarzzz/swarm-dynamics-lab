---
id: gh-worldcoin-open-iris
type: code
title: "open-iris (IRIS): Worldcoin iris recognition pipeline used to check uniqueness for World ID"
repo: worldcoin/open-iris
url: https://github.com/worldcoin/open-iris
authors: ["Worldcoin AI"]
year: 2023
language: "Python"
license: "MIT"
stars: 421
last_commit: 2026-08-24
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Open-source iris recognition inference system from the Worldcoin Foundation. The pipeline segments the iris from an image, extracts features into an iris code template, and matches templates for uniqueness checks; the README claims it is built to verify uniqueness among billions of users. It installs from PyPI as `open-iris` with an `IRIS_ENV` flag selecting SERVER, ORB (the Worldcoin capture device) or DEV dependencies. Citation given as Worldcoin AI, 2023.

## What it can do for us

Shows the biometric end of Sybil resistance: personhood rooted in a physical body, which by construction no software agent can satisfy. For agent swarms this matters as the model for "human-backed" agents, where an agent's identity is delegated from a biometric credential via [[gh-worldcoin-world-id-contracts]].

## Run notes

Not run. `pip install open-iris`, then `python3 -c "import iris; print(iris.__version__)"` per README.

## Limitations

The matching thresholds and false-match rates at billion scale are claims in the README, not checked here. Uniqueness is only as strong as the Orb hardware and operator trust, which this repo does not cover.
