"""Measured-output report only; never calls a model or synthesizes outcomes."""
import argparse
import json
from pathlib import Path

HTML = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Swarm of Theseus — qualification results</title><style>
body{background:#111c26;color:#e5edf1;font:16px system-ui;margin:0}main{max-width:1250px;margin:auto;padding:32px}h1{font-size:36px;margin-bottom:12px}.banner{background:#48361d;color:#ffda93;padding:15px;position:sticky;top:0;z-index:3}p{line-height:1.6}.muted{color:#a5b8c6}select,button{font:inherit;background:#223847;color:white;border:1px solid #728b9a;border-radius:5px;padding:8px;margin:5px}.panel{background:#1b2d3b;border-radius:8px;padding:20px;margin:18px 0}.bad{color:#ffb197}.good{color:#8be1b8}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:10px;border-bottom:1px solid #39515e;text-align:left}.right{background:#1a4137}.wrong{background:#492f2b}.tiny{font-size:12px}.rule{font-family:monospace;white-space:pre-wrap}code{color:#b7d5ea}img{width:100%}.controls{display:flex;flex-wrap:wrap;align-items:center} @media(max-width:700px){main{padding:16px}h1{font-size:27px}}
</style><div class="banner">MEASURED QUALIFICATION · Joint gate failed · No turnover pilot ran</div><main><div class="muted">SOC-24 · Swarm of Theseus v2</div><h1>Valid outputs. Unreliable decisions.</h1><p>Both attempts completed, with no provider failures or scoring disagreements. The incident task qualified after repair; release and console migration did not. These observations cannot establish whether culture survives replacement.</p><div class="panel"><strong>48 model calls · 24 completed runs · $0.165211 estimated API cost</strong><p class="muted">No threshold was lowered. The planned 612-call pilot was not launched. Initial and repair use different fresh worlds, so their differences do not isolate a formatting effect.</p></div><h2>Prespecified competence checks</h2><div style="overflow:auto"><table><thead><tr><th>Scenario</th><th>Attempt</th><th>Ceiling stable ≥90%</th><th>Ceiling changed ≥90%</th><th>Learner stable ≥75%</th><th>Individual gate</th></tr></thead><tbody id="metrics"></tbody></table></div><h2>Inspect actual decisions</h2><div class="controls"><label>Attempt <select id="attempt"></select></label><label>Scenario <select id="scenario"></select></label><label>World <select id="seed"></select></label><label>Reader <select id="arm"></select></label><label>Checkpoint <select id="checkpoint"><option value="0">Stable</option><option value="5">Changed / interface</option></select></label><button id="play">Play checkpoints</button></div><div class="panel"><div id="score"></div><p class="muted" id="boundary"></p><div id="rule" class="rule"></div></div><div style="overflow:auto"><table><thead><tr><th>Case / class</th><th>Probe signal / fresh</th><th>Ledger signal / fresh</th><th>Canary signal / fresh</th><th>Model command</th><th>Accepted action</th><th>Outcome</th></tr></thead><tbody id="cases"></tbody></table></div><h3>Recorded notebook</h3><div id="notebook" class="panel rule"></div><p class="muted">The notebook is an observable model output, not a verified explanation of internal reasoning. Evaluator truth below is for the viewer; learners did not receive current answers.</p><details><summary>Exact repaired user input, where recorded</summary><pre id="prompt" class="panel tiny" style="white-space:pre-wrap;overflow-wrap:anywhere"></pre></details><h2>What this changes</h2><p>Do not scale this three-task instrument on the current model and prompt. A future diagnostic should separate single-case from batched decisions, and decisions from note-writing. Incident-only work would be a newly scoped prospective study, not a rescue of this failed joint gate.</p><p class="muted">Two worlds per scenario/checkpoint, 12 case decisions per cell. Sixteen offline checks. Same-author scoring audit; no independent scientific review or novelty claim. Source and immutable plan receipts are preserved in each manifest.</p></main><script>
const DATA=__DATA__,$=id=>document.getElementById(id);
function el(tag,value,parent,cls){const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;parent.append(e);return e}
function opts(id,values){$(id).replaceChildren();values.forEach(v=>{let o=el('option',v,$(id));o.value=v})}
for(const scenario of ['release','incident','migration'])for(const attempt of ['S0','S0-repair']){let m=DATA.summaries[attempt].metrics[scenario],tr=el('tr','',$('metrics'));el('td',scenario,tr);el('td',attempt,tr);let pass=true;for(const [key,gate] of [['ceiling-0',.90],['ceiling-5',.90],['learner-0',.75]]){let x=m[key],ok=x.conservative_accuracy>=gate;pass=pass&&ok;el('td',x.correct+'/'+x.assigned+' ('+(100*x.conservative_accuracy).toFixed(1)+'%)',tr,ok?'good':'bad')}el('td',pass?'PASS':'FAIL',tr,pass?'good':'bad')}
opts('attempt',['S0-repair','S0']);opts('scenario',['release','incident','migration']);opts('arm',['ceiling','learner']);
function seeds(){opts('seed',[...new Set(DATA.events.filter(e=>e.attempt===$('attempt').value).map(e=>e.seed))]);draw()}
function draw(){let e=DATA.events.find(e=>e.attempt===$('attempt').value&&e.scenario===$('scenario').value&&e.seed===+$('seed').value&&e.arm===$('arm').value&&e.step===+$('checkpoint').value);$('cases').replaceChildren();if(!e){$('score').textContent='No recorded event';return}let call=e.calls[0],obs=call.request.observation,correct=e.scores.filter(r=>r.correct).length;$('score').textContent=correct+'/6 correct · '+e.run+' · checkpoint '+e.step;$('boundary').textContent=e.arm==='ceiling'?'Ceiling reader: current rule explicitly supplied. Accuracy failures here are application errors.':'Historical learner: class-to-source mapping learned from past labeled examples; current rule withheld.';$('rule').textContent='Viewer-only evaluator mapping: '+JSON.stringify(e.evaluator.rule);e.cases.forEach(c=>{let r=e.scores.find(r=>r.id===c.id),tr=el('tr','',$('cases'));el('td',c.id.split(':').slice(-2).join(' / '),tr);for(let source of ['probe','ledger','canary']){let v=c.evidence[source];el('td',(v.signal?'YES':'NO')+' / '+(v.fresh?'YES':'NO'),tr)}let ds=call.result.value?.decisions||[];el('td',ds.find(d=>d.id===c.id)?.command||'MISSING',tr);el('td',r.truth,tr);el('td',r.correct?'correct':r.observed?'incorrect':'missing',tr,r.correct?'right':'wrong')});$('notebook').textContent=call.result.value?.notebook||'No notebook';$('prompt').textContent=e.exact_user_text||'Initial attempt used the recorded JSON observation; exact structured observation is preserved in the evidence bundle.'}
$('attempt').onchange=seeds;['scenario','seed','arm','checkpoint'].forEach(id=>$(id).onchange=draw);let timer=null;$('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;$('play').textContent='Play checkpoints'}else{timer=setInterval(()=>{$('checkpoint').value=$('checkpoint').value==='0'?'5':'0';draw()},2000);$('play').textContent='Pause'}};seeds();</script></html>'''


def build(results, output):
    results=Path(results); output=Path(output);output.mkdir(exist_ok=True,parents=True)
    summaries={};events=[]
    for stage in ('S0','S0-repair'):
        root=results/stage;summaries[stage]=json.loads((root/'summary.json').read_text())
        starts={c['call']:c for p in root.glob('calls/*-started.json') for c in [json.loads(p.read_text())]}
        for p in sorted(root.glob('events/*.json')):
            e=json.loads(p.read_text());e['attempt']=stage
            e['exact_user_text']=starts[e['calls'][0]['result']['call']].get('exact_user_text')
            events.append(e)
    assert len(events)==48
    data=json.dumps({'summaries':summaries,'events':events}).replace('<','\\u003c')
    (output/'qualification-replay.html').write_text(HTML.replace('__DATA__',data))
    # The figure is a measured count chart, not a simulation of unexecuted turnover.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(18,7),sharey=True)
    labels=['Ceiling\nstable','Ceiling\nchanged','Learner\nstable'];keys=['ceiling-0','ceiling-5','learner-0']
    for ax,scenario in zip(axes,('release','incident','migration')):
        for j,(stage,color) in enumerate((('S0','#8593a1'),('S0-repair','#147f89'))):
            metrics=summaries[stage]['metrics'][scenario];ys=[metrics[k]['correct']/12 for k in keys];xs=[i+(j-.5)*.34 for i in range(3)]
            ax.bar(xs,ys,width=.32,color=color,label='Initial' if j==0 else 'Repair')
            for x,y,k in zip(xs,ys,keys):ax.text(x,y+.02,f"{metrics[k]['correct']}/12",ha='center',fontsize=10)
        for i,gate in enumerate((.9,.9,.75)):ax.plot([i-.42,i+.42],[gate,gate],color='#b34825',linestyle='--',linewidth=1.8)
        ax.set_title(scenario.capitalize(),fontsize=16);ax.set_xticks(range(3),labels);ax.set_ylim(0,1.18);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    axes[0].set_ylabel('Correct decisions / assigned cases');axes[-1].legend(loc='upper right')
    fig.suptitle('Swarm of Theseus v2: qualification failed before turnover',fontsize=22,y=.98)
    fig.text(.5,.055,'Dashed segments: prespecified gates. Fresh worlds in each attempt; no causal before/after claim.\n48 valid model calls • no provider failures • no scoring discrepancies • no turnover pilot',ha='center',fontsize=12)
    fig.tight_layout(rect=(.02,.14,.99,.91));fig.savefig(output/'qualification-summary.png',dpi=120);plt.close(fig)
    (output/'provenance.json').write_text(json.dumps({'kind':'measured_qualification_analysis','events':48,'model_calls_new':0,'stages':['S0','S0-repair'],'input_files':'saved manifests, call records, events and summaries; no generated outcomes'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results');p.add_argument('output');a=p.parse_args();build(a.results,a.output)
