# B1 public verification HTTP403 diagnosis

2026-10-04. Operational diagnosis; no model calls, credential use or scientific packet changes.

The first B1 operational attempt stopped before collection because the public run registration GET returned HTTP403 through Python urllib. Its registration remained readable through curl. The failed attempt is preserved; replacing the reader does not turn it into a completed experimental run.

## Controlled reproduction

Five unauthenticated GETs used the same public endpoint:
`https://swarm-live.pages.dev/api/runs/influence-swarms/1004-214130-f8e3f2`.

| HTTP client | User-Agent | Status | Response |
|---|---|---:|---|
| Python urllib | Default Python-urllib | 403 | 17-byte text |
| Python urllib | SwarmLab-ReadOnly-Diagnostic/1.0 | 200 | 6,938-byte JSON |
| Python urllib | curl/8.7.1 | 200 | Same JSON |
| curl | Default curl | 200 | Same JSON |
| curl | Python-urllib/3.13 | 403 | Same 17-byte text |

The successful response SHA-256 was `bf7a5c2a7fd461c5fc25cf0f4458e950771e4a58064241a8a2c47adfec1c99f2`; the failure SHA-256 was `2938e9f1284180959e33ab1718d0793a72ff6e4cdb8108c34dcd14e69446de5c`. Only status, allowlisted response headers, length and hash were retained in this report. Successful content was application/json; failure was text/plain. Server identified itself as cloudflare, with no cf-mitigated response header observed.

Changing only User-Agent within either client changes the outcome. This establishes User-Agent-dependent filtering on the tested public path, rather than a requirement for model credentials or additional experiment funding. A subsequent bounded parse of the saved17-byte failure identified Cloudflare error1010. [Cloudflare documents1010](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/) as browser-signature blocking and points to Browser Integrity Check; [BIC documentation](https://developers.cloudflare.com/waf/tools/browser-integrity-check/) says the feature is enabled by default and evaluates client headers/User-Agent. This identifies Cloudflare's browser-signature security layer, but not who enabled/configured the setting on this deployment. Server-side logs were not accessed. The original failed request did not retain its headers/body, so this is a fresh controlled reproduction, not a reconstruction of an unavailable response.

## Repair and acceptance

The owning task already replaced the failing urllib read with its established curl reporting path. The follow-up makes the identity explicit as `SwarmLab-PublicVerification/1.0`, retaining HTTPS, the 25-second deadline, fatal HTTP errors, no redirects and no automatic retries. Registration content must still match the planned condition parameters before any model call. This is not permission to treat a403 as successful verification.

Regression checks cover an explicit client identity and fail-closed behavior without a second client or retry. The exact worker reader is also tested against the public failed-attempt endpoint and its returned run identifier is checked. No scientific qualification claim follows from an HTTP200. Current frozen attempts remain unchanged; adopt the updated runtime only at a fresh source/manifest admission boundary.

Validation: `python3 -m unittest test_runtime test_b1 -q` passed all23 tests (11runtime,12scientific). A live call through the repaired `worker.get` returned the exact failed run identifier and all12 condition TLDR registrations. No credential lookup or model calls occurred in these checks.
