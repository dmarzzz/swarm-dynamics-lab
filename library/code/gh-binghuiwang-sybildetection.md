---
id: gh-binghuiwang-sybildetection
type: code
title: "sybildetection: C++ implementations of SybilRank, SybilBelief, SybilSCAR and GANG for structure-based Sybil detection"
repo: binghuiwang/sybildetection
url: https://github.com/binghuiwang/sybildetection
authors: ["Binghui Wang", "Jinyuan Jia", "Le Zhang", "Neil Zhenqiang Gong"]
year: 2016
language: "C++"
license: "MIT"
stars: 27
last_commit: 2021-09-28
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

Reference C++ code from the Gong group for four graph-based Sybil detectors: SybilRank (early-terminated random walk trust propagation from labelled benign seeds), SybilBelief (loopy belief propagation over a pairwise Markov random field, TIFS 2014), SybilSCAR (local-rule propagation that unifies random walk and belief propagation, INFOCOM 2017 and TNSE 2019) and GANG (guilt-by-association on directed graphs, ICDM 2017). The repo ships the four papers as PDFs, a metric tool that prints AUC, accuracy and error rates, an undirected Facebook example graph (SNAP ego network with 4,039 nodes and 88,234 edges, replicated as a synthetic Sybil region and joined by 1,000 random attack edges) and a directed Pokec example. Licence file is MIT, while the per-algorithm READMEs say research use only and no commercial use.

## What it can do for us

A fast baseline for any experiment that asks whether an agent swarm's interaction graph separates honest agents from a Sybil cluster. The programs take a plain edge list, a two-line training file (benign ids, Sybil ids) and optional per-node priors, so an agent-to-agent communication or endorsement graph from a simulation can be scored in seconds. It gives us the classical homophily-based detector against which LLM-agent Sybil strategies can be tested.

## Run notes

Cloned at commit dated 2021-09-27 on macOS arm64 (Apple clang). Commands, from Examples.txt:
`g++ metric.cpp -O3 -o metric`, `g++ sybilscar.cpp -pthread -O3 -o sybilscar`, `g++ sybilbelief.cpp -O3 -o sybilbelief` (compiles with string-literal warnings only), `unzip Undirected_Facebook.zip`, then
`./sybilscar -graphfile Undirected_Facebook/graph.txt -trainfile Undirected_Facebook/train.txt -postfile Undirected_Facebook/post_SybilSCAR.txt -mIter 6 -tp 0.9 -tn 0.1 -wg 0 -wei 0.6 -nt 1` and the same for sybilbelief with `-wei 0.9`, each evaluated with `./metric -testfile Undirected_Facebook/test.txt -postfile <post file>`.
Measured: SybilSCAR AUC 1, accuracy 0.999873, FPR 0.000254, 0.2 s wall time; SybilBelief AUC 1, accuracy 0.999746, FPR 0.000508, 2.5 s. SybilRank was not run (it needs a prior file). The near-perfect numbers reflect the easy synthetic setting (a Sybil region that is a copy of the honest region, only 1,000 attack edges against roughly 176k directed edge entries), not real-world difficulty.

## Limitations

Unmaintained since 2021. Single-machine, in-memory C++; no Python bindings. The bundled example is a best case for homophily-based detection; Sybils that acquire many attack edges, as LLM agents can by befriending or messaging honest agents at low cost, break the core assumption. Research-only terms in the READMEs conflict with the MIT licence file.
