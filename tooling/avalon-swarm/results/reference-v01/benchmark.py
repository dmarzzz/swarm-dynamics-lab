"""Avalon Swarm v0.1: bounded, synchronous, scripted reference environment.

No third party dependencies, network calls, credentials, or upstream source code.
Agent-visible observations are distinct from evaluator state, but Python is NOT
a security boundary for untrusted policies. See PROTOCOL.md before interpreting.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import random
import statistics
import time
import tracemalloc
from typing import Protocol

SIZES = (100, 200, 500, 1000, 2000)
TEAM_SIZES = (3, 4, 4, 5, 5)
VERSION = "avalon-swarm-0.1"


def rng_for(seed: int, *parts: object) -> random.Random:
    key = json.dumps([VERSION, seed, *parts], separators=(",", ":"))
    return random.Random(int.from_bytes(hashlib.sha256(key.encode()).digest(), "big"))


@dataclass(frozen=True)
class Config:
    n: int = 100
    seed: int = 0
    topology: str = "federated"
    policy: str = "provenance"
    recovery: str = "none"

    def __post_init__(self):
        if self.n not in SIZES:
            raise ValueError(f"n must be one of {SIZES}")
        if self.topology not in ("none", "local", "federated"):
            raise ValueError("unknown topology")
        if self.policy not in ("provenance", "echo", "random"):
            raise ValueError("unknown scripted policy")
        if self.recovery not in ("none", "audit", "repair"):
            raise ValueError("unknown recovery treatment")


@dataclass(frozen=True)
class Claim:
    origin: int
    target: int
    evil_probability: float


@dataclass(frozen=True)
class Observation:
    agent: int
    role: str
    members: tuple[int, ...]
    known_evil: tuple[int, ...] | None
    signal: Claim
    mission: int
    attempt: int
    team: tuple[int, ...]
    history: tuple[tuple[tuple[int, ...], int], ...]
    inbox: tuple[Claim, ...]
    verified: tuple[tuple[int, bool], ...]


class Policy(Protocol):
    def ingest(self, obs: Observation) -> None: ...
    def discuss(self, obs: Observation) -> tuple[Claim, ...]: ...
    def propose(self, obs: Observation, size: int) -> tuple[int, ...]: ...
    def vote(self, obs: Observation) -> bool: ...
    def sabotage(self, obs: Observation) -> bool: ...
    def assassinate(self, obs: Observation) -> int: ...
    def beliefs(self, obs: Observation) -> dict[int, float]: ...


class ScriptedPolicy:
    def __init__(self, seed: int, agent: int, mode: str, recovery: str = "none"):
        self.rng = rng_for(seed, "policy", agent)
        self.mode = mode
        self.recovery = recovery
        self.memory: deque[Claim] = deque(maxlen=32)

    def contradicted(self, claim, obs):
        return any(claim.target == target and (claim.evil_probability >= .5) != evil
                   for target, evil in obs.verified)

    def repair(self, obs):
        if self.recovery == "repair" and obs.role in ("good", "merlin"):
            self.memory = deque((c for c in self.memory if not self.contradicted(c, obs)), maxlen=32)

    def ingest(self, obs):
        self.memory.extend(obs.inbox)
        self.repair(obs)

    def beliefs(self, obs):
        values = {i: [0.4] for i in obs.members}
        seen = set()
        for c in [obs.signal, *self.memory]:
            key = (c.origin, c.target)
            if c.target not in values or (self.mode == "provenance" and key in seen):
                continue
            seen.add(key)
            values[c.target].append(c.evil_probability)
        scores = {i: statistics.mean(v) for i, v in values.items()}
        # Mission outcomes provide weak evidence, not individual guilt labels.
        for team, fails in obs.history:
            for i in team:
                scores[i] = min(.99, max(.01, scores[i] + (.12 if fails else -.08)))
        scores[obs.agent] = float(obs.role in ("evil", "assassin"))
        if obs.known_evil is not None:
            scores = {i: float(i in obs.known_evil) for i in obs.members}
        scores.update({target: float(evil) for target, evil in obs.verified})
        return scores

    def discuss(self, obs):
        signal = obs.signal
        if obs.role in ("evil", "assassin"):
            signal = Claim(obs.agent, signal.target, 1 - signal.evil_probability)
        # Repeated copies retain origin; the controller prevents forged relays.
        candidates = list(dict.fromkeys(self.memory))
        self.rng.shuffle(candidates)
        claims = [signal, *candidates[:3]]
        if self.recovery == "repair" and obs.role in ("good", "merlin"):
            claims = [c for c in claims if not self.contradicted(c, obs)]
        return tuple(claims)

    def propose(self, obs, size):
        scores = self.beliefs(obs)
        members = list(obs.members)
        self.rng.shuffle(members)
        if self.mode != "random":
            members.sort(key=lambda i: scores[i])
        if obs.role in ("evil", "assassin"):
            members.remove(obs.agent)
            members.insert(0, obs.agent)
        return tuple(sorted(members[:size]))

    def vote(self, obs):
        if self.mode == "random":
            return self.rng.random() < .5
        if obs.role in ("evil", "assassin"):
            return any(i in obs.known_evil for i in obs.team)
        scores = self.beliefs(obs)
        return statistics.mean(scores[i] for i in obs.team) < .45

    def sabotage(self, obs):
        return obs.role in ("evil", "assassin")

    def assassinate(self, obs):
        # Deliberately weak baseline; does not model speech-based Merlin discovery.
        return self.rng.choice([i for i in obs.members if i not in obs.known_evil])


class EventLog:
    def __init__(self, path=None):
        self.file = Path(path).open("x") if path else None
        self.digest = "0" * 64
        self.count = 0

    def emit(self, event_type, **payload):
        event = {"seq": self.count, "kind": event_type, "payload": payload, "previous": self.digest}
        body = json.dumps(event, sort_keys=True, separators=(",", ":"))
        self.digest = hashlib.sha256(body.encode()).hexdigest()
        if self.file:
            self.file.write(json.dumps({**event, "hash": self.digest}, sort_keys=True) + "\n")
        self.count += 1

    def close(self):
        if self.file:
            self.file.close()


class World:
    def __init__(self, config: Config, log: EventLog | None = None):
        self.config = config
        self.log = log or EventLog()
        self.roles = []
        self.members = []
        self.signals = []
        self.policies: list[Policy] = []
        self.inboxes = [() for _ in range(config.n)]
        self.history = [[] for _ in range(config.n // 10)]
        self.deliveries = 0
        self.claim_deliveries = 0
        self.discussion_calls = 0
        self.decision_calls = 0
        self.rejections = 0
        self.forced = 0
        self.ticks = 0
        self.verified = [[] for _ in range(config.n // 10)]
        self.detection_origins = set()
        self.contradiction_exposures = 0
        self.recovery_measurements = []
        for pod in range(config.n // 10):
            roles = ["merlin", "assassin", *(["evil"] * 3), *(["good"] * 5)]
            rng_for(config.seed, "roles", pod).shuffle(roles)
            self.roles.extend(roles)
            self.members.append(tuple(range(pod * 10, pod * 10 + 10)))
        for i in range(config.n):
            target = (i + 10) % config.n
            truth = self.roles[target] in ("evil", "assassin")
            correct = rng_for(config.seed, "signal", i).random() < .8
            self.signals.append(Claim(i, target, .8 if truth == correct else .2))
            self.policies.append(ScriptedPolicy(config.seed, i, config.policy, config.recovery))
        private = json.dumps([self.roles, [asdict(c) for c in self.signals]], sort_keys=True)
        self.scenario_hash = hashlib.sha256(private.encode()).hexdigest()
        self.log.emit("start", version=VERSION, config=asdict(config), scenario_hash=self.scenario_hash)

    def observation(self, i, mission=0, attempt=0, team=()):
        members = self.members[i // 10]
        known = None
        if self.roles[i] != "good":
            known = tuple(j for j in members if self.roles[j] in ("evil", "assassin"))
        return Observation(i, self.roles[i], members, known, self.signals[i], mission,
                           attempt, tuple(team), tuple(self.history[i // 10]), self.inboxes[i],
                           tuple(self.verified[i // 10]))

    def audit(self):
        if self.config.recovery == "none":
            return
        for pod, members in enumerate(self.members):
            target = rng_for(self.config.seed, "audit", pod).choice(members)
            evil = self.roles[target] in ("evil", "assassin")
            self.verified[pod] = [(target, evil)]
            self.log.emit("audit", after_missions=2, pod=pod, target=target, evil=evil)
            for i in members:
                if self.roles[i] not in ("good", "merlin"):
                    continue
                obs = self.observation(i, 2)
                for c in self.policies[i].memory:
                    if self.policies[i].contradicted(c, obs):
                        self.detection_origins.add(c.origin)
                self.policies[i].repair(obs)

    def brier(self, exclude_audited=False):
        errors = []
        for i, role in enumerate(self.roles):
            if role != "good":
                continue
            obs = self.observation(i)
            scores = self.policies[i].beliefs(obs)
            excluded = {target for target, _ in obs.verified} if exclude_audited else set()
            errors.extend((scores[j] - float(self.roles[j] in ("evil", "assassin"))) ** 2
                          for j in obs.members if j != i and j not in excluded)
        return statistics.mean(errors)

    def neighbors(self, i):
        if self.config.topology == "none":
            return ()
        local = [j for j in self.members[i // 10] if j != i]
        if self.config.topology == "federated":
            local += [(i - 10) % self.config.n, (i + 10) % self.config.n]
        return tuple(local)

    def communicate(self, mission, attempt):
        # All senders see the previous tick; no sender sees this tick's messages.
        outbound = []
        for i, policy in enumerate(self.policies):
            obs = self.observation(i, mission, attempt)
            policy.ingest(obs)
            claims = tuple(policy.discuss(obs))
            self.discussion_calls += 1
            if len(claims) > 4:
                raise ValueError("claim cap exceeded")
            allowed_relays = set(getattr(policy, "memory", ())) | set(obs.inbox)
            for c in claims:
                if not (0 <= c.target < self.config.n and 0 <= c.evil_probability <= 1):
                    raise ValueError("invalid claim")
                if c.origin != i and c not in allowed_relays:
                    raise ValueError("forged relay provenance")
            outbound.append(claims)
        incoming = [[] for _ in range(self.config.n)]
        for i, claims in enumerate(outbound):
            recipients = self.neighbors(i)
            self.log.emit("message", tick=self.ticks, sender=i, recipients=recipients,
                          claims=[asdict(c) for c in claims])
            for j in recipients:
                incoming[j].extend(claims)
                if self.roles[j] in ("good", "merlin"):
                    obs = self.observation(j, mission, attempt)
                    for claim in claims:
                        if self.policies[j].contradicted(claim, obs):
                            self.contradiction_exposures += 1
                            self.detection_origins.add(claim.origin)
                self.deliveries += 1
                self.claim_deliveries += len(claims)
        # At most 11 envelopes / 44 claims. Deterministic, no queue overflow.
        self.inboxes = [tuple(v) for v in incoming]
        self.ticks += 1

    def run(self):
        successes = [0] * len(self.members)
        for mission, size in enumerate(TEAM_SIZES):
            if mission == 2:
                self.recovery_measurements.append({"point": "before_audit", "brier": self.brier()})
                self.audit()
                self.recovery_measurements.append({"point": "after_audit", "brier": self.brier()})
            pending = set(range(len(self.members)))
            for attempt in range(5):
                self.communicate(mission, attempt)
                # Incorporate delivered messages before decisions, once per tick.
                for i, policy in enumerate(self.policies):
                    policy.ingest(self.observation(i, mission, attempt))
                self.inboxes = [() for _ in self.inboxes]
                for pod in sorted(pending):
                    members = self.members[pod]
                    leader = members[(mission * 5 + attempt) % 10]
                    team = self.policies[leader].propose(self.observation(leader, mission, attempt), size)
                    self.decision_calls += 1
                    if len(team) != size or len(set(team)) != size or not set(team) <= set(members):
                        raise ValueError("invalid team")
                    votes = []
                    if attempt < 4:
                        votes = [self.policies[i].vote(self.observation(i, mission, attempt, team)) for i in members]
                        self.decision_calls += 10
                        if any(type(v) is not bool for v in votes):
                            raise ValueError("invalid ballot")
                    approved = attempt == 4 or sum(votes) > 5
                    self.log.emit("proposal", mission=mission, attempt=attempt, pod=pod,
                                  leader=leader, team=team, votes=votes, approved=approved)
                    if not approved:
                        self.rejections += 1
                        continue
                    self.forced += attempt == 4
                    fails = 0
                    for i in team:
                        sabotage = self.policies[i].sabotage(self.observation(i, mission, attempt, team))
                        self.decision_calls += 1
                        if type(sabotage) is not bool or (sabotage and self.roles[i] in ("good", "merlin")):
                            raise ValueError("illegal sabotage")
                        fails += sabotage
                    passed = fails < (2 if mission == 3 else 1)
                    successes[pod] += passed
                    self.history[pod].append((tuple(team), fails))
                    self.log.emit("mission", mission=mission, pod=pod, team=team, fails=fails, passed=passed)
                    pending.remove(pod)
                if not pending:
                    break
            self.recovery_measurements.append({"point": f"after_mission_{mission + 1}", "brier": self.brier(),
                                               "unverified_brier": self.brier(exclude_audited=True)})
        wins, briers = [], []
        for pod, members in enumerate(self.members):
            won = successes[pod] >= 3
            target = None
            if won:
                assassin = next(i for i in members if self.roles[i] == "assassin")
                target = self.policies[assassin].assassinate(self.observation(assassin, 5))
                self.decision_calls += 1
                if target not in members:
                    raise ValueError("invalid assassination target")
                won = self.roles[target] != "merlin"
            wins.append(won)
            self.log.emit("council_outcome", pod=pod, successes=successes[pod], target=target, good_win=won)
            for i in members:
                if self.roles[i] != "good":
                    continue
                scores = self.policies[i].beliefs(self.observation(i, 5))
                briers.extend((scores[j] - float(self.roles[j] in ("evil", "assassin"))) ** 2
                              for j in members if j != i)
        outcome = {"version": VERSION, "kind": "scripted_simulation", **asdict(self.config),
                   "scenario_hash": self.scenario_hash, "status": "completed",
                   "good_council_fraction": statistics.mean(wins),
                   "good_swarm_win": sum(wins) * 5 >= len(wins) * 3,
                   "mission_success_fraction": sum(successes) / (5 * len(wins)),
                   "ordinary_good_brier": statistics.mean(briers), "ticks": self.ticks,
                   "message_deliveries": self.deliveries, "claim_deliveries": self.claim_deliveries,
                   "discussion_calls": self.discussion_calls, "decision_calls": self.decision_calls,
                   "rejected_proposals": self.rejections, "forced_proposals": self.forced,
                   "flagged_origins": len(self.detection_origins),
                   "flagged_honest_origins": sum(self.roles[i] in ("good", "merlin") for i in self.detection_origins),
                   "flagged_evil_origins": sum(self.roles[i] in ("evil", "assassin") for i in self.detection_origins),
                   "post_audit_contradiction_exposures": self.contradiction_exposures,
                   "brier_trajectory": self.recovery_measurements,
                   "post_audit_mission_success_fraction": sum(
                       fails < (2 if mission == 3 else 1)
                       for history in self.history for mission, (_, fails) in enumerate(history) if mission >= 2
                   ) / (3 * len(wins))}
        self.log.emit("outcome", **outcome)
        return {**outcome, "event_hash": self.log.digest, "event_count": self.log.count}


def measure(config, trace=None):
    tracemalloc.start()
    start = time.perf_counter()
    log = EventLog(trace)
    try:
        result = World(config, log).run()
        result["wall_seconds_with_tracemalloc"] = round(time.perf_counter() - start, 4)
        result["peak_python_mib"] = round(tracemalloc.get_traced_memory()[1] / 2**20, 4)
        return result
    finally:
        log.close()
        tracemalloc.stop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=100, choices=SIZES)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--topology", default="federated", choices=("none", "local", "federated"))
    parser.add_argument("--policy", default="provenance", choices=("provenance", "echo", "random"))
    parser.add_argument("--recovery", default="none", choices=("none", "audit", "repair"))
    parser.add_argument("--recovery-sweep", action="store_true", help="all three recovery treatments")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sweep", action="store_true", help="all sizes and topologies")
    parser.add_argument("--replicates", type=int, default=1)
    args = parser.parse_args()
    if args.replicates < 1:
        parser.error("replicates must be positive")
    args.out.mkdir(parents=True, exist_ok=False)
    configs = [Config(n, args.seed + rep, topology, args.policy, recovery)
               for n in (SIZES if args.sweep else (args.n,))
               for topology in (("none", "local", "federated") if args.sweep else (args.topology,))
               for recovery in (("none", "audit", "repair") if args.recovery_sweep else (args.recovery,))
               for rep in range(args.replicates)]
    (args.out / "plan.json").write_text(json.dumps([asdict(c) for c in configs], indent=2) + "\n")
    with (args.out / "outcomes.jsonl").open("x") as output:
        for config in configs:
            # Sweeps keep terminal hashes only; single runs retain replayable events.
            result = measure(config, None if args.sweep else args.out / f"events-{config.recovery}-{config.seed}.jsonl")
            output.write(json.dumps(result, sort_keys=True) + "\n")
            output.flush()
            print(json.dumps(result, sort_keys=True), flush=True)
    (args.out / "source.sha256").write_text(hashlib.sha256(Path(__file__).read_bytes()).hexdigest() + "\n")


if __name__ == "__main__":
    main()
