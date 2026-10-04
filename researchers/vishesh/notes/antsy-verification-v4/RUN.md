# Reproduction and deployment

Use a fresh dedicated fleet allocation; do not run the model on an unrelated experiment's machine. The completed v4 allocation was sim-test-01, claim vishesh-antsy-verification-v4, expiry 2026-10-04T03:58:07Z. That claim is now released; obtain a fresh allocation before running. Machine identity is public; credentials, endpoints and private inventory are not.

E0 source freeze: e5d684e. Python virtual environment, Tesseract eng/ind language data, pillow, pyarrow, huggingface-hub0.36.2, transformers4.57.6, safetensors, pyyaml and CPU torch. Actual versions are retained in manifests. Install Laya source at the SPEC pin; add its directory to PYTHONPATH because its packaged wheel previously omitted backend modules. Download only the pinned public checkpoint before setting HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1. No secret is needed for that public model.

From the repository root, with src below set to researchers/vishesh/notes/antsy-verification-v4/src:

```sh
python "$src/corpus.py" --out /srv/swarm/antsy-v4/E0-attempt-1
python "$src/run.py" --corpus /srv/swarm/antsy-v4/E0-attempt-1 --out /srv/swarm/antsy-v4/S0-attempt-1 --stage S0
# Inspect qualification and write its post-mortem before S1.
python "$src/run.py" --corpus /srv/swarm/antsy-v4/E0-attempt-1 --out /srv/swarm/antsy-v4/S1-attempt-1 --stage S1
```

The output directory must not already exist. Attempts are immutable. Execution used 30-minute timeouts for S0 and hosted Jev S1, 45 minutes for E0 and local Laya S1. The Laya S1 extension was documented before launch from measured S0 latency. Reporting reads the server's approved configuration locally through swarm_report; never print that file. Set SWARM_SOURCE=vishesh/codex-methods and include /usr/local/lib/swarm in PYTHONPATH. Deployment pins the public code commit and stores corpus SHA256 in every stage manifest.

The measured table contains counterfactual scores and must not be passed wholesale to agents. The policy module constructs an allowlisted observation state. Raw receipts, OCR strings and TSVs remain on run storage; publication uses derived numeric summaries and score-only episodes. Dataset attribution: CORD, Clova AI/NAVER, CC BY4.0; exact upstream revision and source links in SOURCES.md.

Offline tests: `python -m unittest discover -s "$src" -p 'test_*.py'`. Run the renderer smoke script before inference. Stage manifests, episodes, call receipts, overview, headroom chart and six replay GIFs upload to the hub. Public site shows images; machine endpoints and tokens remain private. Release allocation only after completion and artifact verification.

## Analyze without rerunning inference

Install Pillow for tests/renderer and matplotlib for the comparison figure. Unpack each run’s committed `episodes.jsonl.gz` and `receipts.json.gz` into a local directory alongside its manifest. Unpack `results/measured.jsonl.gz` separately; evaluator data never goes into an actor prompt. Then run:

```sh
python "$src/analyze.py" --run RUN_DIR
python "$src/verify_results.py" --run RUN_DIR --corpus measured.jsonl
python "$src/compare.py" --laya LAYA_DIR --jev JEV_DIR --out COMPARISON_DIR
```

The final report is [RESULTS.md](RESULTS.md). The Jev adapter and relay pin the model/provider, enforce the existing cumulative budget and journal invocations before recovery. Follow the published Jev pre-runs; never initialize a fresh ledger to evade the prior cap. Replaying a successful response is not a new independent model trial.
