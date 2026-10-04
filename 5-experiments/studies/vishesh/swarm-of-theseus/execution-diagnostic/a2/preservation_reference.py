"""Development-only selective preservation reference; no native actor or oracle injection."""
from design import SOURCES, worlds, label


def decide(practice, observations, family, epoch):
    visible = [h for h in observations if h['epoch'] == epoch and h['case']['class'] == practice['class']]
    candidates = [s for s in SOURCES if all(label(h['case'], s, family) == h['outcome'] for h in visible)]
    if len(candidates) == 1:
        source = candidates[0]
        return {'state': 'retain' if source == practice['source'] else 'revise',
                'source': source, 'support': [h['case']['id'] for h in visible]}
    return {'state': 'provisional' if practice['source'] in candidates else 'quarantine',
            'source': None, 'support': [], 'candidates': candidates}


def fixtures():
    world = worlds(9300)[0]
    old = world['rule']
    changed = next(s for s in SOURCES if s not in old.values())
    current = dict(old, A=changed)
    def records(rule):
        return [{'epoch': 1, 'case': c, 'outcome': label(c, rule[c['class']], 'release')} for c in world['train']]
    stable = records(old)
    shifted = records(current)
    contradictory = shifted + [dict(shifted[0], outcome='hold' if shifted[0]['outcome']=='ship' else 'ship')]
    return old, stable, shifted, contradictory
