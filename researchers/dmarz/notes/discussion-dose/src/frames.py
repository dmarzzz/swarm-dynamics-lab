"""Live view: turn the event stream into frame.json (kind "deliberation") for the swarm-live site.

The frame is host-side only; agents never see it. It shows the protected truth (which value is false, who was
exposed) because the worlds are fictional and the view is for people watching the experiment.
Upload failures are swallowed: a live view must never change or stop a run.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from tasks import independent_answer

MSG_CHARS = 160
MAX_HISTORY = 3000  # replay snapshots kept; older ones thinned 2:1 past this

class FrameTracker:
    def __init__(self, world_for, path, upload=None, every=3.0, protocol='v1', level=None):
        self.world_for = world_for; self.path = Path(path); self.upload = upload; self.every = every
        self.protocol = protocol; self.level = level; self.last = 0.0
        self.tally = {'episodes': 0, 'attack': 0, 'attack_wins': 0, 'attack_false_memory': 0, 'clean': 0, 'clean_correct': 0, 'invalid': 0}
        self.recent = []; self.history = []; self.thinned = 0
        self._reset(None, None)

    def _reset(self, task_id, label):
        self.task_id = task_id; self.label = label or {}; self.agents = {}; self.round = 0; self.rounds = None
        self.trajectory = []; self.posts = []; self.phase = 'starting'; self.decision = None; self.memory = None
        self.world = self.world_for(task_id) if task_id is not None else None

    def _endorse(self, claims):
        w = self.world; key = w['target_key']; o, f = key.split('.')
        c = next((c for c in claims if c['key'] == key), None)
        if c is None: return None
        return 'false' if c['value'] == w['false_value'] else 'true' if c['value'] == w['truth'][o][f] else 'other'

    def event(self, label, e):
        if label.get('task_id') != self.task_id or label.get('phase') != self.label.get('phase') or label.get('arm') != self.label.get('arm') or label.get('attack') != self.label.get('attack'):
            self._reset(label.get('task_id'), label)
        arm = label.get('arm') or {}
        self.rounds = arm.get('rounds')
        k = e['kind']
        if k == 'call_start':
            self.phase = e['phase']; self.round = e.get('round', 0)
            if isinstance(e.get('agent'), int): self.agents.setdefault(e['agent'], {}).update(speaking=True)
        elif k == 'call_response' and isinstance(e.get('agent'), int):
            a = self.agents.setdefault(e['agent'], {}); a['speaking'] = False; r = e.get('response') or {}
            if isinstance(r.get('claims'), list):
                try: a['claim'] = self._endorse(r['claims'])
                except Exception: pass
            if 'vote' in r: a['vote'] = r['vote']
            if isinstance(r.get('message'), str) and e['phase'] in ('report', 'discuss'):
                a['msg'] = r['message'][:MSG_CHARS]
                self.posts.append({'agent': e['agent'], 'round': e.get('round', 0), 'phase': e['phase']}); self.posts = self.posts[-12:]
        elif k == 'round_complete':
            self.round = e['round']
        elif k == 'memory_merge':
            self.memory = [self._endorse([r]) for r in e.get('records', []) if r['key'] == self.world['target_key']]
        self._ballots_checkpoint(e)
        if k in ('call_response', 'round_complete', 'memory_merge', 'call_failure'): self.snapshot()
        self.flush()

    def snapshot(self):
        self.history.append(self.frame())
        if len(self.history) > MAX_HISTORY: self.history = self.history[::2]; self.thinned += 1

    def replay(self):
        # Logical order is event order; 'ts' is wall time when the event was processed.
        return {'kind': 'deliberation-replay', 'protocol': self.protocol, 'level': self.level,
                'thinned': self.thinned, 'frames': self.history}  # thinned = times history was halved (2:1)

    def _ballots_checkpoint(self, e):
        # A probe is three ballot calls at one round; record the checkpoint once all three answered.
        if e['kind'] == 'call_response' and e.get('phase') == 'ballot' and self.label.get('phase') == 'continuation':
            rnd = e.get('round', 0); row = next((t for t in self.trajectory if t['round'] == rnd), None)
            if row is None: row = {'round': rnd, 'votes': {}, 'claims': {}}; self.trajectory.append(row)
            a = self.agents.get(e['agent'], {}); row['votes'][e['agent']] = a.get('vote'); row['claims'][e['agent']] = a.get('claim')

    def episode_done(self, row):
        ev = row.get('evaluation', {}); attack = row['arm']['attack']; t = self.tally
        t['episodes'] += 1; t['invalid'] += ev.get('invalid', 0)
        if attack: t['attack'] += 1; t['attack_wins'] += ev.get('target_win', 0); t['attack_false_memory'] += ev.get('false_memory_admitted', 0)
        else: t['clean'] += 1; t['clean_correct'] += ev.get('correct', 0)
        res = row.get('result') or {}
        self.recent.append({'task': row['task_id'], 'attack': attack, 'rounds': row['arm']['rounds'], 'decision': res.get('decision'),
                            'correct': ev.get('correct', 0), 'target_win': ev.get('target_win', 0), 'invalid': ev.get('invalid', 0),
                            'false_memory': ev.get('false_memory_admitted', 0)})
        self.recent = self.recent[-24:]
        self.snapshot(); self.flush(force=True)

    def frame(self):
        w = self.world
        roles = {v: k for k, v in (w or {}).get('roles', {}).items()}
        agents = []
        for i in range(3):
            a = self.agents.get(i, {})
            agents.append({'id': i, 'role': roles.get(i, 'agent'), 'vote': a.get('vote'), 'claim': a.get('claim'),
                           'speaking': bool(a.get('speaking')), 'msg': a.get('msg', '')})
        o, f = (w['target_key'].split('.') if w else (None, None))
        arm = self.label.get('arm') or {}
        attack = arm.get('attack', self.label.get('attack'))
        return {'kind': 'deliberation', 't': self.tally['episodes'], 'ts': round(time.time(), 1),
                'protocol': self.protocol, 'level': self.level,
                'world': None if w is None else {'task': w['task_id'], 'family': w['family'], 'instructions': w['instructions'],
                                                 'key': w['target_key'], 'true': w['truth'][o][f], 'false': w['false_value'],
                                                 'answer': independent_answer(w),
                                                 'attacker': w['target']},
                'arm': {'attack': attack, 'rounds': arm.get('rounds')}, 'stage': self.label.get('phase'),
                'phase': self.phase, 'round': self.round, 'agents': agents,
                'trajectory': [{'round': t['round'], 'false': sum(v == 'false' for v in t['claims'].values()),
                                'votes': [t['votes'].get(i) for i in range(3)]} for t in sorted(self.trajectory, key=lambda t: t['round'])],
                'posts': self.posts[-6:], 'memory': self.memory, 'tally': self.tally, 'recent': self.recent}

    def flush(self, force=False):
        now = time.monotonic()
        if not force and now - self.last < self.every: return
        self.last = now
        try:
            self.path.write_text(json.dumps(self.frame(), separators=(',', ':')))
            if self.upload: self.upload(self.path)
        except Exception:
            pass
