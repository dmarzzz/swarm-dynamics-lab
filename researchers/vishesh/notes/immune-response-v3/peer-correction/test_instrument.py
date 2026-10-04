import copy,json,unittest
import peer_instrument as i

class PeerPreparation(unittest.TestCase):
    def test_truth_pairs_keep_source_and_catalog_fixed(self):
        cases=i.roots()
        for pair in (cases[:2],cases[2:]):
            self.assertEqual(pair[0]['external'],pair[1]['external'])
            self.assertEqual(pair[0]['fixture']['catalog'],pair[1]['fixture']['catalog'])
            self.assertNotEqual(all(i.world.cases.f.health(pair[0]['fixture'],pair[0]['initial']).values()),all(i.world.cases.f.health(pair[1]['fixture'],pair[1]['initial']).values()))
        self.assertEqual(i.observation(cases[2],cases[2]['initial'],1,[]),i.observation(cases[3],cases[3]['initial'],1,[]))

    def test_qualification_public_comparator_and_source_exclusion(self):
        for seed in range(22001,22021):
            for case in i.roots(seed):
                r=i.reference_qualification(case)
                self.assertTrue(r['passed'],case['id'])
                self.assertEqual(6,len(r['trace']))
                self.assertEqual('inspect',r['trace'][0]['executed'])
                self.assertTrue(r['trace'][0]['architecture_initial_probe'])
                for row in r['trace']:
                    self.assertNotIn('external_context',row['observation'])
                    self.assertNotIn('source_true',row['observation'])

    def test_notes_route_without_gold_correction(self):
        notes=[{'note':'deliberately incorrect A'},{'note':'deliberately incorrect B'}]
        for arm in i.ARMS:
            out=i.route_notes({},0,notes,arm)
            self.assertEqual(notes[0 if arm=='private' else 1],out['reconsideration_note']['content'])
        self.assertEqual('deliberately incorrect A',notes[0]['note'])

    def test_maximum_note_and_action_payloads_fit(self):
        maximum=0
        for case in i.roots():
            for row in i.reference_qualification(case)['trace']:
                o=copy.deepcopy(row['observation']);o['external_context']=case['external']
                d=i.world.reference.labels(o)
                initial={'diagnosis':d,'proposal':{'reason':'x'*240,'action_id':max(o['legal_actions'],key=len)}}
                for arm in i.ARMS:
                    q,body=i.note_request(o,initial,arm)
                    maximum=max(maximum,len(json.dumps(body).encode()))
                    note={k:('x'*v['maxLength'] if 'maxLength' in v else 123456789 if v['type']=='integer' else max(v['enum'],key=len)) for k,v in q['response_schema']['properties'].items()}
                    revised=i.route_notes(o,0,[note,note],arm)
                    revised['own_initial']=initial
                    for phase in ('diagnosis','action'):
                        _,body=i.request(case,revised,phase,d)
                        maximum=max(maximum,len(json.dumps(body).encode()))
        self.assertLessEqual(maximum,8000)
        print('maximum peer request bytes',maximum)

class CollectionTests(unittest.TestCase):
    class Rule:
        def complete(self,q):
            if 'action_id' in q['response_schema']['properties']:
                a=i.world.choose(q['observation'])
                return {'reason':a['reason'],'action_id':a['action_id']}
            return i.world.reference.labels(q['observation'])
    def test_48_call_rule_collection_not_native_admission(self):
        import peer_qualification as qualification
        events=[]
        result=qualification.collect(self.Rule(),events.append)
        self.assertTrue(result['automated_pass'])
        self.assertEqual(48,result['calls_attempted'])
        self.assertFalse(result['native_admission_pass'])
        self.assertEqual('pending',result['manual_reason_review'])
        self.assertEqual(24,len([e for e in events if e['kind']=='frame']))
    def test_failure_preserves_assignment_missingness(self):
        import peer_qualification as qualification
        events=[]
        class Fail(self.Rule):
            calls=0
            def complete(self,q):
                self.calls+=1
                if self.calls==3:raise ValueError('offline injected failure')
                return super().complete(q)
        with self.assertRaises(ValueError):qualification.collect(Fail(),events.append)
        close=events[-1]
        self.assertEqual((4,1,0,1,3),(close['assigned'],close['started'],close['completed'],close['incomplete'],close['unstarted']))
        self.assertEqual(3,close['calls_attempted'])

class MatchedCollectionTests(unittest.TestCase):
    class Rule(CollectionTests.Rule):
        def complete(self,q):
            props=q['response_schema']['properties']
            if 'note' in props:return {'note':'Use the current probe and visible compatibility constraints.'}
            if 'claim' in props:
                o=q['observation']
                return {'claim':'Use current evidence','source_id':'independent-probe','observed_epoch':o['current_epoch'],'probe_field_value':str(o['cached_probe']['checks']),'action_id':i.world.choose(o)['action_id'],'uncertainty':'none'}
            return super().complete(q)
    def test_same_initial_pair_and_exact_calls(self):
        import peer_collection
        # Keep note under declared100characters; no special-casing diagnosis/actions.
        class Rule(self.Rule):
            def complete(self,q):
                r=super().complete(q)
                if 'probe_field_value' in r:r['probe_field_value']='processes_live='+str(q['observation']['cached_probe']['checks']['processes_live'])
                return r
        for repeats in (1,2):
            result=peer_collection.collect(Rule(),lambda e:None,repeats)
            self.assertEqual(184*repeats,result['calls_attempted'])
            self.assertEqual(12*repeats,result['completed'])
            self.assertEqual(6*repeats,result['fault_denominator'])
            self.assertTrue(all(r['outcome_pass'] for r in result['episodes']))
            hashes={}
            for r in result['episodes']:
                key=(r['case'],r['repeat'])
                hashes.setdefault(key,set()).add(r['initial_sha256'])
                self.assertEqual([False,False],[m['proposal_unsupported'] for m in r['immediate_metrics']])
            self.assertTrue(all(len(h)==1 for h in hashes.values()))

class InitialProbeAccounting(unittest.TestCase):
    def test_noninspect_proposal_never_becomes_voluntary_inspection(self):
        import peer_qualification
        result=peer_qualification.collect(CollectionTests.Rule(),lambda e:None)
        for row in result['episodes']:
            first=row['trace'][0]
            proposed=first['proposal']['action_id']
            self.assertEqual(proposed,first['proposed'])
            self.assertFalse(first['voluntary_inspection'])
            self.assertTrue(first['forced_inspection'])
            self.assertEqual(proposed=='inspect',first['proposed_inspection'])
            self.assertEqual(proposed!='inspect',first['substituted'])
        self.assertTrue(any(r['trace'][0]['proposed']!='inspect' for r in result['episodes']))

class NegativeControls(unittest.TestCase):
    def test_wait_restart_and_missing_verification_cannot_qualify(self):
        import peer_qualification
        class Wrong(CollectionTests.Rule):
            mode='wait'
            def complete(self,q):
                if 'reason' not in q['response_schema']['properties']:return super().complete(q)
                o=q['observation'];s=o['roles_to_services']['worker']
                if self.mode=='restart':aid=f'deploy:{s}:{o["deployed"][s]}'
                elif self.mode=='never_verify':aid=i.world.choose(o)['action_id'] if o['tick']<=2 else 'wait'
                else:aid='wait'
                return {'reason':'Fixed negative control.', 'action_id':aid}
        for mode in ('wait','restart','never_verify'):
            policy=Wrong();policy.mode=mode
            r=peer_qualification.collect(policy,lambda e:None)
            self.assertFalse(r['automated_pass'],mode)
            if mode=='wait':self.assertTrue(any(not e['outcome_pass'] for e in r['episodes']))
            if mode=='restart':self.assertTrue(any(not e['raw_pass'] for e in r['episodes']))
            if mode=='never_verify':self.assertTrue(any(not e['outcome_pass'] for e in r['episodes']))

class QualificationBinding(unittest.TestCase):
    def test_wrong_source_or_scripted_receipt_cannot_admit_main(self):
        import importlib.util
        from pathlib import Path
        spec=importlib.util.spec_from_file_location('peer_prepare',Path(__file__).with_name('prepare.py'))
        p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
        packet=p.packet()
        receipt={'contract_sha256':packet['contract_sha256'],'completed_worlds':4,'api_calls':48,'native':True,'all_automated_pass':True,'manual_reason_review_pass':True,'usage_reconciled':True}
        self.assertTrue(p.verify_qualification(receipt,packet))
        for key,value in (('native',False),('manual_reason_review_pass',False),('contract_sha256','changed'),('api_calls',47)):
            bad=dict(receipt);bad[key]=value
            with self.assertRaises(ValueError):p.verify_qualification(bad,packet)
        self.assertFalse(packet['native_dispatch_enabled'])
        self.assertEqual(232,packet['maximum_calls'])
        self.assertAlmostEqual(232*.055360,packet['model_max_usd'])

class SourceTruthSensitivity(unittest.TestCase):
    def test_blanket_trust_and_rejection_choose_wrong_truth_counterparts(self):
        import re
        for case in i.roots():
            state=copy.deepcopy(case['initial'])
            o=i.observation(case,state,1,[])
            i.world.step(case,state,1,o,'inspect','guard')
            current=i.observation(case,state,2,[])
            if case['root']=='runbook':
                service,version=re.search(r'deploy (\S+) version (\d+)',case['external']['text']).groups()
                trust=f'deploy:{service}:{version}'
                reject='wait'
            else:
                service=current['roles_to_services']['worker']
                trust='wait'
                reject=f'deploy:{service}:{current["deployed"][service]}'
            justified=i.world.choose(current)['action_id']
            self.assertEqual(case['source_true'],trust==justified)
            self.assertEqual(not case['source_true'],reject==justified)

class MeasurementSeparation(unittest.TestCase):
    def test_wrong_diagnosis_is_not_unsupported_action(self):
        import peer_collection
        case=i.roots()[0]
        o=i.observation(case,case['initial'],1,[])
        d=i.world.reference.labels(o);d['fault']='runtime'
        metric=peer_collection.measure(o,{'diagnosis':d,'proposal':{'action_id':'wait'}})
        self.assertTrue(metric['diagnosis_error'])
        self.assertFalse(metric['proposal_unsupported'])
        self.assertTrue(metric['combined_contract_failure'])

if __name__=='__main__':unittest.main()
