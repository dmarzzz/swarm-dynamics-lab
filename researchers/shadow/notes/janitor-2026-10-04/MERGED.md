# Janitor merge ledger, 2026-10-04

Review policy: temporarily, shadow/sol-committee-astra holds both seats by orchestrator instruction. Each PR receives two separately posted review comments: pass 1 correctness/safety, pass 2 scope/teammate impact. This is two passes by one reviewer, not two independent reviewers. Merge requires both APPROVE on the current head and green CI. Merge cutoff 22:30Z.

| UTC | Finding / PR | Squash commit | Validation and review |
| --- | --- | --- | --- |
| 15:28:57 | J003 / [#85](https://github.com/dmarzzz/swarm-lab/pull/85) | `7c9092847db14aaaf39b37b776f99004b3ff9e46` | Both astra passes APPROVE at `f28e39f7`; 7 offline batch tests pass; CI green. Holder guard for touch/release/done, no atomic-CAS claim. |
| 15:29:01 | J001 / [#86](https://github.com/dmarzzz/swarm-lab/pull/86) | `34da547215ce81064e7bf27bf90350532bd05c95` | Both astra passes APPROVE at `0410eff3`; 2 offline batch tests pass; CI green. Explicit talk source mappings. |
| 15:35:07 | J002 / [#87](https://github.com/dmarzzz/swarm-lab/pull/87) | `53f2146fca004634ae349f794b7802f2790ccc3c` | Both astra passes APPROVE at `6b286b62`; 9 offline batch tests pass; CI green. |
| 15:35:13 | J004 / [#88](https://github.com/dmarzzz/swarm-lab/pull/88) | `7729e8a34e9735a771e8ed76e9e9c0b790ca8582` | Both astra passes APPROVE at `cb1545fb`; 8 offline batch tests pass; CI green. |
| 15:35:18 | J005 / [#89](https://github.com/dmarzzz/swarm-lab/pull/89) | `442541b3c2004f84f012d0603d248efbf2e0d4b4` | Both astra passes APPROVE at `b22db2ad`; 12 offline batch tests pass; CI green. |
| 15:41:35 | J021 / [#90](https://github.com/dmarzzz/swarm-lab/pull/90) | `d5b0a74dca4ebe9081104048f0ba0a6464a9b036` | Both astra passes APPROVE at `020b6e05`; 4 targeted offline tests pass; CI green. |
| 15:41:40 | J011 / [#91](https://github.com/dmarzzz/swarm-lab/pull/91) | `3eda81c267cde676d5131fc99f01989b58805d51` | Both astra passes APPROVE at `94f7a055`; 3 targeted offline tests pass; CI green. |
| 15:41:46 | J019 / [#92](https://github.com/dmarzzz/swarm-lab/pull/92) | `e259ad132dbe90d963494b94a83e453248fcb205` | Both astra passes APPROVE at `695f79c3`; 4 targeted offline tests pass; CI green. |
| 15:48:03 | J007 / [#93](https://github.com/dmarzzz/swarm-lab/pull/93) | `632b70a55ec9d92a95c93851408e1dac1e4d5d90` | Both astra passes APPROVE at `3eb5a7b7`; 2 ledger-init tests pass offline; CI green. |
| 15:48:08 | J030 / [#94](https://github.com/dmarzzz/swarm-lab/pull/94) | `84865b2158749ea3701db3d647bea81a478a1b93` | Both astra passes APPROVE at `28258f4f`; 16 factory tests in each of normal and -O modes pass offline; CI green. |
| 15:48:13 | J013 / [#95](https://github.com/dmarzzz/swarm-lab/pull/95) | `91e14cba98f178d8a9915ad3505e776b5529fdfb` | Both astra passes APPROVE at `46f782c3`; 6 endpoint/cost tests pass offline; CI green. |
| 15:54:02 | J008 / [#96](https://github.com/dmarzzz/swarm-lab/pull/96) | `79fb7b6f691a88f6f831caad325c8f04272dacf4` | Both astra passes APPROVE at `8fd218e1`; 4 targeted offline tests pass; CI green. |
| 15:54:07 | J022 / [#97](https://github.com/dmarzzz/swarm-lab/pull/97) | `5d4c12e23a0e4950bf6008530a331960d286644d` | Both astra passes APPROVE at `b724073d`; 8 targeted offline tests pass; CI green. |
| 16:01:57 | J006 / [#98](https://github.com/dmarzzz/swarm-lab/pull/98) | `79263e471c14c796e8bf78abc68685ab3f0ddd3b` | Both astra passes APPROVE at `d4ab29b6`; 17 capture-memory tests pass offline; CI green. Durable shared liability reservations, J009 pricing separate. |
| 16:07:55 | J009 / [#99](https://github.com/dmarzzz/swarm-lab/pull/99) | `011a9dd7e1d822751223ed7af8467352181d4427` | Both astra passes APPROVE at `5ae3a842`; 19 capture-memory tests pass offline; CI green. Combined main after these merges: 24 tests pass. |
| 16:09:20 | J010 / [#100](https://github.com/dmarzzz/swarm-lab/pull/100) | `8615b90debe697ddf6677b72681cd9f2737432d8` | Both astra passes APPROVE at `298df2ce`; 19 capture-memory tests pass offline; CI green. Combined main after these merges: 24 tests pass. |
| 16:09:06 | J031 / [#101](https://github.com/dmarzzz/swarm-lab/pull/101) | `ef986922792f1e2bafb78d9abf3076a35fa98426` | Both astra passes APPROVE at `c31a00e1`; 20 capture-memory tests pass offline; CI green. Combined main after these merges: 24 tests pass. |
| 16:49:32 | JF001 / [#102](https://github.com/dmarzzz/swarm-lab/pull/102) | `6feb652d3732dc486f10860bc37ea9b9488696a9` | Both astra passes APPROVE at `e8c381fc`; 20 factory tests pass in each of normal/-O modes; CI green. Legacy factory launch containment only, no successor execution authorized. |
| 17:00:13 | J041 / [#103](https://github.com/dmarzzz/swarm-lab/pull/103) | `49e9e2d9e5e257ace0e82ef1c42ca7663020e501` | Both astra passes APPROVE at `9dd7a324`; 6 Flight Deck preservation tests pass offline; CI green. Add scopes lock/statement updates to new artifact version. |
| 17:08:48 | J041 identity filing / [#104](https://github.com/dmarzzz/swarm-lab/pull/104) | `36f983cedd390b916647502918b8b613c449531a` | Both astra passes APPROVE at `edd75683`; independently verified 108 old lock entries/95 manifest entries preserved, SVG and ingredient hashes match; CI green. |
