---
id: gh-ept-byzantine-eventual
type: code
title: "byzantine-eventual: paper sources and JavaScript prototype for Byzantine Eventual Consistency"
repo: ept/byzantine-eventual
url: https://github.com/ept/byzantine-eventual
authors: ["Martin Kleppmann", "Heidi Howard"]
year: 2020
language: JavaScript (prototype, Node.js) and TeX (paper sources)
license: "MIT declared in evaluation/package.json; no repository-level licence file detected by the GitHub API"
stars: 23
last_commit: 2022-03-30
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [kleppmann-2020-byzantine, kleppmann-2022-making]
---

## Summary

The repository holds the LaTeX sources for [[kleppmann-2020-byzantine]] and for the PaPoC paper [[kleppmann-2022-making]] (bft-crdt.tex), plus the evaluation prototype in evaluation/. The prototype (replica.js, reconcile.js) implements hash-DAG Byzantine causal broadcast with both reconciliation algorithms (V1: plain heads and needs round trips; V2: stored previous heads plus Bloom filter). evaluation.js runs four replicas in one process with a simulated network and prints per-interval statistics. Maintained by Martin Kleppmann; created January 2020, last commit March 2022.

## What it can do for us

A small, readable reference implementation of merging histories from untrusted peers by content hash, which is the mechanism we would use if sub-agent reports are kept as a signed append-only DAG. It can be extended to inject equivocating or withholding replicas, which the original evaluation does not do.

## Run notes

On macOS (Apple silicon), Node v24.6.0, in a scratch clone:

    git clone --depth 1 https://github.com/ept/byzantine-eventual.git
    cd byzantine-eventual/evaluation
    npm install
    npx mocha        # 7 passing (15ms)
    node evaluation.js > eval_out.txt
    diff eval_out.txt evaluation.data   # identical

The run is deterministic: the output matched the committed evaluation.data exactly. In the output, the V2 average round trips per reconciliation is between 1.01 and 1.07 across update intervals, and between 561 and 592 of 600 reconciliations finish in one round trip, matching the paper's figures. yarn was not installed, so npm was used instead of the README's yarn commands. Plot generation (gnuplot) not run.

## Limitations

Research prototype, not a library. All replicas in the evaluation are correct; there is no Byzantine fault injection, no networking, no persistence. Licence is only declared inside package.json.
