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
