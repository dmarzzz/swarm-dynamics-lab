"""Saved Q0/D1 parser comparison; no OCR, dispatch or dataset fetch."""
import argparse
import json
from pathlib import Path
from fields import base, extract

p=argparse.ArgumentParser(); p.add_argument('--q0',type=Path,required=True); p.add_argument('--d1',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
if a.out.exists(): raise ValueError('preserve_existing_report')
rows=[]
for path in sorted((a.q0/'private').glob('*-?.json')):
    receipt,reader=path.stem.split('-')
    if receipt not in {'60','61','62'} or reader not in {'P','C'}: continue
    data=json.loads(path.read_text())
    rows.append((f'Q0-{receipt}-{reader}',data))
for index in range(1,4):
    data=json.loads((a.d1/f'private/calls/{index:02d}/private/output.json').read_text())
    rows.append((f'D1-{59+index}-C',data))
out=[]
for identity,data in rows:
    old=base.extract(data['raw_words']); new=extract(data['raw_words'])
    out.append({'observation':identity,'old_status':old['status'],'old_value':old['value'],
                'new_status':new['status'],'new_value':new['value'],
                'native_candidate_reproduced':old==data['candidate'],'normalization':new['normalization']})
assert len(out)==8 and all(row['native_candidate_reproduced'] for row in out)
a.out.write_text(json.dumps({'scope':'retrospective inspected development; 8 outputs from 3 receipts, no new OCR or efficacy estimate',
 'image_reading_62':{'value':'3600000.00','basis':'same-author visual reading, not independently retrieved dataset gold'},'rows':out},indent=2)+'\n')
print(json.dumps({'saved_outputs':len(out),'distinct_receipts':3,'changed_outputs':sum(r['old_value']!=r['new_value'] for r in out)}))
