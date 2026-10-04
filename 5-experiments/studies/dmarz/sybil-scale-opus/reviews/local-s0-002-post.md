# Post-mortem: local-s0-002

Offline scripted S0 on orbital-one, 2026-10-04 ~08:25Z, after the transport-retry amendment. Source hash `323f8b7b2089fd6d0355297b58264ad2011784ac31f17df5ef88e9745d0b494f`.

- 264/264 planned, terminal, graded and analyzed; 0 invalid, 0 not started, 0 model calls; qualification cells at all four sizes passed.
- 11/11 selftests, including the mocked Opus contract and the new 429/529 retry test.
- No failures. local-s0-001 (pre-amendment hash) is retained. Next: fleet S0 on the claimed dedicated host.
