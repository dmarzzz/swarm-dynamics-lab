from pathlib import Path
import json,secrets,sys,hashlib
from cases import build
from baseline import solve
from contract import request,digest,bound,score,summarize,ATTEMPT,RESERVE
here=Path(__file__).resolve().parent;private=Path(sys.argv[1]);private.mkdir(parents=True,exist_ok=True)
assert not (here/'qualification-seal.json').exists()
seed=secrets.token_hex(24);rows=build(seed);records=[]
for r in rows:
 a=solve(r['actor']);s=score(r,a);records.append({'case_id':r['id'],'valid':True,'parsed':a,'score':s});assert bound(request(r['actor']))<=10000
assert summarize(rows,records)['qualified'];assert len({digest(request(r['actor'])['response_format']) for r in rows})==1
assignments=[{'id':ATTEMPT+f'-{i:03}','case_id':r['id'],'root':r['root'],'family':r['family'],'condition':r['condition'],'request_sha256':digest(request(r['actor'])),'input_token_upper_bound':bound(request(r['actor'])),'reserve_usd':RESERVE,'tldr':f"PQ-04 separate report assertions and source evidence; {r['family']}, focal source observed={r['condition']['source_observed']}; compare exact facts/labels/decision to typed truth and parser; paired synthetic diagnostic."} for i,r in enumerate(rows)]
manifest={'attempt':ATTEMPT,'stage':'targeted_qualification_only','corpus_sha256':digest(rows),'assignments':assignments,'max_calls':8,'max_reserved_usd':.48,'evaluation_dispatch':False}
for n,v in [('manifest.json',manifest),('qualification-seal.json',{'corpus_sha256':digest(rows),'roots':4,'calls':8,'qa':'8/8 exact including paired assertion invariance and DEFER','operator_individual_case_access_before_run':False,'templates_known':True,'old_evaluation_opened':False})]:(here/n).write_text(json.dumps(v,indent=2)+'\n')
for n,v in [('packet.json',{'manifest':manifest,'rows':rows}),('custody.json',{'seed':seed})]:p=private/n;p.write_text(json.dumps(v));p.chmod(0o600)
print(json.dumps({'calls':8,'roots':4,'max_input_bound':max(a['input_token_upper_bound'] for a in assignments),'max_reservation':.48,'offline_qualified':True}))
