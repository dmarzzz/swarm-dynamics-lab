# Deployment record

Host: the server named in exclusive claim `dmarz-sybil-newcomer-opus` (sim-dmarz-13 was created for this study on 2026-10-04 and provisioned; not yet claimed). No addresses, credentials or account identifiers are recorded here.

| Time (UTC) | Action | Revision / source hash | Run IDs | Result |
|---|---|---|---|---|
| ~08:12 | claim `dmarz-sybil-newcomer-opus` on sim-dmarz-13 (agentops #226); setup | `d289769a` / `a21290e4…` | — | selftests pass |
| ~08:12 | fleet S0 | same | `sybil-newcomer-opus/8f18e7d0` | 198/198 valid, USD 0 |
| ~08:13 | P0 one-call probe | same | (ledger only) | valid, exact packet, about USD 0.007 |
| ~08:13 | Q0 | same | `sybil-newcomer-opus/39421582` | 36/36 valid, passed, USD 0.205 |
| ~08:14 | S1 | same | `sybil-newcomer-opus/14ea6e6b` | 1,944/1,944 valid, USD 14.478, 2,681 s |
| 09:00 | publish, verify, claim released (agentops #246) | — | — | all artifacts read back; study actual USD 14.691 over 1,981 calls |
