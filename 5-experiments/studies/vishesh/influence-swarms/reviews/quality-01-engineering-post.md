# Quality-01 engineering post-mortem

Final state: scripted engineering complete; live qualification blocked on fresh exclusive allocation.

The preregistered 1,200 outcomes completed with zero invalid outcomes and zero reporting errors. All 15 regression tests pass. No API calls or spend occurred. Source hash: `8eb3f60483f31c1d82ab5162d60fdeb9ea7db8752d096b52f2d334c44ea1669a`.

These checks establish implementation consistency, failure accounting and renderer operation, not model robustness. The scripted policy is not scientific evidence. Historical model results remain unchanged. The recorded 6/6 targeted-check counterfactual improvement is retrospective and must not be substituted for live qualification.

## Resume gates

1. Obtain a fresh exclusive fleet claim and confirm the machine is actually idle. Existing accessible spare hosts had active workers; none were interrupted.
2. Atomically reserve the at-most USD 8 subquota from the existing shared budget authority using src/allocation.py. Do not recreate the shared USD 45 ledger or copy its remaining balance.
3. Deploy the committed source and consume the existing model credential securely. Bind allocation receipt to the new host, expiry and subquota ledger.
4. Register an immutable public README plan URL and verify it resolves, then run S0. Only a matching source/config qualification permits S1. Record all failures and valid adverse results; never retry to obtain a favorable outcome.
5. Publish actual S0/S1 traces and measured live figures, and complete a new post-mortem. No claim of successful repair before this evidence exists.

## Deliverable validation

Historical replay reconciles 50 outcomes and 750 responses. Static PNG, measured GIF, MP4 and interactive HTML were attached to the original completed run. Flight Deck recorded the figure, film and app with hashed ingredients. Its strict check currently flags the checkout folder name and missing app deployment source metadata; the tool has no source option and governed manifests were not edited manually. These packaging diagnostics do not change the measured outcomes.
