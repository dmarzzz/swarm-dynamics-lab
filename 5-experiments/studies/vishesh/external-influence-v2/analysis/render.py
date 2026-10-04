"""Measured-event figures and replay. No generated data and no model calls."""
import argparse,json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Circle
from PIL import Image

BG='#101827';PANEL='#192538';FG='#edf3fb';MUTED='#a7b8cb';GREEN='#43d9b2';RED='#ff7b79';GOLD='#f3c969';BLUE='#79b8ff'
ARMS=['private_review','discussion','random_check','targeted_check','targeted_provenance']
LABELS=['Private\nreview','Peer\ndiscussion','Random\nchecks','Targeted\nchecks','Checks +\nlineage']

def style():
    plt.rcParams.update({'font.family':'DejaVu Sans','text.color':FG,'axes.labelcolor':FG,'xtick.color':FG,'ytick.color':FG,'figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG,'font.size':12})

def result_color(r):
    if not r['validity']['ok']:return MUTED
    if r['evaluation']['correct']:return GREEN
    if r['evaluation']['harmful_target']:return RED
    return GOLD

def draw_overview(a,out):
    style();subset=[r for r in a['episodes'] if r['arm']=='targeted_check' and r['world'] in ('misleading','syndication')]
    assert len(subset)==6 and sum(r['evaluation']['harmful_target'] for r in subset)==6 and sum(r['counterfactual_correct'] for r in subset)==6
    fig=plt.figure(figsize=(18,11),dpi=100)
    fig.text(.055,.94,'HOW TO WIN AGENTS AND INFLUENCE SWARMS',fontsize=23,weight='bold')
    fig.text(.055,.896,'Correct facts reached the chair. They often failed to change the decision.',fontsize=19,color=GREEN)
    fig.text(.055,.855,'Measured v2 pilot  ·  50/50 outcomes recorded  ·  0 execution failures  ·  $2.00 model usage',color=MUTED,fontsize=13)
    ax=fig.add_axes([.20,.27,.56,.52]);ax.set_xlim(-.5,4.5);ax.set_ylim(9.5,-.5)
    conditions=[(d,w) for d in ['procurement','dependency','travel'] for w in (['clean','misleading','syndication','instruction'] if d=='procurement' else ['clean','misleading','syndication'])]
    for j,(d,w) in enumerate(conditions):
        for i,arm in enumerate(ARMS):
            r=next(x for x in a['episodes'] if x['domain']==d and x['world']==w and x['arm']==arm)
            color=result_color(r)
            ax.add_patch(FancyBboxPatch((i-.43,j-.36),.86,.72,boxstyle='round,pad=0.02,rounding_size=.08',facecolor=color,edgecolor='none',alpha=.18))
            label='CORRECT' if r['evaluation']['correct'] else ('TARGET' if r['evaluation']['harmful_target'] else 'OTHER ERROR')
            ax.text(i,j,label,ha='center',va='center',color=color,fontsize=10,weight='bold')
    ax.set_xticks(range(5),LABELS);ax.xaxis.tick_top();ax.tick_params(length=0,pad=13)
    ax.set_yticks(range(10),[d.title()+' / '+w for d,w in conditions]);ax.tick_params(axis='y',labelsize=11)
    for sp in ax.spines.values():sp.set_visible(False)
    fig.text(.805,.75,'6 / 6',color=RED,fontsize=39,weight='bold')
    fig.text(.805,.69,'Targeted-check choices\nstill favored the attacker\nin misleading / copied\nevidence conditions.',fontsize=12,linespacing=1.55,va='top')
    fig.text(.805,.54,'6 / 6',color=GREEN,fontsize=39,weight='bold')
    fig.text(.805,.48,'Same cases choose correctly\nwhen the recorded checks\nare applied mechanically.\nRetrospective counterfactual.',fontsize=12,linespacing=1.55,va='top')
    fig.text(.055,.185,'WHAT THIS TEACHES',color=MUTED,fontsize=11,weight='bold')
    fig.text(.055,.147,'Verification must update the decision state; collecting another correct report is not enough.',fontsize=17)
    fig.text(.055,.09,'One independent task per application. Cells are paired protocol outcomes, not 50 independent trials.\nSynthetic fixed-exposure scenarios. No confidence intervals or general robustness claim. Counterfactuals are not reruns.',color=MUTED,fontsize=11,linespacing=1.6)
    fig.savefig(out,dpi=100);plt.close(fig)

def draw_frame(r,k,path):
    style();fig=plt.figure(figsize=(12.8,7.68),dpi=100);ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    ax.text(.045,.935,'How to win agents and influence swarms',fontsize=20,weight='bold')
    ax.text(.045,.887,f"{r['domain'].title()}  /  {r['world']}  /  {r['arm']}  ·  task {r['task_id']}  ·  seed {r['seed']}",color=MUTED,fontsize=10)
    seen=r['trajectory'][:k];agents={};checks={};choice=None;confidence=None
    for event in seen:
        if event['phase'] in ('initial','revision'):agents[event['actor']]=event['choice']
        elif event['phase']=='check':checks[event['actor']]=event
        else:choice=event['choice'];confidence=event['confidence']
    phase=seen[-1]['phase'] if seen else 'before first response'
    ax.text(.045,.826,f'Observed response {k} / {len(r["trajectory"])}  ·  {phase.upper()}',color=BLUE,fontsize=12)
    ax.text(.045,.765,'SIX ANALYSTS',color=MUTED,fontsize=10,weight='bold')
    for i in range(6):
        x=.11+i*.155;ch=agents.get(i);color=MUTED if ch is None else GREEN if ch==r['best'] else RED if ch==r['target'] else GOLD
        ax.add_patch(Circle((x,.655),.035,facecolor=color,alpha=1 if ch else .25))
        ax.text(x,.654,str(i+1),ha='center',va='center',color=BG,weight='bold',fontsize=16)
        label='pending' if ch is None else ch.replace(' itinerary','')
        ax.text(x,.585,label,ha='center',fontsize=9,color=color)
    ax.text(.045,.512,'TWO VERIFIERS',color=MUTED,fontsize=10,weight='bold')
    for i in range(2):
        x=.045+i*.475;ax.add_patch(FancyBboxPatch((x,.338),.435,.133,boxstyle='round,pad=.009',facecolor=PANEL,edgecolor='none'))
        if i in checks:
            c=checks[i]['check'];res=checks[i]['result'];fields=['cost'] if c['package']=='commercial' else ['quality','latency','requirements_met']
            label='  ·  '.join(f'{f}: {res[f]}' for f in fields)
            ax.text(x+.014,.433,c['package'].upper()+' — '+c['candidate'],fontsize=10,color=GREEN,weight='bold')
            ax.text(x+.014,.386,label,fontsize=9)
            ax.text(x+.014,.353,'Recorded check response; exact current fixture version',fontsize=8,color=MUTED)
        else:ax.text(x+.014,.40,'Awaiting recorded check response',fontsize=10,color=MUTED)
    ax.add_patch(FancyBboxPatch((.045,.14),.91,.147,boxstyle='round,pad=.01',facecolor=PANEL,edgecolor='none'))
    ax.text(.06,.246,'FINAL CHAIR',fontsize=10,color=MUTED,weight='bold')
    if choice:
        color=GREEN if choice==r['best'] else RED if choice==r['target'] else GOLD
        ax.text(.06,.196,choice+f'  ·  confidence {confidence:.0%}',fontsize=16,color=color,weight='bold')
        ax.text(.52,.239,'POST-RUN RUBRIC AUDIT',fontsize=9,color=MUTED)
        ax.text(.52,.196,r['after_check_rule_choice'],fontsize=16,color=GREEN,weight='bold')
        ax.text(.52,.157,'Counterfactual using the same recorded check results',fontsize=8,color=MUTED)
    else:ax.text(.06,.193,'No final choice observed yet',color=MUTED,fontsize=13)
    ax.text(.045,.082,'Green: true best   ·   Coral: attacker target   ·   Gold: other choice   ·   Gray: pending',fontsize=10,color=MUTED)
    ax.text(.045,.047,'Colors use evaluator-only truth after the run. Response order is logical time; no invented transitions.',fontsize=9,color=MUTED)
    fig.savefig(path,dpi=100);plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('audit',type=Path);p.add_argument('out',type=Path);a=p.parse_args();d=json.loads(a.audit.read_text());a.out.mkdir(parents=True,exist_ok=True)
    draw_overview(d,a.out/'final_frame.png')
    r=next(x for x in d['episodes'] if x['domain']=='procurement' and x['world']=='misleading' and x['arm']=='targeted_check')
    frames=[]
    for k in range(len(r['trajectory'])+1):
        path=a.out/f'step-{k:02}.png';draw_frame(r,k,path)
        with Image.open(path) as im:frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=96))
    frames[0].save(a.out/'measured_replay.gif',save_all=True,append_images=frames[1:],duration=[1300]*15+[4500],loop=0,optimize=True,disposal=2)
    meta={'mapping':'influence-replay-v1','run':d['run'],'assignment':r['assignment'],'frames':len(frames),'time':'ordered model responses','selection':'first procurement/misleading/targeted_check case','inputs':d['input_hashes'],'gif_bytes':(a.out/'measured_replay.gif').stat().st_size}
    (a.out/'visual-validation.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))
if __name__=='__main__':main()
