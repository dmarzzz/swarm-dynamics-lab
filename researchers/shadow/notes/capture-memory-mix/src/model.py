"""Batched HTTP model policy for capture-memory-mix, with a hard dollar cap.

Same signature as sim.scripted_policy: policy(batch, cfg, ctx) -> list of P(original), one per honest agent that
heard a word this round. The whole round is issued concurrently (decisions are simultaneous by design).

P(original) is read from the FIRST-TOKEN log-probabilities of the two allowed words (every word in sim.WORDS
starts with a distinct letter), renormalised over the two words, the cached-policy construction of
flint-2026-group at temperature 1 (de-marzo-2026-conformity fits the same object). The agent's word is then
ORIG iff its per-round uniform draw < P(original), so the swarm's randomness stays keyed to (task, seed, round)
and arms stay paired. If the two words carry less than `min_mass` of the first-token mass the call is counted
in ctx["low_mass"] and the sampled completion decides; if that matches neither word the episode is invalid.

Guard rails (never relaxed):
- refuses to build without SWARM_MODEL_CONFIG carrying a positive max_cost_usd, and clamps that at HARD_CAP_USD;
- a spend ledger on disk (results/spend-ledger.json) carries actual provider-reported cost across processes
  and restarts, so parallel workers share ONE cap;
- the key is read from the file named in SWARM_MODEL_KEY_FILE (default ~/.moltbot/secrets/openrouter.key),
  never from the environment, never logged;
- every request reserves a worst-case amount before it is sent; the reservation is replaced by the provider's
  reported cost when the response arrives; a request that would exceed the cap raises before sending.
"""
from __future__ import annotations

import fcntl
import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sim

HARD_CAP_USD = 5.0                                     # the goal's cap; the config cannot raise it
ROOT = Path(__file__).resolve().parent.parent
SYSTEM = ("You are one of several agents playing a coordination game. In each round you are paired with another agent and "
          "you both say a name; you score a point when you say the same name as your partner. You will be shown the names "
          "your recent partners said. Reply with exactly one of the two allowed names and nothing else.")


class ModelFailure(Exception):
    pass


class Ledger:
    """Shared spend ledger: {"spent_usd": float, "calls": int, "by_model": {...}}; locked for each update."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({"spent_usd": 0.0, "calls": 0, "by_model": {}}))

    def add(self, model: str, usd: float, calls: int) -> float:
        with open(self.path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            d = json.load(f)
            d["spent_usd"] = round(d["spent_usd"] + usd, 8)
            d["calls"] += calls
            m = d["by_model"].setdefault(model, {"usd": 0.0, "calls": 0})
            m["usd"] = round(m["usd"] + usd, 8)
            m["calls"] += calls
            f.seek(0); f.truncate(); json.dump(d, f)
            return d["spent_usd"]

    def spent(self) -> float:
        with open(self.path) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            return json.load(f)["spent_usd"]


class HTTPPolicy:
    def __init__(self, model: str, max_cost_usd: float, max_calls: int = 2_000_000, timeout: int = 60,
                 concurrency: int = 24, min_mass: float = 0.5, input_usd_per_million: float = 0.5,
                 output_usd_per_million: float = 1.0, base_url: str = "https://openrouter.ai/api/v1",
                 provider_order=None, ledger: str | None = None, retries: int = 3):
        if not max_cost_usd > 0:
            raise ModelFailure("positive dollar cap required")
        if not base_url.startswith("https://"):
            raise ModelFailure("HTTPS endpoint required")
        keyfile = os.environ.get("SWARM_MODEL_KEY_FILE", os.path.expanduser("~/.moltbot/secrets/openrouter.key"))
        self.key = Path(keyfile).read_text().strip()
        if not self.key:
            raise ModelFailure("empty key file")
        self.model, self.base = model, base_url.rstrip("/")
        self.cap = min(float(max_cost_usd), HARD_CAP_USD)
        self.max_calls, self.calls = max_calls, 0
        self.timeout, self.pool = timeout, ThreadPoolExecutor(max_workers=concurrency)
        self.min_mass, self.retries = min_mass, retries
        self.in_rate, self.out_rate = input_usd_per_million, output_usd_per_million
        self.provider_order = provider_order
        self.ledger = Ledger(Path(ledger) if ledger else ROOT / "results" / "spend-ledger.json")
        self.reserved = 0.0
        self.spent_session = 0.0

    # ---- prompt
    def prompt(self, ag, words: dict, flip: bool = False) -> str:
        """The allowed-name order alternates per call (caller passes flip), so position is not a hint."""
        heard = [words[w] for w in ag.mem]
        allowed = sorted(words.values())
        if flip:
            allowed = allowed[::-1]
        return (f"Allowed names: {allowed[0]}, {allowed[1]}.\n"
                f"Names your last {len(heard)} partners said, oldest first: {', '.join(heard) or '(none yet)'}.\n"
                "Which name do you say now?")

    # ---- one request
    def _request(self, user: str) -> dict:
        body = {"model": self.model, "temperature": 1.0, "max_tokens": 4, "logprobs": True, "top_logprobs": 20,
                "usage": {"include": True}, "provider": {"require_parameters": True},
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
        if self.provider_order:
            body["provider"]["order"] = self.provider_order
        raw = json.dumps(body).encode()
        est = ((len(raw) / 3 + 64) * self.in_rate + 8 * self.out_rate) / 1e6      # generous worst case
        if self.ledger.spent() + self.reserved + est > self.cap:
            raise ModelFailure("dollar cap reached")
        if self.calls >= self.max_calls:
            raise ModelFailure("call budget exhausted")
        self.reserved += est
        self.calls += 1
        req = urllib.request.Request(self.base + "/chat/completions", data=raw, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.key,
            "HTTP-Referer": "https://github.com/dmarzzz/swarm-lab", "X-Title": "swarm-lab capture-memory-mix"})
        last = None
        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    resp = json.loads(r.read(400_000))
                break
            except urllib.error.HTTPError as e:
                last = f"provider HTTP {e.code}"
                if e.code in (400, 401, 402, 403):
                    break
                time.sleep(1.5 * (attempt + 1))
            except Exception as e:  # noqa: BLE001
                last = "provider " + type(e).__name__
                time.sleep(1.5 * (attempt + 1))
        else:
            resp = None
        if resp is None or "choices" not in resp:
            self.reserved -= est
            self.ledger.add(self.model, est, 1)          # a failed request may still have cost; charge the estimate
            raise ModelFailure(last or "provider error")
        cost = float((resp.get("usage") or {}).get("cost") or est)
        self.reserved -= est
        self.spent_session += cost
        self.ledger.add(self.model, cost, 1)
        return resp

    @staticmethod
    def _mass(resp: dict, words: dict) -> tuple[dict, str]:
        """First-token probability mass per word (by initial letter, case-insensitive, leading space stripped)."""
        ch = resp["choices"][0]
        content = (ch["message"]["content"] or "").strip().strip('."\'').lower()
        lp = ch.get("logprobs") or {}
        toks = (lp.get("content") or [{}])[0].get("top_logprobs") or []
        mass = {code: 0.0 for code in words}
        for t in toks:
            s = (t.get("token") or "").strip().lower()
            if not s:
                continue
            for code, w in words.items():
                if w.startswith(s) or s.startswith(w):
                    mass[code] += 2.718281828459045 ** float(t["logprob"])
                    break
        return mass, content

    def one(self, ag, words: dict, ctx: dict, flip: bool = False) -> float:
        resp = self._request(self.prompt(ag, words, flip))
        mass, content = self._mass(resp, words)
        tot = mass[sim.ORIG] + mass[sim.ATK]
        if tot >= self.min_mass:
            return mass[sim.ORIG] / tot
        ctx["low_mass"] = ctx.get("low_mass", 0) + 1
        for code, w in words.items():
            if content == w:
                return 1.0 if code == sim.ORIG else 0.0
        raise ModelFailure(f"unparseable reply {content!r} (two-word mass {tot:.2f})")

    def __call__(self, batch: list, cfg: dict, ctx: dict) -> list:
        words = ctx["task"]["words"]
        if not batch:
            return []
        rnd = ctx.get("round", 0)
        futs = [self.pool.submit(self.one, ag, words, ctx, (rnd + i) % 2 == 1) for i, ag in enumerate(batch)]
        out = [f.result() for f in futs]           # raises the first ModelFailure: the episode is recorded invalid
        ctx["calls"] = ctx.get("calls", 0) + len(batch)
        ctx["cost_usd"] = self.spent_session
        return out


def build(backend: str):
    if backend == "scripted":
        return sim.scripted_policy, "scripted"
    if backend != "http":
        raise ModelFailure(f"unknown backend {backend}")
    cfg = json.loads(os.environ.get("SWARM_MODEL_CONFIG", "{}"))
    allowed = {"model", "max_cost_usd", "max_calls", "timeout", "concurrency", "min_mass",
               "input_usd_per_million", "output_usd_per_million", "base_url", "provider_order", "ledger", "retries"}
    if set(cfg) - allowed:
        raise ModelFailure("unknown model config fields")
    if "model" not in cfg or "max_cost_usd" not in cfg:
        raise ModelFailure("model and max_cost_usd required")
    return HTTPPolicy(**cfg), "http:" + cfg["model"]
