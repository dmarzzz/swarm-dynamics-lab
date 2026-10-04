# Reproduction

Use the pinned local Laya source/checkpoint and isolated dependency environment from [the backend record](../adaptive-quorum/BACKENDS.md). Do not install into the user's system Python. Fetch the safetensors checkpoint before running, then use an offline model cache. No hosted key is required.

```
python3 src/selftest.py
python3 src/run.py --backend scripted --out /tmp/api-scripted-attempt-1
PYTHONPATH=/path/to/pinned/laya HF_HOME=/path/to/model-cache HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 src/run.py --backend laya --out /tmp/api-laya-attempt-1
```

Output directories must not already exist. Each run writes its assignments before model loading and has a 30-minute outer limit. All full tapes and model output probabilities are retained. The CLI runs qualification only; it cannot silently launch S1 or S2. Open the generated replay.html locally. Save the exact code hash and model/dependency manifest with results.

The model input-token count is a conservative tokenizer estimate of state plus question JSON, not a hosted billing figure; input exceeding the declared guard is invalidated rather than truncated. CPU wall time excludes model loading. Shared tapes mean physical cost differs from policy-prefix cost.

To report results, use the team's existing hub helper on a claimed reporting slot. Upload only audited synthetic outputs and a public-safe image; never export hub credentials or private addresses. Model inference runs locally. See the v1 reporting bridge for the contract; v2 has 168 assigned arm outcomes and a distinct experiment ID, `adaptive-quorum-api-v2`.
