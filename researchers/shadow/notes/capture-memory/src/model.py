"""HTTP model adapter for capture-memory: a policy with the same signature as sim.scripted_policy.

No endpoint is configured and no key is read unless `--backend http` is chosen explicitly, and the adapter
refuses to start without a positive dollar cap, a positive call cap and explicit token prices (same guard
rails as researchers/dmarz/notes/discussion-dose/src/providers.py). Standard library only.

Budget enforcement (all local, before the request leaves):
- `max_calls`: hard cap on HTTP requests, retries included. Exceeding it raises ModelFailure.
- `max_cost_usd`: before each request the worst-case cost of that request (input bytes/3 + envelope, at
  `input_usd_per_million`, plus `max_output_tokens` at `output_usd_per_million`) is added to a running
  *reservation*; if that would pass the cap the request is refused. After each response the provider's
  `usage` block (prompt/completion tokens and, on OpenRouter, `cost`) is added to the *actual* ledger; if actual
  spend passes the cap the next request is refused too. Reservations are never credited back.
- The budget object is shared across every episode of a worker process (`--budget-file` makes it survive
  restarts), so a stage cannot exceed the cap by being split into many cells.

The prompt gives the agent only what the scripted policy sees: the words it heard from its last L partners
(oldest first), and its two options. The pull h of the scripted policy is NOT in the prompt; for a model the
label prior comes from the model itself, which is why the original word alternates with task parity
(sim.task). Mapping h_inside / h_outside onto a model is a pre-step this adapter does not do.

Parsing (Q0 finding, 2026-10-04: llama-3.1-8b writes 'brusk' for 'brisk' in about 3% of calls, every other
reply was exact): the reply is lowercased and stripped of punctuation. Exact match wins. Otherwise a reply within
edit distance 1 of exactly one allowed word is accepted and counted as `fuzzy_parses`. Otherwise the same prompt
is asked ONCE more (the sample is at temperature 0.7, so the second draw is a fresh decision, not a repair of the
first) and counted as `parse_retries`; if that reply is unparseable too the call raises ModelFailure, the episode
is recorded invalid and is never retried. One further retry exists for transport errors (HTTP 429/5xx, timeouts).
Every retry of either kind counts against both caps.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import sim

SYSTEM = ("You are one agent in a group that is agreeing on a name. You will see the names your recent partners "
          "used. Reply with exactly one of the two allowed names and nothing else.")


class ModelFailure(Exception):
    pass


class Budget:
    """Process-wide ledger: calls, reservations, actual usage from provider `usage` fields. Thread-safe."""

    def __init__(self, max_calls: int, max_cost_usd: float, in_rate: float, out_rate: float, file: str | None = None):
        if not (isinstance(max_calls, int) and max_calls > 0):
            raise ModelFailure("positive integer call cap required")
        if not (isinstance(max_cost_usd, (int, float)) and max_cost_usd > 0):
            raise ModelFailure("positive dollar cap required")
        if in_rate is None or out_rate is None or min(in_rate, out_rate) < 0:
            raise ModelFailure("explicit nonnegative token prices required")
        self.max_calls, self.max_cost_usd, self.in_rate, self.out_rate = max_calls, float(max_cost_usd), in_rate, out_rate
        self.calls = self.retries = self.parse_failures = self.transport_failures = self.usage_missing = 0
        self.fuzzy_parses = self.parse_retries = self.exact_parses = 0
        self.prompt_tokens = self.completion_tokens = 0
        self.reserved_usd = self.actual_usd = self.priced_usd = 0.0
        self.lock = threading.Lock()
        self.file = Path(file) if file else None
        if self.file and self.file.exists():
            self.__dict__.update({k: v for k, v in json.loads(self.file.read_text()).items() if k in self.state()})

    def state(self) -> dict:
        return {k: getattr(self, k) for k in ("calls", "retries", "parse_failures", "transport_failures", "usage_missing",
                                              "exact_parses", "fuzzy_parses", "parse_retries",
                                              "prompt_tokens", "completion_tokens", "reserved_usd", "actual_usd",
                                              "priced_usd", "max_calls", "max_cost_usd")}

    def save(self):
        if self.file:
            self.file.write_text(json.dumps(self.state(), indent=1))

    def reserve(self, body_bytes: int, max_out: int):
        reservation = ((body_bytes / 3 + 64) * self.in_rate + max_out * self.out_rate) / 1_000_000
        with self.lock:
            if self.calls >= self.max_calls:
                raise ModelFailure(f"call budget exhausted ({self.calls}/{self.max_calls})")
            if self.actual_usd >= self.max_cost_usd:
                raise ModelFailure(f"dollar cap reached by actual usage ({self.actual_usd:.4f}/{self.max_cost_usd})")
            if self.reserved_usd + reservation > self.max_cost_usd:
                raise ModelFailure(f"dollar reservation exhausted ({self.reserved_usd:.4f}+{reservation:.6f}/{self.max_cost_usd})")
            self.reserved_usd += reservation
            self.calls += 1

    def settle(self, usage: dict | None):
        with self.lock:
            if not usage:
                self.usage_missing += 1
                return
            pt, ct = int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)
            self.prompt_tokens += pt
            self.completion_tokens += ct
            priced = (pt * self.in_rate + ct * self.out_rate) / 1_000_000
            self.priced_usd += priced
            cost = usage.get("cost")
            self.actual_usd += float(cost) if isinstance(cost, (int, float)) else priced
            if self.calls % 50 == 0:
                self.save()


class HTTPPolicy:
    """Chat-completions style endpoint. One policy object per worker process; the Budget is shared."""
    concurrent = True        # sim.step issues one round's decisions in parallel threads (they are simultaneous by design)

    def __init__(self, model: str, max_calls: int, max_output_tokens: int = 8, timeout: int = 30,
                 max_cost_usd: float = 0.0, input_usd_per_million=None, output_usd_per_million=None,
                 base_url: str | None = None, budget_file: str | None = None, provider: dict | None = None,
                 temperature: float = 0.7):
        self.model = model
        self.base = (base_url or os.environ.get("SWARM_MODEL_BASE_URL", "")).rstrip("/")
        self.key = os.environ.get("SWARM_MODEL_API_KEY", "")
        if not self.base or not self.model:
            raise ModelFailure("model endpoint and model id required")
        if not (self.base.startswith("https://") or self.base.startswith("http://127.0.0.1:")
                or self.base.startswith("http://localhost:")):
            raise ModelFailure("HTTPS or loopback endpoint required")
        self.budget = Budget(max_calls, max_cost_usd, input_usd_per_million, output_usd_per_million, budget_file)
        self.max_output_tokens, self.timeout, self.temperature = max_output_tokens, timeout, temperature
        self.provider = provider          # OpenRouter provider routing, e.g. {"order": [...], "allow_fallbacks": false}
        self.last_raw = None

    # ---- policy signature
    def __call__(self, m: float, cfg: dict, draw: float, ctx: dict) -> int:
        """`m` and `draw` are ignored: the model sees the memory words, not the magnetisation.
        The caller must put the agent's memory list under ctx["mem"] before calling."""
        words = ctx["task"]["words"]
        heard = [words[w] for w in ctx["mem"]]
        allowed = sorted(words.values())                       # alphabetical, so the order is not a hint
        user = (f"Allowed names: {allowed[0]}, {allowed[1]}.\n"
                f"Names your last {len(heard)} partners used, oldest first: {', '.join(heard) or '(none yet)'}.\n"
                "Which name do you use now?")
        for attempt in (0, 1):
            raw, usage, retries = self._complete(user)
            ctx["calls"] = ctx.get("calls", 0) + 1 + retries
            ctx["retries"] = ctx.get("retries", 0) + retries
            if usage:
                ctx["prompt_tokens"] = ctx.get("prompt_tokens", 0) + int(usage.get("prompt_tokens") or 0)
                ctx["completion_tokens"] = ctx.get("completion_tokens", 0) + int(usage.get("completion_tokens") or 0)
                c = usage.get("cost")
                ctx["cost_usd"] = ctx.get("cost_usd", 0.0) + (float(c) if isinstance(c, (int, float)) else 0.0)
            code, kind = self.parse(raw, words)
            if code is not None:
                with self.budget.lock:
                    setattr(self.budget, kind, getattr(self.budget, kind) + 1)
                if kind == "fuzzy_parses":
                    ctx["fuzzy_parses"] = ctx.get("fuzzy_parses", 0) + 1
                return code
            if attempt == 0:
                with self.budget.lock:
                    self.budget.parse_retries += 1
                ctx["parse_retries"] = ctx.get("parse_retries", 0) + 1
        with self.budget.lock:
            self.budget.parse_failures += 1
        ctx["parse_failures"] = ctx.get("parse_failures", 0) + 1
        raise ModelFailure(f"unparseable reply {raw[:40]!r}")

    @staticmethod
    def parse(raw: str, words: dict):
        """(code, 'exact_parses' | 'fuzzy_parses') or (None, None). Fuzzy = edit distance 1 to exactly one word."""
        text = raw.strip().strip('."\'`*\n ').lower()
        for code, w in words.items():
            if text == w:
                return code, "exact_parses"
        near = [code for code, w in words.items() if _edit1(text, w)]
        if len(near) == 1:
            return near[0], "fuzzy_parses"
        return None, None

    # ---- transport
    def _complete(self, user: str):
        body = {"model": self.model, "temperature": self.temperature, "max_tokens": self.max_output_tokens,
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
        if "openrouter.ai" in self.base:
            body["usage"] = {"include": True}
            if self.provider:
                body["provider"] = self.provider
        raw = json.dumps(body).encode()
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = "Bearer " + self.key
        retries = 0
        while True:
            self.budget.reserve(len(raw), self.max_output_tokens)
            req = urllib.request.Request(self.base + "/chat/completions", data=raw, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    resp = json.loads(r.read(200_000))
                usage = resp.get("usage") or {}
                self.budget.settle(usage)
                content = resp["choices"][0]["message"]["content"]
                self.last_raw = content
                return content or "", usage, retries
            except urllib.error.HTTPError as e:
                code = e.code
                try:
                    e.read()
                except Exception:  # noqa: BLE001
                    pass
                with self.budget.lock:
                    self.budget.transport_failures += 1
                if retries < 1 and (code == 429 or code >= 500):
                    retries += 1
                    time.sleep(2.0)
                    continue
                raise ModelFailure(f"provider HTTP {code}") from None
            except ModelFailure:
                raise
            except Exception as e:  # noqa: BLE001
                with self.budget.lock:
                    self.budget.transport_failures += 1
                if retries < 1:
                    retries += 1
                    time.sleep(2.0)
                    continue
                raise ModelFailure("provider " + type(e).__name__) from None


def _edit1(a: str, b: str) -> bool:
    """True if a and b are within one substitution, insertion or deletion of each other (and not equal)."""
    if a == b or abs(len(a) - len(b)) > 1 or not a or not b:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == a:
            return True
    return False


def build(backend: str):
    """Return (policy, backend_name). 'scripted' costs nothing; 'http' needs SWARM_MODEL_CONFIG (JSON)."""
    if backend == "scripted":
        return sim.scripted_policy, "scripted"
    if backend != "http":
        raise ModelFailure(f"unknown backend {backend}")
    cfg = json.loads(os.environ.get("SWARM_MODEL_CONFIG", "{}"))
    allowed = {"model", "max_calls", "max_output_tokens", "timeout", "max_cost_usd",
               "input_usd_per_million", "output_usd_per_million", "budget_file", "provider", "temperature"}
    if set(cfg) - allowed:
        raise ModelFailure("unknown model config fields")
    return HTTPPolicy(**cfg), "http:" + cfg.get("model", "?")
