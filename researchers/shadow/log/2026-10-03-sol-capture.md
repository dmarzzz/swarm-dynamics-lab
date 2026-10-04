# 2026-10-03 sol-capture

Built the capture-memory exploratory environment under `researchers/shadow/notes/capture-memory/` as a labelled
hunch (hypothesis PR 82 is `proposed`, survey review says `revise`, so nothing goes in `experiments/`). Followed
`templates/experiment-worker/README.md` steps 0 to 7: simulator with the template's contract (deterministic,
paired across arms and across memory lengths, blind, total), JSON-in-yaml design with a declared primary
contrast, pre-registration draft, selftest (32 checks, passes), coordinator without S2, hub worker, analysis with
cluster bootstrap. Scripted tanh-over-memory policy only; the HTTP adapter exists and refuses to start without a
dollar cap.

Chose beta = 2.5, h_inside = 0.1, h_outside = 0.5 from the mean-field fixed-point map of the rule over a
binomial memory before looking at removal-phase output per memory length. The map says the attack state becomes
a second attractor only from memory 3 up, which is the mechanism the hunch needs.

S0: clean world holds at every memory. S1 (9,600 episodes, 47 s): primary contrast memory 20 minus 1 under
purge = -0.294 [-0.311, -0.277] on the fraction back on the original at round 50. Surprise: full memory never
captured within 100 rounds at 10 or 12 of 24 committed. The hypothesis file's dose rule (1.5x tipping) does not
carry to unbounded memory; that has to be decided before any model run, not tuned after. Second surprise: a full
private memory wipe adds almost nothing over a bare purge inside the spinodal (+0.01 to +0.06), because
surviving peers re-infect emptied agents faster than a weak prior pulls them back. That number is the bridge to
vishesh's private-versus-shared restoration arms.

Next: fleet run on sim-shadow for hub provenance, PR to main (not merged), then wait for the hypothesis gate.

Fleet: ran on sim-shadow (claim running then released via agentops PRs #28, #31). swarm_report is importable
there with PYTHONPATH=/usr/local/lib/swarm (the profile.d export is not picked up by non-login ssh commands; the
box is otherwise unprovisioned per agentops ROADMAP D1, did not touch that). S0 + S1 done, analysis attached on
the hub, numbers identical to local. PR dmarzzz/swarm-lab#83 open, not merged.

## 2026-10-04 03:30Z to 05:00Z: land PRs, run the pilot

dmarz's point stood: PRs 82 and 83 had sat open while everyone else pushed to main, and AGENTS.md says push to
main directly. Rebased both onto origin/main (clean, `lab.py check` 0 errors), squash-merged them myself: 82 =
three hypotheses at `proposed` (no self-acceptance; `accepted` still needs another researcher's review), 83 = the
capture-memory note tree. The one red check on 83 was the repo-wide flightdeck artifact schema error from vishesh's
artifacts 10 to 13 (`by: vishesh/codex-theseus` not in the enum), unrelated and since fixed on main.

Then the real-model pilot on Shadow's GO. Built: prefix fork in sim (arms share the entrench + takeover run,
bit-identical for scripted), a Budget ledger in the adapter (call cap, dollar cap by reservation AND by provider
usage, saved to disk), Q0 as a gate stage, S2_pilot as a dev-only stage needing `--go`. Q0 attempt 0 failed: the
8B model wrote 'brusk' for 'brisk' 3 times in 36. Edit-distance-1 accept + one re-ask fixed it (hub Q0 validity
1.00). S2_pilot: 12 episodes, 10,384 calls, 0.031 USD, 24/24 valid.

Surprises: (1) the model's full-memory agents tip in 8 rounds, a running mean needs 80 to 100: it is not averaging
the list. (2) Running the scripted rule at the pilot's own N = 12 / entrench 10 shows no freeze either, so the S1b
freeze is about depth of banked history, not unbounded memory as such; the pre-run should have run
`pilot_reference.py` first. (3) Two of six word pairs never captured because the model prefers one nonsense word
(pira, olam): the yang-2026-when artefact, and the reason the (beta, h) per-pair fit is now a hard prerequisite.

Memory 1 looks scripted-like (+0.18 back after purge vs +0.19 to +0.24 scripted). The memory contrast is
undetermined at 4 tasks. sim-shadow refused ssh, so this ran on shadow's box again, no claim held.

Next: per-pair prior fit (~1K calls), model-side dose sweep at N = 12 (~5K calls), a same-dose cell to test the
"copies the last word" alternative, and nothing on holdout until the hypothesis is reviewed.
