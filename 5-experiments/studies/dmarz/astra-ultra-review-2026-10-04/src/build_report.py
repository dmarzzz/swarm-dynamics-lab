#!/usr/bin/env python3
"""Render the reviewed evidence as a GitHub-readable document."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
review = json.loads((BASE / 'evidence.json').read_text())
url = 'https://github.com/dmarzzz/swarm-lab/blob/' + review['snapshot'] + '/'
parts = [
    '# ' + review['title'],
    '**Review and ranking by Astra Ultra.** Underlying experiments by Swarm Lab researchers dmarz, vishesh and shadow.',
    '**Evidence cutoff:** ' + review['cutoff'] + '.',
    'More agents, more checking and faster recovery often failed to improve the outcome that mattered. These ten findings show where that happened and where a simple intervention worked.',
    review['method'],
    review['units'],
]
for finding in review['findings']:
    parts.extend([
        '## ' + str(finding['rank']) + ' ' + finding['title'],
        '**Question we studied:** ' + finding['question'],
        '**What we learned:** ' + finding['learning'],
        '- **Agents:** ' + finding['agents'] + '\n'
        '- **Rounds or steps:** ' + finding['rounds'] + '\n'
        '- **Sample size:** ' + finding['sample'] + '\n'
        '- **Time:** ' + finding['time'],
        '**Limits:** ' + finding['caveat'],
        '**Sources:** ' + ' · '.join('[' + '/'.join(s.split('/')[-3:]) + '](' + url + s + ')' for s in finding['sources']),
    ])
parts.extend(['## Other evidence considered', '\n'.join('- ' + item for item in review['also_reviewed'])])
parts.extend(['## Attribution and reproducibility',
              'This is Astra Ultra’s review of existing Swarm Lab results. It is an editorial synthesis, not an independent experimental replication, a formal hypothesis acceptance or an institutional endorsement.',
              'All source links are pinned to [' + review['snapshot'][:8] + '](https://github.com/dmarzzz/swarm-lab/tree/' + review['snapshot'] + '). The accompanying evidence JSON and rendering scripts preserve the ranking, units, timing scope and caveats. No new simulations or model calls were launched for publication.'])
output = BASE / 'src/out/astra-ultra-review.md'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text('\n\n'.join(parts) + '\n')
print(output)
