---
id: strobel-2020-blockchain
type: paper
title: "Blockchain Technology Secures Robot Swarms: A Comparison of Consensus Protocols and Their Resilience to Byzantine Robots"
authors: ["Volker Strobel", "Eduardo Castelló Ferrer", "Marco Dorigo"]
year: 2020
venue: "Frontiers in Robotics and AI"
url: https://www.frontiersin.org/articles/10.3389/frobt.2020.00054/pdf
doi: "10.3389/frobt.2020.00054"
arxiv: null
cite: "Strobel, V., Castelló Ferrer, E., & Dorigo, M. (2020). Blockchain Technology Secures Robot Swarms: A Comparison of Consensus Protocols and Their Resilience to Byzantine Robots. Frontiers in Robotics and AI, 7, 54."
topics: [sybil-resistance, swarm-robotics, collective-decision, sync-consensus]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "128 (OpenAlex, 2026-10-03)"
code: [gh-pold87-ab-interface-blockchain-module]
---

## Summary

Twenty simulated e-puck-like robots in ARGoS estimate the fraction of white tiles on a 2 x 2 m floor. Three aggregation rules are compared: the linear consensus protocol (LCP), W-MSR with F = 2 [[leblanc-2013-resilient]], and a smart contract on a private Ethereum proof-of-work chain run by the robots (one geth Docker container per robot, links only within 50 cm). Robots submit sensor readings with a 40 ether deposit; every 20 submissions the contract keeps readings within epsilon = 0.2 of the running mean, refunds inliers with the pooled deposits and confiscates outlier deposits. Ether is earned only by mining (5 ether per block) or by being an inlier.

## Contribution

The first direct experimental comparison of classical robot-swarm consensus with blockchain-mediated consensus under Byzantine and Sybil attack, and the clearest statement in robotics of Sybil resistance by scarcity: "it is not the number of entities forged but rather an attacker's wealth that determines the success of the attack."

## Key results

- No Byzantines: all three methods reach mean absolute error below 0.08.
- Byzantine robots sending 0.0 (0 to 7 of 20): LCP harm exceeds 10% median with a single Byzantine; W-MSR copes with a few but error rises above three; the blockchain contract stays roughly flat (mean absolute error near 20% with 7 Byzantines in the consensus experiment).
- Sybil attack (one identity per time step): LCP and W-MSR fail with a single attacker; the contract is unaffected because each submission costs 40 ether and new identities hold no ether.
- Overheads measured: 148-byte transactions, 6.8 MB chain after 1000 s, 33 MB after 24 h with 20 robots.

## Methods and models

ARGoS plus Ethereum via shell scripts and IPC (ARGoS-Blockchain interface), 40 repetitions per condition, average degree 2.4 so the swarm is usually partitioned. Statistics: absolute error of a randomly picked robot, harm relative to the no-Byzantine baseline, consensus time.

## Limitations and open questions

Simulation only (physical Pi-puck port deferred to later work, see [[strobel-2023-robot]]). The outlier rule biases estimates even with no attackers. Proof of work makes the system vulnerable to a 51% hash-power attacker, which a mobile cluster of malicious robots might achieve locally. Deposit size was tuned in a pilot. A wealthy attacker is not stopped, only priced.

## Relevance to us

Primary robotics source for economic Sybil resistance: deposits plus redistribution make spam and fake identities self-defeating. The same structure (stake to speak, slash outliers, reward inliers) maps directly to LLM agent swarms and to Flashbots-style settings where order-flow or bids must cost something to submit. Its weakness (honest minority outliers lose stake; wealth buys influence) is the open design question. Compare the physical-identity route [[gil-2015-guaranteeing]] and the accusation route [[wardega-2023-byzantine]]; predecessor [[strobel-2018-managing]], successor [[strobel-2023-robot]].
