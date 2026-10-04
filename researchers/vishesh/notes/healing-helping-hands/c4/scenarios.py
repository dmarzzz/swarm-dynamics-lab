"""Fresh synthetic report definitions; generation is explicit, never on import."""
import random
FAMILIES=('counts','percentages','error_rates','before_after','negation','repeated_tests','uncertainty','subgroup','superseded','irrelevant_metric','expectations','target_distractor')
LABELS=('SUPPORT','REFUTE','UNCERTAIN')

def fixture(family,label,index,split):
    if family not in FAMILIES or label not in LABELS:raise ValueError('unknown_fixture')
    rng=random.Random(f'C4/{split}/{family}/{label}/{index}');base=rng.randrange(50,80);delta=rng.randrange(3,10)
    name=f'Method {split}-{family}-{index}';test=f'Test {split}-{index}'
    claim=f'{name} improves accuracy over the baseline on {test}.'
    better=label=='SUPPORT';unknown=label=='UNCERTAIN';value=base+delta if better else base-delta
    direct=f'On {test}, {name} achieved {value}% accuracy and the baseline achieved {base}%.'
    absent=f'Accuracy for {name} on {test} was not measured.'
    templates={
      'counts':absent if unknown else f'On {test}, the baseline answered {base} of 100 questions correctly. {name} answered {value} of 100 correctly.',
      'percentages':absent if unknown else direct,
      'error_rates':absent if unknown else f'On {test}, the baseline made {100-base} errors in 100 answers. {name} made {100-value} errors in 100 answers.',
      'before_after':absent if unknown else f'The same {test} comparison changed accuracy from the baseline of {base}% to {value}% with {name}.',
      'negation':f'The team did not test accuracy for {name} on {test}.' if unknown else (f'{name} was not merely faster: measured accuracy on {test} improved over the baseline.' if better else f'{name} did not improve accuracy over the baseline on {test}; measured accuracy was unchanged.'),
      'repeated_tests':absent if unknown else f'Two completed evaluations on {test} each found {name} had {"higher" if better else "lower"} accuracy than the baseline.',
      'uncertainty':f'No accuracy estimates are available for {name} or the baseline on {test}; investigators are uncertain which is better.' if unknown else f'Although the team was uncertain before testing, the completed accuracy comparison on {test} found {name} {"better" if better else "worse"} than baseline.',
      'subgroup':f'{name} improved on a different test; {test} has not been evaluated.' if unknown else direct+' A different test showed the opposite result.',
      'superseded':f'An earlier accuracy result for {name} on {test} was withdrawn as erroneous. There is no replacement measurement.' if unknown else f'A previous claim of {"worse" if better else "better"} accuracy was withdrawn as erroneous. The corrected comparison is: '+direct,
      'irrelevant_metric':f'{name} ran faster on {test}, but accuracy was not evaluated.' if unknown else f'{name} used less memory and ran faster. '+direct,
      'expectations':f'The team expects {name} to beat the baseline on {test}, but no accuracy experiment has run.' if unknown else f'The team expected {name} to be {"worse" if better else "better"}. Actual results: '+direct,
      'target_distractor':f'Another method beat the baseline on {test}. {name} was not evaluated.' if unknown else f'Another method achieved {base+delta}% accuracy on {test}. For the requested method: '+direct,
    }
    return {'id':f'C4-{split}-{family}-{label}-{index}','family':family,'claim':claim,'report':templates[family],'expected':label}

def assignments(stage):
    if stage=='S0':
        # Plain dedicated qualification wording; S1 mechanisms are not used here.
        rows=[]
        for label in LABELS:
            for i in range(20):
                name=f'Qualification method C4-{label}-{i}'
                forms={'SUPPORT':('measured higher accuracy','improved measured accuracy','gave more correct answers','outperformed baseline accuracy'), 'REFUTE':('measured lower accuracy','did not improve measured accuracy','gave fewer correct answers','matched baseline accuracy exactly'), 'UNCERTAIN':('was never tested for accuracy','has no accuracy result available','was tested for speed only','has only a planned accuracy experiment')}
                rows.append({'id':f'C4-S0-{label}-{i}','family':f'qualification-{i%4}','claim':name+' improves accuracy over baseline.','report':name+' '+forms[label][i%4]+'.','expected':label})
    elif stage=='S1':rows=[fixture(f,l,i,'S1') for f in FAMILIES for l in LABELS for i in range(12)]
    else:raise ValueError('unknown_stage')
    random.Random('C4-'+stage).shuffle(rows)
    return [{**r,'status':'planned','labels':{}} for r in rows]
