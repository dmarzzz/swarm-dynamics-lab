"""Offline freeze; no authority to allocate, amend ledger or dispatch."""
import hashlib,json
from pathlib import Path
import instrument as i
BASE=Path(__file__).resolve().parent

def freeze():
    worlds={c['id']:c for c in i.study.roots()}; initial={}; wires=[]
    for a in i.assignments():
        c=worlds[a['case_id']];o=i.study.observation(c,c['initial'],1,[])
        initial[a['id']]={'observation_sha256':i.digest(o),'diagnosis_wire_sha256':i.digest(i.request(c,o,'diagnosis')[1])}
        row=i.episode(c,a)
        wires.extend(len(json.dumps(e['wire']).encode()) for e in row['events'])
    sources={}
    for directory in ('src','scenario-study','evidence-study','freshness-study','controller-study','verification-study'):
        for p in sorted((BASE.parent/directory).rglob('*.py')):
            sources[str(p.relative_to(BASE.parent))]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in (BASE/'PLAN.md',BASE/'RUNBOOK.md'):
        sources[str(p.relative_to(BASE.parent))]=hashlib.sha256(p.read_bytes()).hexdigest()
    packet={'stage':'verification-v1','status':'offline_frozen_unfunded','model':i.MODEL,
            'schedule_seed':i.SEED,'assignments':i.assignments(),'initial_inputs':initial,
            'max_calls':192,'max_wire_bytes':8000,'max_output_tokens':512,
            'offline_rule_max_wire_bytes':max(wires),'input_rate_usd_per_million':5,'output_rate_usd_per_million':25,
            'rates_status':'proposal; reverify exact route and rates before admission',
            'request_reservation_formula':'((wire_bytes+512)*5+512*25)/1000000',
            'max_request_usd':0.055360,'model_max_usd':10.629120,'infrastructure_max_usd':0.15,'all_in_max_usd':10.779120,
            'prior_calls':517,'prior_reserved_usd':6.248035,'current_model_cap_usd':8,
            'required_model_cap_usd':16.877155,'native_dispatch_enabled':False,'successor_authorized':False,
            'source_sha256':sources}
    (BASE/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
    return packet
if __name__=='__main__':freeze()
