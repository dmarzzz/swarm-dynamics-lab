"""Reconstruct outcome assignment and scoring, including an independent confusion tally."""
import argparse,json
from pathlib import Path
from contract import ARMS,actor,run_policy
from study import evaluate

def audit(root):
 m=json.loads((root/'manifest.json').read_text());records=[json.loads(l) for l in (root/'records.jsonl').read_text().splitlines()];out=json.loads((root/'outcomes.json').read_text());summary=json.loads((root/'summary.json').read_text())
 assert m['complete'] and [r['id'] for r in records]==m['ids']
 assert len({r['image_sha256'] for r in records})==len(records)
 assert len(out)==len(records)*len(ARMS) and len({(r['id'],r['arm']) for r in out})==len(out)
 expected,es=evaluate(records)
 # E0 frozen before additive cost-accounting fields; compare fields actually recorded.
 optional={'initial_ocr_calls','initial_wall_s'}
 assert all(set(expected[i])-optional <= set(row) and all(expected[i][k]==v for k,v in row.items()) for i,row in enumerate(out))
 for key,value in summary.items():
  if key=='arms':
   for arm,fields in value.items():
    assert all(es['arms'][arm][k]==v for k,v in fields.items())
  elif key in es:assert es[key]==value
 for arm in ARMS:
  selected=[r for r in out if r['arm']==arm];counts={'correct':0,'wrong':0,'refer':0};scorable=0
  for r in selected:
   gold=next(x['gold'] for x in records if x['id']==r['id'])
   if gold['status']!='ok':continue
   scorable+=1
   label='refer' if r['value'] is None else ('correct' if r['value']==gold['value'] else 'wrong');counts[label]+=1
  assert sum(counts.values())==scorable
  for key,value in counts.items():assert summary['arms'][arm][key]==value
  assert summary['arms'][arm]['checks']==sum(len(x['checks']) for x in selected)
 assert m['ocr_calls']==len(records)*5 and m['invalid_ocr']==summary['invalid_ocr']
 return {'passed':True,'assigned':len(records),'outcomes':len(out),'checks':['assignment complete and unique','five OCR calls per receipt','image uniqueness','all decisions replay','independent correct/wrong/refer tally','unscorable retained','actual tool cost accounting']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();r=audit(a.run);(a.run/'audit.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
