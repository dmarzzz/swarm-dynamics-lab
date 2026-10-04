"""Pin real cases without exposing qualification/evaluation contents to the operator."""
import argparse
from collections import Counter
from decimal import Decimal
import io
import json
from pathlib import Path
import re
from common import digest,sha,write

SPLITS={'development':list(range(80,92)),'qualification':list(range(100,106)),'evaluation':list(range(120,138))}
REV='7f0115a4b758a71d6473b8d085751692da2fef98'
SHARD_SHA256='da3994eee1bf9bd3c57f0d53a72c3a6812c8696c5ba26245987949ddf73483cc'


def label(text):
    # Independent total-label grammar, not imported from either predictor.
    if not isinstance(text,str):return None
    s=re.sub(r'^(?:Rp\.?|IDR)\s*','',text.strip(),flags=re.I).replace(' ','')
    if re.fullmatch(r'\d{1,3}(?:[.,]\d{3})+',s):s=re.sub(r'[.,]','',s)
    elif re.fullmatch(r'\d+(?:[.,]\d{2})?',s):s=s.replace(',','.')
    elif re.fullmatch(r'\d{1,3}(?:\.\d{3})+,\d{2}',s):s=s.replace('.','').replace(',','.')
    elif re.fullmatch(r'\d{1,3}(?:,\d{3})+\.\d{2}',s):s=s.replace(',','')
    else:return None
    return format(Decimal(s),'.2f')


def build(parquet,out,qa):
    import pyarrow.parquet as pq
    from PIL import Image
    if sha(parquet)!=SHARD_SHA256:raise ValueError('dataset_shard_mismatch')
    out.mkdir(mode=0o700,exist_ok=False)
    rows=pq.read_table(parquet).to_pylist()
    result={'dataset':'naver-clova-ix/cord-v2','revision':REV,'shard_sha256':sha(parquet),'splits':{}}
    for split,indices in SPLITS.items():
        d=out/split; (d/'actor').mkdir(parents=True,mode=0o700);(d/'evaluator').mkdir(mode=0o700)
        actors=[];gold=[];counts=Counter();seen=set()
        for offset,index in enumerate(indices):
            item=rows[index];gt=json.loads(item['ground_truth']);raw=item['image']['bytes']
            image=Image.open(io.BytesIO(raw));image.verify();image=Image.open(io.BytesIO(raw));width,height=image.size
            identity=f'case-{offset+1:03d}'
            target=gt.get('gt_parse',{}).get('total',{})
            value=label(target.get('total_price')) if isinstance(target,dict) else None
            total_lines=[line for line in gt.get('valid_line',[]) if line.get('category')=='total.total_price']
            witnesses=[]
            for line in total_lines:
                candidates=[label(w['text']) for w in line['words']]
                candidates=[v for v in candidates if v is not None]
                if len(candidates)==1:witnesses.append(candidates[0])
            consistent=value is not None and value in witnesses
            counts['scorable']+=value is not None;counts['line_corroborated']+=consistent
            counts['large_image']+=width*height>1_000_000
            counts['has_quantity']+=any('qty' in str(line.get('category','')) for line in gt.get('valid_line',[]))
            counts['has_subtotal']+=any('subtotal' in str(line.get('category','')) for line in gt.get('valid_line',[]))
            dest=d/'actor'/f'{identity}.png'
            image.convert('RGB').save(dest)
            image_hash=sha(dest);counts['duplicate_images']+=image_hash in seen;seen.add(image_hash)
            actors.append({'id':identity,'image':dest.name,'sha256':image_hash,'width':width,'height':height})
            gold.append({'id':identity,'source_row':index,'value':value,'status':'ok' if value is not None else 'unscorable',
                         'label_corroborated':consistent,'source_total_sha256':digest(target)})
            if split=='development':
                # Total-field crops only, never full customer receipt publication.
                boxes=[w.get('quad',{}) for line in total_lines for w in line['words']]
                if boxes:
                    xs=[b[k] for b in boxes for k in ('x1','x2','x3','x4')];ys=[b[k] for b in boxes for k in ('y1','y2','y3','y4')]
                    crop=image.crop((max(0,min(xs)-8),max(0,min(ys)-8),min(width,max(xs)+8),min(height,max(ys)+8)))
                    crop.save(d/'evaluator'/f'{identity}-total.png')
        write(d/'actor'/'manifest.json',{'cases':actors});write(d/'evaluator'/'gold.json',{'cases':gold})
        result['splits'][split]={'count':len(indices),'source_rows':indices,'actor_sha256':sha(d/'actor'/'manifest.json'),
          'gold_sha256':sha(d/'evaluator'/'gold.json'),'counts':dict(counts)}
    write(out/'freeze.json',result);write(qa,result)
    print(json.dumps({'counts':{s:v['counts'] for s,v in result['splits'].items()},'new_model_calls':0}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parquet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--qa',type=Path,required=True);a=p.parse_args();build(a.parquet,a.out,a.qa)
