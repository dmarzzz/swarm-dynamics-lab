import collections,hashlib,json,sys
from pathlib import Path
import freshness as s

def audit(out):
 out=Path(out);m=json.loads((out/'manifest.json').read_text());summary=json.loads((out/'summary.json').read_text());rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()]
 key=lambda r:(r['case'],r['arm'],r['seed']);assert collections.Counter(map(key,rows))==collections.Counter(map(key,m['assigned'])) and len(rows)==12
 for r in rows:
  f,initial=s.fixture(r['case'],r['seed']);assert r['initial']==initial;peer=next(q for q in rows if q['case']==r['case'] and q['arm']!=r['arm']);assert r['advice']==peer['advice'] and s.digest(r['advice'])==r['proposal_hash'];assert len(r['trace'])==4;assert r['reviewer_epoch_errors']==sum(a['observed_epoch']!=initial['probe']['epoch'] for a in r['advice'])
  state=initial
  for x in r['trace']:
   o=x['observation'];assert o['cached_probe']==state['probe'] and o['current_epoch']==state['epoch'];assert 'case' not in o and 'live' not in o and 'health_probe' not in o
   if r['arm']=='checked':assert o['probe_receipt']==s.receipt(state['probe'],state['epoch'])
   else:assert 'probe_receipt' not in o
   after=x['state'];d=after['deployed'];c=f['catalog'];g=c['gateway'][str(d['gateway'])];w=c['worker'][str(d['worker'])];st=c['store'][str(d['store'])]
   checks={'rpc_compatible':g['requires_rpc']==w['rpc'],'data_readable':f['data'] in w['reads'],'storage_format':st['format']==f['data'],'requested_feature':f['feature'] in g['features'],'processes_live':all(after['live'].values())}
   assert checks==x['checks'] and x['healthy']==int(all(checks.values()))
   a=x['action'];role=next((k for k,v in f['alias'].items() if v==a['service']),None)
   if a['action']=='deploy' and not x['rejected']:
    same=state['deployed'][role]==a['version'];assert x['redundant']==int(same and state['live'][role]);assert x['useful_restart']==int(same and not state['live'][role]);assert after['epoch']==state['epoch']+1 and after['probe']==state['probe']
   state=after
  for metric,field in [('healthy_ticks','healthy'),('redundant','redundant'),('useful_restarts','useful_restart')]:assert r[metric]==sum(x[field] for x in r['trace'])
  frames=[e for e in events if e['kind']=='frame' and e['case']==r['case'] and e['arm']==r['arm']];assert len(frames)==4
  assert all(all(e[k]==v for k,v in x.items()) for x,e in zip(r['trace'],frames))
 assert sum(e['kind']=='advice' for e in events)==12 and sum(e['kind']=='decision' for e in events)==48 and not any(e['kind']=='error' for e in events)
 result={'assigned':12,'recorded':12,'paired_worlds':6,'advice_records':12,'decision_records':48,'source_records_identical_within_pairs':True,'all_frames_match':True,'health_and_restart_classification_recomputed':True,'paired_healthy_tick_deltas':{c:next(r['healthy_ticks'] for r in rows if r['case']==c and r['arm']=='checked')-next(r['healthy_ticks'] for r in rows if r['case']==c and r['arm']=='raw') for c in s.CASES}}
 if m['backend']=='anthropic':
  usage=[json.loads(x) for x in (out/'usage.jsonl').read_text().splitlines()];assert len(usage)==60 and all(x['actual_usd'] is not None for x in usage);assert abs(sum(x['actual_usd'] for x in usage)-summary['actual_usd'])<1e-9;result['usage_receipts']=60
  transport=[json.loads(x) for x in (out/'transport.jsonl').read_text().splitlines()];reqs=[x for x in transport if x['kind']=='request'];responses=[x for x in transport if x['kind']=='response'];assert len(reqs)==len(responses)==60
  assert {x['request_id'] for x in reqs}=={x['request_id'] for x in responses}=={x['request_id'] for x in usage}
  lookup={x['request_id']:x for x in usage}
  for x in reqs:assert hashlib.sha256(json.dumps(x['body']).encode()).hexdigest()==x['request_hash']==lookup[x['request_id']]['request_hash']
  assert all('headers' not in x for x in reqs+responses);result['credential_free_request_bodies']=60;result['pre_parse_response_bodies']=60
 (out/'audit.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))
