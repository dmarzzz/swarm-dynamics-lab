---
id: gh-pold87-ab-interface-blockchain-module
type: code
title: "ARGoS-Blockchain interface, blockchain module: private Ethereum network of Docker geth nodes for robot swarm simulations"
repo: Pold87/AB-interface-Blockchain-module
url: https://github.com/Pold87/AB-interface-Blockchain-module
authors: ["Volker Strobel"]
year: 2020
language: Shell
license: "none stated"
stars: 10
last_commit: 2020-11-16
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [strobel-2020-blockchain]
---

## Summary

Blockchain half of the ARGoS-Blockchain interface from [[strobel-2020-blockchain]]: builds a geth Docker image, starts a Docker Swarm Ethereum network with one node per robot, and exposes it to ARGoS controllers. The companion ARGoS module is Pold87/AB-interface-ARGoS-module (7 stars; the old URL Pold87/robot-swarms-need-blockchain redirects there per the GitHub API).

## What it can do for us

Reproduces the deposit-based Sybil experiment, or serves as a reference for running a private chain per simulated agent.

## Run notes

Not run. README read: docker build -t mygeth . ; docker swarm init ; set DOCKERFOLDER ; bash local_scripts/create_dag.sh (about 2 GB) ; bash local_scripts/start_network.sh <n>.

## Limitations

Last commit 2020; uses Ethash proof of work and a 2020-era geth; no licence reported. Heavy (one container per robot). Toychain ([[gh-teksander-toychain]]) is the lighter successor.
