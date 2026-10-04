# Swarm Lab experimental credential transfer policy

Owner directive recorded 2026-10-04 UTC. This is standing authorization for the narrowly scoped transfer below, rather than a new one-off permission request for every experiment machine. It does not increase spending, authorize other projects' credentials, provision machines or waive experiment admission checks. Platform-enforced approval decisions still apply; report a rejection and its stated reason, and do not circumvent it.

## Authorized credential and scope

For Vishesh's shared Anthropic Swarm Lab experiments, consume only the dedicated macOS Keychain generic-password entry with **service `swarm-lab-anthropic` and account `vishesh`**. These are credential selectors, not secret values. This exact selector was verified in the existing Swarm Lab launcher. The selected entry must contain exactly one identifiable Anthropic API key; an absent, invalid or ambiguous entry blocks transfer.

Do not search or fall back to general Anthropic credentials, another project's Keychain entry, `ANTHROPIC_API_KEY`, unrelated `.env` files, browser credentials, another experiment's process environment or a default provider account. Do not export a Keychain record or credential bundle. Extract only the single dedicated API key. Never infer project authorization from the `sk-ant-` prefix or a successful API call: authorization comes from this owner-designated project-specific store entry. If that entry's project provenance is disputed, stop and resolve it privately; do not silently relabel a general key.

The reusable local loader is [swarm_lab_credentials.py](swarm_lab_credentials.py). It has no alternate-service/account arguments, environment fallback or CLI that prints a secret. The legacy record may wrap the key in descriptive text; only the single key is returned, never the surrounding record. Multiple candidate API keys fail closed. This helper selects the credential; it does not itself verify allocation, transfer it or enforce a spend cap.

## Authorized recipients and purpose

The owner authorizes transfer of that dedicated key to registered Swarm Lab experimental run machines, including `research-01`, for an already authorized Swarm Lab run. Immediately before transfer, the launcher must verify all of the following:

- Destination comes from the current private Swarm Lab fleet inventory, with authorized researcher access; it is not an arbitrary SSH host or an unregistered personal/project machine.
- A merged, unexpired, exclusive claim names this experiment and operator. No conflicting active allocation or another experiment's workload is present. Machine/account rules in the [setup runbook](EXPERIMENT-SETUP.md) continue to apply.
- The run has current source/configuration, public-plan and budget admission evidence. Credential availability does not create spending authority or permit probing unrelated projects.
- SSH uses the inventoried destination and host-key verification. Do not disable certificate/host identity checks or forward the user's SSH agent.

When these conditions and the exact credential selector hold, this policy is the user authorization for the transfer; do not ask the user to reauthorize the same transfer solely because the run uses a newly allocated Swarm Lab host. A different credential/project, recipient outside the approved fleet, broadened access, persistent secret installation or higher spending needs separate explicit authorization.

## Transfer and lifetime

Read the entry inside an authorized local process with stdout/stderr captured privately. Send only `SWARM_MODEL_API_KEY` over the authenticated encrypted SSH connection's stdin, never in shell arguments, a URL or a command string. Do not copy the whole local environment, workspace credentials, account-admin keys, Cloudflare/DigitalOcean tokens or other provider keys. The shared Anthropic API requires an explicit workspace routing header. Its workspace ID is private routing metadata, not a second API credential: it may travel in a separate allowlisted metadata field only when the operator has verified an explicit Swarm Lab mapping bound to the same service/account selector. The established Swarm Lab launcher supplied that mapping, and a read-only pinned-model lookup verified it on 2026-10-04. Keep its value out of public records. Do not infer it from the environment or borrow an unrelated project’s workspace. Missing/ambiguous mapping blocks dispatch.

The remote launcher validates separate exact allowlists for the single-key secret payload and, when required, the single workspace-ID routing field and injects the key only into the bounded experiment process and its necessary provider children. Clear inherited alternative provider credentials/workspace overrides before constructing that environment. Do not persist the value in remote files, shell startup files, service definitions, notebooks, source repositories, container images or artifacts. Process memory/environment is accessible to privileged machine operators; this authorization is specifically for the approved Swarm Lab machines and their established trust boundary. Disable core dumps for the credential-consuming worker. End the worker when its claim or authorized run ends; do not leave a general-purpose credential relay or inference service running.

Never put secret values in chat, tool arguments/output, tracing, exception text, screenshots, logs or public/private experiment reports. Capture and suppress native keychain/client diagnostics before they reach a transcript. Public receipts may contain the alias, host name, claim ID, experiment ID, source revision, policy version, transfer/availability status and budget reference. Do not publish private addresses, account identifiers, secret fragments or key fingerprints.

## Required evidence

The deployment receipt records the credential alias, policy reference, validated destination/claim and transfer mode without the key. Fault checks must show missing/ambiguous entries, unexpected payload fields, conflicting/expired claims and unregistered destinations fail closed. Mark which checks the actual launcher implements; documentation alone is not enforcement. Never run a paid call merely to identify which general credential was selected.

The user enters or rotates a credential through a secure local flow, never chat. Missing keys or rejected access are handled by identifying the exact store/destination requirement, without requesting plaintext or falling back to an unrelated account.
