"""Measure real OCR/checker candidates without reference-guided crops or hints."""
import argparse,collections,csv,hashlib,io,json,os,subprocess,time,urllib.request
from pathlib import Path
from PIL import Image,ImageOps
from contract import extract,reference
REV='7f0115a4b758a71d6473b8d085751692da2fef98'
PIPELINES={'A':(3,False),'B':(6,False),'C':(11,False),'D':(6,True),'E':(11,True)}

def lines_from_tsv(raw):
    words=[]
    for w in csv.DictReader(io.StringIO(raw),delimiter='\t',quoting=csv.QUOTE_NONE):
        if w.get('text','').strip() and float(w['conf'])>=0:
            words.append({'text':w['text'],'confidence':float(w['conf'])/100,'x':int(w['left']),'y':int(w['top'])+int(w['height'])/2,'h':int(w['height'])})
    groups=[]
    for w in sorted(words,key=lambda w:(w['y'],w['x'])):
        eligible=[g for g in groups if abs(w['y']-g['y'])<=max(3,min(w['h'],g['h'])*.5)]
        if eligible:g=min(eligible,key=lambda g:abs(w['y']-g['y']));g['words'].append(w)
        else:groups.append({'y':w['y'],'h':w['h'],'words':[w]})
    return [{'text':' '.join(w['text'] for w in sorted(g['words'],key=lambda w:w['x'])),'confidence':sum(w['confidence'] for w in g['words'])/len(g['words'])} for g in groups]

def measure(row,ident,split,private):
    raw=row['image']['bytes'];image=private/f'{split}-{ident}.png';image.write_bytes(raw);gt=json.loads(row['ground_truth'])
    record={'id':ident,'split':split,'image_sha256':hashlib.sha256(raw).hexdigest(),'pipelines':{}}
    for name,(psm,transform) in PIPELINES.items():
        start=time.monotonic()
        try:
            path=image
            if transform:
                with Image.open(image) as im:
                    im=ImageOps.autocontrast(im.convert('L'));im=im.resize((im.width*2,im.height*2));path=private/f'{split}-{ident}-{name}.png';im.save(path)
            r=subprocess.run(['tesseract',str(path),'stdout','-l','ind+eng','--psm',str(psm),'tsv'],capture_output=True,text=True,timeout=30,env=dict(os.environ,OMP_THREAD_LIMIT='1'))
            if r.returncode:raise RuntimeError('ocr_exit')
            lines=lines_from_tsv(r.stdout);candidate=extract(lines)
            record['pipelines'][name]={'candidate':candidate,'wall_s':time.monotonic()-start,'valid':True}
            (private/f'{split}-{ident}-{name}.tsv').write_text(r.stdout)
            if name=='B':
                import re
                header=' '.join(x['text'].casefold() for x in lines[:3]);header=re.sub(r'[^a-z]+',' ',header).strip()
                record['header_fingerprint']=hashlib.sha256(header.encode()).hexdigest() if header else None
        except Exception as e:record['pipelines'][name]={'candidate':{'status':'error','value':None,'confidence':0.},'wall_s':time.monotonic()-start,'valid':False,'error':type(e).__name__}
    # Truth is attached only after every pixel-only pipeline returns.
    record['gold']=reference(gt)
    return record

def dataset(split,private):
    url=f'https://huggingface.co/api/datasets/naver-clova-ix/cord-v2/tree/{REV}/data'
    with urllib.request.urlopen(url,timeout=30) as r:files=json.load(r)
    files=sorted(x['path'] for x in files if x['path'].startswith('data/'+split+'-') and x['path'].endswith('.parquet'))
    if not files:raise ValueError('missing split')
    # The planned prefix fits within the first shard; verify row count at caller.
    dest=private/(split+'.parquet');urllib.request.urlretrieve(f'https://huggingface.co/datasets/naver-clova-ix/cord-v2/resolve/{REV}/{files[0]}',dest)
    import pyarrow.parquet as pq
    return pq.read_table(dest).to_pylist(),{'file':files[0],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
