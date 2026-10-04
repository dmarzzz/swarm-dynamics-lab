import copy
import itertools
import unittest
from gate import decide


def valid():
    registry={f'r{i}':{'acquisition_id':f'a{i}','value':bit,'q':.65} for i,bit in enumerate((1,0,0))}
    reports=[{'declared_root':f'label{i}','receipt_id':f'r{i}','value':bit,'q':.65} for i,bit in enumerate((1,0,0))]
    return reports,registry


def split_merge_attack():
    reports,registry=valid()
    packet=[dict(reports[0],declared_root='claimed-a')]*4+[dict(reports[0],declared_root='claimed-b')]*3
    packet.extend(dict(r,declared_root='claimed-c') for r in reports[1:])
    return packet,registry


class GateTests(unittest.TestCase):
    def test_upstream_verification_required(self):
        reports,registry=valid()
        for attest in (False,None,1,'true'):
            self.assertEqual(decide(reports,registry,registry_verified=attest)['reason'],'registry_not_verified')
    def test_valid_complete_evidence(self):
        reports,registry=valid();self.assertEqual(decide(reports,registry,registry_verified=True)['decision'],'ZERO')
    def test_split_merge_attack(self):
        reports,registry=split_merge_attack()
        declared={r['declared_root']:r['value'] for r in reports}
        self.assertEqual(len(declared),3);self.assertEqual(sum(declared.values()),2)
        self.assertEqual(decide(reports,registry,registry_verified=True)['decision'],'ZERO')
    def test_multiple_receipts_same_acquisition_collapse(self):
        reports,registry=valid();registry['alias']=dict(registry['r0']);reports+=[dict(reports[0],receipt_id='alias')]*7
        self.assertEqual(decide(reports,registry,registry_verified=True)['verified_acquisitions'],3)
        self.assertEqual(decide(reports,registry,registry_verified=True)['decision'],'ZERO')
    def test_count_and_order_invariance_all_patterns(self):
        for bits in itertools.product((0,1),repeat=3):
            reports,registry=valid()
            for i,bit in enumerate(bits):reports[i]['value']=registry[f'r{i}']['value']=bit
            for counts in ((1,1,1),(7,1,1),(1,7,1),(1,1,7)):
                packet=[r for r,n in zip(reports,counts) for _ in range(n)]
                for ordered in (packet,list(reversed(packet))):
                    self.assertEqual(decide(ordered,registry,registry_verified=True)['decision'],'ONE' if sum(bits)>=2 else 'ZERO')
    def test_missing_receipt_abstains_without_dropping(self):
        reports,registry=valid();reports.append(dict(reports[0],receipt_id='missing'))
        result=decide(reports,registry,registry_verified=True)
        self.assertEqual(result['decision'],'DEFER');self.assertEqual(result['missing_receipts'],['missing'])
    def test_unknown_receipt_ids_not_inferred_from_same_text(self):
        reports,registry=valid();reports[0]['receipt_id']='unknown'
        self.assertEqual(decide(reports,registry,registry_verified=True)['reason'],'missing_receipt')
    def test_altered_value_or_reliability(self):
        for key,value in (('value',0),('q',.8)):
            reports,registry=valid();reports[0][key]=value
            self.assertEqual(decide(reports,registry,registry_verified=True)['reason'],'observation_mismatch')
    def test_registry_conflict_refused(self):
        reports,registry=valid();registry['alias']=dict(registry['r0'],value=0)
        self.assertEqual(decide(reports,registry,registry_verified=True)['reason'],'inconsistent_registry')
    def test_insufficient_or_extra_sources(self):
        reports,registry=valid()
        self.assertEqual(decide(reports[:2],registry,registry_verified=True)['reason'],'three_verified_acquisitions_required')
        registry['r3']=dict(registry['r0'],acquisition_id='a3');reports.append(dict(reports[0],receipt_id='r3'))
        self.assertEqual(decide(reports,registry,registry_verified=True)['reason'],'three_verified_acquisitions_required')
    def test_unequal_reliability(self):
        reports,registry=valid();reports[0]['q']=registry['r0']['q']=.8
        self.assertEqual(decide(reports,registry,registry_verified=True)['reason'],'equal_reliability_required')
    def test_malformed_inputs(self):
        reports,registry=valid()
        for broken in (None,[],[None],[{}],[dict(reports[0],value=True)],[dict(reports[0],q=float('nan'))],[dict(reports[0],receipt_id='../secret')]):
            self.assertEqual(decide(broken,registry,registry_verified=True)['decision'],'DEFER')
        for broken in (None,{'r':None},{'r':{'value':0,'q':.65,'acquisition_id':None}}):
            self.assertEqual(decide(reports,broken,registry_verified=True)['decision'],'DEFER')
    def test_same_observable_packet_different_ancestry(self):
        reports,registry=split_merge_attack()
        # Without receipts these same values/claimed labels fit either 1/0/0 or 1/1/0 origins.
        self.assertEqual([r['value'] for r in reports],[1]*7+[0]*2)
        first_truth='ONE' if sum((1,0,0))>=2 else 'ZERO'
        second_truth='ONE' if sum((1,1,0))>=2 else 'ZERO'
        self.assertNotEqual(first_truth,second_truth)
        self.assertEqual(decide(reports,{},registry_verified=True)['decision'],'DEFER')
    def test_does_not_mutate_inputs(self):
        reports,registry=valid();saved=copy.deepcopy((reports,registry));decide(reports,registry,registry_verified=True)
        self.assertEqual((reports,registry),saved)

if __name__=='__main__':unittest.main()
