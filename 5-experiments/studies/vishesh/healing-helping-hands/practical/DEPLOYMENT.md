# Practical diagnostic: deployment and reproduction

Fresh exclusive fleet claim `vishesh-healing-practical-01`, sim-vishesh, merged private fleet PR 76. Existing authorized machine, four CPU cores, Python 3.12.3; one standard-library worker per attempt. No new infrastructure or model inference charge. Allocation retained across the two stages of the same experiment and rechecked immediately before each launch. Credentials were consumed only by the installed reporting process; no model key was needed or moved.

Executed source: practical-01 `51ca83d4d087c686903de67bd6c784dcb375c084`; practical-02 `f4b5b5d7bf2fe5e4d559ed4cbe0fce84eaf5becf`. Public plan URL, exact tracked code and eight parent input hashes were checked before each run. Parent corpus/tapes come from pilot-03 (`46678b2b99936383d01b268075e0ae2cf8b405fc`). New source updates after execution are reporting, packaging, rendering, analysis or documentation; frozen executed versions remain authoritative.

## Replay without model calls

Download the full attempt records from the hub or use the durable local `healing-helping-hands/results/practical-01` and `practical-02` folders. From this source directory:

```
python3 audit.py --results /path/to/results/practical-01
python3 audit.py --results /path/to/results/practical-02 --prior /path/to/results/practical-01
python3 -m unittest discover -s . -p 'test_*.py' -q
```

The audit verifies all frames/metrics, paired event payloads, observed outages, safe verification, and unchanged central controls. It makes no provider calls. A new scientific execution must use a new registered plan/attempt; do not overwrite these directories or infer permission from old plan receipts. The repaired reporting adapter requires acknowledged startup, uses SWARM_HOST rather than unsupported SDK kwargs, and records safe error types locally.

## Build measured visuals

With Matplotlib, NumPy and Pillow installed:

```
python3 render.py --results /path/to/results/practical-01 --out /path/to/cap4-site
python3 render.py --results /path/to/results/practical-02 --out /path/to/cap16-site
python3 compare.py --root /path/to/results --out /path/to/comparison --site /path/to/cap16-site
python3 package.py --site /path/to/cap4-site --mapping H3
python3 package.py --site /path/to/cap16-site --mapping H3
```

The inner artifact manifest hashes payloads only. The outer `archive-checksums.json` hashes the ZIP and manifest and is not itself archived. Renderer/template/comparison-compiler hashes accompany derived outputs. Repeated packaging is deterministic and covered by a regression test. The full local HTML player is interactive; public Swarm Lab supports its measured GIF and PNG fallback, not arbitrary HTML hosting.

The historical pilot-03 renderer/template were synchronized into the durable local visualization directory and rebuilt in `site-repaired`, leaving `site` unchanged. Its H2 mapping, Jev default, missing-model state, exchange-phase labels and noncircular checksums are validated separately. Its corrected bundle is attached to `pilot-03-artifact-repair`; the original checksum failure is retained as `pilot-03-archive-integrity-failure`.

## Cleanup

Both workers exited and all result records/artifacts verified. The exclusive claim was released via private fleet PR 97 on 2026-10-04 UTC, then mirrored to the hub through the host's existing reporting process because the optional local mirror lacked sops. No model runtime or new infrastructure was started in this cycle. Existing VM and evidence files were retained; no subsequent run is queued.
