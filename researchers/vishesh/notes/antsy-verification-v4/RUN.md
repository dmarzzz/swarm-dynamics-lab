# Reproduction and deployment

Use a fresh dedicated fleet allocation; do not run the model on an unrelated experiment's machine. The existing v4 allocation is sim-test-01, claim vishesh-antsy-verification-v4, expiry2026-10-04T03:58:07Z. Machine identity is public; credentials, endpoints and private inventory are not.

E0 source freeze: e5d684e. Python virtual environment, Tesseract eng/ind language data, pillow, pyarrow, huggingface-hub0.36.2, transformers4.57.6, safetensors, pyyaml and CPU torch. Actual versions are retained in manifests. Install Laya source at the SPEC pin; add its directory to PYTHONPATH because its packaged wheel previously omitted backend modules. Download only the pinned public checkpoint before setting HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1. No secret is needed for that public model.

From the repository root, with src below set to researchers/vishesh/notes/antsy-verification-v4/src:

```sh
python "$src/corpus.py" --out /srv/swarm/antsy-v4/E0-attempt-1
python "$src/run.py" --corpus /srv/swarm/antsy-v4/E0-attempt-1 --out /srv/swarm/antsy-v4/S0-attempt-1 --stage S0
# Inspect qualification and write its post-mortem before S1.
python "$src/run.py" --corpus /srv/swarm/antsy-v4/E0-attempt-1 --out /srv/swarm/antsy-v4/S1-attempt-1 --stage S1
```

The output directory must not already exist. Attempts are immutable. Execution uses30-minute process timeouts for S0/S1 and45minutes for E0. Reporting reads the server's approved configuration locally through swarm_report; never print that file. Set SWARM_SOURCE=vishesh/codex-methods and include /usr/local/lib/swarm in PYTHONPATH. Deployment pins the public code commit and stores corpusSHA256 in every stage manifest.

The measured table contains counterfactual scores and must not be passed wholesale to agents. The policy module constructs an allowlisted observation state. Raw receipts, OCR strings and TSVs remain on run storage; publication uses derived numeric summaries and score-only episodes. Dataset attribution: CORD, Clova AI/NAVER, CC BY4.0; exact upstream revision and source links in SOURCES.md.

Offline tests: `python -m unittest discover -s "$src" -p 'test_*.py'`. Run the renderer smoke script before inference. Stage manifests, episodes, call receipts, overview, headroom chart and six replay GIFs upload to the hub. Public site shows images; machine endpoints and tokens remain private. Release allocation only after completion and artifact verification.
