# Deployment and reproduction

Experiment `swarm-of-theseus`, candidate SOC-24. Dedicated host `sim-shadow`; exclusive merged allocation `vishesh-swarm-theseus` (fleet claim PR 32), initially expiring 2026-10-04T05:28:09Z. Private addresses and credentials are deliberately absent. Deployed checkout `/srv/swarm/vishesh-swarm-theseus`; Python environment `/srv/swarm/theseus-venv`; outputs `/srv/swarm/theseus-results/<attempt>` remain separate from source. Four CPU cores; three concurrent world-arm workers. Recorded runtime: Python 3.12.3, Linux 6.8.0-142-generic, x86_64, PyYAML 6.0.1, Pillow 11.3.0. Runtime metadata was sampled during S1; packages were not changed between stages. Model is pinned in model-config.json; exact prompts and schema live in src/study.py and src/provider.py.

The existing shared USD 45 authority reserved a non-overlapping quota under `swarm-of-theseus-v1`: initially USD 12 / 1,152 calls, then 1,728 calls for repair, then USD 15 after another USD 3 was reserved from the same authority. This did not create new spending authorization. The dedicated local ledger tracks use within that allocation and cannot spend the shared cap independently. Reservations are conservative byte/output-token bounds and are not refunded; usage estimates are separately reported. No new machine was provisioned.

Credentials are consumed from the existing approved Keychain alias by a local process and passed through SSH stdin into worker memory. No secret is written to source, results, arguments, transcript or launch logs. The local launcher is not a public credential distribution mechanism. Replicators must supply their own authorized secret mechanism, dedicated host and budget reservation.

| Attempt | Frozen source | Plan / state |
|---|---|---|
| S0-a1 | e94b0fa1c8c6f711dad36b48723e28a6f10f966c | public-plan HTTP failure before model initialization; no calls |
| S0-a2 | 4c1272651eecf4d2ceef3dd6ebd4e473c08be066 | 12 outcomes, 4 failures; qualification failed |
| S0-a3 | fcee9c26074ec72dfa262ae750812828b983421b | 12 outcomes, no execution failures; observatory below qualification threshold |
| S0-a4 | 586c476892c442c29fc290358ce21a75cbcc07fe | 12/12 complete; 72 independently audited frames; every verbatim control 1.0 / 1.0; qualification passed |

A concurrent main push initially rejected the publication of the S0-a4 revision. Deployment of that unpublished revision failed at checkout, before registration/inference. Pull/rebase/check/push resolved the race without force or overwriting team work, then the published exact revision was deployed. This is a deployment setup event, not an extra experimental outcome.

## Reproduce checks

From the repository root:

```sh
python3 -m unittest discover -s researchers/vishesh/notes/swarm-of-theseus/tests -v
python3 researchers/vishesh/notes/swarm-of-theseus/src/audit.py /path/to/downloaded/attempt
python3 researchers/vishesh/notes/swarm-of-theseus/src/analyze.py /path/to/downloaded/attempt
python3 researchers/vishesh/notes/swarm-of-theseus/src/summary_figure.py /path/to/summary.json /path/to/summary.png
```

Offline unit tests do not require fleet allocation or credentials. They exercise synthetic fixtures, not model evidence. Existing attempts must never be overwritten. For a new model attempt, publish a new pre-run review and immutable plan, register/verify its public page, obtain/verify a dedicated exclusive allocation, reserve budget centrally, deploy/test the exact source, and use the runner with a fresh output path. S1 requires the reviewed passing qualification summary, independent audit, and matching model/study/provider hashes. S2 is not implemented or authorized by research gates.

The hub supports live/final images; custom HTML replay is a downloadable artifact, not a native spatial view. Public plan page: https://swarm-live.pages.dev/#/x/swarm-of-theseus . Per-run plan metadata preserves the original immutable source even after an experiment-level amendment.

S1-a1 is frozen at source `a773ff5410442fcf351cfc817550b3fc92a88994`, exact model/study/provider hashes matched to S0-a4. It contains 36 prospective world-arm outcomes, maximum 864 calls. Terminal accounting is recorded in S1-a1-post.md after completion.

## Final publication verification

The public hub was visually verified after completion: 72 started runs, 68 done, 4 failed; S1 is 36/36 complete. The initial blocked setup is recorded separately and did not start a run. Original condition TLDRs and immutable plan receipts remain attached. The 36 S1 receipts reference `586c476892c442c29fc290358ce21a75cbcc07fe`, the already-published v3 plan containing the S1 design; source is `a773ff5410442fcf351cfc817550b3fc92a88994`. The later README revision only adds qualification status, not a changed S1 treatment or analysis. Plan revision and executed source revision are distinct.

The public artifact proxy verified the final PNG byte-for-byte but returned HTTP errors for the Markdown, HTML, JSON and gzip downloads. All six uploads were reported to the hub. Repository Flight Deck artifacts provide durable report, replay, figure and evidence downloads instead. The evidence archive contains 305 source files and a hash index (306 entries), SHA256 `be53597095953fdf3ad717df93d1e3d4b9d6a22399b6a815c80d1571ebc0eafc`. Extracting it into `data/theseus-inputs` recreates the evidence ingredients referenced by Flight Deck.

Flight Deck registration used `fd.py add`, with per-input provenance. Strict validation passed in a correctly named `swarm-lab` validation copy; the working clone's different directory name otherwise produces a naming warning. Its first refresh changed unrelated historical ingredient records; approval review rejected staging those changes. Restoring the exact historical input bytes and timestamps for the tool's refresh preserved every pre-existing lock entry and attestation unchanged. Only Theseus artifact additions are published.
