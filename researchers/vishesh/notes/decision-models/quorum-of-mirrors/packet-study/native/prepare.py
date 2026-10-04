from pathlib import Path
import argparse,json,hashlib
from contract import ATTEMPT,request,digest,bound,RESERVE
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--custody',type=Path,required=True);p.add_argument('--private-out',type=Path,required=True);a=p.parse_args()
seal=json.loads((HERE.parent/'SEAL.json').read_text());raw=(a.custody/'qualification.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()==seal['splits']['qualification']['corpus_sha256']
rows=json.loads(raw);rows.sort(key=lambda r:hashlib.sha256(('PQ-order-v1'+r['id']).encode()).hexdigest())
assignments=[]
for i,row in enumerate(rows):
 req=request(row['actor']);b=bound(req);assert b<=6000
 assignments.append({'id':ATTEMPT+f'-{i:03}','case_id':row['id'],'request_sha256':digest(req),'input_token_upper_bound':b,'reserve_usd':RESERVE,
 'tldr':f"One source-first Sonnet decision; copies={row['condition']['copies']}, inverted={row['condition']['inverted']}; compare fixed source majority, fidelity and quote validity; synthetic qualification only."})
manifest={'attempt':ATTEMPT,'stage':'qualification_only','corpus_sha256':hashlib.sha256(raw).hexdigest(),'assignments':assignments,'max_calls':24,'max_reserved_usd':.72,'evaluation_dispatch':False}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
a.private_out.write_text(json.dumps({'manifest':manifest,'rows':rows}));a.private_out.chmod(0o600)
print(json.dumps({'assignments':len(rows),'max_input_token_bound':max(x['input_token_upper_bound'] for x in assignments),'max_reservation':.72,'sealed_evaluation_opened':False}))
