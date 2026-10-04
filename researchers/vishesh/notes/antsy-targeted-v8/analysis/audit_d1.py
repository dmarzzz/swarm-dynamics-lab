"""Recompute D1 from retained private traces; publish only numeric evidence/hashes."""
from pathlib import Path
import sys,json,hashlib,math
import argparse
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);cli_args=p.parse_args()
study=Path(__file__).resolve().parents[1];root=cli_args.results
if cli_args.out.exists():raise ValueError('preserve existing audit')
sys.path.insert(0,str(study/'src'));from fields import extract
records=json.loads((root/'records.json').read_text());summary=json.loads((root/'summary.json').read_text());order=[60,61,62,60,61,62];rows=[]
for seq,i in enumerate(order,1):
 if seq>len(records):rows.append({'seq':seq,'receipt':i,'status':'unstarted'});continue
 r=records[seq-1];assert r['seq']==seq and r['receipt']==i
 call=root/'private/calls'/f'{seq:02d}';journal=[json.loads(x) for x in (call/'calls.jsonl').read_text().splitlines()];assert [x['status'] for x in journal]==['started',r['status']]
 row={'seq':seq,'receipt':i,'status':r['status'],'category':r['category'],'wall_s':r['wall_s'],'latency_eligible':r['latency_eligible'],'last_phase':r['phases']['last_phase'],'phase_durations_s':{}}
 ev={e['phase']:e['elapsed_s'] for e in r['phases']['events']}
 for label in ['imports','reader_init','ocr','extract','output']:
  a,b=label+'_begin',label+'_end';row['phase_durations_s'][label]=ev[b]-ev[a] if a in ev and b in ev else None
 assert all(x is None or math.isfinite(x) and x>=0 for x in row['phase_durations_s'].values())
 for n,meta in r['streams'].items():assert hashlib.sha256((call/'private'/n).read_bytes()).hexdigest()==meta['sha256']
 assert hashlib.sha256((call/'private/phases.jsonl').read_bytes()).hexdigest()==r['phase_file_sha256']
 p=call/'private/output.json';row['raw_output_retained']=p.is_file()
 if p.is_file():
  assert hashlib.sha256(p.read_bytes()).hexdigest()==r['output_sha256'];d=json.loads(p.read_text());row['candidate']=d['candidate'];row['parser_replay_match']=extract(d['raw_words'])==d['candidate'];assert row['parser_replay_match'];row['word_count']=len(d['raw_words'])
 rows.append(row)
assert len(records)==summary['started'] and 6-len(records)==summary['unstarted']
assert sum(r['status']=='valid' for r in records)==summary['valid']
result={'scope':'Same-author saved-output audit, no OCR rerun; repeated receipts are not independent units','rows':rows,'started':len(records),'unstarted':6-len(records),'unresolved_started':0,'distinct_receipts_observed':len({r['receipt'] for r in records}),'all_retained_stream_phase_output_hashes_match':True,'native_source':json.loads((root/'manifest.json').read_text())['source']}
cli_args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'audited_calls':len(records),'unresolved_started':0}))
