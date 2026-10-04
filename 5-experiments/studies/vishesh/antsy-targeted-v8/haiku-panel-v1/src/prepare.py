"""Create private delivered-image payloads and evaluator references from frozen cases."""
import argparse,json,os
from pathlib import Path
from PIL import Image
from design import request,digest,sha,role

def prepare(corpus,out):
    out.mkdir(mode=0o700,exist_ok=False);(out/'images').mkdir(mode=0o700)
    freeze=json.loads((corpus/'freeze.json').read_text());cases=[];allowed={}
    for stage,split,n in [('Q0','qualification',2),('E0','evaluation',18)]:
        actor=corpus/split/'actor/manifest.json';truth=corpus/split/'evaluator/gold.json'
        if sha(actor)!=freeze['splits'][split]['actor_sha256'] or sha(truth)!=freeze['splits'][split]['gold_sha256']:raise ValueError('freeze_mismatch')
        manifest=json.loads(actor.read_text())['cases'];gold=json.loads(truth.read_text())['cases']
        for a,g in zip(manifest[:n],gold[:n]):
            if a['id']!=g['id']:raise ValueError('case_pair_mismatch')
            original=corpus/split/'actor'/a['image']
            if sha(original)!=a['sha256']:raise ValueError('image_mismatch')
            image=Image.open(original).convert('RGB');image.thumbnail((1536,1536))
            identity=stage+'-'+a['id'];dest=out/'images'/(identity+'.png');image.save(dest)
            data=dest.read_bytes()
            cases.append({'id':identity,'stage':stage,'image':dest.name,'image_sha256':sha(dest),'original_sha256':a['sha256'],
                          'size':list(image.size),'gold':g['value']})
            for seat in range(1,41):allowed[f'{identity}-a{seat:02d}']=digest(request(data,seat))
    (out/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');(out/'allowlist.json').write_text(json.dumps(allowed,indent=2)+'\n')
    return {'case_count':len(cases),'assignment_count':len(allowed),'case_sha256':sha(out/'cases.json'),'allowlist_sha256':sha(out/'allowlist.json'),
            'image_hashes':{c['id']:c['image_sha256'] for c in cases},'delivered_max_edge':1536,'corpus_freeze_sha256':sha(corpus/'freeze.json')}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--corpus',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--public',type=Path,required=True);a=p.parse_args();os.umask(0o077)
    report=prepare(a.corpus,a.out);a.public.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'cases':report['case_count'],'assignments':report['assignment_count']}))
