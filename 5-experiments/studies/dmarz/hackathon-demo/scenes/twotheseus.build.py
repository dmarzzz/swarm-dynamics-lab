"""Reduce the public event log of the fifty-member Swarm of Theseus run to scenes/twotheseus.data.js.

    python3 scenes/twotheseus.build.py

Source: 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-EVENTS.json (700 events:
50 founders learning, then per arm the replacements, the source selections and the decisions, each with the index of
its model call). Nothing is estimated; the sums are checked against S50-POST-MORTEM.md ("Observed comparison").
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / '../../../vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-EVENTS.json'
events = json.loads(SRC.read_text())
pos = lambda e: int(e['owner'].split('_')[1])

out = {'positions': 50, 'calls': 1118, 'cases': 6, 'arms': {}}
out['founder'] = [[e['seq'], pos(e), int(e['correct'])] for e in events if e['type'] == 'founder']
for arm in ('common', 'static', 'interactive', 'broken', 'retained'):
    pick = lambda kind: [e for e in events if e['type'] == kind and e.get('arm') == arm]
    out['arms'][arm] = {
        'replacement': [[e['seq'], pos(e), int(e['correct'])] for e in pick('replacement')],      # correct = the inherited note is correct
        'selection': [[e['seq'], pos(e), int(e['correct'])] for e in pick('selection')],          # correct = it asked its two authoritative sources
        'decision': [[e['seq'], pos(e), e['correct'], e['harmful']] for e in pick('decision')],   # correct decisions of 6, harmful approvals
    }
total = lambda arm: sum(d[2] for d in out['arms'][arm]['decision'])
assert [total(a) for a in ('common', 'static', 'interactive', 'broken', 'retained')] == [299, 297, 295, 166, 298]
assert sum(f[2] for f in out['founder']) == 50 and max(e['seq'] for e in events) == 1117
assert [sum(r[2] for r in out['arms'][a]['replacement']) for a in ('static', 'interactive', 'broken')] == [50, 50, 0]

header = ('// Reduced event log for scenes/twotheseus.js, written by scenes/twotheseus.build.py from\n'
          '// 5-experiments/studies/vishesh/swarm-of-theseus/execution-diagnostic/sol50/scale50/S50-EVENTS.json.\n'
          '// Each event is [model call index, position, ...]: founder [.., learned its sources correctly]; replacement [.., note correct];\n'
          '// selection [.., asked its two authoritative sources]; decision [.., correct of 6, harmful approvals].\n')
(HERE / 'twotheseus.data.js').write_text(header + 'FILM.data = FILM.data || {};\nFILM.data.twotheseus = ' + json.dumps(out, separators=(',', ':')) + ';\n')
print('wrote twotheseus.data.js', (HERE / 'twotheseus.data.js').stat().st_size, 'bytes')
