from pathlib import Path
import json,secrets,sys
from cases import build
from baseline import solve
from contract import request,digest,bound,score,summarize,ATTEMPT,RESERVE
here=Path(__file__).resolve().parent;private=Path(sys.argv[1]);private.mkdir(parents=True,exist_ok=True)
assert not (here/'qualification-seal.json').exists()
seeds={s:secrets.token_hex(24) for s in ['qualification','evaluation']}
rows=build(seeds['qualification'],1,'qualification')+build(seeds['evaluation'],4,'evaluation');records=[]
for r in rows:
 a=solve(r['actor']);s=score(r,a);records.append(dict(case_id=r['id'],valid=True,parsed=a,score=s));assert bound(request(r['actor']))<=7000
assert summarize(rows,records)['qualified'] and summarize(rows,records)['evaluation_accepted']
assert len({digest(request(r['actor'])['response_format']) for r in rows})==1
assignments=[{'id':ATTEMPT+f'-{i:03}','case_id':r['id'],'root':r['root'],'stage':r['stage'],'family':r['family'],'condition':r['condition'],'request_sha256':digest(request(r['actor'])),'input_token_upper_bound':bound(request(r['actor'])),'reserve_usd':RESERVE,'tldr':f"R1 {r['stage']}: {r['family']}, contradictory-claim copies={r['condition']['copies']}, focal evidence observed={r['condition']['source_observed']}; compare exact facts/modes/labels/decisions to typed truth and same-input parser, paired authored robustness only."} for i,r in enumerate(rows)]
manifest={'attempt':ATTEMPT,'stage':'qualification_then_conditional_evaluation','corpus_sha256':digest(rows),'assignments':assignments,'max_calls':50,'max_reserved_usd':2.4,'evaluation_dispatch':'only_after_all_qualification_gates'}
for n,v in [('manifest.json',manifest),('qualification-seal.json',{'corpus_sha256':digest(rows),'roots':25,'calls':50,'qualification_calls':10,'evaluation_calls':40,'qa':'50/50 exact against typed labels using same-input parser; disjoint fresh split seeds','operator_individual_case_access_before_run':False,'templates_known':True,'old_evaluation_opened':False})]:(here/n).write_text(json.dumps(v,indent=2)+'\n')
for n,v in [('packet.json',{'manifest':manifest,'rows':rows}),('custody.json',{'seeds':seeds})]:p=private/n;p.write_text(json.dumps(v));p.chmod(0o600)
print(json.dumps({'calls':50,'roots':25,'max_input_bound':max(a['input_token_upper_bound'] for a in assignments),'max_reservation':2.4,'offline_qualified':True}))
