# Backend plan and deferred Jev comparison

Owner decision, 2026-10-03: use **Laya locally now**, then swap in **Jev through OpenRouter once an OpenRouter API key is securely configured**. Laya is a separate open model; it is not Jev's weights or a replication of Jev's training.

Current pilot pins Laya source `2e4d9c87e8b1621deb344eac7de5c7258f32f849` (package 0.3.26), English checkpoint `convaiinnovations/laya`, revision `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851`. Use one explicit checkpoint, no automatic model routing. CPU inference, two torch threads, safetensors, no remote model code. The run records installed dependency versions. Model artifacts stay outside git.

Before the later Jev run: verify OpenRouter's then-current Jev model ID, provider route, typed-decision support, response semantics, data policy and pricing against its official documentation. Do not assume the native TypeSafe `systemone` endpoint is interchangeable with OpenRouter chat completions. Implement and qualify that adapter separately. Pin the route/model and refuse unrequested fallback to another model. Consume the key from an approved local credential store; never put it in a prompt, repo, argument, screenshot or report.

Freeze fixtures, prompts, option order, deadlines, stopping policies and analysis before switching. Backend is a declared factor: never pool Laya and Jev outcomes or describe Laya results as Jev results. Record tokens, latency, invalid outputs and actual cost for both; requalify clean-task competence for Jev. No hosted calls are currently enabled. Initial hosted qualification spending ceiling remains $5, subject to verified route pricing and a conservative request reservation ledger.

Sources inspected 2026-10-03: [Laya source](https://github.com/NandhaKishorM/laya), its loader/revision implementation, and [TypeSafe model specifications](https://docs.typesafe.ai/models). The latter describes native Jev, not an OpenRouter route. No claim of verified OpenRouter availability is made here.
