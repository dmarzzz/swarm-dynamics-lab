---
id: hanff-2025-security
type: paper
title: "Security Analysis of Privately Verifiable Privacy Pass"
authors: [Konrad Hanff, Anja Lehmann, Cavit Özbay]
year: 2025
venue: "Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25)"
url: https://doi.org/10.1145/3719027.3765172
doi: 10.1145/3719027.3765172
arxiv: null
cite: "Hanff, K., Lehmann, A., & Özbay, C. (2025). Security Analysis of Privately Verifiable Privacy Pass. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25), pp. 2922-2936. https://doi.org/10.1145/3719027.3765172"
topics: [sybil-resistance]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Formal security analysis of the IETF-standardised, privately verifiable variant of Privacy Pass, the anonymous token protocol originally designed to spare Tor users from repeated CAPTCHAs. In this variant the issuer and verifier share a symmetric key and issue single-use tokens whose redemption is anonymous and unlinkable to issuance. The original protocol of Davidson et al. (PETS 2018) had a formal analysis, but the IETF standard changed the protocol, leaving the deployed version's security unproven; this paper fills that gap. Only the abstract (via Crossref/OpenAlex; the ACM page sits behind a bot check) was read, so the specific security notions, proof results and any issues found are not recorded here.

## Contribution

Closes the gap between the analysed academic protocol and the standardised one that actually ships (e.g. in browsers and CDNs).

## Key results

- Not read beyond the abstract.

## Methods and models

Provable-security analysis of the IETF privately verifiable Privacy Pass issuance and redemption.

## Limitations and open questions

Unknown from the abstract whether the analysis found weaknesses or confirmed the standard's security, and under which assumptions. Privately verifiable tokens require issuer and verifier to share a key, which limits use across organisations.

## Relevance to us

Privacy Pass tokens are a deployed way to rate-limit anonymous clients (one token per solved challenge), and so a candidate building block for metering agent swarms without identifying them; knowing the standard is formally sound matters if we build on it. Context: [[davidson-2018-privacy]] (original), [[davidson-2024-privacy]] (architecture), [[chu-2023-security]] (rate-limited variant), [[gh-cloudflare-privacypass-issuer]]; used inside [[durak-2025-sandi]].
