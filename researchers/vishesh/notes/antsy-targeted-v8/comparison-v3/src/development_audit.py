"""Annotation-transcription upper-information diagnostic, not an OCR benchmark."""
import argparse
import json
from pathlib import Path
from common import original,repaired,write,digest
from pack_cases import label


def run(parquet,out):
    import pyarrow.parquet as pq
    rows=pq.read_table(parquet).to_pylist();results=[]
    for index in range(80,92):
        gt=json.loads(rows[index]['ground_truth']);words=[]
        for line in gt['valid_line']:
            for w in line['words']:
                q=w['quad'];xs=[q[f'x{i}'] for i in range(1,5)];ys=[q[f'y{i}'] for i in range(1,5)]
                x,y=min(xs),min(ys);width,height=max(xs)-x,max(ys)-y
                words.append({'text':w['text'],'x':x,'y':y+height/2,'h':height,'box':[x,y,width,height],'confidence':1})
        value=label(gt['gt_parse'].get('total',{}).get('total_price'))
        a=original.extract(words);b=repaired.extract(words)
        results.append({'source_row':index,'gold':value,'original':a['value'],'repaired':b['value'],
          'repaired_correct':b['value']==value and value is not None,'observation_sha256':digest(words),
          'reasons':b['reasons']})
    report={'scope':'Development annotation text with true geometry; labels stripped before parser; not native OCR or fresh evaluation',
            'cases':12,'original_correct':sum(r['original']==r['gold'] and r['gold'] is not None for r in results),
            'repaired_correct':sum(r['repaired_correct'] for r in results),'rows':results}
    write(out,report);print(json.dumps({k:v for k,v in report.items() if k!='rows'}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--parquet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.parquet,a.out)
