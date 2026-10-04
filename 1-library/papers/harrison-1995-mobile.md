---
id: harrison-1995-mobile
type: paper
title: "Mobile Agents: Are they a good idea?"
authors: ["Colin G. Harrison", "David M. Chess", "Aaron Kershenbaum"]
year: 1995
venue: "IBM Research Report, IBM T. J. Watson Research Center (March 28, 1995); later in Mobile Object Systems, LNCS 1222, Springer 1997, with authors ordered Chess, Harrison, Kershenbaum"
url: http://web.archive.org/web/20110408235003/http://www.research.ibm.com/massive/mobag.ps
doi: null
arxiv: null
cite: "Harrison, C. G., Chess, D. M., & Kershenbaum, A. (1995). Mobile Agents: Are they a good idea? IBM Research Report, IBM T. J. Watson Research Center, Yorktown Heights, NY, March 28, 1995. Republished as Chess, D., Harrison, C., & Kershenbaum, A. (1997), in Mobile Object Systems: Towards the Programmable Internet, LNCS 1222, pp. 25-45, Springer."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "44 (Crossref, LNCS 1997 version, 2026-10-03)"
code: []
---

## Summary

The IBM report that the mobile-agent security literature cites as its starting point (read from the archived PostScript, EBCDIC-encoded text decoded locally; I read the abstract, introduction, security section and conclusions). It weighs each claimed benefit of mobile agents (bandwidth, latency, disconnected operation, asynchrony, flexibility) against alternatives such as messaging and RPC, and concludes that no single advantage is overwhelming but that a pervasive agent framework would enable many network services. Security is described as a severe concern: authentication of the sending user and of the execution environment (the latter flagged as unclear how to do, because the agent is passive during authentication), protection of servers from agents, and the cost of running large numbers of resident agents.

## Contribution

Frames mobile agents as a design choice to be justified against simpler alternatives, with security as the main obstacle. Later papers ([[farmer-1996-security]], [[sander-1998-protecting]]) quote the related IBM view that agent tampering cannot be prevented without trusted hardware.

## Key results

- Individual advantages of agents are each achievable by other means; the case for agents is the aggregate framework (argued, no measurement).
- Authenticating the host environment to the agent is identified as an open problem.
- Raises the scalability question of hosting hundreds of thousands of resident agents on a single data source.

## Methods and models

Qualitative engineering and commercial analysis; no experiments.

## Limitations and open questions

Position paper from 1995; the security discussion is a list of concerns rather than a threat model.

## Relevance to us

Background for all three questions. Its useful point for fork-merge design is the alternative it keeps proposing: instead of sending a stateful part to a hostile domain and merging it back, send messages or stateless queries and keep the decision-making state at home, which removes the merge attack surface at the cost of latency and bandwidth. That is the baseline any Sutton-style fork-merge design should beat. Q1 and Q3: host authentication by a passive agent is the root problem later work tries to fix with secure coprocessors ([[yee-1997-sanctuary]]) and remote attestation ([[menetrey-2022-attestation]]).
