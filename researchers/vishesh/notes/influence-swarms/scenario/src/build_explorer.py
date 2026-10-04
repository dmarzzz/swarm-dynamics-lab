import json
import sys
from pathlib import Path
from dossier import FAMILIES,WORLDS,build
payload=[build(f,p,w) for f in FAMILIES for p in range(4) for w in WORLDS]
html=Path(__file__).with_name('explorer.html').read_text().replace('__DATA__',json.dumps(payload).replace('<','\\u003c'))
Path(sys.argv[1]).write_text(html)
print('built 96 case/world views; authored scenario data only')
