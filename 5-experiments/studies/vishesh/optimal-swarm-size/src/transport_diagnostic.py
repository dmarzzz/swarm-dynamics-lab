"""One registered Anthropic transport call, charged to the canonical Q1 ledger."""
import argparse,json,time,re
from pathlib import Path
from budget import Budget
from provider import Provider
from reporting import Reporter
from replay import render
from failures import safe_code
from tasks import strict_json


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--budget-ledger',type=Path,required=True);p.add_argument('--attempt',default='anthropic-transport-q0-a1');a=p.parse_args()
    if not re.fullmatch(r'anthropic-transport-q0-a[1-9][0-9]*',a.attempt):raise ValueError('invalid_attempt')
    cfg=json.loads(a.config.read_text());a.output.mkdir(exist_ok=False)
    row={'id':a.attempt,'stage':'transport-diagnostic','family':'exact-json','structure':'one-call','root':0,'n':1}
    tldr='TLDR: One real Anthropic Haiku transport call versus exact JSON {ok:true}; verify served route, complete response, usage, cost and public artifacts. Charged to the shared $20 cap. Plumbing qualification only, not model task competence or swarm-size evidence.'
    (a.output/'assignment.json').write_text(json.dumps(row|{'tldr':tldr},indent=2))
    reporter=Reporter(cfg['experiment_id'],row,tldr)
    bank=Budget(a.budget_ledger,cfg['stage_cap_microdollars']);start=time.monotonic()
    def journal(event):
        with (a.output/'trace.jsonl').open('a') as f:f.write(json.dumps(event)+'\n');f.flush()
    journal({'kind':'service_start','t':0,'actor':0,'phase':'transport','item':None})
    failure=None;answer=None
    try:
        answer=Provider(cfg,bank,row['id'],journal)([{'role':'system','content':'Return raw JSON only. Do not use Markdown code fences, formatting or commentary.'},{'role':'user','content':'Return exactly {"ok":true}.'}],start+60,0,'transport',None)
        try:
            if strict_json(answer)!={'ok':True}:failure='diagnostic_answer_mismatch'
        except ValueError:failure='malformed_output'
    except Exception as exc:failure=safe_code(exc)
    elapsed=time.monotonic()-start
    journal({'kind':'service_end','t':elapsed,'actor':0,'phase':'transport','item':None})
    record={'assignment':row,'failure':failure,'artifact':answer,'elapsed_s':elapsed,'evaluation':{'quality':int(failure is None)},'operational_success':failure is None,'exposure_microdollars':bank.exposure(row['id']),'note':'Transport diagnostic only; not qualification-task competence.'}
    (a.output/'outcome.json').write_text(json.dumps(record,indent=2))
    render(a.output/'trace.jsonl',a.output/'replay.html')
    receipt=reporter.finish(a.output,record)
    summary={'run':reporter.id,'passed':failure is None and receipt['complete'],'failure':failure,'exposure_microdollars':record['exposure_microdollars'],'publication_complete':receipt['complete']}
    (a.output/'diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
    return 0 if summary['passed'] else 2

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as e:print(json.dumps({'diagnostic_failed':True,'safe_code':safe_code(e)}));raise SystemExit(2)
