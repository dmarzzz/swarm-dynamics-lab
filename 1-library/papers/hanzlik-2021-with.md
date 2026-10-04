---
id: hanzlik-2021-with
type: paper
title: "With a Little Help from My Friends"
authors: [Lucjan Hanzlik, Daniel Slamanig]
year: 2021
venue: Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security (CCS '21), pp. 2004-2023
url: https://eprint.iacr.org/2021/1419
doi: 10.1145/3460120.3484582
arxiv: null
cite: "Hanzlik, L., & Slamanig, D. (2021). With a Little Help from My Friends: Constructing Practical Anonymous Credentials. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security (CCS '21), pp. 2004-2023. ACM. https://doi.org/10.1145/3460120.3484582"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "60 (Crossref, 2026-10-03)"
code: []
---

## Summary

Full title: "With a Little Help from My Friends: Constructing Practical Anonymous Credentials" (Crossref stores only the first clause). Addresses two practical obstacles to deploying multi-show anonymous credentials (ACs): credential sharing (a paying user lends the credential to others, which breaks any per-person guarantee) and the resource limits of secure elements. The proposal is core/helper anonymous credentials (CHAC): the credential is bound to a constrained core device (SIM card, smart card, TPM) that must participate in every showing but only performs work independent of the credential size (a single elliptic-curve scalar multiplication), while a powerful helper (smartphone) does the attribute-dependent work yet cannot show the credential without the core. Security is formalised so that the helper alone learns nothing useful. Construction: signatures with flexible public keys (SFPK) combined with new aggregatable attribute-based equivalence-class signatures (AAEQ), proven secure generically and instantiated concretely; showing-token size is independent of the number of attributes. Implementation on a Multos smart card (core) and Android phone (helper): a showing takes under 500 ms on the card and about 200 ms on the phone even with 1,000 attributes. Read: abstract, introduction (motivation including the credential-sharing problem), related work, model overview, performance claims; constructions and proofs skimmed.

## Contribution

Makes credential non-transferability practical by hardware binding without pushing the full AC computation onto the secure element, via a core/helper split and size-independent showing.

## Key results

- Core device cost: one EC scalar multiplication per showing regardless of attribute count.
- Showing: <500 ms on Multos smart card, ~200 ms on Android helper, 1,000 attributes.
- Showing token size independent of number of attributes.

## Methods and models

Pairing-based SFPK and AAEQ signatures, equivalence-class randomisation for unlinkability, generic-then-concrete construction, smart card plus phone prototype.

## Limitations and open questions

Non-transferability rests on the tamper resistance of the core device; it bounds credential sharing, not credential issuance (someone with many SIMs still gets many credentials). No Sybil-count mechanism on its own.

## Relevance to us

Marginal to the identity-multiplication problem but relevant to one piece of it: if agent credentials are to mean "one credential per device or person", the credential must be unsharable, and CHAC is the practical pattern for that. Combine with the uniqueness layer in [[abdolmaleki-2026-attribute]] and the issuer-hiding showings in [[mir-2023-aggregate]] (same AIT group) to get the full privacy-preserving, capped-identity stack. Background: [[ford-2020-identity]], [[douceur-2002-sybil]].
