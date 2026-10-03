---
id: fax-2004-information
type: paper
title: Information Flow and Cooperative Control of Vehicle Formations
authors: [J. Alexander Fax, Richard M. Murray]
year: 2004
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2004.834433
doi: 10.1109/tac.2004.834433
arxiv: null
cite: "Fax, J. A., & Murray, R. M. (2004). Information flow and cooperative control of vehicle formations. IEEE Transactions on Automatic Control, 49(9), 1465-1476."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "4616 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies vehicles cooperating on a shared task through inter-vehicle communication. Modelling the communication
network with algebraic graph theory, the authors prove a Nyquist criterion that uses the eigenvalues of the
graph Laplacian to decide formation stability, and propose a decentralised information-exchange scheme (a
consensus-like dynamical system) that gives each vehicle a common reference. A separation principle splits
formation stability into stability of the information flow for the given graph and stability of each vehicle
under its local controller.

## Contribution

Introduced the Laplacian-eigenvalue decomposition for formation stability with general vehicle dynamics,
the template later generalised in [[li-2010-consensus]]; a founding paper of graph-based cooperative control.

## Key results

- Abstract-level: Nyquist criterion over Laplacian eigenvalues; separation principle; information flow can be
  made highly robust to graph changes, enabling tight formation control despite limited communication.

## Methods and models

Linear vehicle dynamics, graph Laplacian, frequency-domain stability. Abstract from OpenAlex.

## Limitations and open questions

Linear time-invariant models; fixed graphs in the main result.

## Relevance to us

The method to reuse when swarm agents have non-trivial dynamics (drones, not points): check stability per
Laplacian eigenvalue.
