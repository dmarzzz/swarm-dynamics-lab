import copy
import json
import unittest
from tasks import generate, reference_answer, evaluate, strict_json, operational, qualification_manifest, digest

class Fixtures(unittest.TestCase):
    def test_roots_and_sizes(self):
        rows=qualification_manifest()
        self.assertEqual(len(rows),80)
        self.assertEqual(sum(r['stage']=='Q-A' for r in rows),16)
        self.assertEqual(len({r['id'] for r in rows}),80)
        for root in {r['root_id'] for r in rows}:
            self.assertEqual(len({r['input_sha256'] for r in rows if r['root_id']==root}),1)
        for family in ('evidence','repository'):
            for structure in ('parallel','chain'):
                for root in range(4):
                    a=generate(family,structure,root)
                    self.assertEqual(a,generate(family,structure,root))
                    self.assertEqual(len({digest(generate(family,structure,root,s).public) for s in ('qualification','fit','validation')}),3)
                    self.assertNotIn('truth',a.public)
                    self.assertNotIn('hidden_inputs',a.public)
        with self.assertRaises(ValueError): generate('evidence','parallel',0,'transfer')

    def test_every_reference_and_broken_repository(self):
        for family in ('evidence','repository'):
            for structure in ('parallel','chain'):
                for root in range(20):
                    task=generate(family,structure,root)
                    result=evaluate(task,json.dumps(reference_answer(task)))
                    self.assertTrue(result['substantive_success'],task.public['id'])
                    if family=='repository':
                        self.assertFalse(evaluate(task,json.dumps({'files':task.public['files']}))['substantive_success'])

    def test_matched_coefficients_and_graph(self):
        for family in ('evidence','repository'):
            a,b=[generate(family,s,0) for s in ('parallel','chain')]
            self.assertEqual(len(a.public['items']),len(b.public['items']))
            self.assertEqual(sum(map(len,a.public['dependencies'].values())),0)
            self.assertEqual(sum(map(len,b.public['dependencies'].values())),15)
            if family=='evidence': self.assertEqual(a.public['records'],b.public['records'])
            else: self.assertEqual(a.truth['coefficients'],b.truth['coefficients'])

    def test_evidence_mutations(self):
        t=generate('evidence','chain',0);ref=reference_answer(t);key=t.public['items'][-1]
        for kind in ('wrong_value','missing_source','extra_source','duplicate_source','boolean','omitted','extra_field'):
            a=copy.deepcopy(ref)
            if kind=='wrong_value': a['answers'][key]['value']+=1
            if kind=='missing_source': a['answers'][key]['source_ids'].pop()
            if kind=='extra_source': a['answers'][key]['source_ids'].append('imaginary')
            if kind=='duplicate_source': a['answers'][key]['source_ids'].append(a['answers'][key]['source_ids'][0])
            if kind=='boolean': a['answers'][key]['value']=True
            if kind=='omitted': del a['answers'][key]
            if kind=='extra_field': a['truth']='anything'
            self.assertFalse(evaluate(t,json.dumps(a))['substantive_success'],kind)
        reordered=copy.deepcopy(ref)
        reordered['answers'][key]['source_ids'].reverse()
        self.assertTrue(evaluate(t,json.dumps(reordered))['substantive_success'])

    def test_strict_json(self):
        for text in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}','x'*65537):
            with self.assertRaises(ValueError): strict_json(text)

    def test_forbidden_python(self):
        t=generate('repository','chain',1);ref=reference_answer(t)
        cases=['import os\ndef item_00(x):\n return x',
               'def item_00(x):\n return __import__("os")',
               'def item_00(x):\n return x.__class__',
               'def item_00(x):\n return item_00(x)',
               'def item_00(x):\n while True: pass',
               'def item_00(x):\n return 2**10000000',
               'def item_00(x=1):\n return x',
               '@print\ndef item_00(x):\n return x',
               'def item_00(x):\n return True',
               'def item_00(x):\n return item_07(x)']
        for source in cases:
            a=copy.deepcopy(ref);a['files']['item_00.py']=source
            self.assertFalse(evaluate(t,json.dumps(a))['valid'],source)
        a=copy.deepcopy(ref);a['files']['../test.py']='pass'
        self.assertFalse(evaluate(t,json.dumps(a))['valid'])

    def test_equivalent_repair_and_constant_cheat(self):
        t=generate('repository','chain',2);ref=reference_answer(t)
        a=copy.deepcopy(ref)
        for key in a['files']: a['files'][key]=a['files'][key].replace('return ','return 0 + ')
        self.assertTrue(evaluate(t,json.dumps(a))['substantive_success'])
        b=copy.deepcopy(ref);b['files']['item_00.py']='def item_00(x):\n return 0\n'
        self.assertFalse(evaluate(t,json.dumps(b))['substantive_success'])

    def test_outcome_boundaries(self):
        t=generate('evidence','parallel',0);r=evaluate(t,json.dumps(reference_answer(t)))
        self.assertTrue(operational(r,10,1,10,1))
        self.assertFalse(operational(r,10.01,1,10,1))
        self.assertFalse(operational(r,10,1.01,10,1))
        self.assertFalse(operational(r,10,1,10,1,False))
        for bad in (float('nan'),float('inf'),-1,True):
            with self.assertRaises(ValueError): operational(r,bad,1,10,1)
        self.assertFalse(operational(evaluate(t,'{}'),0,0,10,1))

if __name__=='__main__': unittest.main()
