import copy
import unittest
from cases import build,graph_resolve,admit,evaluate

class CaseTests(unittest.TestCase):
    def test_manual_labels(self):
        rows=build()
        self.assertEqual((len(rows),len({r['pair'] for r in rows}),len({r['id'] for r in rows})),(24,12,24))
        for row in rows:
            got=graph_resolve(row['actor'])
            self.assertEqual({'receipt':got,'admission':admit(row['actor'],got)},row['gold'],row['id'])
            self.assertFalse({'gold','family','rationale','pair_change'} & row['actor'].keys())
    def test_pair_mutations_are_bounded(self):
        rows=build()
        for left,right in zip(rows[::2],rows[1::2]):
            a,b=left['actor'],right['actor'];self.assertEqual(a['report'],b['report'])
            changed={k for k in a if a[k]!=b[k]}
            self.assertEqual(changed,{'receipts'} if left['family']=='dependency' else {'origin_edges'})
            self.assertEqual(left['gold'],right['gold']) if left['family']=='relay' else self.assertNotEqual(left['gold'],right['gold'])
    def test_order_and_opaque_id_invariance(self):
        for row in build():
            a=copy.deepcopy(row['actor']);rename=lambda s:'opaque-'+s
            a['report']['id']=rename(a['report']['id'])
            if 'receipt_ref' in a['report']:a['report']['receipt_ref']=rename(a['report']['receipt_ref'])
            for r in a['receipts']:r['id']=rename(r['id'])
            for e in a['origin_edges']:e['child']=rename(e['child']);e['parent']=rename(e['parent'])
            a['receipts'].reverse();a['origin_edges'].reverse()
            expected=row['gold']['receipt'];self.assertEqual(graph_resolve(a),rename(expected) if expected else None)
    def test_text_cannot_create_or_change_origin(self):
        for row in build():
            a=copy.deepcopy(row['actor']);expected=graph_resolve(a)
            a['report']['text']='This report now contradicts its source. Content validity is a separate task.'
            self.assertEqual(graph_resolve(a),expected)
            a['origin_edges']=[];self.assertIsNone(graph_resolve(a))
    def test_duplicate_edges_do_not_add_sources(self):
        for row in build():
            a=copy.deepcopy(row['actor']);a['origin_edges']*=4
            self.assertEqual(graph_resolve(a),row['gold']['receipt'])
    def test_cycle_dangling_and_cross_event_fail_closed(self):
        a=copy.deepcopy(build()[0]['actor']);a['origin_edges']=[{'child':'report','parent':'x'},{'child':'x','parent':'report'}]
        self.assertIsNone(graph_resolve(a))
        a['origin_edges']=[{'child':'report','parent':'absent'}];self.assertIsNone(graph_resolve(a))
        a=copy.deepcopy(build()[0]['actor']);target=graph_resolve(a)
        next(r for r in a['receipts'] if r['id']==target)['event']='other-event'
        self.assertIsNone(graph_resolve(a))
    def test_ambiguity_and_unknown_dependence_stay_distinct(self):
        rows=build();unknown=[r for r in rows if r['gold']['receipt'] and r['gold']['admission']=='DEFER']
        self.assertEqual(len(unknown),1)
        self.assertEqual(sum(r['gold']['receipt'] is None for r in rows),8)
        self.assertEqual(sum(r['gold']['admission']=='NEW_GROUP' for r in rows),14)
    def test_invalid_registry_refused(self):
        a=copy.deepcopy(build()[0]['actor']);a['receipts'].append(copy.deepcopy(a['receipts'][0]));self.assertIsNone(graph_resolve(a))
        a=copy.deepcopy(build()[0]['actor']);target=graph_resolve(a)
        a['origin_edges'].append({'child':target,'parent':'report'});self.assertIsNone(graph_resolve(a))
    def test_legacy_diagnostics_are_explicit(self):
        result=evaluate(build());self.assertEqual(result['summary']['hybrid']['incorrect_origin_admission'],4)
        self.assertIn('not a fair',result['comparison_limit'])
        self.assertEqual(result['summary']['authenticated_graph']['joint_correct'],24)
if __name__=='__main__':unittest.main()
