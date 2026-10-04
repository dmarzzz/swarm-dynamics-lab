# Deployment and accounting

Exploratory scaling study, authorized for autonomous execution by dmarz. S2 is disabled; seeds 10000–19999 remain unused. The runtime was frozen before paid qualification and the comparison.

## Fleet and source

- Host: sim-dmarz-4; exclusive claim: dmarz-sybil-scale-api, held by dmarz/sybil-specialists. The preceding pilot worker was stopped before this allocation.
- Execution revision: `722bfc3308affc75ab34d360bae6aca36b50acb5`.
- Runtime fingerprint: `134fd9552ee8bf45777cb751b4104465a7bfd079eb33bc27f1c226c8a6f4b322`. The fingerprint covers all Python runtime files, design, experiment registration and dependencies. Later reporting and documentation changes do not alter execution.
- Server Python virtual environment with PyYAML 6.0.1, Pillow 11.3.0 and NumPy 2.2.6; nine self-tests passed on deployment.
- One finite worker, at most four API requests in flight, no automatic retries. Native provider snapshot `claude-haiku-4-5-20251001`, temperature 0, maximum 500 output tokens.
- Credentials are transported through the private agentops launcher; no credentials or private endpoints are stored in this public study.

## Attempts

| Attempt | Run | Outcome |
|---|---|---|
| Local S0 | local-s0-001 | 264 scripted cases passed; plot spacing repaired before fleet qualification. Original outputs retained locally. |
| Fleet S0 | sybil-scale-api/2c43c19e | 264/264 valid, no API calls. Every saved evaluation and analysis recomputed exactly. |
| API Q0 | sybil-scale-api/27014911 | 64/64 exact clean answers, 16/16 at each size, including all required missing-fact abstentions. |
| API S1 | sybil-scale-api/56defc84 | Launched at the revision above; final reconciliation pending. |

The initial setup failures occurred before API calls: SSH identity and Python environment selection were corrected. Image publication ordering was corrected by re-uploading existing image bytes with the final frame first; no observation or image contents changed. See the individual pre-run and post-run reviews.

## Budget

The user authorized USD 500 aggregate model spend across dmarz's experiments. This study is bounded to 2,600 attempted calls and USD 180 conservative reservations in a persistent, locked ledger. The full planned 64 Q0 + 2,400 S1 assignments require USD 68.300028 of conservative reservation; this bound is distinct from actual model charges.

Q0 used 649,312 input and 2,537 output tokens, costing USD 0.661997; its conservative reservation was USD 2.205736. The final S1 ledger and token totals will be recorded after collection and reconciliation. No claim of final spend is made while requests remain in flight.

## Visual delivery

The hub stores live progress, initial/final 1800×1200 images, a separate hidden-badge image and a measured 33-frame completion replay. This is progress through sampled model calls, not an animation of autonomous identity conversations. The final contact image is explicitly ordered first after worker exit. The verification command checks uploaded checksums, all GIF frames, image dimensions and evaluation/analysis recomputation.

The public [experiment page](https://swarm-live.pages.dev/#/x/sybil-scale-api) and [comparison run](https://swarm-live.pages.dev/#/r/sybil-scale-api%2F56defc84) are registered. During execution, public API/image routes returned Cloudflare 1010/HTTP 403 from this session, including the old pilot's image; the static shell alone loaded. The authenticated hub remains operational. Public browser availability must be rechecked at closeout; local figures will be regenerated from recorded data and filed with provenance.

## Closeout

Pending: all S1 assignments terminal, independent recomputation, artifact verification, final public/UI availability check, worker exit and exclusive-claim release.
