"""Prespecified clean/omission contrast; incomplete decisions retain bounds."""
import argparse,json
from collections import defaultdict
from pathlib import Path

def subtract(a,b):return [a[0]-b[1],a[1]-b[0]]
def harm(row):
    if row is None or not row['valid']:return [0,1]
    h=row['evaluation']['harmful_target'];return [h,h]
def analyze(rows):
    groups=defaultdict(dict)
    for row in rows:
        key=(row['family'],row['profile']);slot=(row['world'],row['arm'])
        if slot in groups[key]:raise ValueError('duplicate assignment; never silently pool retries')
        groups[key][slot]=row
    pairs=[]
    for (family,profile),cells in sorted(groups.items()):
        if family in ('genuine_value','evidence_gap'):continue
        # A one-world diagnostic must not masquerade as a paired effect.
        worlds={w for w,a in cells}
        if not worlds.intersection({'clean','omission'}):continue
        differences={w:subtract(harm(cells.get((w,'team_ballots'))),harm(cells.get((w,'team_evidence')))) for w in ('clean','omission')}
        interval=subtract(differences['omission'],differences['clean'])
        pairs.append({'family':family,'profile':profile,'contrast_bounds':interval,
                      'identified':interval[0]==interval[1],
                      'required_chair_cells_present':sum((w,a) in cells for w in ('clean','omission') for a in ('team_ballots','team_evidence'))})
    counts={}
    for arm in ('team_ballots','team_evidence','solo'):
        rs=[r for r in rows if r['arm']==arm];valid=[r for r in rs if r['valid']]
        counts[arm]={'assigned':len(rs),'valid':len(valid),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in valid),
                     'avoidable_deferrals':sum(r['evaluation']['avoidable_deferral'] for r in valid),
                     'constraint_breaches':sum(bool(r['evaluation']['constraint_violations']) for r in valid)}
    return {'contrast':'(ballots - evidence) omission minus clean; harmful target selection',
            'pairs':pairs,'per_arm':counts,'independence':'Descriptive dossier pairs; shared prefixes are not independent trials. Missing outcomes are bounded, never set to zero.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('out');a=p.parse_args()
    report=analyze(json.loads((Path(a.run)/'outcomes.json').read_text()))
    Path(a.out).write_text(json.dumps(report,indent=2)+'\n')
