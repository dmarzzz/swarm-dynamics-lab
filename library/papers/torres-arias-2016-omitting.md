---
id: torres-arias-2016-omitting
type: paper
title: "On Omitting Commits and Committing Omissions: Preventing Git Metadata Tampering That (Re)introduces Software Vulnerabilities"
authors: ["Santiago Torres-Arias", "Anil Kumar Ammula", "Reza Curtmola", "Justin Cappos"]
year: 2016
venue: "25th USENIX Security Symposium (USENIX Security 2016)"
url: https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_torres-arias.pdf
doi: null
arxiv: null
cite: "Torres-Arias, S., Ammula, A. K., Curtmola, R., & Cappos, J. (2016). On Omitting Commits and Committing Omissions: Preventing Git Metadata Tampering That (Re)introduces Software Vulnerabilities. In Proceedings of the 25th USENIX Security Symposium, Austin, TX, pp. 379-395. USENIX Association."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Shows that signing Git commits does not protect a repository, because branch and tag references (metadata) are unsigned. An attacker with write access to the server can perform "metadata manipulation attacks" that present inconsistent views of the repository to different developers for just long enough to trick one into a harmful action, then leave no trace. The paper identifies teleport attacks (branch or tag reference moved to an arbitrary commit, for example pointing master at an unstable feature commit), rollback attacks (reference moved back to omit a security patch), and reference deletion attacks (hide a branch or release), and calls them reconcilable fork attacks. The defence is a cryptographically signed reference state log of developer actions kept in the repository, checked on fetch; the authors report modest overhead and responsible disclosure to the Git community. I read the abstract, introduction, attack taxonomy and conclusions.

## Contribution

Identifies the merge-and-reference layer, not the content layer, as the attack surface in signed version control, and supplies a log-based defence.

## Key results

- Commit signing and push certificates prevent content tampering but not metadata manipulation.
- Three attack classes: teleport, rollback, reference deletion; each can remove patches or merge untested code without forging any signature.
- Attacks are transient: the server can return to a consistent state afterwards, which defeats after-the-fact auditing.
- Signed reference state log defence with modest overhead (claimed; I did not read the evaluation section in detail).

## Methods and models

Threat analysis of Git's object and reference model, proof-of-concept attacks, a defence implementation and evaluation.

## Limitations and open questions

Assumes an attacker controlling the server but not developer keys. Developers must check the log; out-of-band channels between developers are assumed to exist.

## Relevance to us

Q3: a close analogue of a merge attack where every individual contribution is authentic but the attacker controls which contributions the parent sees and in what order: omit the child report that contradicts the attacker, or teleport the parent's "current belief" pointer to a corrupted branch. A defence based only on signing each sub-agent's output is therefore insufficient; the parent also needs a signed log of which reports were expected and merged. Q1: transient inconsistent views are also a way for an attacker to learn which branch the parent will merge. Related: [[li-2004-secure]] (fork consistency), [[torres-arias-2019-in-toto]], [[kleppmann-2022-making]].
