from pathlib import Path
import json,secrets,sys,hashlib
from cases import build
from baseline import solve
from contract import request,digest,bound,score,ATTEMPT,RESERVE
here=Path(__file__).resolve().parent;private=Path(sys.argv[1]);private.mkdir(parents=True,exist_ok=True)
assert not (here/'qualification-seal.json').exists(),'do_not_regenerate_consumed_cases'
seed=secrets.token_hex(24);rows=build(seed)
first=next(i for i,r in enumerate(rows) if r['condition']['copies']==3);rows.insert(0,rows.pop(first))
for r in rows:
 s=score(r,solve(r['actor']));assert s['source_facts_correct']==3 and s['report_facts_correct']==len(r['actor']['reports']) and s['quotes_valid'] and s['labels_correct'] and s['decision_correct'];assert bound(request(r['actor']))<=10000
assignments=[{'id':ATTEMPT+f'-{i:03}','case_id':r['id'],'root':r['root'],'family':r['family'],'condition':r['condition'],'request_sha256':digest(request(r['actor'])),'input_token_upper_bound':bound(request(r['actor'])),'reserve_usd':RESERVE,'tldr':f"PQ-03 explicit fact extraction; {r['family']}, contradiction copies={r['condition']['copies']}; deterministic fidelity versus typed truth and parser, synthetic paired qualification only."} for i,r in enumerate(rows)]
manifest={'attempt':ATTEMPT,'stage':'qualification_only','corpus_sha256':digest(rows),'assignments':assignments,'max_calls':24,'max_reserved_usd':1.44,'evaluation_dispatch':False}
for name,value in [('manifest.json',manifest),('qualification-seal.json',{'corpus_sha256':digest(rows),'roots':12,'calls':24,'mechanisms':6,'automated_parser_qa':'24/24 exact','individual_qualification_read_by_operator':False,'fresh_values_known_grammar':True,'old_evaluation_opened':False,'source_sha256':{n:hashlib.sha256((here/n).read_bytes()).hexdigest() for n in ['cases.py','contract.py','baseline.py','runtime.py']}})]:
 (here/name).write_text(json.dumps(value,indent=2)+'\n')
for name,value in [('packet.json',{'manifest':manifest,'rows':rows}),('custody.json',{'seed':seed})]:
 p=private/name;p.write_text(json.dumps(value));p.chmod(0o600)
print(json.dumps({'calls':24,'roots':12,'max_input_bound':max(a['input_token_upper_bound'] for a in assignments),'max_reservation':1.44,'gold_parser_checks':'24/24'}))
