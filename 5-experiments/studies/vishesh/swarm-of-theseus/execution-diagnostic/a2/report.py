"""Offline figure and completion-order replay. Never calls a model."""
import argparse,json,csv,html
from pathlib import Path
from analyze import summarize

def render(root):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    root=Path(root);s=summarize(root);m=json.loads((root/'manifest.json').read_text());
    with (root/'decisions.csv').open() as source: rows=list(csv.DictReader(source))
    fixture=s['evidence_type']!='measured_model_outputs'
    title='SCRIPTED SOFTWARE FIXTURE — NOT MODEL EVIDENCE' if fixture else 'Theseus A2 • withheld-policy acquisition screen'
    fig,axes=plt.subplots(1,2,figsize=(16,7),gridspec_kw={'width_ratios':[1.3,1]});fig.suptitle(title,fontsize=17)
    worlds=sorted(s['arms']['learned']['root_correct']);x=list(range(len(worlds)))
    from matplotlib.patches import Patch
    palette={'correct':'#3b9d76','wrong':'#cf5552','invalid':'#e7a342','missing':'#d5d9de'}
    for offset,arm in [(-.18,'learned'),(.18,'ceiling')]:
        bottom=[0]*len(worlds)
        for state,color in palette.items():
            values=[]
            for w in worlds:
                rs=[r for r in rows if r['arm']==arm and r['seed']==w]
                def status(r):
                    if r['response_received']!='True':return 'missing'
                    if r['valid_response']!='True':return 'invalid'
                    return 'correct' if r['correct']=='True' else 'wrong'
                values.append(sum(status(r)==state for r in rs))
            axes[0].bar([i+offset for i in x],values,bottom=bottom,width=.34,color=color,hatch='//' if arm=='ceiling' else None)
            bottom=[a+b for a,b in zip(bottom,values)]
        for i,w in enumerate(worlds):axes[0].text(i+offset,16.25,str(s['arms'][arm]['root_correct'][w]),ha='center',fontsize=10)
    axes[0].set_xticks(x,worlds);axes[0].set_ylim(0,18);axes[0].set_ylabel('16 assigned actions per root and arm; numbers = correct');axes[0].set_xlabel('Left: learned policy • Right / hatch: true-policy ceiling\nSix fixed roots; nested cases are not independent n')
    axes[0].legend(handles=[Patch(color=c,label=k) for k,c in palette.items()],loc='upper center',ncol=4,fontsize=9);axes[0].set_title('Paired held-out execution • missingness stays visible')
    axes[1].axis('off');text=[f"Policies qualified: {s['learning']['qualified_policies']}/12",f"Started / assigned: {s['started_calls']}/204",f"Terminal calls: {s['terminal_calls']}",f"Observed decisions: {s['observed_decisions']}/192",f"Overall qualification: {'PASS' if s['qualification_passed'] else 'NOT PASSED'}",'']
    for arm in ('learned','ceiling'):
        a=s['arms'][arm];text += [f"{arm}: {a['observed']}/96 observed; {a['correct']} correct",f"  Observed accuracy: {a['observed_accuracy'] if a['observed_accuracy'] is not None else 'UNOBSERVED'}",f"  False release / incident: {a['false_releases']} / {a['false_incident_activations']}"]
    text+=['',f"New known model USD: {s['actual_model_usd']:.6f}",f"Unresolved model exposure USD: {s['unresolved_exposure_usd']:.6f}",'No swarm or cultural-preservation result.','Missing responses are not measured errors.','Assigned-denominator qualification stays conservative.']
    axes[1].text(0,.96,'\n'.join(text),va='top',fontsize=12,linespacing=1.6)
    fig.tight_layout(rect=(0,.02,1,.92));fig.savefig(root/'results.png',dpi=120);plt.close(fig)
    events=[];by_id={r['assignment']:r for r in rows};policies=json.loads((root/'policies.json').read_text())
    for a in m['assignments']:
        p=root/'calls'/(a['id']+'-finished.json')
        if p.exists():
            r=json.loads(p.read_text());row=by_id.get(a['id']);state='provider_failure' if r.get('error') else ('correct' if policies[a['id']]['qualified'] else 'invalid') if a['kind']=='learn' else ('invalid' if row['valid_response']!='True' else 'correct' if row['correct']=='True' else 'wrong');events.append({'id':a['id'],'kind':a['kind'],'arm':a['arm'],'root':a['seed'],'state':state,'end':r.get('finished_epoch',0)})
    events.sort(key=lambda e:(e['end'],e['id']))
    script=json.dumps(events).replace('<','\\u003c');safe=html.escape(title)
    document='''<!doctype html><meta charset="utf-8"><title>Theseus A2 replay</title><style>body{font:18px system-ui;background:#f7f8fa;color:#142536;margin:40px;max-width:1100px}input{width:90%}td,th{padding:8px;border-bottom:1px solid #ccd}#count{font-size:28px}small{color:#456}img{width:100%}</style>'''+f'<h1>{safe}</h1><p>Completion-order replay; this is execution progress, not cultural evolution.</p><p id="count"></p><input id="slider" type="range" min="0" value="0"><p id="last"></p><table><thead><tr><th>Arm</th><th>Observed terminal calls</th><th>Assigned</th></tr></thead><tbody id="counts"></tbody></table><p>Unfinished or unstarted assignments remain missing; they are never displayed as successful. Case outcomes, root denominators and invalid responses are retained in decisions.csv.</p><img src="results.png" alt="Final scored results; the replay slider does not change this final figure."><small>Six fixed acquisition-world roots. Twelve learners and192 execution calls are nested measurements.</small>'+'''<script>const events='''+script+''';const slider=document.getElementById('slider');slider.max=events.length;function draw(){let n=+slider.value;document.getElementById('count').textContent=n+' terminal calls shown / 204 assigned';document.getElementById('last').textContent=n?events[n-1].id:'Initial state: no observed completion';document.getElementById('counts').innerHTML=['learner','learned','ceiling'].map(a=>'<tr><td>'+a+'</td><td>'+events.slice(0,n).filter(e=>e.arm===a).length+'</td><td>'+(a==='learner'?12:96)+'</td></tr>').join('')}slider.oninput=draw;draw();</script>'''
    (root/'replay.html').write_text(document)
    return {'figure':'results.png','replay':'replay.html','terminal_events':len(events),'fixture':fixture}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');args=p.parse_args();print(json.dumps(render(args.results)))
