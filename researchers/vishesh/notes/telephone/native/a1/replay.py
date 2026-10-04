"""Recompute public authored A1 semantic results; no model/network calls."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/'src'),str(HERE.parents[1]/'t1/src')]
from contract import request,sha
from scoring import score,paired_summary

def main():
 audit=json.loads((HERE/'AUTHORED-TRACE-AUDIT.json').read_text());reviews=json.loads((HERE/'SEMANTIC-ANNOTATIONS.json').read_text())['reviews'];gold=json.loads((HERE/'gold.json').read_text());packet=json.loads((HERE/'packet.json').read_text());expected=json.loads((HERE/'SEMANTIC-SCORES.json').read_text());cases={c['id']:c for c in packet['cases']};parents={};actual=[]
 assert len(audit)==len(reviews)==len(expected)==72
 for a,row in zip(packet['assignments'],audit):
  assert all(row[k]==v for k,v in a.items())
  req=request(a['arm'],a['hop'],cases[a['component']]['records'],parents.get((a['component'],a['arm'])))
  assert req==row['request'] and sha(req)==row['request_sha256']
  parents[a['component'],a['arm']]=row['output']
  result=score(row['output'],reviews[a['call_id']],gold[a['component']],[r['id'] for r in cases[a['component']]['records']]);actual.append({**a,**result})
 assert actual==expected
 terminal={arm:{s['component']:s['retention'] for s in actual if s['arm']==arm and s['hop']==3} for arm in ('P','S','R')}
 print(json.dumps({'scored':len(actual),'all_parent_and_source_bindings_match':True,'all_published_scores_reproduced':True,'paired_S_minus_P_hop3':paired_summary(list(terminal['P']),terminal['P'],terminal['S']),'semantic_judgments':'manual evidence inputs; replay validates aggregation and binding, not independent semantic truth'},indent=2))
if __name__=='__main__':main()
