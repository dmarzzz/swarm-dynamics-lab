# V2 deployment record

2026-10-04 UTC. Owner explicitly approved additional USD15. Authority entry `theseus-v2-additional-15-20261004` reserves USD15 exclusively to `sim-shadow`, maximum 660 calls and two hours total. Other authority increases remain separate; no pre-existing study allocation is reused. Local quota `/srv/swarm/theseus-v2-quota.sqlite` uses transactional pre-dispatch reservations and a persistent shared deadline. No refund after ambiguous failures.

Fresh exclusive claim `vishesh-theseus-v2`, private fleet PR99, merged 2026-10-04T04:05:45Z; expiry 08:05:38Z. Existing Dmarz-fleet host `sim-shadow` was inspected: four CPUs, no non-heartbeat model runtimes. No new machine purchase. Claim refreshed and verified merged immediately before qualification dispatch.

Dedicated checkout `/srv/swarm/vishesh-theseus-v2`; interpreter `/srv/swarm/theseus-v2-venv/bin/python`, Python3.12.3, Pillow11.3.0. Fourteen offline tests passed on host. Source `3aead11342b0097ce098bf40f1e69e6f40b3b001`; public plan SHA256 `e038e15a2e20b20f8752c8e0e596ecca30b291882c4bc43aea24eaf008368197`. Plan and diagnostic-only S0 review published before launch, exact preflight checked, public page visually verified with 0 runs before dispatch. Every assigned condition retains its specific TLDR and immutable plan receipt.

Native pinned Haiku model, 900 output tokens, 18,000 encoded input bytes, max two concurrent world workers, zero transport or semantic retries. Existing approved Keychain alias is consumed by a local process, passed through SSH stdin into worker memory, never printed or written in artifacts. Non-secret config and fresh deployment receipt are stored separately from source. Outputs under `/srv/swarm/theseus-v2-results/<stage>` are immutable raw evidence; derived summaries may be recomputed, never used to overwrite raw failures.

S0 is 24 calls (12 two-checkpoint qualification runs). S1 requires passing qualification with identical instrument hash and a separately published pre-run assessment. One documented repair may use fresh seeds302/303. No S2 is authorized. A model qualification pass does not establish a continuity effect or independent researcher approval.

Prior publication correction: four artifact versions had an invalid `by` harness value. Corrected to `codex` through Flight Deck's metadata/statement writer; authorship retained in notes, session and ingredient hashes preserved, bytes unchanged. Full strict validation with jsonschema4.26.0 passed. The earlier environment lacked jsonschema, so its reported strict pass did not cover enum validation; this limitation is now resolved.

## Terminal execution status

S0: 12 runs /24calls, completed but failed qualification. S0-repair: fresh302/303, source095534bfab16085ac6f4032cd5137cf1e2c7b875,16 server tests passed, planSHA256 7cd472518a76eb901598852847a004c23e8d39836cd9c6523f96284021af4110;12runs/24calls completed but joint qualification again failed. Two-hour ledger retained; total48calls, estimatedUSD0.165211, conservativeUSD0.568098. No S1, no hidden retry, no quota/deadline reset. Full records retrieved with verified bundle hashes. Fleet checkout was isolated before repair because another agent had uncommitted private infrastructure state; that state was left untouched.
