# Post-mortem: haiku45-v2-calibrate-H5 and -H6

- Runs: `discussion-dose-v2/d42f5357` (H5, sim-dmarz-3, claim dmarz-discussion-dose-v2-h5), `discussion-dose-v2/0cfb900e` (H6, sim-test-01, claim dmarz-discussion-dose-v2-h6). Source `80dc519`. 24/24 episodes recorded in each; no missing outcomes.
- Status: execution complete; both runs marked failed by the worker's clean-accuracy gate (6/12 < 80%). Diagnostic-only by design, so this gate does not block anything.
- Result: see V2-DESIGN.md, "Ceiling-search results". H6 reaches 12/12 belief and memory corruption, but attacker win is 8/12.
- Experiment quality: the manipulation occurred (role endorsements as designed). Clean competence is low at H5 and H6 (6/12), so attacker-win rates there are capped by decision errors and are not a clean measure of persuasion.
- Issues: (1) H5 had 3 invalid episodes: two duplicate-key ballots (known) and one not yet inspected. (2) Replays uploaded live by this source aliased the running tally (every snapshot showed final counts). Fixed in `frames.py` with a regression test; all six calibration replays were rebuilt from saved events and re-uploaded. (3) No post-mortem yet for H1 to H4 calibration or v1 S0.
- Visualization: live `frame.json` was uploaded during both runs. Backfilled replays pass the tally check against the episode records.
- Next action: diagnostic. Inspect the third H5 invalid episode and the four H6 decision errors (atomic probe: same evidence, single agent, rule application only) before any H5/H6 S0.
