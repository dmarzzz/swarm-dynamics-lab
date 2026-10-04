"""Retrospective comparator repair on saved Q0 only; never changes native source."""
import copy,json,re,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'src'))
from contract import parser,ledger_labels,outcome,development_world,packet

def scoped_parser(p):
 p=copy.deepcopy(p)
 for r in p['records']:
  if 'text' in r:
   r['text']=re.sub(r'An unverified preliminary impression suggested [^;]+; the final verified finding was that ', '', r['text'])
 return parser(p)

if __name__=='__main__':
 p=Path(sys.argv[1]);rs=json.loads((p/'records.json').read_text());ws=json.loads((p/'worlds.json').read_text());assert len(ws)==8 and set(ws)==set(map(str,range(4100,4108)))
 rows=[]
 for r in rs:
  w=ws[str(r['seed'])];inp=r['request']['state'];pred=scoped_parser(inp)
  rows.append(dict(id=r['id'],labels=pred,score=outcome(w,pred)))
  if r['representation']=='prose':
   changed=copy.deepcopy(inp)
   for x in changed['records']:x['text']=x['text'].replace('impression suggested agreement;', 'impression suggested uncertainty;').replace('impression suggested disagreement;', 'impression suggested uncertainty;')
   assert scoped_parser(changed)==pred
 for seed in range(4000,4008):
  w=development_world(seed)
  assert scoped_parser(packet(w,'prose'))==ledger_labels(w['records'])
 out=dict(retrospective=True,holdout_opened=False,new_native_calls=0,scope='saved Q0 authored grammar only; tuned after outcomes',records=rows,correct=sum(6-r['score']['field_errors'] for r in rows),denominator=96,protected_errors=sum(r['score']['protected_errors'] for r in rows),max_first_action_regret=max(r['score']['first_action_regret'] for r in rows),development_checks=8,preliminary_perturbation_packets=8)
 print(json.dumps(out,indent=2))
