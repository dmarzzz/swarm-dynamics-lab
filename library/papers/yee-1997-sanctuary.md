---
id: yee-1997-sanctuary
type: paper
title: "A Sanctuary for Mobile Agents"
authors: ["Bennet S. Yee"]
year: 1997
venue: "Technical report, UCSD (dated April 28, 1997); later in Secure Internet Programming, LNCS 1603, Springer 1999"
url: http://web.archive.org/web/20000815100250/http://www.cs.ucsd.edu:80/~bsy/pub/sanctuary.ps
doi: null
arxiv: null
cite: "Yee, B. S. (1997). A Sanctuary for Mobile Agents. Technical report, Department of Computer Science and Engineering, University of California, San Diego, April 28, 1997. Published version: Secure Internet Programming, Lecture Notes in Computer Science 1603, pp. 261-273, Springer, 1999."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "71 (Crossref, LNCS 1999 version, 2026-10-03)"
code: []
---

## Summary

Read from the archived April 1997 PostScript (text extracted). Yee asks how an agent's owner can trust results returned from a tour of possibly malicious servers, using the air-fare agent that a Fly-By-Night server "brainwashes" by editing its memory of visited airlines and prices. Key observations: signed code and read-only state let honest servers detect tampering with them; the read-write state cannot be trusted after visiting a malicious server, so only results from the maximal honest suffix of the route are trustworthy; two or more colluding malicious servers can hand the agent between them and brainwash it into believing it visited the servers in between. He criticises server replication (Minsky et al.) because replicas under one administrative domain or running identical software fail together. He proposes agent replication for the at-most-one-bad-server case: two agents traverse the route in opposite orders, which yields at worst second-price (Vickrey-like) results. He introduces Partial Result Authentication Codes (PRACs): per-server MAC keys that the agent erases before migrating, giving perfect forward integrity for the honest prefix; one-way-function key chains and publicly verifiable signature variants; and floats holographic and CS proofs for verifying remote execution. The Sanctuary project itself is a secure-coprocessor host for Java agents.

## Contribution

Introduced forward integrity (PRACs) and the honest-prefix versus honest-suffix framing that the free-roaming agent literature (Karjoth et al., NIST [[jansen-1999-mobile]]) builds on, plus the earliest critique I found of independence assumptions in replicated agent defences.

## Key results

- Departures from the dispatch-time route must begin and end at a malicious server (argued).
- After a malicious visit, all prior read-write memory is suspect, including data from earlier honest servers.
- Server replication fails when replicas share an operator or software stack: bribing one engineer or one exploit compromises all replicas.
- Two agents on S and its reverse recover the true minimum fare with one malicious server unless that server also has the minimum, in which case the outcome is second-best minus epsilon.
- Per-server signed partial results stop full brainwashing; at worst the agent forgets a quote, which is detected by enumerating signatures. Queries must be signed and timestamped with the answers to stop substitution.

## Methods and models

Analytical argument and protocol design; no implementation results reported. Threat model: one or more malicious servers that can rewrite all mutable agent state; secure channels between honest servers.

## Limitations and open questions

The agent-replication result covers only one malicious server and a specific (minimisation) function. Proof-based verification is described by the author as speculative and impractical at the time. Trusted coprocessors move trust to hardware vendors.

## Relevance to us

Q3: this is a precise threat model for "the corrupted part returns and corrupts the parent": the returning agent's mutable memory is entirely attacker-controlled after one bad hop, and colluding hosts can forge a consistent-looking itinerary. Q2: the critique of replication is the key caution for any k-of-n merge rule: k-of-n only buys security if the n children's corruption events are independent, which fails if they visit the same hostile domain or share the same model weights (compare [[schneider-2005-implementing]]). The two-direction itinerary design is a small threshold construction. Q1: varying route order and splitting the tour are ways of making which returning copy is decisive unpredictable. PRAC-style erasure suggests a concrete mechanism for sub-agents: commit and sign each observation as it is made, then destroy the signing key, so later corruption cannot rewrite earlier evidence. Related: [[sander-1998-protecting]], [[minsky-1996-cryptographic]], [[farmer-1996-security]].
