# Post-mortem s0-local-001

- Experiment / owner / stage / date: market-split / dmarz / scripted S0 / 2026-10-04.
- Pre-run: s0-local-001-pre.md; code 6d928d2, configuration market-split-v1; no model.
- Disposition: advance to identical fleet qualification.

## What ran and what happened

18 planned → 18 started → 18 terminal → 18 valid → 18 analyzed episodes, no duplicates or missing attempts. Model calls/tokens/cost: 0/0/$0. Three cells completed locally in under 30 seconds. Artifacts and exact per-cell timing are under results/s0-local-001. Two task clusters, one seed, all three policies and regulators. Descriptive scripted mean profit lift of programmed registration versus one firm: +7202.42 credits under firm regulation, -91 under ownership regulation, -91 without regulation. Sustained evasion was 2/2 for the split control with firm regulation and 0/2 with owner regulation. These are mechanical controls, not estimates of model behavior.

## Visualization review

Mapping market-split-v1; each cell has 12-frame GIF and 1800×1200 final PNG. Inspected the firm-regulation final image: firm boundaries, registrations at rounds 4/5, persistent ownership HHI, lower firm HHI, and recorded finance labels agree with task 0/seed 11. Offline tests also compare frames before/after registration and exercise an injected failure. UI playback awaits fleet upload. No missing rounds or renderer failures in the pilot.

## Experiment quality

All 10 offline test groups pass with sockets disabled. This establishes deterministic paired accounting and supported artifact generation. It does not test an API adapter, LLM task competence, unprompted discovery, tacit collusion, or statistical power. Ownership information is supplied by the simulator. Rival capacity constraints and the simple HHI trigger are deliberately chosen sandbox assumptions.

## Failure and repair ledger

During the preflight unit tests, GIF duration construction used a scalar where Pillow expected a duration list. Corrected before the pilot; the transition/failure renderer test now verifies all 12 GIF frames. No scientific attempt was repeated. Flight Deck's strict folder-name check also required placing the isolated clone in a directory named swarm-lab; the project metadata was preserved. No unresolved execution defect remains.

## Next run

Run identical S0 on an exclusively claimed temporary server; verify artifact receipts and real UI playback before S1. Existing fleet machines are all claimed, so do not borrow them. Model transport stays disabled and the paid budget remains zero. Formal research gates remain unmet.
