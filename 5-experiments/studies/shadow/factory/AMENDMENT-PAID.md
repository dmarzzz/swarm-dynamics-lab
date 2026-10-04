# Prospective route amendment, 2026-10-04

Written after the initial pool dispatch, before any paid request. Original preregistration and runner: `577cc1de`. The five pool specs each stopped after their first four qualification requests failed (8 HTTP429 and12 HTTP503 in total; corrected from the initial429-only shorthand): **20/20 transport failures, no model answer, no main comparison calls**. Records and timestamps are retained in the original result directories. This is a provider-capacity failure, not failed Sonnet competence or negative scientific evidence. Read-only pool health inspection also showed the enabled Anthropic accounts rate-limited. No pool configuration, keys, quotas or account selection was changed.

Under the explicitly authorized USD20 factory cap, create a **new `-or` attempt of each spec** on OpenRouter `anthropic/claude-sonnet-4.6`, Anthropic provider only, no provider fallback. Original attempt outcomes never enter the new cohort. All 12 clean qualification fixtures are repeated before any of the 192 main comparison calls. Every new attempt stays paired on the same 48 parent roots; this is route repair, not a new independent scientific replication.

The changes are operational/request configuration: OpenRouter chat endpoint rather than native Messages, explicit reasoning disabled, temperature 0 and max_tokens 500, identical user packet and system text, two concurrent calls instead of four. Source `paid.py` is added to the pin set; original `factory.py` and parent pins are unchanged. No outcome-based tuning, source-simulator change, new endpoint or sample-size extension occurs.

## Spend enforcement

Published OpenRouter model metadata fetched 2026-10-04 15:07Z: input USD3/M, output USD15/M, cache-write USD3.75/M (one hour USD6/M). `provider_metadata.py` reproduces this read-only query. Request provider max-price fields pin input3/output15; no tools/search, no cache configuration, no reasoning and no provider fallback.

`paid.py` reserves `(request bytes + 2048) * USD6/M + 500 * USD15/M` **before** every request, a deliberately loose per-byte input bound including cache-write headroom. The append-only locked shared ledger refuses a reservation above **USD4 per spec or USD20 factory aggregate**, counting settled reported charges plus every unsettled reservation. A failed/unknown request keeps its entire reservation. No retries. A corrupt ledger, duplicate reservation, spec drift or deadline refuses dispatch. The nominal USD4 caps cannot be increased through specs. The unit tests exercise per-spec, aggregate, concurrent and corrupt-ledger behavior plus deadline no-dispatch.

The first attempt used $0 paid spend. New paid requests will begin only after this amendment, new specs, and adapter are committed and pushed. Results will state both provider failures and route-repaired outcomes. If the new route fails, retain those failures as well; do not silently switch models or relax qualification.

Exact launch:

```sh
nice -n 10 python3 5-experiments/studies/shadow/factory/paid.py queue --watch
```
