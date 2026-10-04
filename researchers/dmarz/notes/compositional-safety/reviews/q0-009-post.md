# Post-mortem: q0-009

- Experiment / owner / stage / date: compositional-safety / dmarz (operated by dmarz/compositional-opus) / Q0, first stage of chain q0-009 → p1-002 / 2026-10-04 UTC.
- Pre-run assessment: [q0-009-pre.md](q0-009-pre.md) at source `2b5fb09b4c7bf1deaec25d938930d597998527ce`.
- Disposition: **setup failure, zero model calls.** Runtime admission refused the attempt. Next action: `repair-and-rerun` as [q0-010](q0-010-pre.md).

## What happened

The chain started at 08:18:56 UTC on sim-dmarz-5, registered the q0-009 plan on the hub (receipt written) and called `worker.execute('Q0', 'q0-009')`. Admission read the public site's experiment record before the site showed the new URL and TLDR and raised `public_registration_mismatch`. No results directory was created, no ledger entry was written (still 2,185 calls) and no hub run was started. About three minutes later the public site showed the q0-009 registration correctly; it serves `cache-control: public, max-age=3` behind Cloudflare.

## Cause (verified)

`chain.py` called admission immediately after registering. The hub accepted the registration, but the public read path lagged by an unmeasured interval of seconds. q0-008 passed the same sequence by timing. The same race would have hit p1-002's start after a passing Q0.

## Repair

`chain.py` polls the public site after each registration until its URL and description match the receipt, for at most 120 seconds, then proceeds to admission; if the site never matches, the chain stops before any call. Offline test with a stub that matches only on the third read, and one that never matches.

## Accounting

Zero calls, USD 0. Ledger unchanged at 2,185 calls, USD 59.813121 reserved, USD 8.006142 actual.
