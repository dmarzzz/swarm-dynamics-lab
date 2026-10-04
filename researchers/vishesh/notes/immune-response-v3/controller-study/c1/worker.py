"""One-shot admitted C1 worker with source-pinned reporting and no successor."""
import argparse,importlib.util,json,os,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('immune_c1_run',BASE/'run.py');run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);a=p.parse_args();out=Path(a.out)
    receipt=run.verify_admission(a.admission);assert not out.exists()
    fd=os.open(str(out)+'.dispatch',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    job=sr.start('immune-response-v3',params={'stage':'controller-c1','runtime_commit':receipt['commit'],'max_calls':32,'episodes':8},message='C1: paired output-order discriminator,4development roots,32calls; same explicit diagnosis and fixed outcomes. No hidden-reasoning or population claim; no Q/A admission.')
    print(json.dumps({'run':job.id}),flush=True)
    def render_and_upload():
        if (out/'episodes.jsonl').exists():
            rs=importlib.util.spec_from_file_location('c1_reporting',BASE.parent/'render.py');render=importlib.util.module_from_spec(rs);rs.loader.exec_module(render);render.render(out)
        ws=importlib.util.spec_from_file_location('c1_upload_worker',BASE.parent/'worker.py');old=importlib.util.module_from_spec(ws);ws.loader.exec_module(old);old.old.upload(job,out)
    try:
        summary=run.execute(out,'openrouter',a.admission)
        render_and_upload();job.done(message='C1 collection complete; manual action/explanation review and PI successor decision pending.',episodes=summary['recorded'],api_calls=summary['api_calls'],actual_usd=summary['actual_usd'],scientific_review_complete=0)
    except Exception as e:
        try:render_and_upload()
        except Exception:pass
        job.fail('C1 stopped; preserve partial evidence: '+type(e).__name__);raise
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)
