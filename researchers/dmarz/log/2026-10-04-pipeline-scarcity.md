# 2026-10-04 dmarz/pipeline-scarcity

- Built the launch-ready package for sybil-scarcity-opus (the scarcity plan on Opus 5.5) in researchers/dmarz/notes/sybil-scarcity-opus: plan documents first, then code, manifest, READY file, runbook, visualization mapping and the chain-001 pre-run review. Pinned commit 36a03510, source hash 82efefd1.
- Offline evidence: selftest 33 OK; offline S0 168/168 with 20 invariants; manifest check equal; rehearsal against a local throwaway hub passed (full chain 158 s for 1,489 stub calls; failed qualification stops at Q0 with exit 3 and no S1 run). No model call, no server, nothing launched.
- Surprises: 233 of the 1,440 S1 assignments share a packet with another cell (1,207 distinct packets), mostly where few outside identities are admitted. The scripted plurality rule gives 0% specialist accuracy at 1 carrier on the engineering roots because admitted attacker reports outnumber the single truthful one, so the model has to use more than counts to do better.
- Next: the lead's review; then the fleet monitor's same-researcher check and the run request. Not tested here: Python 3.12, the real hub, the private launcher, a real model response.
