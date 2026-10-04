"""HTTP model adapter for capture-memory: a policy with the same signature as sim.scripted_policy.

NOT RUN. No endpoint is configured, no key is read unless `--backend http` is chosen explicitly, and the
adapter refuses to start without a positive dollar cap and explicit token prices (same guard rails as
researchers/dmarz/notes/discussion-dose/src/providers.py). Standard library only.

The prompt gives the agent only what the scripted policy sees: the words it heard from its last L partners
(oldest first), and its two options. The pull h of the scripted policy is NOT in the prompt; for a model the
label prior comes from the model itself, which is why the original word alternates with task parity
(sim.task) and why the W2_OUTSIDE pair would have to be chosen from a fitted (beta, h) map, not from cfg.
Mapping this adapter onto design.yaml's h_inside / h_outside is a pre-step for a paid run, not done here.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import sim

SYSTEM = ("You are one agent in a group that is agreeing on a name. You will see the names your recent partners "
          "used. Reply with exactly one of the two allowed names and nothing else.")


class ModelFailure(Exception):
    pass


class HTTPPolicy:
    """Chat-completions style endpoint. Call budget, byte budget and dollar reservation are enforced locally."""

    def __init__(self, model: str, max_calls: int, max_output_tokens: int = 8, timeout: int = 30,
                 max_cost_usd: float = 0.0, input_usd_per_million=None, output_usd_per_million=None,
                 base_url: str | None = None):
        self.model = model
        self.base = (base_url or os.environ.get("SWARM_MODEL_BASE_URL", "")).rstrip("/")
        self.key = os.environ.get("SWARM_MODEL_API_KEY", "")
        if not self.base or not self.model:
            raise ModelFailure("model endpoint and model id required")
        if not (self.base.startswith("https://") or self.base.startswith("http://127.0.0.1:")
                or self.base.startswith("http://localhost:")):
            raise ModelFailure("HTTPS or loopback endpoint required")
        if not max_cost_usd > 0 or input_usd_per_million is None or output_usd_per_million is None:
            raise ModelFailure("positive dollar cap and explicit token prices required")
        self.max_calls, self.calls = max_calls, 0
        self.max_output_tokens, self.timeout = max_output_tokens, timeout
        self.max_cost_usd, self.reserved_usd = max_cost_usd, 0.0
        self.in_rate, self.out_rate = input_usd_per_million, output_usd_per_million

    def __call__(self, m: float, cfg: dict, draw: float, ctx: dict) -> int:
        """`m` and `draw` are ignored: the model sees the memory words, not the magnetisation.
        The caller must put the agent's memory list under ctx["mem"] before calling."""
        words = ctx["task"]["words"]
        heard = [words[w] for w in ctx["mem"]]
        allowed = sorted(words.values())                       # alphabetical, so the order is not a hint
        user = (f"Allowed names: {allowed[0]}, {allowed[1]}.\n"
                f"Names your last {len(heard)} partners used, oldest first: {', '.join(heard) or '(none yet)'}.\n"
                "Which name do you use now?")
        text = self._complete(user).strip().strip('."\'').lower()
        ctx["calls"] = ctx.get("calls", 0) + 1
        for code, w in words.items():
            if text == w:
                return code
        raise ModelFailure(f"unparseable reply {text!r}")

    def _complete(self, user: str) -> str:
        if self.calls >= self.max_calls:
            raise ModelFailure("call budget exhausted")
        body = {"model": self.model, "temperature": 0.7, "max_tokens": self.max_output_tokens,
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
        raw = json.dumps(body).encode()
        reservation = ((len(raw) + 256) * self.in_rate + self.max_output_tokens * self.out_rate) / 1_000_000
        if self.reserved_usd + reservation > self.max_cost_usd:
            raise ModelFailure("dollar reservation exhausted")
        self.reserved_usd += reservation
        self.calls += 1
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        req = urllib.request.Request(self.base + "/chat/completions", data=raw, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                resp = json.loads(r.read(200_000))
            return resp["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            raise ModelFailure(f"provider HTTP {e.code}") from None
        except Exception as e:  # noqa: BLE001
            raise ModelFailure("provider " + type(e).__name__) from None


def build(backend: str):
    """Return (policy, backend_name). 'scripted' costs nothing; 'http' needs SWARM_MODEL_CONFIG (JSON)."""
    if backend == "scripted":
        return sim.scripted_policy, "scripted"
    if backend != "http":
        raise ModelFailure(f"unknown backend {backend}")
    cfg = json.loads(os.environ.get("SWARM_MODEL_CONFIG", "{}"))
    allowed = {"model", "max_calls", "max_output_tokens", "timeout", "max_cost_usd",
               "input_usd_per_million", "output_usd_per_million"}
    if set(cfg) - allowed:
        raise ModelFailure("unknown model config fields")
    return HTTPPolicy(**cfg), "http:" + cfg.get("model", "?")
