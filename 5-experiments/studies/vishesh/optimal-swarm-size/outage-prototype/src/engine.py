"""Same-world paired strategies; injected model transport; no implicit retries."""
import concurrent.futures,copy,json,time
from world import World,ARMS,digest
from checker import grade
from policies import reference_actions,should_contract
SYSTEM='You operate a synthetic incident-response tool environment. Return JSON with an actions list only. Use inspect, patch, or wait. A patch requires service, service_version, directory_version, capacity_version, and set with endpoint/protocol/pool. Inspect returns authoritative configuration and directory versions. Work from observed facts, never guess versions. Respect the shared tool capacity. Keep monitoring to window end. All available evidence is shared via tool results. Coordinate by actor identity to avoid duplicated repairs.'

def execute(case,arm,call=None,event=None,team_size=None,ownership=False):
    if arm not in ARMS:raise ValueError('unknown_arm')
    events=[]
    def emit(row):
        events.append(copy.deepcopy(row))
        if event:event(copy.deepcopy(row))
    w=World(case);n=1 if arm in ('single','scheduled') else (team_size or 4);slots=case.get('tool_slots',4)
    if n not in (1,4,8) or slots%n:raise ValueError('invalid_roster_capacity')
    violations=[];duplicates=0
    histories={i:[{'role':'system','content':SYSTEM}] for i in range(n)}
    started=time.monotonic();failure=None;calls=0;roster=[]
    try:
        for tick in range(case['horizon']):
            if arm=='contract' and n==4 and should_contract(w.receipts):
                emit({'kind':'contract','tick':tick,'before':4,'after':1,'in_flight':0});n=1
            obs=w.observation();roster.append(n);emit({'kind':'observation','tick':tick,'public':obs,'n':n})
            if arm=='scheduled':
                actions=[(0,a) for a in reference_actions(obs,limit=slots)]
            else:
                packets=[]
                for actor in range(n):
                    packet={'observation':obs,'actor':actor,'roster':list(range(n)),'max_actions':slots//n}
                    if ownership:
                        packet['ownership']={'owned_services':obs['service_ids'][actor::n],'rule':'Only inspect or patch your owned services. Ownership is exclusive; other actors repair their services. Use public tool receipts and current versions. You may wait when no repair is needed.'}
                    histories[actor]=histories[actor][:1]+histories[actor][1:][-2:]
                    histories[actor].append({'role':'user','content':json.dumps(packet,separators=(',',':'))})
                    packets.append((actor,copy.deepcopy(histories[actor])))
                def turn(packet):
                    actor,messages=packet
                    return actor,call(messages,actor,tick)
                # All calls admitted in this round drain before roster changes. Failure stops next round.
                with concurrent.futures.ThreadPoolExecutor(max_workers=n) as pool:
                    futures=[pool.submit(turn,p) for p in packets];calls+=len(futures)
                    answers=[f.result() for f in futures]
                actions=[]
                for actor,text in answers:
                    if not isinstance(text,str):raise ValueError('response_shape')
                    parsed=json.loads(text)
                    if set(parsed)!= {'actions'} or type(parsed['actions']) is not list or len(parsed['actions'])>slots//n:raise ValueError('response_shape')
                    histories[actor].append({'role':'assistant','content':text})
                    emit({'kind':'decision','actor':actor,'tick':tick,'answer':parsed})
                    for action in parsed['actions']:
                        if ownership and action.get('op') in ('inspect','patch') and action.get('service') not in obs['service_ids'][actor::n]:
                            violation={'kind':'ownership_rejection','actor':actor,'tick':tick,'action':action};violations.append(violation);emit(violation)
                        else:actions.append((actor,action))
            targets=[a.get('service') for _,a in actions if a.get('op')=='patch'];duplicates+=len(targets)-len(set(targets))
            receipts=w.step(actions)
            for world_event in w.events:
                if world_event['kind']=='world_change' and world_event['tick']==w.tick:emit(world_event)
            emit({'kind':'step','tick':w.tick,'receipts':receipts,'state':w.snapshot(),'health':w.health()})
        evaluation=grade(w.snapshot(),case['horizon'])
    except Exception as exc:
        # Transport uses safe categories; arbitrary exceptions are never logged.
        failure=getattr(exc,'code',None) or ('response_shape' if isinstance(exc,(ValueError,TypeError,KeyError)) else 'execution_failed')
        evaluation={'success':False,'quality':None,'unobserved':True}
    elapsed=time.monotonic()-started
    result={'case_id':case['case_id'],'case_sha256':digest(case),'root':case['root'],'cluster':case['cluster'],'changing':case['changing'],
            'ownership':ownership,'team_size':team_size,'ownership_violations':len(violations),'duplicate_patch_targets':duplicates,
            'arm':arm,'evaluation':evaluation,'failure':failure,'model_calls':calls,'elapsed_s':elapsed,'roster':roster,'ticks':w.tick,
            'stale_writes':sum(r['result']['status']=='stale_version' for r in w.receipts),'actions':len(w.receipts),'events':events}
    emit({'kind':'terminal','failure':failure,'evaluation':evaluation,'elapsed_s':elapsed})
    return result
