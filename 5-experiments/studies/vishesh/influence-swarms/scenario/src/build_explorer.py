import json
import sys
from pathlib import Path
from dossier import FAMILIES,WORLDS,build
payload=[]
for family in FAMILIES:
    for profile in range(4):
        c=build(family,profile)
        item={k:c[k] for k in ('family','profile','brief','evaluator','documents')}
        item['worlds']={w:[d for d in build(family,profile,w)['documents'] if d['kind']=='comparison'] for w in WORLDS}
        payload.append(item)
html=Path(__file__).with_name('explorer.html').read_text().replace('__DATA__',json.dumps(payload).replace('<','\\u003c'))
Path(sys.argv[1]).write_text(html)
print('built 24 dossiers with 4 comparison variants each; authored scenario data only')
