"""J0: prerequisite competence, separately recorded from receipt performance."""
import argparse,json,subprocess,time
from pathlib import Path
from jev import Runtime,probes
from render import canvas,write,COLORS,MUTED

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--relay',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    import swarm_report as sr
    exp='antsy-verification-v4';rid=exp+'/J0-jev-attempt-1';sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();url=f'https://github.com/dmarzzz/swarm-lab/tree/{sha}/researchers/vishesh/notes/antsy-verification-v4'
    rt=Runtime(a.relay);results=[];cases=probes();manifest={'source':sha,'runtime':rt.metadata,'assigned':len(cases),'complete':False}
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    sr.report('start',exp,rid,params={'stage':'J0','backend':'jev-1.13','kind':'qualification'},url=url,message='Jev competence screen: four option controls and twelve numeric reading/update cases; no receipt-performance claim.',strict=True)
    try:
        for i,c in enumerate(cases):
            q=c['question'];choice=rt.choose(c['state'],q['instructions'],q['criteria'],{'stage':'J0','case':i});results.append({'id':i,'kind':c['kind'],'expected':c['target'],'choice':choice,'correct':choice==c['target']})
            (a.out/'results.json').write_text(json.dumps(results,indent=2));(a.out/'receipts.json').write_text(json.dumps(rt.receipts,indent=2))
        option=sum(r['correct'] for r in results if r['kind']=='option');reading=sum(r['correct'] for r in results if r['kind']!='option');passed=option==4 and reading>=10
        manifest.update(complete=True,passed=passed,option_correct=option,reading_update_correct=reading,cost_usd=sum(r['usage']['cost'] for r in rt.receipts),calls=len(rt.receipts),call_wall_s=sum(r['wall_s'] for r in rt.receipts));(a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
        im,d=canvas('Antsy | Jev competence qualification','Prerequisites only: reading labels and updating a numeric comparison; not optimal verification')
        write(d,(70,170),f"Gate: {'PASS' if passed else 'FAIL'}",42,COLORS[0] if passed else COLORS[1]);write(d,(70,245),f'Option controls {option}/4 | reading and update {reading}/12',30)
        for i,r in enumerate(results):
            x=70+(i%4)*375;y=335+(i//4)*110;write(d,(x,y),f"{r['kind']} {r['id']+1}: {'correct' if r['correct'] else 'incorrect'}",23,COLORS[0] if r['correct'] else COLORS[1]);write(d,(x,y+38),f"Expected {r['expected']} / chose {r['choice']}",20,MUTED)
        write(d,(70,820),'Pinned Jev 1.13 / TypeSafe. No model fallback. All sixteen cases retained.',23,MUTED);im.save(a.out/'final_frame.png')
        for p in a.out.iterdir():sr.upload(rid,p,p.name)
        sr.report('done' if passed else 'fail',exp,rid,metrics={'correct':option+reading,'total':16,'cost_usd':manifest['cost_usd']},message='Jev competence prerequisites passed; receipt qualification still required.' if passed else 'Jev competence prerequisites failed; receipt escalation blocked.',strict=True)
        print(json.dumps(manifest))
    except Exception as exc:
        manifest.update(error=type(exc).__name__,completed=len(results),not_run=len(cases)-len(rt.receipts));(a.out/'manifest.json').write_text(json.dumps(manifest,indent=2));(a.out/'receipts.json').write_text(json.dumps(rt.receipts,indent=2));sr.report('fail',exp,rid,message='Jev qualification execution failure: '+type(exc).__name__+'; no retries, remaining cases not run.',strict=True);raise
if __name__=='__main__':main()
