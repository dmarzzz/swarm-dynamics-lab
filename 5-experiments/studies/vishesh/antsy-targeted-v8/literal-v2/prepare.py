import argparse,json
from pathlib import Path
from PIL import Image
from contract import sha,digest,order

def prepare(corpus,out):
 out.mkdir(mode=0o700,exist_ok=False);(out/'images').mkdir();cases=[];specs={}
 frozen=json.loads((corpus/'freeze.json').read_text())
 for stage,split,lo in [('Q1','qualification',2),('E1','evaluation',0)]:
  ap=corpus/split/'actor/manifest.json';gp=corpus/split/'evaluator/gold.json'
  assert sha(ap)==frozen['splits'][split]['actor_sha256'] and sha(gp)==frozen['splits'][split]['gold_sha256']
  aa=json.loads(ap.read_text())['cases'][lo:];gg=json.loads(gp.read_text())['cases'][lo:]
  for i,(a,g) in enumerate(zip(aa,gg)):
   assert a['id']==g['id'];original=corpus/split/'actor'/a['image'];assert sha(original)==a['sha256']
   im=Image.open(original).convert('RGB');im.thumbnail((1536,1536));identity='V2-'+stage+'-'+a['id'];dest=out/'images'/(identity+'.png');im.save(dest)
   c={'id':identity,'stage':stage,'image':dest.name,'image_sha256':sha(dest),'gold':g['value'],'index':i,'source_row':g['source_row']};cases.append(c)
   for kind in order(stage,i):specs[identity+'-'+kind]={'case':identity,'stage':stage,'kind':kind,'image':dest.name,'image_sha256':sha(dest)}
 assert len(cases)==22 and len(specs)==92
 (out/'cases.json').write_text(json.dumps(cases,indent=2));(out/'specs.json').write_text(json.dumps(specs,indent=2))
 return {'cases':22,'calls':92,'qualification_receipts':4,'evaluation_receipts':18,'cases_sha256':sha(out/'cases.json'),'specs_sha256':sha(out/'specs.json'),'images':{c['id']:c['image_sha256'] for c in cases}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--corpus',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--public',type=Path,required=True);a=p.parse_args();r=prepare(a.corpus,a.out);a.public.write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ('cases','calls','qualification_receipts','evaluation_receipts')}))
