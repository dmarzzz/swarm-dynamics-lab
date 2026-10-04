"""Exposes how authored business assumptions change the acceptable set."""
import copy
import json
from pathlib import Path
from dossier import FAMILIES,build,evaluate

def audit():
    rows=[]
    for family in FAMILIES:
        for profile in range(4):
            c=build(family,profile);variants=[]
            for multiplier in (.5,1,1.5):
                for tolerance in (0,.03,.10):
                    v=copy.deepcopy(c);v['brief']['human_cost_per_unresolved_ticket']*=multiplier;v['brief']['cost_tolerance_fraction']=tolerance
                    e=evaluate(v,{'choice':'DEFER','annual_total_usd':None})
                    variants.append({'human_cost_multiplier':multiplier,'tolerance':tolerance,'acceptable':e['acceptable']})
            sets={tuple(x['acceptable']) for x in variants}
            rows.append({'case_id':c['case_id'],'acceptable_set_changes':len(sets)>1,'variants':variants})
    return {'cases':len(rows),'sensitivity_dependent':sum(r['acceptable_set_changes'] for r in rows),'note':'Scenario sensitivity, not a model result. Do not hide unstable cases.','rows':rows}
if __name__=='__main__':
    import sys
    a=audit();Path(sys.argv[1]).write_text(json.dumps(a,indent=2));print(json.dumps({k:v for k,v in a.items() if k!='rows'}))
