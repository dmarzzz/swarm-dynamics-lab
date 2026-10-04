"""Rebuild deterministic software-fixture evidence, never native/model execution."""
import hashlib,json
from pathlib import Path
from worlds import World,ROOTS,STRUCTURE,probes
from broker import scripted_run

out=Path(__file__).resolve().parent/'validation';out.mkdir(exist_ok=True)
rows=[];max_packet=0
for root in ROOTS:
    for condition in ('fault','clean','missing'):
        for n in (1,3):
            w=World(root,condition);start=w.start();initial=probes(root,w.state);b,r=scripted_run(w,n)
            assert r['joint_correct']
            if condition!='fault':assert b.rounds<=4
            size=max(len(json.dumps(b.packet(a)).encode()) for a in range(n));max_packet=max(max_packet,size)
            record={'kind':'SCRIPTED_UNIT_FIXTURE_NOT_MODEL_EVIDENCE','root':root,'structure':STRUCTURE[root],'condition':condition,'contexts':n,'public_start':start,'initial_probes':initial,'events':b.events,'answer':b.answer,'grade':r,'rounds':b.rounds,'final_packet_bytes':size}
            p=out/f'{root}-{condition}-n{n}.json';p.write_text(json.dumps(record,indent=2)+'\n')
            rows.append({'root':root,'condition':condition,'n':n,'rounds':b.rounds,'grade':r,'max_round_tool_units':max(e['tool_units'] for e in b.events),'artifact':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
summary={'native_calls':0,'native_repetitions':0,'validated_authored_mechanisms':6,'independent_field_incidents':0,'fixtures':36,'all_reference_fixtures_pass':True,'max_control_rounds':max(x['rounds'] for x in rows if x['condition']!='fault'),'max_fault_rounds':max(x['rounds'] for x in rows if x['condition']=='fault'),'max_serialized_public_packet_bytes':max_packet,'scope':'Unit fixture truth/reference/broker validation only; not native competence, fresh replication, field realism or broad causal evidence.','rows':rows}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
