# Post-mortem: s0-local-001

- Result (measured, orbital-one, Python 3.12): 198/198 valid scripted observations, 0 invalid, scripted qualification passed, zero model calls.
- Offline selftests: 10/10 pass, including the new Opus request-contract test (no temperature/top_p/top_k/thinking/tool_choice/fallbacks; effort low; JSON-schema format) and response-handling test (thinking blocks dropped; `refusal` and `max_tokens` stops classified separately; missing or duplicated text block invalid).
- Pairing: Q0 (36) and S1 (1,944) assignment IDs and packet hashes equal to sybil-newcomer-api.
- Failures: none. Next: fleet S0 on the claimed host.
