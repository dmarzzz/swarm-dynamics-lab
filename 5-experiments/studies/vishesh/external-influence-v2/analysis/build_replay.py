import json,sys
from pathlib import Path
data=json.loads(Path(sys.argv[1]).read_text())
assert len(data['episodes'])==50
payload=json.dumps(data,separators=(',',':')).replace('<','\\u003c')
Path(sys.argv[2]).write_text(Path(__file__).with_name('replay_template.html').read_text().replace('__DATA__',payload))
print('Self-contained replay generated for all 50 recorded outcomes')
