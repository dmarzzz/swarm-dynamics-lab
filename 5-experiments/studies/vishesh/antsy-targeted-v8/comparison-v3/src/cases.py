"""Deterministic parser controls; these are not simulated native OCR performance."""
from common import original,repaired,digest


def words(lines):
    result=[]
    for y,line in enumerate(lines):
        for x,text in enumerate(line):
            result.append({'text':text,'x':float(x*300),'y':float(y*80+20),'h':24.,
                           'box':[float(x*300),float(y*80+8),200.,24.],'confidence':.9})
    return result


def suite():
    cases=[]
    for n in (17000,86000,245000):
        value=f'{n:.2f}'; amount=f'{n:,}'.replace(',','.')
        definitions=[
            ('ordinary',[['Total',amount]],value),
            ('quantity',[['Total(Qty=2)',amount]],value),
            ('distractors',[['Subtotal','10.000'],['Tax','1.000'],['Total',amount],['Cash','300.000'],['Change','55.000']],value),
            ('missing',[['Subtotal',amount],['Cash','300.000']],None),
            ('damaged_quantity',[['Total(Qty-2',amount]],None),
            ('conflicting',[['Total',amount],['Total',f'{n+1000}']],None),
            ('spurious_number',[['Total(Qty=2)','1',amount]],None),
            ('explicit_final_unresolved',[['Total',amount],['Grand Total','1','2']],None),
        ]
        for family,lines,gold in definitions:
            cases.append({'id':f'{family}-{n}','family':family,'words':words(lines),'expected':gold})
    return cases


def validate():
    rows=[]
    for case in suite():
        new=repaired.extract(case['words']);old=original.extract(case['words'])
        reverse=repaired.extract(list(reversed(case['words'])))
        shifted=[{**w,'x':w['x']+137,'y':w['y']+59,'box':[w['box'][0]+137,w['box'][1]+59,*w['box'][2:]]} for w in case['words']]
        value=new['value']
        rows.append({'case':case['id'],'family':case['family'],'expected':case['expected'],'original':old['value'],
          'repaired':value,'pass':value==case['expected'],'order_invariant':reverse['value']==value,
          'translation_invariant':repaired.extract(shifted)['value']==value})
    return {'scope':'24 authored parser controls, 8 families, 3 amount variants; no OCR sampling',
            'case_sha256':digest(suite()),'passed':all(r['pass'] and r['order_invariant'] and r['translation_invariant'] for r in rows),'rows':rows}

if __name__=='__main__':
    import argparse
    from common import write
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();v=validate();write(a.out,v)
    print({'cases':len(v['rows']),'passed':v['passed']})
    raise SystemExit(0 if v['passed'] else 1)
