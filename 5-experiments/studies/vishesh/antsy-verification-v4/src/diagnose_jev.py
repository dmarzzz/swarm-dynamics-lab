"""One preplanned diagnostic of the rejected payload; no policy outcome selection."""
import argparse,json,subprocess
from pathlib import Path
from jev import Runtime
from render import canvas,write,MUTED

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--previous',type=Path,required=True);ap.add_argument('--relay',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    import swarm_report as sr
    sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();exp='antsy-verification-v4';rid=exp+'/D1-jev-attempt-1';url=f'https://github.com/dmarzzz/swarm-lab/tree/{sha}/researchers/vishesh/notes/antsy-verification-v4'
    old=[r for r in json.loads(a.previous.read_text()) if not r['valid']];assert len(old)==1;r=old[0];rt=Runtime(a.relay,attempt='D1')
    sr.report('start',exp,rid,params={'stage':'D1','backend':'jev-1.13','kind':'diagnostic'},url=url,message='One-call validation diagnostic; original failure and successful choices retained.',strict=True)
    try:q=r['question'];rt.choose(r['state'],q['instructions'],q['criteria'],r['context'])
    except Exception:pass
    result={'source':sha,'previous_context':r['context'],'response':rt.receipts[0]};(a.out/'diagnostic.json').write_text(json.dumps(result,indent=2))
    im,d=canvas('Antsy | response validation diagnostic','One preplanned repeated payload; not a rerun of successful decisions')
    write(d,(70,190),'Result: '+('valid response' if rt.receipts[0]['valid'] else str(rt.receipts[0].get('reason'))),32)
    diag=rt.receipts[0].get('diagnostic') or {'validated':True}
    for j,(k,v) in enumerate(diag.items()):write(d,(70,285+j*75),f'{k}: {v}',22,MUTED)
    im.save(a.out/'final_frame.png')
    for p in a.out.iterdir():sr.upload(rid,p,p.name)
    sr.report('done',exp,rid,message='Diagnostic captured. Receipt escalation remains blocked pending post-mortem.',strict=True)
    print(json.dumps({'valid':rt.receipts[0]['valid'],'reason':rt.receipts[0].get('reason'),'diagnostic':diag}))
if __name__=='__main__':main()
