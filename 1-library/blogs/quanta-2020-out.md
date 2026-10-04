---
id: quanta-2020-out
type: blog
title: "Out-of-Sync 'Loners' May Secretly Protect Orderly Swarms"
authors: [Jordana Cepelewicz]
year: 2020
url: https://www.quantamagazine.org/out-of-sync-loners-may-secretly-protect-orderly-swarms-20200521/
site: quantamagazine.org
topics: [collective-decision, sync-consensus, fork-merge-security]
added_by: shadow/sol-w3
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Quanta article (21 May 2020) on Corina Tarnita's Princeton group and slime-mould "loners". When Dictyostelium discoideum starves, up to a million amoebas aggregate into a fruiting body in which about 20 percent die to form the stalk. A 2015 PNAS paper showed the cells left behind are viable and their offspring aggregate normally while leaving loners again. A March 2020 PLOS Biology paper (with Fernando Rossine and Thomas Gregor) counted them precisely: loners were up to 30 percent of the population, and instead of a constant fraction they found a roughly constant number per strain (some strains about 10,000, others 50,000 to 100,000), so the trait is heritable. A simple model explains it: cells switch to aggregating at different rates, the starvation signal degrades as callers leave, and late cells no longer hear the signal. The authors propose collective-level bet hedging: loners insure against predators, cheater invasion of the aggregate, or sudden return of food, possibly preserving the social behaviour itself. Couzin notes locusts also leave loners when they swarm.

## Key claims

- Non-participants in collective behaviour can be a regulated, heritable quantity rather than noise (measured: constant number per strain).
- Loner count depends on environment via signal diffusion and decay (experiments plus simulation).
- Loners are a collective bet-hedging strategy (hypothesis; fitness benefit not yet shown, as the authors say).
- Game-theory work shows optional opt-out can stabilise cooperation and resist parasites (cited, not detailed).

## Evidence quality

Journalism on two peer-reviewed papers (PNAS 2015, PLOS Biology 2020), neither catalogued here. Measured counts are clearly separated from the bet-hedging interpretation, which the researchers themselves flag as unproven.

## Relevance to us

For fork-and-merge agents, this is a biological precedent for deliberately keeping some units out of a merge or consensus step as insurance against a corrupted or cheater-infested collective, with the held-out fraction tuned by environment. It also suggests that in swarm detection, a stable count of non-participating accounts could be a designed parameter of an operator's swarm rather than noise. Related: [[strassmann-2000-altruism]] (Dictyostelium cheating), [[buss-1982-somatic]] (fusion parasitism).
