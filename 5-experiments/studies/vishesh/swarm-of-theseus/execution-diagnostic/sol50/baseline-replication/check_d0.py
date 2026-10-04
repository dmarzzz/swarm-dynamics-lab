"""Full offline case/contract audit, public development inputs only."""
from pathlib import Path
import copy,json,random,collections
import families as f,contract as c
from development import dev_world

def actor(w,p,note=None):return {'position':p,'roster':list(w['members']),'private_note':copy.deepcopy(note),'current_observations':[]}
def schedule():
 rows=[('common','learn')]*6+[('common',phase) for phase in ('select','attest','decide') for _ in range(6)]
 for arm in ('interactive','static','broken','retained'):
  phases=('question','teach','commit') if arm=='interactive' else ('teach','question','commit') if arm=='static' else ('commit',) if arm=='broken' else ()
  rows.extend((arm,phase) for _ in range(6) for phase in phases)
  rows.extend((arm,phase) for phase in ('select','attest','decide') for _ in range(6))
 return rows

def run():
 stats=collections.Counter();maxwire=collections.Counter();maxreply=0;examples=[]
 def check(phase,family,p):
  wire=c.wire(phase,family,p);maxwire[phase]=max(maxwire[phase],len(json.dumps(wire,separators=(',',':')).encode()))
 for seed in range(8600,8606):
  w=dev_world(seed)
  for family in f.FAMILIES:
   stats['development_institutions']+=1
   notes={}
   for owner in w['members']:
    h=f.history(w,family,owner);pair=f.infer(owner,[p for p in w['members'] if p!=owner],h);notes[owner]={'witnesses':pair};stats['unique_founder_policies']+=1
    p=actor(w,owner);p['history']=h;check('learn',family,p)
    for kind in f.KINDS:
     for variant in f.VARIANTS[family] if kind=='invalid' else [None]:
      case=f.example(w,family,owner,kind,variant);records=case['private_records']+case['public_records'];rng=random.Random(seed);rng.shuffle(records)
      assert f.decide(pair,records,case['target'])==case['gold'];stats['declared_labels_checked']+=1
      wrongcase=copy.deepcopy(case['target']);wrongcase['case']='not-this-case';assert f.decide(pair,records,wrongcase)=='defer';stats['scope_negative_controls']+=1
    if seed==8600 and owner==w['members'][0]:
     for kind in ('allow','invalid','irrelevant_veto'):examples.append(f.example(w,family,owner,kind))
   for changed in (False,True):
    # Simple controller derives changes solely from public-to-this-owner history.
    current=copy.deepcopy(notes)
    for owner in w['members']:
     if changed and set(w['routes'][owner])!=set(w['changed_routes'][owner]):current[owner]={'witnesses':f.infer(owner,[p for p in w['members'] if p!=owner],f.history(w,family,owner,True))}
    cases={p:f.panel(w,family,p,index=seed,changed=changed) for p in w['members']};inboxes={p:[] for p in w['members']};delivered={p:[] for p in w['members']}
    for owner in w['members']:
     p=actor(w,owner,notes[owner]);p['current_observations']=f.history(w,family,owner,True) if changed and current[owner]!=notes[owner] else [];check('select',family,p)
     for peer in current[owner]['witnesses']:inboxes[peer].extend(f.witness_inbox(cases[owner],peer))
    assert all(len(inbox)==2 for inbox in inboxes.values())
    for peer,inbox in inboxes.items():
     p=actor(w,peer,current[peer]);p['private_inbox']=inbox;check('attest',family,p)
     response={'reports':[{'owner':row['owner'],'evidence_ids':[r['id'] for r in row['records']]} for row in inbox]};maxreply=max(maxreply,len(json.dumps(response,separators=(',',':')).encode()))
     for report in response['reports']:
      # Addressed envelope controls delivery, including deliberately wrong owner metadata.
      delivered[report['owner']]+=f.hydrate(peer,inbox,{'reports':[report]})
     stats['witness_inboxes_checked']+=1
    for owner in w['members']:
     packet=f.decision_packet(owner,current[owner],cases[owner],delivered[owner]);check('decide',family,packet)
     rows=[{'case':x['target']['case'],'action':f.decide(current[owner]['witnesses'],packet['received_records']+packet['public_audit_records'],x['target'])} for x in cases[owner]]
     score=f.score({'actions':rows},cases[owner]);assert score['correct']==6 and score['harmful']==0;stats['controller_correct_actions']+=6
     if changed and current[owner]!=notes[owner]:
      oldrows=[{'case':x['target']['case'],'action':f.decide(notes[owner]['witnesses'],packet['received_records']+packet['public_audit_records'],x['target'])} for x in cases[owner]]
      assert f.score({'actions':oldrows},cases[owner])['correct']<6;stats['stale_policy_negative_controls']+=1
     q={'position':owner,'inherited_note':notes[owner]};check('question',family,q)
     teach=actor(w,owner,notes[owner]);teach['question']={'question':'Which locally learned sources should be retained?'};check('teach',family,teach)
     message={'note':notes[owner],'explanation':'Retain the two local sources; revise only from identifying new evidence.'}
     for arm in ('interactive','static','broken'):
      p=c.successor(owner,w['members'],arm,notes[owner] if arm!='broken' else None,message if arm!='broken' else None,{'question':'Private inspection'} if arm=='static' else None);check('commit',family,p)
 rows=schedule();assert len(rows)==138
 result={'evidence_type':'offline public development only; not model results','checks':dict(stats),'wire_max_bytes_by_phase':dict(maxwire),'wire_limit_bytes':6500,'maximum_exact_witness_response_bytes':maxreply,'no_truncation':True,'schedule_calls_per_execution':len(rows),'schedule_calls_by_arm':dict(collections.Counter(a for a,p in rows)),'shared_founding_checkpoint_calls':18,'terminal_checkpoint_calls':72,'family_count':3,'fresh_native_replications':0,'native_calls':0,'sealed_worlds_opened':False,'stage_caps':{k:{'calls':v[0],'model_usd':float(v[1])} for k,v in c.STAGES.items()},'all_R3_infrastructure_cap_usd':1,'through_P1_additional_cap_usd':22.2004,'through_P2_additional_cap_usd':40.9546,'prior_exposure_usd':1.1637270437,'through_P2_study_cumulative_usd':42.1183270437,'remaining_runtime_work':['Integrate these pure contracts into a source-pinned native worker; old SOL50 launcher is incompatible','Validate actual portfolio reservation, stage admission, source/runtime and exclusive claim; no generic guard grants authority','Freeze uninspected qualification/evaluation worlds and native prompt snapshots after offline development','Record exact post-retirement identity resolution and per-world/repeat/stratum output in integrated runner']}
 base=Path(__file__).resolve().parent;(base/'D0-AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');(base/'CASE-EXAMPLES.json').write_text(json.dumps(examples,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':run()
