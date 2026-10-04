"""Local model only. No credentials, hosted fallback or automatic model routing."""
import importlib.metadata
import math

MODEL = 'convaiinnovations/laya'
REVISION = '55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851'
SOURCE = '2e4d9c87e8b1621deb344eac7de5c7258f32f849'
QUESTION = {'vote': {'type': 'choice',
    'instructions': 'Choose the API provider supported by the most distinct benchmark roots. Count each root once. If tied choose ABSTAIN. Use only the supplied reports.',
    'criteria': {'A': 'Select provider A', 'B': 'Select provider B', 'C': 'Select provider C',
                 'ABSTAIN': 'Evidence is tied or insufficient'}}}


class Laya:
    def __init__(self):
        import torch
        from laya import load
        torch.set_num_threads(2)
        torch.manual_seed(0)
        self.model = load(MODEL, revision=REVISION, device='cpu', backend='eager')
        self.metadata = {'backend': 'laya', 'model': MODEL, 'revision': REVISION,
                         'source_revision': SOURCE, 'device': 'cpu',
                         'versions': {p: importlib.metadata.version(p) for p in
                                      ('laya', 'torch', 'transformers', 'safetensors')}}

    def __call__(self, reports):
        state = '\n'.join(f"{r['root']} recommends provider {r['recommendation']}." for r in reports)
        result = self.model.predict(state, QUESTION, max_len=1024)
        answer = result['answers']['vote']
        p = answer['probabilities']
        if set(p) != set(QUESTION['vote']['criteria']):
            raise ValueError('invalid_probabilities')
        if not all(isinstance(v, (int, float)) and math.isfinite(v) and 0 <= v <= 1 for v in p.values()):
            raise ValueError('invalid_probability_range')
        if abs(sum(p.values()) - 1) > 0.001 or p[answer['choice']] < max(p.values()) - 0.00001:
            raise ValueError('invalid_probability_distribution')
        return answer['choice']
