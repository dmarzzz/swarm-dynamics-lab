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
  and restarts; unresolved reservations are included, so parallel workers share ONE cap;
- the key is read from the file named in SWARM_MODEL_KEY_FILE (default ~/.moltbot/secrets/openrouter.key),
  never from the environment, never logged;
- every request reserves a worst-case amount before it is sent; the reservation is replaced by the provider's
  reported cost when the response arrives; a request that would exceed the cap raises before sending.
"""
from __future__ import annotations

import fcntl
import json
import math
import os
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sim

HARD_CAP_USD = 10.0                                    # raised from 5 at 05:45Z (dmarz OK, up to 20); the config cannot raise it
ROOT = Path(__file__).resolve().parent.parent
SYSTEM = ("You are one of several agents playing a coordination game. In each round you are paired with another agent and "
          "you both say a name; you score a point when you say the same name as your partner. You will be shown the names "
          "your recent partners said. Reply with exactly one of the two allowed names and nothing else.")


class ModelFailure(Exception):
    pass


class NoCredentialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ModelFailure("credential-bearing requests must not follow redirects")


class Ledger:
    """Shared liability ledger. spent_usd includes actual costs and unresolved
    reservations; calls counts dispatched/reserved attempts. Old aggregate fields
    are preserved. All live workers must use this reservation-aware runtime.
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # A stable sidecar serializes constructors even before the ledger exists.
        # Exclusive creation never truncates an existing spend/reservation file.
        with open(str(self.path) + ".init.lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                with self.path.open("x") as ledger:
                    json.dump({"spent_usd": 0.0, "calls": 0, "by_model": {}}, ledger)
                    ledger.flush()
                    os.fsync(ledger.fileno())
            except FileExistsError:
                pass

    def add(self, model: str, usd: float, calls: int) -> float:
        if isinstance(usd, bool) or not isinstance(usd, (int, float)) or not math.isfinite(usd) or usd < 0:
            raise ModelFailure("ledger cost must be finite and nonnegative")
        if isinstance(calls, bool) or not isinstance(calls, int) or calls < 0:
            raise ModelFailure("ledger calls must be a nonnegative integer")
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

    @staticmethod
    def _write_locked(stream, data):
        stream.seek(0)
        stream.truncate()
        json.dump(data, stream)
        stream.flush()
        os.fsync(stream.fileno())

    def reserve(self, model: str, usd: float, cap: float) -> str:
        """Charge durable liability before dispatch, in the same lock as admission."""
        if not math.isfinite(usd) or usd < 0 or not math.isfinite(cap) or cap <= 0:
            raise ModelFailure("invalid reservation amount or cap")
        with self.path.open("r+") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            d = json.load(stream)
            if not math.isfinite(d["spent_usd"]) or d["spent_usd"] < 0:
                raise ModelFailure("invalid existing spend")
            if d.get("reservation_breached") or d["spent_usd"] + usd > cap:
                raise ModelFailure("dollar cap reached or reservation previously breached")
            ident = uuid.uuid4().hex
            d.setdefault("reservations", {})[ident] = {"model": model, "usd": usd}
            d["spent_usd"] += usd
            d["calls"] += 1
            m = d["by_model"].setdefault(model, {"usd": 0.0, "calls": 0})
            m["usd"] += usd
            m["calls"] += 1
            self._write_locked(stream, d)
            return ident

    def settle(self, ident: str, usd: float):
        """Only a known reservation may release liability against a valid receipt."""
        if isinstance(usd, bool) or not isinstance(usd, (int, float)) or not math.isfinite(usd) or usd < 0:
            raise ModelFailure("invalid settlement cost; reservation retained")
        with self.path.open("r+") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            d = json.load(stream)
            reservation = d.get("reservations", {}).pop(ident, None)
            if reservation is None:
                raise ModelFailure("unknown or already settled reservation")
            delta = usd - reservation["usd"]
            d["spent_usd"] += delta
            d["by_model"][reservation["model"]]["usd"] += delta
            breached = usd > reservation["usd"]
            if breached:
                d["reservation_breached"] = True
            self._write_locked(stream, d)
        if breached:
            raise ModelFailure("provider cost exceeded reservation; future dispatch blocked")

    def spent(self) -> float:
        with open(self.path) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            return json.load(f)["spent_usd"]


class HTTPPolicy:
    def __init__(self, model: str, max_cost_usd: float, max_calls: int = 2_000_000, timeout: int = 60,
                 concurrency: int = 24, min_mass: float = 0.5, input_usd_per_million: float = 0.5,
                 output_usd_per_million: float = 1.0, base_url: str = "https://openrouter.ai/api/v1",
                 provider_order=None, ledger: str | None = None, retries: int = 3, call_log: str | None = None,
                 logit_temperature: float = 1.0, mode: str = "logprobs"):
        if not math.isfinite(max_cost_usd) or not max_cost_usd > 0:
            raise ModelFailure("finite positive dollar cap required")
        for rate in (input_usd_per_million, output_usd_per_million):
            if isinstance(rate, bool) or not math.isfinite(rate) or rate < 0:
                raise ModelFailure("prices must be finite and nonnegative")
        if base_url.rstrip("/") != "https://openrouter.ai/api/v1":
            raise ModelFailure("this adapter only authorizes the OpenRouter API endpoint")
        self._opener = urllib.request.build_opener(NoCredentialRedirect())
        keyfile = os.environ.get("SWARM_MODEL_KEY_FILE", os.path.expanduser("~/.moltbot/secrets/openrouter.key"))
        self.key = Path(keyfile).read_text().strip()
        if not self.key:
            raise ModelFailure("empty key file")
        self.model, self.base = model, base_url.rstrip("/")
        self.cap = min(float(max_cost_usd), HARD_CAP_USD)
        self.max_calls, self.calls = max_calls, 0
        self.timeout, self.pool = timeout, ThreadPoolExecutor(max_workers=concurrency)
        # Keep the legacy config parameter readable, but never retry a dispatch:
        # a timeout/5xx may already have incurred cost or produced an outcome.
        self.min_mass, self.retries = min_mass, 1
        self.in_rate, self.out_rate = input_usd_per_million, output_usd_per_million
        self.provider_order = provider_order
        # Decoding temperature applied to the two-word first-token logits (providers report logprobs at T = 1).
        # Restricted to the two allowed words this is exactly sampling at temperature T; de-nobili-2026-microscopic
        # uses decoding temperature as the control parameter of an LLM naming game. Recorded in every episode.
        self.T = float(logit_temperature)
        # mode "logprobs": P(original) from first-token mass (default). mode "sample": no logprobs requested, the
        # sampled completion IS the agent's word (P = 1 or 0), for models whose providers return no logprobs. In sample
        # mode the recovery-phase randomness comes from the provider, so arms are paired only through the shared prefix.
        if mode not in ("logprobs", "sample"):
            raise ModelFailure("mode must be logprobs or sample")
        self.mode = mode
        self.ledger = Ledger(Path(ledger) if ledger else ROOT / "results" / "spend-ledger.json")
        self.spent_session = 0.0
        self._lock = threading.Lock()
        self.call_log = Path(call_log) if call_log else None   # per-call (memory counts -> P) for policy extraction
        if self.call_log:
            self.call_log.parent.mkdir(parents=True, exist_ok=True)

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
        body = {"model": self.model, "temperature": self.T if self.mode == "sample" else 1.0, "max_tokens": 6,
                "usage": {"include": True},
                "provider": {"max_price": {"prompt": self.in_rate, "completion": self.out_rate, "request": 0}},
                "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
        if self.mode == "logprobs":
            body.update({"logprobs": True, "top_logprobs": 20})
            body["provider"]["require_parameters"] = True
        if self.provider_order:
            body["provider"]["order"] = self.provider_order
        raw = json.dumps(body).encode()
        # Treat every request byte as a token, plus framing allowance. Reserve
        # twice the bounded prompt rate for cache-write variation, and all output
        # tokens (with two extra). Provider routing enforces these price ceilings.
        est = ((len(raw) + 2048) * 2 * self.in_rate + 8 * self.out_rate) / 1e6
        with self._lock:
            if self.calls >= self.max_calls:
                raise ModelFailure("call budget exhausted")
            reservation = self.ledger.reserve(self.model, est, self.cap)
            self.calls += 1
        req = urllib.request.Request(self.base + "/chat/completions", data=raw, headers={
            "Content-Type": "application/json", "Authorization": "Bearer " + self.key,
            "HTTP-Referer": "https://github.com/dmarzzz/swarm-lab", "X-Title": "swarm-lab capture-memory-mix"})
        last, resp = None, None
        try:
            with self._opener.open(req, timeout=self.timeout) as r:
                resp = json.loads(r.read(400_000))
        except urllib.error.HTTPError as e:
            try:
                detail = e.read(600).decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                detail = ""
            last = f"provider HTTP {e.code} {detail[:200]}"
        except Exception as e:  # noqa: BLE001
            last = "provider " + type(e).__name__
        if resp is None or "choices" not in resp:
            # Unknown outcomes retain their durable pre-dispatch liability.
            raise ModelFailure(last or "provider error")
        reported_cost = (resp.get("usage") or {}).get("cost")
        if reported_cost is None:
            cost = est
        elif (isinstance(reported_cost, bool) or not isinstance(reported_cost, (int, float))
              or not math.isfinite(reported_cost) or reported_cost < 0):
            raise ModelFailure("invalid provider cost; estimate retained")
        else:
            cost = float(reported_cost)
        if reported_cost is not None:
            self.ledger.settle(reservation, cost)
        with self._lock:
            self.spent_session += cost
        resp["_cost"] = cost
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
        with self._lock:
            ctx["cost_usd"] = ctx.get("cost_usd", 0.0) + resp["_cost"]     # per-episode cost, not session total
        mass, content = self._mass(resp, words)
        tot = mass[sim.ORIG] + mass[sim.ATK]
        p = None
        if self.mode == "sample":
            c = content.strip('*` ').lower()
            for code, w in words.items():
                if c.startswith(w):
                    p = 1.0 if code == sim.ORIG else 0.0
            if p is None:
                ctx["low_mass"] = ctx.get("low_mass", 0) + 1
                raise ModelFailure(f"unparseable reply {content!r}")
            tot = 1.0
        elif tot >= self.min_mass:
            if self.T == 1.0:
                p = mass[sim.ORIG] / tot
            else:
                lo, la = math.log(max(mass[sim.ORIG], 1e-12)), math.log(max(mass[sim.ATK], 1e-12))
                p = 1.0 / (1.0 + math.exp((la - lo) / self.T))
        if self.call_log:
            n_o = sum(1 for w in ag.mem if w == sim.ORIG)
            last = [w for w in ag.mem[-5:]]
            with self.call_log.open("a") as f:
                f.write(json.dumps({"task": ctx["task"]["task_id"], "round": ctx.get("round"), "arm": ctx.get("arm"),
                                    "kind": getattr(ag, "kind", None), "L": ag.L, "n": len(ag.mem), "n_orig": n_o,
                                    "last5_orig": sum(1 for w in last if w == sim.ORIG), "flip": flip,
                                    "p_orig": None if p is None else round(p, 4), "mass": round(tot, 4),
                                    "provider": resp.get("provider")}) + "\n")
        if p is not None:
            return p
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
        return out


def build(backend: str):
    if backend == "scripted":
        return sim.scripted_policy, "scripted"
    if backend != "http":
        raise ModelFailure(f"unknown backend {backend}")
    cfg = json.loads(os.environ.get("SWARM_MODEL_CONFIG", "{}"))
    allowed = {"model", "max_cost_usd", "max_calls", "timeout", "concurrency", "min_mass",
               "input_usd_per_million", "output_usd_per_million", "base_url", "provider_order", "ledger", "retries", "call_log",
               "logit_temperature", "mode"}
    if set(cfg) - allowed:
        raise ModelFailure("unknown model config fields")
    if "model" not in cfg or "max_cost_usd" not in cfg:
        raise ModelFailure("model and max_cost_usd required")
    return HTTPPolicy(**cfg), ("http:" + cfg["model"] + (f"@T{cfg['logit_temperature']}" if cfg.get("logit_temperature", 1.0) != 1.0 else "")
                               + (":sample" if cfg.get("mode") == "sample" else ""))
