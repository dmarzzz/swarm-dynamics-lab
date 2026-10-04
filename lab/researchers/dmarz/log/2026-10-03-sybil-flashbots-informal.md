# 2026-10-03 sybil-flashbots-informal

What I did: scanned ethresear.ch (Discourse search API, 9 queries) plus web searches for Flashbots-adjacent informal writing on Sybil resistance. Added 19 entries tagged sybil-resistance: 17 blogs (mostly ethresear.ch posts, plus Vitalik's biometric PoP essay, the IC3 Complete Knowledge post, an EigenPhi guest post on BuilderNet and a functor.network post on AUCIL), the Devcon SEA Dave talk (read via slides) and the Complete-Knowledge/ck repo. 12 read in full. Coverage note filled in tasks/scan-flashbots-sybil-informal.md. Did not commit or push; the coordinator handles git.

What surprised me:
- The most transferable ideas for agent swarms are Sybil-tolerant rather than Sybil-excluding: Dave's tournament lets one honest party with a laptop beat any number of coordinated copies with logarithmic delay, and Vitalik's anti-correlation penalty detects hidden common control through co-failures without identifying anyone.
- Bahrani and Neuder's capacity-oracle post shows staking alone does not stop splitting when rewards are linear; convex rewards are needed. AUCIL shows the same pattern: individually incentive-compatible, not Sybil-proof.
- TEE attestation is no longer a credible "one agent, one machine" identity: TEE.fail forged TDX quotes with about $1,000 of hardware in about 15 minutes, and every TEE network responded with allowlists.
- ERC-8004 agent registries already hit the Sybil-reviewer problem; ACTA proposes per-context nullifiers.

What next: pull X threads by Flashbots researchers (needs a human X session), get transcripts for MEV-SBC and TEE.salon talks, and catalogue the formal papers these posts rest on (Dave arXiv 2411.05463, Proof of Cloud arXiv 2510.12469, Liquefaction arXiv 2412.02634, WireTap, TEE.fail) in a paper lane.
