# 2026-10-04 dmarz/pipeline-split-qwen

- 12:00Z Took the fleet monitor's brief: cross-model replication of sybil-split-opus on byte-identical packets; renamed to sybil-split-xmodel when a second model (gpt-6-sol via OpenAI) was added at dmarz's request to use an OpenAI model.
- Built on the parent's sim/study/analyze/render (sim.py byte-identical) and trust-credit-qwen's chain/worker/coordinator/rehearse wiring; both reference adapters copied unchanged. S0 proves byte identity by running the parent's own code in its own process and by matching the parent's recorded S1 packet hashes.
- Surprise: the parent's prompt says "Return only the specified JSON object" but the schema itself travelled in the Anthropic request; on JSON-object routes the shape has to be stated, so one paragraph is appended (the only change to what a model reads).
- Harmless-variant audit: the validator now accepts 12.0 as 12 (JSON Schema integer semantics); strings, fences and extra keys stay invalid; tested through both adapters and a whole rehearsal chain.
- Noticed: experiments/evidence-metadata.json on main has a duplicate `sybil-scale-opus` entry, so `experiment_evidence.py --write` refuses; rendered only this study's block with the script's own functions.
- 12:27Z Full-chain rehearsals passed for both models (stub endpoints, local hub); remaining rehearsal chains running. Next: pin and report to the fleet monitor.
