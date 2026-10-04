---
id: sander-1998-protecting
type: paper
title: "Protecting Mobile Agents Against Malicious Hosts"
authors: ["Tomas Sander", "Christian F. Tschudin"]
year: 1998
venue: "Mobile Agents and Security (G. Vigna, ed.), Lecture Notes in Computer Science 1419, Springer"
url: http://web.archive.org/web/20001010082131/http://www.icsi.berkeley.edu:80/~tschudin/ps/ma-security.ps.gz
doi: "10.1007/3-540-68671-1_4"
arxiv: null
cite: "Sander, T., & Tschudin, C. F. (1998). Protecting Mobile Agents Against Malicious Hosts. In G. Vigna (Ed.), Mobile Agents and Security, Lecture Notes in Computer Science 1419, pp. 44-60. Springer."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "275 (Crossref, 2026-10-03)"
code: []
---

## Summary

Read from the authors' February 1998 preprint (archived PostScript from ICSI, text extracted). The paper attacks the folklore, quoted from Chess et al., that a host executing an agent can always read and modify it, so agents cannot keep secrets without tamper-resistant hardware. The authors argue the folklore assumes cleartext programs, and propose non-interactive Computing with Encrypted Functions (CEF): the originator sends a program for an encrypted function E(f), the host evaluates it on its own input, and only the originator can decrypt f(x). They give concrete schemes for polynomials over Z/nZ using additively homomorphic encryption (they show additive homomorphism implies mixed-multiplicative homomorphism on Z/nZ), an exponentiation-based instance, a composition-based idea for rational functions, and "undetachable signatures" so an agent can sign only outputs of a fixed function. They name the canonical attack: a host that "brainwashes" an air-fare agent so it forgets servers already visited and picks the host's offer.

## Contribution

The founding claim that software-only protection of an agent's computation on a hostile host is possible in principle for restricted function classes. Later work ([[algesheimer-2001-cryptographic]]) shows the limitation that the host must not receive output.

## Key results

- Three problems are posed: code and execution integrity, code privacy, and computing with secrets in public (remote signing without revealing the key).
- Lemma 5 and Corollary 6: an additively homomorphic scheme on Z/nZ allows CEF for polynomials.
- Information leakage: the scheme reveals which coefficients are zero or equal, and low-entropy coefficients are open to table attacks; RSA-style polynomials with one non-zero exponent are vulnerable.
- The undetachable signature construction lists four attacks (left decomposition, two interpolation attacks, inversion) and a strengthened multivariate variant; its security rests on birational maps whose earlier Shamir constructions were broken (Coppersmith, Stern, Vaudenay).
- Section 2.1 notes, without analysis, that a task can be split across several collaborating agents using secret sharing, with execution platforms chosen at random to make collusion unlikely.

## Methods and models

Theoretical cryptography; no implementation or measurement. Model: originator Alice, host Bob, non-interactive protocol, function classes limited to polynomials and rational functions.

## Limitations and open questions

Authors state the security analysis of all schemes remains to be done, and that general (Boolean circuit) CEF was not achieved. Denial of service, replay and repeated black-box probing by the host remain possible.

## Relevance to us

Q3: the paper's air-fare example is the earliest clear statement I found of the attack dmarz describes: the visited host rewrites the agent's memory of where it has been and what it saw, so the agent returns as the host's advocate. Q2: the side remark about splitting a task across several agents with secret sharing on randomly chosen platforms is an early threshold design for the fork-merge setting, later made concrete by [[minsky-1996-cryptographic]]. Q1: random choice of execution platform is a hiding defence against targeted corruption. For LLM sub-agents there is no analogue of CEF for natural-language reasoning, so the practical lesson is negative: protection of the returning part must come from detection and redundancy, not secrecy. Related: [[yee-1997-sanctuary]], [[farmer-1996-security]], [[harrison-1995-mobile]].
