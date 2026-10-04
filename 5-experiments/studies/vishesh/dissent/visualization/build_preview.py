"""Render software-fixture replay. No model, network or credential access."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from cli import fixture_bundle
p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);a=p.parse_args()
data=fixture_bundle();html=(ROOT/'visualization/replay.html').read_text()
# Protect script-element boundaries even if future evidence contains hostile markup.
encoded=json.dumps(data,ensure_ascii=True,allow_nan=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
a.out.parent.mkdir(parents=True,exist_ok=True)
with a.out.open('x') as f:f.write(html.replace('__REPLAY_DATA__',encoded))
print('Fixture preview written; no model observations.')
