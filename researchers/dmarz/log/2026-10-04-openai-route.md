# 2026-10-04 dmarz/openai-route

- 12:30Z Added `pipeline/reference/openai_provider.py` + 28 offline tests (stub opener and a stub HTTP server on 127.0.0.1), README section with the GPT-6 price table read from developers.openai.com at 12:10Z, and the `openai` provider plus mixed-provider ladders (`providers:` mapping) in READY-CHAIN.md. Surprise: the shared `HTTPError` objects in a `[x] * n` test script are read once, so a body-matched billing test passes only with fresh objects per attempt. Next: launcher support in agentops `scripts/run-ready-chain.py`.
