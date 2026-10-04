# Validation and publication review

Date: 2026-10-03. Scope: this methods/tooling contribution and its new canonical source records. The original standalone guide was adapted to swarm-dynamics-lab's ownership, citation, research-gate and generated-data conventions.

## Local checks

Run `PYTHONDONTWRITEBYTECODE=1 python3 5-experiments/toolkit/agent-experiments/scripts/validate.py` from the repository root. It executes 960 scripted worlds twice, verifies 12,480 events per execution, and checks pairing, score replay, reset isolation, known-answer behavior, invalid-config rejection, integrity detection, overwrite rejection and local Markdown links. The compact reference summary is retained; full traces are regenerated under ignored `data/`.

The first standalone version was checked on Python 3.14.5. The contribution adds a Python 3.12 CI check. Exact-byte replay is tested within a runtime, not claimed across arbitrary Python versions. No model provider, network call, credential or paid action is used by the harness or its tests.

Repository checks: `scripts/lab.py check`, source metadata verification for added records, and `.flightdeck/fd.py check --strict .`. The initial repository baseline had zero errors and five unrelated unresolved-citation warnings; this contribution does not claim to fix those warnings. No generated dashboard, existing source body, survey gate or artifact manifest is edited.

## Secret and privacy review

Publication is limited to explicitly staged text/code/configuration files. Full generated traces, original machine-specific manifests, local filesystem paths, private project handoffs and unrelated workspace files are excluded. Templates use placeholder identifiers and empty credential aliases, never credential values. Primary-source author names are public bibliographic metadata.

Before publication, scan the exact file set with Gitleaks using complete redaction and review for home-directory paths, credential files, signed URLs, authorization headers and sensitive context. Scanner output must remain redacted; only rule names, counts and file paths are suitable for diagnostics. A clean scan cannot prove the absence of every possible secret, so it complements explicit file selection and content review. See the researcher's session log for the executed checks and publication result.

## Limits

This is teaching and planning infrastructure, not production experiment software. Provider adapters, distributed failure recovery, hostile-code containment, general JSON Schema validation and real-model statistical power remain project-specific work. Reference-summary differences between programmed policies do not establish LLM effects. The reading guide is not a gate-passing survey, and conservative new source records are marked `abstract` rather than claiming full reads.
