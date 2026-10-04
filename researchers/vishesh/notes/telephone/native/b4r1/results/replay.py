"""Reconstruct the published main evidence with no network or model calls."""
import json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'src'))
from native import packet
from corpus import sha
from report import analyze
p=packet();traces=json.loads((HERE/'AUTHORED-TRACE-AUDIT.json').read_text());by={r['assignment']:r for r in traces};gold=json.loads((HERE.parent/'prepared/gold.json').read_text());audit=json.loads((HERE/'SEMANTIC-AUDIT.json').read_text())
assert len(traces)==92 and len({r['response']['id'] for r in traces})==92
with tempfile.TemporaryDirectory() as td:
 out=Path(td)
 for t in traces:
  assert sha(t['request'])==t['request_sha256'] and sha(t['response'])==t['response_sha256']
  for kind in ('request','response'):(out/(t['assignment']+'.'+kind+'.json')).write_text(json.dumps(t[kind]))
 for a in p['assignments']:
  t=by[a['id']];receipt={'request_sha256':t['request_sha256'],'response_sha256':t['response_sha256'],'parent_response_sha256':None if a['parent']is None else by[a['parent']]['response_sha256']};(out/(a['id']+'.receipt.json')).write_text(json.dumps(receipt))
 r=analyze(p,out,gold);assert all(x['status']=='valid' for x in r['rows'])
 assert [x['correct'] for x in r['cells']]==[3,9,4,9]
 assert len(audit)==36 and len({a['assignment'] for a in audit})==36
 for a in audit:
  assert a['response_sha256']==by[a['assignment']]['response_sha256'] and a['parent_response_sha256']==by[a['parent']]['response_sha256']
 print(json.dumps({'offline_replay_passed':True,'main_responses':90,'reader_annotations':36,'correct_by_block_policy':[3,9,4,9],'new_model_calls':0}))
