# 2026-10-04 dmarz/program-filer

## 10:28Z: filed the Codex overnight research program and sibling documents on main

- Task from dmarz/fleet-monitor: put the research-program documents that two Codex sessions
  (codex:01a10604-8694-7b71-8df7-11fea1aee0da and codex:01a105f5-6a1f-7810-909b-adf5391d72de) left uncommitted
  in the shared checkout onto main, so builders and remote sessions can cite them. No experiment launched, no
  code changed, no document edited.
- Carried, byte for byte (sha256 compared file by file, 189 files): `artifacts/overnight-research-program-2026-10-04/`
  (v1-v5), `artifacts/overnight-research-canvas-2026-10-04/` (v1-v5), `artifacts/large-swarm-experiment-proposal-2026-10-04/`
  (v1-v2), `artifacts/latest-experiment-results-2026-10-04/` (v1), `artifacts/evaluation-shortlist-2026-10-04/` (v1),
  their 14 `attestations/*.intoto.json` statements, and the notes folders `5-experiments/studies/dmarz/overnight-program-2026-10-04/`,
  `large-swarm-proposal-2026-10-04/`, `latest-results-review-2026-10-04/` and `eval-search-2026-10-04/`.
- Registry: the five artifact entries in `artifacts.yaml` and their 14 keys in `artifacts.lock.json` are the ones
  Codex's `fd.py add` runs wrote (on base e4dd48fc). They were appended unchanged to main's current files; every
  other entry is identical to main before the commit (checked by parsing both). `by`, `model`, `session`,
  `prompt` and `commit` fields are Codex's, untouched. No `fd.py add`, `adopt` or `fill` was run.
- Protocol conflict, noted as AGENTS.md asks: the table in "Where you may write" says `artifacts/` and the
  registry change only through `fd.py add`. Here the entries were made by `fd.py add` in another checkout and
  were transported, on the fleet monitor's instruction, because re-running `add` would re-attribute Codex's
  documents to this agent.
- Left out: `researchers/dmarz/notes/overnight-program-2026-10-04/inputs/researchers__dmarz__notes__pipeline__READY-CHAIN.md`.
  The pre-commit address scan matched it (two mentions of the loopback address, in the rehearsal paragraph that
  is also in `5-experiments/studies/dmarz/pipeline/READY-CHAIN.md` on main). The filing rule was to hold back any
  file with an IP address and report it. The overnight program and canvas versions still list this snapshot as
  an ingredient, with its digest in the lock and statements; the file itself is not in the repo until dmarz
  decides.
- Scan of everything staged (key prefixes, authorization headers, IPv4, long high-entropy tokens, fleet addresses): no
  secret, no fleet or hub address. Nothing about the autonomous research lab design is in these folders.
- Checks: `lab.py check` 0 errors, 5 warnings, identical to main before the commit. `fd.py check --strict .`
  reports the same 4 errors as main before the commit (four film mp4 paths absent from git) and no new one.
- Surprise: program v5 is titled "Can a 180-agent economy develop and sustain identity gaming?"; the
  "Will a 180-agent economy Sybil under rules?" title belongs to v4. The v1 prompt of the program and canvas is
  stored as a sha256 (Codex redacted it). The eval-search inputs include files copied from five external
  benchmark repositories with their LICENSE files.
- Next: dmarz decides on the held-back READY-CHAIN snapshot. Nothing else is open in this lane.
