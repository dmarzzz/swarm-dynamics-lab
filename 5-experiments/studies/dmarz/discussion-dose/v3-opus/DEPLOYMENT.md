# Deployment record: discussion-v3-opus

Server `sim-dmarz-9` (dmarz fleet), exclusive claim `dmarz-v3-q0-opus` (agentops PR #227, 14 h), launcher
`scripts/run-discussion-v3-opus.py` in the private agentops repository. Host addresses and credentials are not recorded here.

| Attempt | Revision | What ran | Result | Model calls / cost |
|---|---|---|---|---|
| rehearsal-v3o-a1 | eb7a4d3a | scripted chain (no model), Q0 636 + S1 2,436 | complete, replay-audited | 0 / $0 |
| rehearsal-v3o-a1b | 626c9de2 | scripted chain after clean-first + retry change | complete, replay-audited | 0 / $0 |
| v3o-a1 | 626c9de2 | Opus chain: probe only | probe answer was correct (`value` 51 with its source, `end_turn`, model id matched, 1,162 in / 28 out tokens), but the chain's probe check wrongly required the key set `{value}` while the v3 parent contract is `{value, sources}`; chain stopped before Q0 by design. Operator defect, not a model failure. Fixed by validating the probe with the runner's own contract (`test_probe_accepts_valid_parent_answer_and_rejects_bad`). | 1 / $0.005208 |
| v3o-a2 | 2c261f3d | Opus chain: probe, Q0 (clean-first, early gate), S1 if Q0 passes | probe ok; Q0 passed 6/6, 6/6, 636/636, audited; S1 stopped 10:14:26Z after 61 provider_credit_balance_low failures ([post-mortem](reviews/v3o-a2-s1-post.md)) | Q0 636 / $22.68; S1 291 / $6.81 |
| v3o-a3 | this commit | probe, then S1 only on fresh worlds 54201–54224, admitted by the v3o-a2 Q0 record; credit halt | pending | pending |
