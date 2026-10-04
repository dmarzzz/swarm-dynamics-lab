"""One-call Opus interface probe on an engineering (S0) packet before any batch.

Uses the study ledger, so its cost counts toward the study cap. Writes one JSON record;
exits nonzero unless the answer parsed, validated and was evaluated.
"""
import json,os,sys
from pathlib import Path
import provider,study

def main(out):
    out=Path(out)
    if out.exists():raise SystemExit('probe_record_exists')
    a=study.assignments('S0')[-1]  # last S0 row: an engineering-world pilot packet, not a Q0/S1 packet
    assert a['kind']=='pilot' and a['task'] in study.design()['engineering_worlds']
    ledger=provider.Ledger(os.environ['SYBIL_API_BUDGET_LEDGER'])
    rec={'probe':'p0-001','assignment':a['id'],'task':a['task'],'model':study.design()['model'],
         'effort':study.design()['request']['effort'],'source_hash':study.source_hash()}
    try:
        answer,acct=provider.Anthropic(ledger).call(a['packet'],'p0-001:'+a['id'])
        rec.update(status='valid',answer=answer,accounting=acct,evaluation=study.evaluate(a,answer))
    except provider.CallFailure as exc:
        rec.update(status='failed',error=exc.category,accounting=exc.accounting)
    rec['study_accounting']=ledger.transact()
    out.write_text(json.dumps(rec,indent=2,sort_keys=True))
    print(json.dumps({k:rec[k] for k in ('status','accounting')} | {'error':rec.get('error')}))
    if rec['status']!='valid':raise SystemExit(1)

if __name__=='__main__':main(sys.argv[1])
