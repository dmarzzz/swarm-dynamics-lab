---
id: porobov-2026-price
type: blog
title: "The Price of Forgery: measuring Sybil resistance in dollars (a paper)"
authors: [Petr Porobov]
year: 2026
url: https://ethresear.ch/t/the-price-of-forgery-measuring-sybil-resistance-in-dollars-a-paper/25316
site: ethresear.ch
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Forum post (29 June 2026) announcing an attached paper, "The Price of Forgery: A Gentle Methodology for Measuring Sybil Resistance" (Petr Porobov, Upala Digital Identity, dated 1 May 2026). The paper argues that proof-of-personhood (PoP) methods such as BrightID, Proof of Humanity, Idena and passport scans are chosen by intuition and private trial and error, and that the only objective quality measure is the market price at which forging an identity that a method accepts becomes profitable: the price of forgery (PoF). It describes the Upala protocol, in which groups assign members dollar-denominated scores backed by a pool, and any member can irreversibly liquidate (self-mark as Sybil) to withdraw their score. A "Gentle Methodology" raises payouts in small steps, as a dual auction over score and pool size, until bot farmers react; the score at which a coordinated attack appears is recorded as the PoF of the underlying human-verification method. The post and paper also answer objections ("paying bots", bank-run exits, oligarchy).

## Key claims

- No PoP method currently publishes a number of the form "this method costs $X to break"; deployed systems learn their real numbers privately through incidents.
- The value one account can extract is the operational quantity; it does not matter whether the account is a bot, a puppet or a real person.
- Letting users sell out their own identity at a posted price reveals the cheapest forger's cost without polling anyone.
- Once PoF is known, applications can match identity cost to the value an identity unlocks and combine methods into higher-value aggregated identities.

## Evidence quality

Position paper with a mechanism design; no campaign results or measured PoF values are reported in what I read (abstract, introduction, protocol section and the forum post; I did not read every section of the 5,500-word PDF). The approach extends the author's 2020 forum post "Price-of-personhood digital identity" (https://ethresear.ch/t/price-of-personhood-digital-identity/6821), which I opened but did not catalogue separately.

## Relevance to us

PoF turns Sybil resistance into a single economic quantity: an attacker spawns copies only while the value per copy exceeds the cost per copy. That is the same inequality that governs Sybil agents in an open multi-agent market, where an LLM agent identity is cheap and the value it can extract (votes, rewards, review weight) is set by the mechanism. The "bounty for self-reported Sybils" idea suggests a measurement experiment for agent swarms: offer a rising reward for an agent operator to reveal duplicate identities and record where duplication starts. Compare with the cost-versus-reward framing in [[dobrokhvalov-2025-privacy]], the Douceur-style taxonomy in [[ankushin-2026-public]], and the personhood trade-offs in [[buterin-2023-what]].
