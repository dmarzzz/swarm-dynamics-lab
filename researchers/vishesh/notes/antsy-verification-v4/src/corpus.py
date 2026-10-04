"""Measure OCR on externally authored, revision-pinned CORD receipts."""
import argparse,collections,csv,hashlib,io,json,os,re,subprocess,time,urllib.request
from pathlib import Path
import pyarrow.parquet as pq
from PIL import Image

REV='7f0115a4b758a71d6473b8d085751692da2fef98'
FILE='data/validation-00000-of-00001-cc3c5779fe22e8ca.parquet'
MODES={'A':3,'B':6,'C':11}

def tokens(s):return re.findall(r'\w+',s.casefold())
def bounds(word):
    q=word['quad'];return min(q[f'x{i}'] for i in range(1,5)),min(q[f'y{i}'] for i in range(1,5)),max(q[f'x{i}'] for i in range(1,5)),max(q[f'y{i}'] for i in range(1,5))

def score(lines,words,height):
    refs=[]
    for line in lines:
        bs=[bounds(w) for w in line['words']]
        if not bs:continue
        box=(min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs))
        refs.append({'box':box,'text':' '.join(w['text'] for w in line['words']),'category':line['category'],'region':min(2,int(((box[1]+box[3])/2)/height*3)),'pred':[]})
    for w in words:
        x=w['left']+w['width']/2;y=w['top']+w['height']/2
        candidates=[(abs(y-(r['box'][1]+r['box'][3])/2),i) for i,r in enumerate(refs) if r['box'][0]-4<=x<=r['box'][2]+4 and r['box'][1]-4<=y<=r['box'][3]+4]
        if candidates:refs[min(candidates)[1]]['pred'].append(w['text'])
    region=[{'matched':0,'target':0} for _ in range(3)];details=[]
    for r in refs:
        g=collections.Counter(tokens(r['text']));p=collections.Counter(tokens(' '.join(r['pred'])));match=sum((g&p).values());n=sum(g.values());reg=region[r['region']];reg['matched']+=match;reg['target']+=n
        details.append({'category':r['category'],'region':r['region'],'matched':match,'target':n,'exact':g==p})
    total=sum(r['target'] for r in region)
    return {'recall':sum(r['matched'] for r in region)/total if total else None,'regions':[r['matched']/r['target'] if r['target'] else None for r in region],'denominators':[r['target'] for r in region],'line_details':details,'total_field_exact':all(r['exact'] for r in details if r['category']=='total.total_price') if any(r['category']=='total.total_price' for r in details) else None}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    manifest={'dataset':'naver-clova-ix/cord-v2','revision':REV,'split':'validation','assigned_ids':list(range(100)),'complete':False,'license':'CC-BY-4.0','psm':MODES,'languages':'ind+eng','tesseract':subprocess.check_output(['tesseract','--version'],text=True).splitlines()[0]}
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    parquet=a.out/'source.parquet';urllib.request.urlretrieve(f'https://huggingface.co/datasets/naver-clova-ix/cord-v2/resolve/{REV}/{FILE}',parquet)
    manifest['parquet_sha256']=hashlib.sha256(parquet.read_bytes()).hexdigest();table=pq.read_table(parquet).to_pylist();assert len(table)==100
    records=[]
    with (a.out/'measured.jsonl').open('x') as stream:
        for i,row in enumerate(table):
            raw=row['image']['bytes'];path=a.out/f'receipt-{i:03}.png';path.write_bytes(raw);im=Image.open(path);gt=json.loads(row['ground_truth'])
            rec={'id':i,'image_sha256':hashlib.sha256(raw).hexdigest(),'width':im.width,'height':im.height,'modes':{}}
            for mode,psm in MODES.items():
                start=time.monotonic()
                try:
                    run=subprocess.run(['tesseract',str(path),'stdout','-l','ind+eng','--psm',str(psm),'tsv'],capture_output=True,text=True,timeout=30,env=dict(os.environ,OMP_THREAD_LIMIT='1'))
                    if run.returncode:raise RuntimeError('ocr_nonzero_exit')
                    words=[]
                    for w in csv.DictReader(io.StringIO(run.stdout),delimiter='\t'):
                        if w.get('text','').strip() and float(w['conf'])>=0:words.append({k:float(w[k]) for k in ('left','top','width','height','conf')}|{'text':w['text']})
                    scores=score(gt['valid_line'],words,im.height)
                    regions=[]
                    for region in range(3):
                        ws=[w for w in words if min(2,int((w['top']+w['height']/2)/im.height*3))==region]
                        regions.append({'confidence':sum(w['conf'] for w in ws)/len(ws)/100 if ws else 0,'words':len(ws)})
                    rec['modes'][mode]={'valid':True,'wall_s':time.monotonic()-start,'observations':regions,'evaluation':scores}
                    (a.out/f'ocr-{i:03}-{mode}.tsv').write_text(run.stdout)
                except Exception as exc:rec['modes'][mode]={'valid':False,'error':type(exc).__name__,'wall_s':time.monotonic()-start}
            stream.write(json.dumps(rec)+'\n');stream.flush();records.append(rec)
    manifest.update(complete=True,completed=len(records),invalid=sum(not m['valid'] for r in records for m in r['modes'].values()))
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    cal=records[:20];assert all(m['valid'] for r in cal for m in r['modes'].values())
    means={m:sum(r['modes'][m]['evaluation']['recall'] for r in cal)/20 for m in MODES};best=max(means,key=means.get);oracle=sum(max(r['modes'][m]['evaluation']['recall'] for m in MODES) for r in cal)/20
    report={'calibration_n':20,'mode_mean_recall':means,'best_fixed':best,'oracle_gain_over_best_fixed':oracle-means[best],'winner_counts':dict(collections.Counter(max(MODES,key=lambda m:r['modes'][m]['evaluation']['recall']) for r in cal)),'routing_relevance_gate':oracle-means[best]>=.01,'invalid':manifest['invalid']}
    (a.out/'calibration.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
