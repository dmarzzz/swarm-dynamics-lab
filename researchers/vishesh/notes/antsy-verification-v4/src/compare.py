"""Post-run paired backend comparison; common controls are counted once."""
import argparse,json,statistics
from pathlib import Path
from analyze import interval,avg
from policies import ARMS

def load(p):return [json.loads(s) for s in (p/'episodes.jsonl').read_text().splitlines()]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--laya',type=Path,required=True);ap.add_argument('--jev',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    data={'Laya':load(a.laya),'Jev':load(a.jev)};assert [r['id'] for r in data['Laya']]==[r['id'] for r in data['Jev']]==list(range(30,100))
    for l,j in zip(data['Laya'],data['Jev']):
        assert l['mode_scores']==j['mode_scores']
        for arm in ARMS[:4]:assert l['arms'][arm]==j['arms'][arm]
    report={'n_unique_receipts':70,'shared_controls_counted_once':True,'backend_contrasts':{},'arms':{}}
    for model,blocks in data.items():
        report['arms'][model]={}
        for arm in ARMS:
            rows=[b['arms'][arm]['metrics'] for b in blocks];qualities=[r['quality'] for r in rows]
            report['arms'][model][arm]={'quality':avg(qualities),'quality_bootstrap_95':interval(qualities),'checks':avg([r['checks'] for r in rows]),'regret':avg([r['regret'] for r in rows]),'total_exact':sum(r['total_field_exact'] is True for r in rows),'total_exact_n':sum(r['total_field_exact'] is not None for r in rows)}
    for arm in ARMS[4:]:
        diffs=[j['arms'][arm]['metrics']['quality']-l['arms'][arm]['metrics']['quality'] for l,j in zip(data['Laya'],data['Jev'])]
        report['backend_contrasts'][arm]={'jev_minus_laya':avg(diffs),'paired_bootstrap_95':interval(diffs)}
    (a.out/'comparison.json').write_text(json.dumps(report,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'figure.facecolor':'#0d1424','axes.facecolor':'#0d1424','text.color':'#eef4ff','axes.labelcolor':'#eef4ff','xtick.color':'#9cacc6','ytick.color':'#eef4ff','axes.edgecolor':'#53637f'})
    fig,ax=plt.subplots(figsize=(16,10),dpi=120);fig.subplots_adjust(left=.21,right=.86,top=.83,bottom=.20)
    colors={'Laya':'#50d9c6','Jev':'#9992ff'}
    for i,arm in enumerate(ARMS):
        models=['Laya'] if i<4 else ['Laya','Jev']
        for model in models:
            row=report['arms'][model][arm];y=i+({'Laya':-.15,'Jev':.15}[model] if i>=4 else 0);m=row['quality']*100;lo,hi=[x*100 for x in row['quality_bootstrap_95']]
            color='#b7c4d8' if i<4 else colors[model]
            ax.errorbar(m,y,xerr=[[m-lo],[hi-m]],fmt='o',capsize=4,color=color,markersize=8,lw=2,label=model if i==4 else None)
            ax.text(1.04,y,f"{row['quality']:.1%} / {row['checks']:.2f}",transform=ax.get_yaxis_transform(),ha='left',va='center',fontsize=12,color=color)
    ax.set_yticks(range(len(ARMS)),ARMS);ax.invert_yaxis();ax.set_xlabel('Mean annotated-token recall (%) · descriptive receipt bootstrap 95% intervals',labelpad=16);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False);ax.legend(loc='lower left',frameon=False)
    fig.text(.07,.94,'Antsy | does a committee beat the cheap controls?',fontsize=26,weight='bold');fig.text(.07,.89,'70 paired real receipts · same OCR outputs, QA tool and policies · distinct Laya and Jev conditions',fontsize=15,color='#9cacc6');fig.text(.87,.85,'Quality / checks',fontsize=12)
    fig.text(.07,.07,'Four deterministic/random controls are shared—not additional samples. Higher recall is better; checks have a separate cost.',fontsize=12,color='#9cacc6');fig.text(.07,.035,'Exploratory CORD validation study; ideal regional QA, same-checkpoint roles, no production or general swarm-superiority claim.',fontsize=12,color='#9cacc6')
    fig.savefig(a.out/'comparison.png',facecolor=fig.get_facecolor());plt.close(fig)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
