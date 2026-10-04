# Evaluating the experiment, not just its outcomes

The suite covers three distinct failure classes. Run with Python and Pillow installed:

```sh
python -m unittest discover -s 5-experiments/studies/vishesh/antsy-receipt-v6/src -p 'test_*.py'
python 5-experiments/studies/vishesh/antsy-receipt-v6/src/mutation_check.py
```

## Contract and policy regressions

Canonical amounts: zero, integer, Rp/IDR prefix, both documented grouping orders and two-digit fractions; reject negatives, malformed grouping, unsupported precision, letters and numeric salvage from invalid text. Total extraction rejects subtotal, cash, quantity and tax, ambiguous conflicting totals and multi-number tails. Reference parsing uses the labeled total field only and marks missing/conflicting references unscorable.

Policies require distinct pipeline identities, abstain on tied consensus, preserve missing evidence, stop before unnecessary checks, continue when unresolved and count referrals separately from correctness. Tests explicitly include unanimous wrong candidates: agreement is not ground truth. Mutating the evaluator answer cannot change any policy action.

## Instrument and accounting regressions

Assignment completeness and uniqueness, exact count reconciliation, independent correct/wrong/refer tallies, actual invoked-tool latency, invalid-tool counts, unknown-reference error bounds and spatial OCR-line reconstruction are covered. Deliberately changed score counts, missing rows and duplicate assignments must be rejected by the post-run audit.

## Deliberate code mutations

A separate harness temporarily injects six defects into the live functions, runs focused regressions, and requires each mutant to fail: subtotal accepted, arbitrary string stripped into a number, referral counted correct, truth leaked to actor, STOP ignored, one source counted as consensus. It restores code after each mutation. These six mutants are a targeted adequacy check, not an exhaustive mutation score.

Current local result:46 tests pass and6/6 mutants killed. A renderer fixture produces a PNG and3 GIFs; every frame decodes and is at least1600px wide. Deployed E0 attempt1 passed its then-frozen30 tests, but development exposed two integration defects; attempt2 froze41 tests including schema and quote regressions. S1 adds all-unscorable rejection and timeout-retention tests. Additional analysis/rendering changes do not alter frozen extraction or policies.

## Post-run audit and review

`audit.py --run RUN_DIR` checks saved output assignment and independently tallies classifications after replaying policies. `analyze.py --run RUN_DIR` provides pipeline failure/missing/correct counts, measured latency distribution, paired descriptive intervals bounds for unscorable accepted references and Wilson intervals for error among scorable accepted receipts. Receipt is the analysis unit. Shared pipelines, repeated costs and policy rows are not new independent samples. Header fingerprints are only a rough dependence diagnostic; they are not certified vendor identities.

These checks establish internal consistency and catch specified defects. They do not replace external scoring review, measured human review cost, model competence qualification, a larger sample or production validation.

A targeted repair regression covers hyphenated subtotals; a replay integration test proves that parent records and measured costs remain unchanged while candidates are reconstructed, and prevents overwriting an existing attempt.
