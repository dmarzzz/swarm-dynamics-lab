"""Reviewer probes use development examples only. No network or native policy."""
from pathlib import Path
import sys,json,copy
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'researchers/vishesh/notes/dissent/src'))
from cases import make_case,development_examples
from protocol import actor_packet,step,episode,Ledger
from policies import ExactReference

rows=[]
for case,expected in zip(development_examples(),[['HOLD'],['PROCEED'],['PROCEED','PROCEED','HOLD']]):
 result=episode(case,'always-check',ExactReference())
 assert [r['final'] for r in result]==expected
 rows.append({'scenario':case['scenario'],'decisions':expected,'checks':[r['checks'] for r in result],'closures':[r['closure'] for r in result]})
c=make_case('bridge',1101);ledger=Ledger(max_checks=2)
a=step(c,'always-check',ExactReference(),ledger)
d=copy.deepcopy(c);alias=copy.deepcopy(next(e for e in d['evidence'] if e['id']=='e4'));alias['id']='same-observation-copy';d['evidence'].append(alias)
d['challenge']['evidence_ids']=['e4','same-observation-copy']
b=step(d,'always-check',ExactReference(),ledger)
assert b['checks']==1 and b['closure']=='supported'
base=actor_packet(c);mutated=copy.deepcopy(c);mutated['gold']={'action':'PROCEED'};mutated['condition']='SECRET';mutated['task']['future_truth']='SECRET'
assert actor_packet(mutated)==base
# A supported challenge followed by the identical packet reverts to old votes.
l=Ledger(max_checks=2);first=step(c,'always-check',ExactReference(),l);repeat=step(c,'always-check',ExactReference(),l)
assert first['final']=='HOLD' and repeat['final']=='PROCEED' and repeat['closure']=='suppressed_repeat'
result={'examples':rows,'alias_multiplicity':{'first_checks':a['checks'],'duplicate_only_checks':b['checks'],'ledger_total':ledger.checks,'reason':b['reason']},'supported_repeat':{'first_final':first['final'],'repeat_final':repeat['final'],'repeat_closure':repeat['closure'],'repeat_correct':repeat['correct_completion']},'gold_mutation_projection_unchanged':True}
Path(__file__).with_name('dissent-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
