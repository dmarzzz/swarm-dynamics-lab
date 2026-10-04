import json, random, sys, unittest
from copy import deepcopy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from corpus import CASES, actor, canonical, copy_output, decide, gold, mutated, reference, source_controller
from prepare import assignments, request, validate

class PacketTests(unittest.TestCase):
    def test_labels_and_counterfactuals_have_two_witnesses(self):
        for c in CASES:
            with self.subTest(c=c['id']):
                self.assertEqual(decide(c),c['expected']);self.assertEqual(reference(c),c['expected'])
                m=mutated(c);self.assertNotEqual(decide(m),decide(c));self.assertEqual(reference(m),m['expected'])
    def test_balance_and_all_target_spans(self):
        self.assertEqual(sum(c['expected']=='GO' for c in CASES),6)
        for c in CASES:
            p=actor(c);g=gold(c);self.assertTrue(6<=len(g['targets'])<=12)
            self.assertEqual([r['text'] for r in p['records']],[r['source_span'] for r in g['targets']])
    def test_actor_allowlist_excludes_state_labels_and_root_ids(self):
        for c in CASES:
            p=actor(c);self.assertEqual(set(p),{'records'})
            for r in p['records']:self.assertEqual(set(r),{'id','time','text'})
            self.assertNotIn(c['id'],canonical(p));self.assertNotIn('updates',canonical(p))
    def test_reordering_and_opaque_record_ids_do_not_change_labels(self):
        for c in CASES:
            v=deepcopy(c);random.Random(613).shuffle(v['events'])
            for i,e in enumerate(v['events']):e['id']=f'opaque-{100-i}'
            self.assertEqual(decide(v),c['expected']);self.assertEqual(reference(v),c['expected'])
    def test_duplicate_same_origin_records_do_not_add_evidence(self):
        for c in CASES:
            v=deepcopy(c);v['events']+=deepcopy(v['events'])
            self.assertEqual(decide(v),c['expected']);self.assertEqual(reference(v),c['expected'])
    def test_full_copy_and_source_reopen_fit_caps(self):
        self.assertEqual(len(validate()),12)
    def test_source_access_is_only_arm_information_difference(self):
        for c in CASES:
            p=actor(c);old=copy_output(c)
            self.assertEqual(request('P',p),request('R',p))
            a,b=request('P',p,old),request('R',p,old)
            ap,bp=json.loads(a['messages'][1]['content']),json.loads(b['messages'][1]['content'])
            self.assertEqual(ap,{'previous_handoff':old});self.assertEqual(bp,dict(ap,source_packet=p))
            a['messages'][1]['content']='';b['messages'][1]['content']='';self.assertEqual(a,b)
    def test_assignment_coverage_and_parent_isolation(self):
        rows=assignments();self.assertEqual(len(rows),144);ids={r['id'] for r in rows};self.assertEqual(len(ids),144)
        for r in rows:
            if r['hop']==1:self.assertIsNone(r['parent'])
            else:self.assertIn(r['parent'],ids);self.assertEqual(r['parent'].rsplit(':',1)[0],r['id'].rsplit(':',1)[0])
        for block in (1,2):
            for c in CASES:
                self.assertEqual(sum(r['block']==block and r['case_id']==c['id'] for r in rows),6)
    def test_missing_essential_structured_evidence_is_not_silently_scored(self):
        for c in CASES:
            v=deepcopy(c);v['events']=[]
            with self.assertRaises((KeyError,StopIteration)):decide(v)
            with self.assertRaises((KeyError,StopIteration)):reference(v)
    def test_partial_repairs_do_not_accidentally_grant_release(self):
        c=deepcopy(CASES[0]);m=deepcopy(c['mutation']);m['updates']={'approval':True};c['events'].append(m)
        self.assertEqual(decide(c),'HOLD');self.assertEqual(reference(c),'HOLD')
    def test_full_copy_three_hops_preserves_every_target(self):
        for c in CASES:
            out=copy_output(c)
            for _ in range(3):out=json.loads(canonical(out))
            for t in gold(c)['targets']:self.assertIn(t['source_span'],out['handoff'])
    def test_unknown_arm_and_oversized_input_fail_closed(self):
        p=actor(CASES[0])
        with self.assertRaises(ValueError):request('X',p)
        with self.assertRaises(ValueError):request('R',p,{'handoff':'x'*9000,'decision':'HOLD'})
    def test_controller_uses_only_actor_packet_and_rejects_unknown_evidence(self):
        for c in CASES:
            for v in (c,mutated(c)):
                p=actor(v);random.Random(31).shuffle(p['records'])
                for i,r in enumerate(p['records']):r['id']=f'anonymous-{i}'
                self.assertEqual(source_controller(p),v['expected'])
                p['records'].append({'id':'extra','time':'10:00','text':'Unrecognized contradictory update.'})
                with self.assertRaises(ValueError):source_controller(p)

if __name__=='__main__':unittest.main()
