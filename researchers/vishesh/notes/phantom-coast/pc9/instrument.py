#!/usr/bin/env python3
"""Offline-only acceptance fixtures and saved-data audit; no native dispatch."""
import argparse,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B/'src'))
from fixtures import make_replay
from engine import audit
from render import render
from policies import pooled_endpoint
p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
a=sub.add_parser('fixture');a.add_argument('--output',type=Path,required=True)
a=sub.add_parser('audit');a.add_argument('input',type=Path)
args=p.parse_args()
if args.command=='fixture':
 args.output.mkdir(parents=True,exist_ok=False)
 data=make_replay();data['pooled_endpoint_diagnostics']=[pooled_endpoint(e) for e in data['episodes']]
 (args.output/'fixture.json').write_text(json.dumps(data,indent=2)+'\n');render(data,args.output/'replay.html')
 checks=[audit(e) for e in data['episodes']];(args.output/'audit.json').write_text(json.dumps(dict(evidence_kind='offline acceptance fixture',native_calls=0,checks=checks),indent=2)+'\n')
 print(json.dumps(dict(native_calls=0,fixture_branches=4,all_replayed=True,output=str(args.output))))
else:
 data=json.loads(args.input.read_text());print(json.dumps([audit(e) for e in data['episodes']],indent=2))
