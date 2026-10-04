"""Independent record checks: measured scores, paid-only truth, paired tapes and inputs."""
import argparse,hashlib,json,math
from pathlib import Path
from policies import ARMS,MODES,calibrate,initial,actor_input,estimate,choose

def verify(root,corpus):
    blocks=[json.loads(s) for s in (root/'episodes.jsonl').read_text().splitlines()];manifest=json.loads((root/'manifest.json').read_text());receipts=json.loads((root/'receipts.json').read_text());cal=calibrate(corpus[:20])
    assert [b['id'] for b in blocks]==manifest['ids'] and manifest['complete']
    assert all(r['valid'] for r in receipts)
    lookup={json.dumps(r['context'],sort_keys=True):r for r in receipts if r['context'].get('task') is not None}
    examined=0
    for b in blocks:
        record=corpus[b['id']];assert set(b['arms'])==set(ARMS)
        assert b['mode_scores']=={m:record['modes'][m]['evaluation']['recall'] for m in MODES}
        for arm,result in b['arms'].items():
            assert result['valid'] and len(result['checks'])<=2
            assert len({(c['mode'],c['region']) for c in result['checks']})==len(result['checks'])
            for c in result['checks']:assert c['quality']==record['modes'][c['mode']]['evaluation']['regions'][c['region']]
            assert abs(result['metrics']['quality']-b['mode_scores'][result['choice']])<1e-10
            for e in result['events']:
                allowed=initial(record,cal);allowed['checks']=result['checks'][:e['step']]
                assert e['before']==allowed
                if arm in ['single-agent','swarm-fixed']:
                    roles=[4] if arm=='single-agent' else range(5)
                    for vote_index,role in enumerate(roles):
                        context={'task':b['id'],'arm':'single-agent' if arm=='single-agent' else 'swarm','step':e['step'],'role':role}
                        r=lookup[json.dumps(context,sort_keys=True)]
                        assert r['state']==actor_input(allowed,role,arm=='single-agent')
                        assert r['choice']==e['votes'][vote_index]
                        assert r['input_hash']==hashlib.sha256(json.dumps([r['state'],r['question']],sort_keys=True).encode()).hexdigest()
                        examined+=1
        for i,e in enumerate(b['arms']['swarm-adaptive']['events']):
            fixed=b['arms']['swarm-fixed']['events'][i]
            assert e['votes']==fixed['votes'] and e['before']==fixed['before']
    result={'receipts':len(blocks),'paired_arm_outcomes':len(blocks)*len(ARMS),'model_inputs_verified':examined,'unique_images':len({r['image_sha256'] for r in corpus}),'checks':['assigned receipts complete','scores equal measured OCR table','QA exposes only purchased regional score','actor state equals allowlisted observations at that step','votes equal recorded model choices','input hashes match','adaptive ballots share the fixed prefix','budgets and check uniqueness'],'passed':True}
    (root/'integrity.json').write_text(json.dumps(result,indent=2));return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--corpus',type=Path,required=True);a=ap.parse_args();corpus=[json.loads(s) for s in a.corpus.read_text().splitlines()];print(json.dumps(verify(a.run,corpus),indent=2))
if __name__=='__main__':main()
