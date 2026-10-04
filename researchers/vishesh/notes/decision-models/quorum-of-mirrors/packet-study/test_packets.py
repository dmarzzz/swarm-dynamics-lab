import copy,unittest
from corpus import generate,validate
from instrument import parse,predict,inspect

class PacketTests(unittest.TestCase):
    def test_development_oracle_and_source_conservation(self):
        r=validate(generate('development',20261004),'development')
        self.assertEqual((r['roots'],r['packets'],r['critical_mismatches']),(12,48,0))
        self.assertEqual(r['correct']['source_parser'],48)
    def test_parser_authored_cases_not_generator_roundtrips(self):
        q={'kind':'running','entity':'motorX','time':'11:30'}
        examples=[('At 11:30, motorX was not stopped.',True),('At 11:30, motorX was not running.',False),
         ('At 11:29, motorX was running.',None),('At 11:30, other was running.',None),
         ('Plan: at 11:30, motorX will be running.',None),
         ('Initial: at 11:30, motorX was running.\nCorrection: at 11:30, motorX was stopped.',False),
         ('At 11:30, motorX was running.\nAt 11:30, motorX was stopped.',None),
         ('At 11:30, motorX may have been running.',None)]
        for text,want in examples:self.assertEqual(parse(text,q),want,text)
    def test_units_boundaries_and_equivalence(self):
        q={'kind':'mass','entity':'loadX','time':'12:15','threshold_grams':5000}
        for n,u,v in [('5','kilograms',True),('5000','grams',True),('4.999','kilograms',False),('4999','grams',False),('0.005','kilograms',False)]:
            self.assertEqual(parse(f'At 12:15, loadX measured {n} {u}.',q),v)
    def test_order_rename_and_copy_invariance(self):
        for row in generate('development',7):
            a=copy.deepcopy(row['actor']);expected=predict(a)
            a['receipts'].reverse();a['reports'].reverse()
            rename={r['id']:'opaque-'+str(i) for i,r in enumerate(a['receipts'])}
            for r in a['receipts']:r['id']=rename[r['id']]
            for r in a['reports']:r['receipt_id']=rename[r['receipt_id']];r['id']='renamed-'+r['id']
            extra=copy.deepcopy(a['reports'][0]);extra['id']='extra-report';a['reports'].append(extra)
            self.assertEqual(predict(a),expected)
    def test_report_inversion_changes_fidelity_not_source_decision(self):
        rows=generate('development',11)
        for a,b in zip(rows[::2],rows[1::2]):
            self.assertEqual(predict(a['actor']),predict(b['actor']))
            self.assertNotEqual([c['faithful'] for c in inspect(a['actor'])['claims']],[c['faithful'] for c in inspect(b['actor'])['claims']])
    def test_wrong_schema_or_missing_or_untrusted_source_fails_closed(self):
        base=generate('development',1)[0]['actor'];bad=[]
        a=copy.deepcopy(base);a['gold']='ONE';bad.append(a)
        a=copy.deepcopy(base);a['reports'][0]['receipt_id']='absent';bad.append(a)
        a=copy.deepcopy(base);a['receipts'].pop();bad.append(a)
        a=copy.deepcopy(base);a['receipts'][0]['group']=None;bad.append(a)
        a=copy.deepcopy(base);a['receipts'][0]['id']=a['receipts'][1]['id'];bad.append(a)
        a=copy.deepcopy(base);a['receipts'][0]['text']='not a supported statement';bad.append(a)
        a=copy.deepcopy(base);a['reports'].append(copy.deepcopy(a['reports'][0]));bad.append(a)
        a=copy.deepcopy(base);a['receipts'][0]['group']=a['receipts'][1]['group'];bad.append(a)
        for a in bad:self.assertEqual(predict(a),'DEFER')
    def test_ablations_are_not_cherry_picked(self):
        d=validate(generate('development',31),'development')
        self.assertGreater(d['correct']['report_vote'],0);self.assertLess(d['correct']['report_vote'],48)
        self.assertGreater(d['correct']['deduplicated_claims'],0);self.assertLess(d['correct']['deduplicated_claims'],48)
    def test_gold_not_available_to_parser(self):
        row=generate('development',1)[0];a=copy.deepcopy(row['actor']);got=predict(a)
        row['gold']['decision']='DEFER';self.assertEqual(predict(a),got)
    def test_conflicting_corrections_fail_closed(self):
        q={'kind':'running','entity':'M','time':'12:00'}
        self.assertIsNone(parse('Correction: at 12:00, M was running.\nCorrection: at 12:00, M was stopped.',q))
if __name__=='__main__':unittest.main()
