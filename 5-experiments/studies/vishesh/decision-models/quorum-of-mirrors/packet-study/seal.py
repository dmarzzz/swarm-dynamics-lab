"""One-time holdout creation after development freeze. Prints no sealed case contents."""
from pathlib import Path
import argparse,hashlib,json,secrets,datetime,os
from corpus import generate,validate
HERE=Path(__file__).resolve().parent
SOURCES=('instrument.py','corpus.py','test_packets.py','seal.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--custody',type=Path,required=True);args=ap.parse_args()
    if (HERE/'SEAL.json').exists() or args.custody.exists():raise SystemExit('Refuse overwrite: preserve existing seal and explicitly version any successor.')
    freeze=json.loads((HERE/'FREEZE.json').read_text())
    assert freeze['source_sha256']=={n:sha(HERE/n) for n in SOURCES}
    args.custody.mkdir(parents=True,mode=0o700);os.chmod(args.custody,0o700)
    manifest={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':freeze['source_sha256'],
              'access_policy':'Operator has not read individual qualification/evaluation contents. Automated QA reads all cases; shared controlled grammar is known. This is a tuning holdout, not independent authorship or held-out language.',
              'splits':{},'native_calls':0}
    private={'seeds':{},'public_manifest':'packet-study/SEAL.json'};all_events=set();all_receipts=set()
    for split in ('qualification','evaluation'):
        seed=secrets.randbits(128);rows=generate(split,seed);quality=validate(rows,split)
        events={r['actor']['event'] for r in rows};receipts={x['id'] for r in rows for x in r['actor']['receipts']}
        assert not events&all_events and not receipts&all_receipts;all_events|=events;all_receipts|=receipts
        p=args.custody/(split+'.json');p.write_text(json.dumps(rows,indent=2)+'\n');os.chmod(p,0o600)
        q=args.custody/(split+'-qa.json');q.write_text(json.dumps(quality,indent=2)+'\n');os.chmod(q,0o600)
        private['seeds'][split]=seed
        manifest['splits'][split]={'packets':quality['packets'],'roots':quality['roots'],'families':quality['family_counts'],
            'critical_mismatches':quality['critical_mismatches'],'target_balance':quality['target_balance'],'corpus_sha256':sha(p),'qa_sha256':sha(q),
            'source_parser_correct':quality['correct']['source_parser'],'individual_cases_inspected_by_operator':False}
    dev=generate('development',20261004)
    assert not {r['actor']['event'] for r in dev}&all_events
    assert not {x['id'] for r in dev for x in r['actor']['receipts']}&all_receipts
    private['source_sha256']=freeze['source_sha256'];private['created_at']=manifest['created_at']
    p=args.custody/'custody.json';p.write_text(json.dumps(private,indent=2)+'\n');os.chmod(p,0o600)
    (HERE/'SEAL.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'sealed':True,'qualification_packets':24,'evaluation_packets':96,'cross_split_source_overlap':0,'individual_contents_printed':False}))
if __name__=='__main__':main()
