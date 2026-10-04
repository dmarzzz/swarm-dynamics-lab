"""Deterministic lexical clusters and coverage-aware descriptive metrics."""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from hashlib import blake2b
import math
import random
import re
import statistics
import unicodedata
import numpy as np
from .adapters import Event, iso_time

VERSION = "0.1.1"
DISSENT = re.compile(r"\b(disagree|disagreement|dissent|reject|rejected|incorrect|false|refute|refuted|not true)\b", re.I)
REVERT = re.compile(r"\b(revert|reverted|reverting|rollback|roll back|undo|undid)\b", re.I)


def normalize(text):
    return " ".join(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", text).lower(), re.UNICODE))


def shingles(normalized, cap=512):
    words = normalized.split()
    spans = max(0, len(words) - 2)
    indices = range(spans) if spans <= cap else sorted({i * (spans - 1) // (cap - 1) for i in range(cap)})
    return frozenset(int.from_bytes(blake2b(" ".join(words[i:i + 3]).encode(), digest_size=4).digest(), "big") for i in indices)


class Clusterer:
    """MinHash LSH candidates, exact sampled-shingle Jaccard verification.

    Fixed representatives avoid transitive chaining. Empty texts have no cluster.
    Exact duplicate normalized texts match even below the six-token minimum.
    """
    def __init__(self, threshold=.7, seed=20261004, cap=512):
        if not 0 < threshold <= 1 or cap < 2:
            raise ValueError("threshold must be in (0, 1], shingle cap >=2")
        self.threshold, self.cap = threshold, cap
        rng = random.Random(seed)
        self.a = np.array([rng.randrange(1, 4294967291) for _ in range(64)], dtype=np.uint64)
        self.b = np.array([rng.randrange(0, 4294967291) for _ in range(64)], dtype=np.uint64)
        self.exact = {}
        self.representatives = []
        self.buckets = defaultdict(list)
        self.long_texts = 0
        self.candidate_comparisons = 0

    def add(self, text):
        normalized = normalize(text)
        if not normalized:
            return None
        digest = blake2b(normalized.encode(), digest_size=16).digest()
        if digest in self.exact:
            return self.exact[digest]
        words = normalized.split()
        self.long_texts += len(words) - 2 > self.cap
        features = shingles(normalized, self.cap) if len(words) >= 6 else frozenset()
        bands = []
        candidates = set()
        if features:
            values = np.array(list(features), dtype=np.uint64)
            signature = ((self.a[:, None] * values[None, :] + self.b[:, None]) % np.uint64(4294967291)).min(axis=1)
            bands = [(i, signature[i * 4:(i + 1) * 4].tobytes()) for i in range(16)]
            for band in bands:
                candidates.update(self.buckets.get(band, ()))
        best, best_score = None, self.threshold
        for candidate in sorted(candidates):
            other = self.representatives[candidate]
            if min(len(features), len(other)) / max(len(features), len(other)) < self.threshold:
                continue
            self.candidate_comparisons += 1
            overlap = len(features & other)
            score = overlap / (len(features) + len(other) - overlap)
            if score >= best_score:
                if best is None or score > best_score:
                    best, best_score = candidate, score
        if best is None:
            best = len(self.representatives)
            self.representatives.append(features)
            for band in bands:
                self.buckets[band].append(best)
        self.exact[digest] = best
        return best


def gini(values):
    values = sorted(values)
    if not values or sum(values) == 0:
        return None
    n = len(values)
    return (2 * sum((i + 1) * value for i, value in enumerate(values)) / (n * sum(values))) - (n + 1) / n


def quantiles(values):
    values = sorted(values)
    if not values:
        return {"n": 0, "min": None, "median": None, "p90": None, "max": None}
    return {"n": len(values), "min": values[0], "median": statistics.median(values),
            "p90": values[math.ceil(.9 * len(values)) - 1], "max": values[-1]}


def analyze(events, name="swarm", threshold=.7, window=100, k_values=(2, 3, 5, 10)):
    if window < 1 or not k_values or any(k < 2 for k in k_values):
        raise ValueError("window must be positive and adopter targets >=2")
    events = list(events)
    # Unknown clocks last. Stable id breaks ties for reproducibility, never for causal credit.
    events.sort(key=lambda e: (e.time is None, e.time if e.time is not None else 0, e.event_id))
    clusterer = Clusterer(threshold)
    members = defaultdict(list)
    activity, kinds, task_counts = Counter(), Counter(), Counter()
    actor_times = defaultdict(list)
    flags = Counter()
    dated = sum(e.time is not None for e in events)
    known = sum(e.agent_id is not None for e in events)
    both = sum(e.agent_id is not None and e.time is not None for e in events)
    text_count = sum(bool(normalize(e.text)) for e in events)
    for index, event in enumerate(events):
        kinds[event.kind] += 1
        if event.kind.startswith("task_"):
            task_counts[event.kind] += 1
        if event.agent_id is not None:
            activity[event.agent_id] += 1
            if event.time is not None:
                actor_times[event.agent_id].append(event.time)
        flags["dissent"] += bool(DISSENT.search(event.text))
        flags["revert"] += bool(REVERT.search(event.text))
        cluster = clusterer.add(event.text)
        if cluster is not None:
            members[cluster].append((index, event))
    clusters = []
    influence = Counter()
    reached = {str(k): [] for k in k_values}
    adoption_curve = Counter()
    temporal_clusters = 0
    for cluster, rows in members.items():
        all_actors = {e.agent_id for _, e in rows if e.agent_id is not None}
        first_by_actor = {}
        for index, event in rows:
            if event.agent_id is not None and event.time is not None:
                first_by_actor.setdefault(event.agent_id, (event.time, index))
        ordered = sorted(first_by_actor.items(), key=lambda pair: (pair[1][0], pair[0]))
        start = ordered[0][1][0] if ordered else None
        temporal_clusters += bool(ordered)
        firsts = [actor for actor, (time, _) in ordered if time == start]
        clusters.append({"cluster": cluster, "records": len(rows), "identities": len(all_actors),
                         "dated_identities": len(ordered), "first_time": iso_time(start),
                         "first_movers": firsts, "first_mover_tie": len(firsts) > 1,
                         "time_to_k_seconds": {str(k): ordered[k - 1][1][0] - start if len(ordered) >= k else None for k in k_values}})
        for k in k_values:
            if len(ordered) >= k:
                reached[str(k)].append(ordered[k - 1][1][0] - start)
        for rank, (_, (time, _)) in enumerate(ordered, 1):
            adoption_curve[(int((time - start) // 3600), rank)] += 1
    # Global dated-event step positions. Equal timestamps occupy the same boundary.
    time_boundary = {}
    for index, event in enumerate(events):
        if event.time is not None:
            time_boundary.setdefault(event.time, index)
    for rows in members.values():
        seen = set()
        previous = deque()
        for index, event in rows:
            if event.agent_id is None or event.time is None:
                continue
            boundary = time_boundary[event.time]
            while previous and boundary - previous[0][0] > window:
                previous.popleft()
            if event.agent_id not in seen:
                prior = {actor for old_index, time, actor in previous
                         if time < event.time and 0 < boundary - old_index <= window and actor != event.agent_id}
                if prior:
                    for actor in sorted(prior):
                        influence[actor] += 1 / len(prior)
                seen.add(event.agent_id)
            previous.append((boundary, event.time, event.agent_id))
    lifetimes = [max(times) - min(times) for times in actor_times.values()]
    total = len(events)
    summary = {"records": total, "nonempty_text_records": text_count, "identities": len(activity),
               "identity_coverage": known / total if total else None, "time_coverage": dated / total if total else None,
               "identity_and_time_records": both, "known_identity_records": known, "dated_records": dated,
               "clusters": len(clusters), "multi_identity_clusters": sum(c["identities"] >= 2 for c in clusters) if known else None,
               "multi_record_clusters": sum(c["records"] >= 2 for c in clusters),
               "participation_gini": gini(activity.values()), "identity_span_seconds": quantiles(lifetimes),
               "single_record_identities": sum(n == 1 for n in activity.values()) if known else None,
               "dissent_marker_records": flags["dissent"], "dissent_marker_fraction": flags["dissent"] / total if total else None,
               "revert_marker_records": flags["revert"], "revert_marker_fraction": flags["revert"] / total if total else None,
               "temporal_clusters": temporal_clusters,
               "time_to_k": {str(k): {"reached": len(reached[str(k)]), "at_risk_clusters": temporal_clusters,
                                          "not_observed_to_reach": temporal_clusters - len(reached[str(k)]),
                                          "seconds_among_reached": quantiles(reached[str(k)])} for k in k_values}}
    return {"schema_version": VERSION, "name": name, "summary": summary,
            "parameters": {"jaccard_threshold": threshold, "minhash_permutations": 64, "lsh_bands": 16,
                           "shingle_cap": 512, "seed": 20261004, "influence_step_window": window},
            "diagnostics": {"long_unique_texts_sampled": clusterer.long_texts,
                            "candidate_comparisons": clusterer.candidate_comparisons},
            "record_kinds": dict(sorted(kinds.items())), "task_events": dict(sorted(task_counts.items())),
            "participation_counts_descending": sorted(activity.values(), reverse=True),
            "identity_spans_seconds_sorted": sorted(lifetimes),
            "influence": [{"identity": actor, "fractional_new_adopter_credit": score,
                           "credit_per_record": score / activity[actor]} for actor, score in influence.most_common()],
            "clusters": sorted(clusters, key=lambda c: (-c["identities"], -c["records"], c["cluster"])),
            "adoption_events_by_elapsed_hour_and_rank": [{"elapsed_hour": hour, "adopter_rank": rank, "clusters": count}
                                                         for (hour, rank), count in sorted(adoption_curve.items())],
            "limits": ["Lexical similarity, not semantic ideas or proof of copying.",
                       "First observed identity is not inventor; no causal influence is identified.",
                       "Missing clocks/identities are not imputed. Identity spans are observation-window censored.",
                       "Fixed-representative LSH can miss near duplicates; long texts use sampled shingles.",
                       "Dissent/revert are unvalidated English lexical markers, not behavioral outcomes.",
                       "Full-corpus descriptive statistics have no IID confidence interval."]}
