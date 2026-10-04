"""Bounded paired S0/S1 worker; measured truth is accessed only through QA and scoring."""
import argparse,hashlib,json,os,subprocess,time,traceback
from pathlib import Path
from policies import ARMS,calibrate,policy,evaluate,budget_oracle
from runtime import Runtime

class Bounded:
    def __init__(self,base,limit=1100):self.base=base;self.limit=limit
    def choose(self,*args):
        if len(self.base.receipts)>=self.limit:raise RuntimeError('call_cap')
        return self.base.choose(*args)

def dump(p,x):p.write_text(json.dumps(x,indent=2))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--corpus',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--stage',choices=['S0','S1'],required=True);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    records=[json.loads(x) for x in (a.corpus/'measured.jsonl').read_text().splitlines()]
    assert len(records)==100 and all(v['valid'] for r in records for v in r['modes'].values())
    assert json.loads((a.corpus/'calibration.json').read_text())['routing_relevance_gate']
    cal=calibrate(records[:20]);dump(a.out/'calibration.json',cal)
    manifest={'stage':a.stage,'complete':False,'source':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'corpus_sha256':hashlib.sha256((a.corpus/'measured.jsonl').read_bytes()).hexdigest(),'ids':list(range(20,30) if a.stage=='S0' else range(30,100)),'arms':ARMS,'physical_call_cap':124 if a.stage=='S0' else 840,'seed':71,'utc_start':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    dump(a.out/'manifest.json',manifest)
    import swarm_report as sr
    exp='antsy-verification-v4';rid=f'{exp}/{a.stage}-attempt-1'
    url=f'https://github.com/dmarzzz/swarm-lab/tree/{manifest["source"]}/researchers/vishesh/notes/antsy-verification-v4'
    sr.register(exp,title='Antsy: test before trust',description='Can five local decision agents buy useful verification for real receipt OCR? Compare a fixed configuration, confidence and deterministic controls. Exploratory, ideal QA, no paid API.',owner='vishesh',params={'stage':{'type':'str','role':'stage'},'backend':{'type':'str','role':'fixed'}},metrics=['completed','invalid','mean_regret','mean_checks'],primary_metric='mean_regret',url=url)
    sr.report('start',exp,rid,params={'stage':a.stage,'backend':'local-laya','code':manifest['source'][:12],'kind':'qualification' if a.stage=='S0' else 'experiment'},url=url,strict=True)
    rt=None;outcomes=[];start=time.monotonic()
    try:
        rt=Runtime();bounded=Bounded(rt,manifest['physical_call_cap']);manifest['runtime']=rt.metadata
        if a.stage=='S0':
            probes=[]
            for answer in ['A','B','C','STOP']:
                result=bounded.choose('Interface calibration. The required response is '+answer+'.','Select exactly the required response.',{'A':'A','B':'B','C':'C','STOP':'STOP'},{'kind':'interface','target':answer})
                probes.append({'target':answer,'choice':result,'correct':answer==result})
            dump(a.out/'interface.json',probes)
            if not any(p['correct'] for p in probes):raise RuntimeError('all_interface_probes_failed')
            # Partial semantic failures are disclosed; do not tune policies on outcomes.
        with (a.out/'episodes.jsonl').open('x') as stream:
            for i in manifest['ids']:
                record=records[i];block={'id':i,'arms':{},'mode_scores':{m:v['evaluation']['recall'] for m,v in record['modes'].items()},'budget_oracle':budget_oracle(record,cal)}
                for arm in ARMS:
                    tape=[e['votes'] for e in block['arms']['swarm-fixed']['events']] if arm=='swarm-adaptive' else None
                    result=policy(record,cal,arm,bounded,tape=tape);result['metrics']=evaluate(record,result);block['arms'][arm]=result
                    if not result['valid']:
                        stream.write(json.dumps(block)+'\n');stream.flush();raise RuntimeError('actor_execution_failure')
                stream.write(json.dumps(block)+'\n');stream.flush();outcomes.append(block)
                dump(a.out/'receipts.json',rt.receipts)
                sr.report('progress',exp,rid,step=len(outcomes),total=len(manifest['ids']),metrics={'completed':len(outcomes),'invalid':0,'mean_regret':sum(b['arms']['swarm-adaptive']['metrics']['regret'] for b in outcomes)/len(outcomes),'mean_checks':sum(b['arms']['swarm-adaptive']['metrics']['checks'] for b in outcomes)/len(outcomes)},strict=True)
        manifest.update(complete=True,completed=len(outcomes),physical_calls=len(rt.receipts),invalid=sum(not r['valid'] for r in rt.receipts),wall_s=time.monotonic()-start)
        dump(a.out/'manifest.json',manifest)
        # Render only after durable outcomes. A presentation fault cannot lose a measurement.
        from render import render_all
        render_all(outcomes,a.out,a.stage)
        for p in a.out.iterdir():
            if p.suffix in ('.png','.gif','.json','.jsonl'):sr.upload(rid,p,p.name)
        sr.report('done',exp,rid,metrics={'completed':len(outcomes),'invalid':0},message='Paired measured-receipt study complete. See results and post-mortem; completion does not imply swarm benefit.',strict=True)
        print(json.dumps({'stage':a.stage,'completed':len(outcomes),'calls':len(rt.receipts),'invalid':manifest['invalid']}))
    except Exception as exc:
        manifest.update(error=type(exc).__name__,completed=len(outcomes),wall_s=time.monotonic()-start)
        dump(a.out/'manifest.json',manifest)
        if rt:dump(a.out/'receipts.json',rt.receipts)
        sr.report('fail',exp,rid,message='Execution or publication failed: '+type(exc).__name__+'. Durable attempt retained for diagnosis.',strict=True)
        raise

if __name__=='__main__':main()
