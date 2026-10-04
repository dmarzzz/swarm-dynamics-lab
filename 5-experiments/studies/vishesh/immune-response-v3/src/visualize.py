"""Trace-backed plots, animated GIF and self-contained interactive replay; no model calls."""
import argparse,json,os,tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'immune-matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import io

ORDER=['N','Q00','Q10','Q01','Q10F','Q11R','Q11','Q11S','CLEAN']
EVENTS={4:'Damage',7:'Repair',13:'Replay',18:'Update'}
COLORS={'good':'#34b6a2','bad':'#ec756a','fail':'#e8bb63','bg':'#101820','muted':'#8da3b5'}

def load(out):return [json.loads(x) for x in (Path(out)/'episodes.jsonl').read_text().splitlines()]
def plot(rows,out,step=24,title='Immune response',backend='scripted'):
    rows=sorted(rows,key=lambda r:ORDER.index(r['arm']));fig=plt.figure(figsize=(16,10),dpi=100,facecolor=COLORS['bg']);gs=fig.add_gridspec(3,1,height_ratios=[1.1,1.4,1],hspace=.5)
    axes=[fig.add_subplot(gs[i]) for i in range(3)]
    for ax in axes:
        ax.set_facecolor(COLORS['bg']);ax.tick_params(colors='#d7e2eb');ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color('#405260');ax.xaxis.label.set_color('#d7e2eb');ax.yaxis.label.set_color('#d7e2eb')
    fig.text(.08,.955,title,color='#f1f5f8',fontsize=23,weight='bold');fig.text(.08,.925,f'{backend} • task {rows[0]["task_id"]} • {rows[0]["world"]} • round {step}/24',color='#c2d0db',fontsize=13)
    ax=axes[0]
    for i,r in enumerate(rows):
        for x in r['trajectory']:
            t=x['round'];c=COLORS['fail'] if x.get('failures') else COLORS['good'] if x['utility'] else COLORS['bad']
            ax.barh(i,.83,left=t-.415,height=.68,color=c if t<=step else '#253440')
    ax.set_yticks(range(len(rows)),[r['arm'] for r in rows]);ax.invert_yaxis();ax.set_xlim(.4,24.6);ax.set_xticks([1,4,7,13,18,24]);ax.set_title('Each scheduled request: correct deploy / failed task / response error',loc='left',color='#f1f5f8',fontsize=12)
    for t,label in EVENTS.items():ax.axvline(t-.5,color='#758a9c',lw=.8,alpha=.6);ax.text(t,.99,label,transform=ax.get_xaxis_transform(),color='#c2d0db',fontsize=9,va='bottom')
    ax=axes[1];palette=plt.cm.tab10.colors
    for i,r in enumerate(rows):
        hist=[x for x in r['trajectory'] if x['round']>=7 and x['round']<=step]
        if hist:
            ys=[sum(x['utility'] for x in hist[:j+1])/(j+1) for j in range(len(hist))]
            ax.plot([x['round'] for x in hist],ys,label=r['arm'],lw=2,marker='.',color=palette[i%10])
    ax.set_ylim(-.03,1.03);ax.set_xlim(7,24);ax.set_ylabel('Useful completion / requests so far');ax.set_xlabel('Logical round');ax.grid(axis='y',alpha=.13)
    if ax.lines:ax.legend(ncol=5,loc='upper center',bbox_to_anchor=(.5,1.22),frameon=False,labelcolor='#d7e2eb',fontsize=10)
    ax=axes[2];selected=[r for r in rows if r['arm'] in ['Q10F','Q11R','Q11','Q11S','CLEAN']]
    for i,r in enumerate(selected):
        hist=[x for x in r['trajectory'] if x['round']<=step]
        if not hist:continue
        x=hist[-1]
        for agent in range(8):
            statuses=x.get('private_status');status=statuses[agent] if statuses else None
            text=f'{status["correct"]}/12' if status else ('affected' if agent in x.get('affected',[]) else 'not flagged')
            wrong=status['wrong']>0 if status else agent in x.get('affected',[])
            ax.text(agent,i,text,ha='center',va='center',fontsize=10,color=COLORS['bad'] if wrong else COLORS['good'] if status else COLORS['muted'])
    ax.set_xlim(-.6,7.6);ax.set_ylim(len(selected)-.5,-.5);ax.set_yticks(range(len(selected)),[r['arm'] for r in selected]);ax.set_xticks(range(8),[f'A{i}' for i in range(7)]+['Coordinator']);ax.set_title('Private-state trace • correct facts / 12; red = contains wrong facts • evaluator-only',loc='left',color='#f1f5f8',fontsize=12)
    fig.text(.08,.025,'Teal = correct authorized deploy    Coral = task not completed    Gold = response error | Logical steps; no fabricated transitions.',color='#a9bdcd',fontsize=10)
    buf=io.BytesIO();fig.savefig(buf,format='png',facecolor=fig.get_facecolor());plt.close(fig);buf.seek(0)
    if out:Path(out).write_bytes(buf.getvalue())
    return Image.open(buf).convert('RGB')

def render(out,dest,world=None,task=None):
    out=Path(out);dest=Path(dest);dest.mkdir(parents=True,exist_ok=True);rows=load(out);manifest=json.loads((out/'manifest.json').read_text());backend=manifest.get('backend',manifest.get('params',{}).get('backend','unknown'))
    world=world or rows[0]['world'];task=task if task is not None else rows[0]['task_id'];sample=[r for r in rows if r['world']==world and r['task_id']==task]
    plot(sample,dest/'final_frame.png',title='Memory repair: recovery and relapse',backend=backend)
    frames=[plot(sample,None,t,title='Memory repair: recovery and relapse',backend=backend) for t in range(1,25)]
    frames=[frame.quantize(colors=32) for frame in frames]
    frames[0].save(dest/'replay.gif',save_all=True,append_images=frames[1:],duration=[450]*23+[1800],loop=0,optimize=True)
    template=(Path(__file__).with_name('replay.html')).read_text();data={'backend':backend,'rows':rows,'manifest':{k:manifest.get(k) for k in ['source_hash','git_commit','model']}}
    (dest/'replay.html').write_text(template.replace('/* DATA_SLOT */{}',json.dumps(data).replace('</','<\\/')))
    (dest/'visualization-provenance.json').write_text(json.dumps({'input':str(out/'episodes.jsonl'),'source_hash':manifest.get('source_hash'),'backend':backend,'gif_world':world,'gif_task':task,'frames':24,'width':1600,'height':1000,'event_markers':EVENTS,'history':'measured round snapshots, no interpolation'},indent=2))
    return dest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('dest');p.add_argument('--world');p.add_argument('--task',type=int);a=p.parse_args();render(a.out,a.dest,a.world,a.task)
