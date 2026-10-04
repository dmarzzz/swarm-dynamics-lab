# Prospective offline engineering review

Reviewer: vishesh/codex-independent-reviews. User explicitly approved this review in the receiving task. Same-researcher engineering review only; not a formal independent researcher approval.

TLDR: Test whether optimal-swarm-size Q-A software safely preserves budget exposure, evaluates restricted tasks and reports execution failures. Compare existing reference fixtures with offline malformed/failure inputs. Metrics are unit-test outcomes and explicit counterexamples; no model capability or size-effect claims. No paid calls, credentials, fleet allocation, model requests, or fit/validation/transfer cases.

Before diagnostics publish this plan at an immutable commit URL and verify its public bytes. Run the existing offline test suite; inspect source and use bounded mocked checks for provider-failure classification, reporting failure handling, launch readiness and arithmetic evaluator behavior. Keep all outputs including failed checks. Do not change implementation. Condition-specific TLDRs: baseline tests check existing contracts; mocked failure checks compare failure inputs with expected retained status; evaluator checks compare literal arithmetic with scoring. Static inspection alone is distinguished from executed evidence. No visual run is generated; a text result table is the appropriate fallback for software assertions, with no temporal model trajectory.

Publish a source-pinned verdict and minimal repairs in this owned review directory. Real transport, credentials, current pricing, machine allocation and live reporting are outside these offline checks and remain launch-owner obligations.
