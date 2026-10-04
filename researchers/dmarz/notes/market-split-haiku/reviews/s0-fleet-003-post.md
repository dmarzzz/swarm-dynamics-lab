# Post-mortem: s0-fleet-003

2026-10-04; market-split-haiku; dmarz/market-split. Disposition: advance to bounded D0 diagnosis, not discovery. Read s0-fleet-003-pre.md and s1-001-post.md.

All six planned bundles started once and finished:12/12 valid mock episodes,zero model calls,zero paid cost. All17 network-blocked checks passed locally and on the dedicated host. The100-call/$0.822515 paid ledger was unchanged. Source8e355a187d212ece4c6469c5fdd949c06641e52c44d785382c834817e5b2a465; designbdcbdbcf7d25d0de64e4187272b9bb50557180e281ad00f61b18b38bc3238530. No duplicate/missing episodes,unpriced requests or visualization errors.

All42 artifact hashes matched hub receipts. Every final frame is1800×1200 and every replay1080×720 with all eight logical rounds. Pinned-runtime replay reproduced all96 actor observations/actions and all12 traces/evaluations exactly. The mapping remains market-split-api-v1; mock status is explicit. This tests mechanics/reporting, not model competence or natural discovery. The stage manifest is s0-fleet-003-verified.json and recovered files retain original receipts.

The new accounting preserves a safe stop_reason; its regression test rejects max_tokens output while retaining priced usage. The new gate test proves that Q0 alone cannot authorize S1 and that a missing/unpriced R0 blocks it. Same neutral ordinary prompt/economy; no strategy hints added. H3 remains open because no real response has exercised the increased headroom yet. Next is exactly two D0 calls on the preserved failed observations. Passing them permits fresh mechanics/competence/reliability tests, not a discovery conclusion. Claim dmarz-market-split-haiku is visible in the hub through10:09:38UTC; one active assignment per host.
