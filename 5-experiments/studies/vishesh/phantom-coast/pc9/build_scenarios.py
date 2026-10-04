#!/usr/bin/env python3
"""Build inspected development evidence only; no native transport or reserved cases."""
import argparse,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;sys.path.insert(0,str(BASE/'src'))
from scenario_fixtures import SCENARIOS,fixture
from qualification import cases
from engine import audit
from render import render

def build(out):
 out.mkdir(parents=True,exist_ok=False);checks={}
 for name in SCENARIOS:
  d=out/name;d.mkdir();data=fixture(name)
  (d/'fixture.json').write_text(json.dumps(data,indent=2)+'\n');render(data,d/'replay.html')
  checks[name]=[audit(e) for e in data['episodes']]
 (out/'audit.json').write_text(json.dumps(checks,indent=2)+'\n')
 (out/'development-cases.json').write_text(json.dumps(dict(evidence_kind='INSPECTED DEVELOPMENT ONLY — NO NATIVE CALLS',cases=cases()),indent=2)+'\n')
 links=''.join(f'<li><a href="{s}/replay.html">{s.replace("-"," ")}</a></li>' for s in SCENARIOS)
 (out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Phantom Coast scenarios</title><style>body{font:18px system-ui;background:#09131c;color:#dce8f1;max-width:760px;margin:64px auto;padding:24px;line-height:1.7}a{color:#58d4bf}li{margin:20px 0}</style><h1>Phantom Coast: three diagnostic scenarios</h1><p>Scripted acceptance fixtures. No native model ran; these demonstrate what the instrument measures.</p><ul>'+links+'</ul><p>False positives test wasted exploration. Consensus correction tests recovery after direct evidence. Missing evidence tests honest uncertainty when repeated visits leave places unseen.</p></html>')
 return checks
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.output);print('Three development fixtures audited; eight development packets saved; zero native calls.')
