import itertools,json,sqlite3,tempfile,unittest,time,socket
from pathlib import Path
from contextlib import closing
from types import SimpleNamespace
from unittest.mock import patch
from next_stage import make_manifest,validate_manifest,checked_response,count_reference,analyze
from next_runtime import Ledger,hashes,run,allocation_check,preflight,safe_reason,research_check
from qualification import SNAPSHOT,PROVIDER,RESERVE,manifest as old_manifest,digest
from relay import Budget

def response(choice):
    return {'model':SNAPSHOT,'provider':PROVIDER,'usage':{'cost':.00001,'input_tokens':500,'output_tokens':0},'answers':{'decision':{'choice':choice,'probabilities':{c:float(c==choice) for c in ['ZERO','ONE','DEFER']}}}}
def receipt(a,choice=None):
    return {'id':a['id'],'request_sha256':a['request_sha256'],'status':'complete','response':response(choice or a['expected'])}
def original_ledger(path):
    with closing(sqlite3.connect(path)) as db,db:
        db.execute('CREATE TABLE authority (id INTEGER PRIMARY KEY,experiment TEXT,cap REAL)')
        db.execute('INSERT INTO authority VALUES (1,?,?)',('quorum-of-mirrors',1.))
        db.execute('CREATE TABLE calls (id TEXT PRIMARY KEY,reserved REAL,status TEXT,actual REAL)')
        db.executemany('INSERT INTO calls VALUES (?,?,?,?)',[(a['id'],RESERVE,'complete',.00001) for a in old_manifest()['assignments']])
    return Ledger(path)

class NextContract(unittest.TestCase):
    def test_fixture_coverage_and_anti_majority(self):
        m=make_manifest();self.assertEqual(len(m['assignments']),16)
        full=[a for a in m['assignments'] if a['lineage']=='full'];self.assertEqual(len(full),8)
        self.assertEqual({(a['q'],a['expected'],a['context']) for a in full},set(itertools.product((.65,.8),('ZERO','ONE'),('peer','self'))))
        for a in full:
            reports=a['request']['state']['reports'];majority='ONE' if sum(r['value'] for r in reports)>=5 else 'ZERO'
            self.assertNotEqual(majority,a['expected']);self.assertEqual(count_reference(reports),a['expected'])
            slots=a['request']['state']['prior_decisions']
            if a['context']=='peer':
                self.assertEqual(len(slots),5);self.assertEqual(sum(s['status']=='unavailable' for s in slots),1)
                self.assertEqual(sum(s.get('choice')!=a['expected'] for s in slots if s['status']=='available'),3)
            else:self.assertNotEqual(slots[0]['choice'],a['expected'])
    def test_neutral_ids_mask_and_label_symmetry(self):
        pairs={}
        for a in make_manifest()['assignments']:
            state=a['request']['state'];self.assertEqual(set(state),{'reports','focal_slot','prior_decisions'});self.assertNotIn(a['id'],json.dumps(a['request']))
            for r in state['reports']:
                self.assertEqual(set(r),{'id','value','q','visible_root'});self.assertRegex(r['id'],r'^d\d{2}$')
            if a['lineage']=='partial':self.assertEqual(sum(r['visible_root'] is None for r in state['reports']),2)
            pairs.setdefault((a['lineage'],a['context'],a['q']),[]).append(a)
        for group in pairs.values():
            x,y=[a['request']['state']['reports'] for a in group]
            self.assertEqual([(r['id'],r['visible_root']) for r in x],[(r['id'],r['visible_root']) for r in y]);self.assertTrue(all(a['value']!=b['value'] for a,b in zip(x,y)))
    def test_distribution_aware_shortcut_all_support(self):
        n=0
        for bits,favored,balanced in itertools.product(itertools.product((0,1),repeat=3),range(3),(True,False)):
            shape=[3]*3 if balanced else [7 if i==favored else 1 for i in range(3)];reports=[{'value':b} for b,c in zip(bits,shape) for _ in range(c)]
            self.assertEqual(count_reference(reports),'ONE' if sum(bits)>1 else 'ZERO');n+=1
        self.assertEqual(n,48)
    def test_frozen_contract_rejects_target_payload_and_order_changes(self):
        for change in ('target','payload','order'):
            m=make_manifest()
            if change=='target':m['assignments'][0]['expected']='DEFER'
            if change=='payload':m['assignments'][0]['request']['state']['truth']=1
            if change=='order':m['assignments'].reverse()
            with self.assertRaises(ValueError):validate_manifest(m)
    def test_partial_defer_not_oracle_graded(self):
        m=make_manifest();s=analyze(m,[receipt(a,'DEFER' if a['lineage']=='partial' else a['expected']) for a in m['assignments']])
        self.assertTrue(s['qualified']);self.assertEqual(s['full_correct'],8);self.assertTrue(all(x['expected_MAP'] is None for x in s['cells'] if x['lineage']=='partial'))
    def test_all_assigned_failure_missing_and_duplicates(self):
        m=make_manifest();rows=[receipt(a) for a in m['assignments']];self.assertTrue(analyze(m,rows)['qualified']);self.assertFalse(analyze(m,rows[:-1])['qualified'])
        rows[0].update(status='failed');s=analyze(m,rows);self.assertEqual(s['assigned'],16);self.assertEqual(s['failed'],1);self.assertFalse(s['qualified'])
        with self.assertRaises(ValueError):analyze(m,rows+[rows[0]])
    def test_scoring_and_schema_rejections(self):
        for field,value in [('cost',float('nan')),('input_tokens',True),('output_tokens',1),('cost',.5)]:
            r=response('ONE');r['usage'][field]=value
            with self.assertRaises(ValueError):checked_response(r)
        r=response('ONE');r['answers']['decision']['choice']='ZERO'
        with self.assertRaises(ValueError):checked_response(r)
        r=response('ONE');r['model']='other'
        with self.assertRaises(ValueError):checked_response(r)
    def test_m1_pairing_and_stopping(self):
        m=make_manifest('QM-M1-01');self.assertEqual(len(m['assignments']),64);cells={}
        for a in m['assignments']:cells.setdefault((tuple(a['bits']),a['q'],a['repetition']),[]).append(a)
        for pair in cells.values():self.assertEqual(pair[0]['request']['state'],pair[1]['request']['state'])
        self.assertFalse(analyze(m,[receipt(a) for a in m['assignments']])['advance']);rows=[]
        for a in m['assignments']:
            c=a['expected']
            if a['instruction']=='standard' and a['repetition']=='skewed':c='ONE' if sum(r['value'] for r in a['request']['state']['reports'])>=5 else 'ZERO'
            rows.append(receipt(a,c))
        s=analyze(m,rows);self.assertTrue(s['advance']);self.assertEqual(s['adverse_copy'],4);self.assertEqual(s['rescued'],4)
    def test_repair_namespace_and_finite_reuse(self):
        x,y=make_manifest(),make_manifest('QM-Q1-02');self.assertFalse({a['id'] for a in x['assignments']}&{a['id'] for a in y['assignments']})
        self.assertEqual(sorted((a['lineage'],a['context'],a['q'],a['expected']) for a in x['assignments']),sorted((a['lineage'],a['context'],a['q'],a['expected']) for a in y['assignments']))

class NextRuntime(unittest.TestCase):
    def test_ledger_requires_original_history(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'budget.sqlite'
            with self.assertRaises(ValueError):Ledger(p)
            self.assertFalse(p.exists())
            with closing(sqlite3.connect(p)) as db,db:
                db.execute('CREATE TABLE authority (id INTEGER PRIMARY KEY,experiment TEXT,cap REAL)');db.execute('INSERT INTO authority VALUES (1,?,?)',('quorum-of-mirrors',1.));db.execute('CREATE TABLE calls (id TEXT PRIMARY KEY,reserved REAL,status TEXT,actual REAL)')
            with self.assertRaises(ValueError):Ledger(p)
    def test_reservations_replay_and_concurrency(self):
        with tempfile.TemporaryDirectory() as d:
            b=original_ledger(Path(d)/'budget.sqlite');m=make_manifest();h=hashes();self.assertEqual(b.audit()['calls'],32);b.begin_attempt(m,h)
            with self.assertRaises(ValueError):b.begin_attempt(m,h)
            a=m['assignments'][0];b.reserve(m,a['id'],h)
            with self.assertRaises(sqlite3.IntegrityError):b.reserve(m,a['id'],h)
            with self.assertRaises(ValueError):b.reserve(m,'unknown',h)
            with self.assertRaises(ValueError):b.reserve(m,m['assignments'][1]['id'],{})
            b.finish(a['id'],'failed_or_uncertain');self.assertEqual(b.audit()['calls'],33);self.assertAlmostEqual(b.audit()['reserved_usd'],33*RESERVE);b.close(m['attempt'],False)
            with self.assertRaises(ValueError):b.begin_attempt(make_manifest('QM-Q1-02'),h)
    def test_tampered_history(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'budget.sqlite';b=original_ledger(p)
            with closing(sqlite3.connect(p)) as db,db:db.execute('DELETE FROM calls WHERE id=?',(old_manifest()['assignments'][0]['id'],))
            with self.assertRaises(ValueError):b.audit()
    def test_research_block_precedes_provider_and_credential(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);m=make_manifest();config={'manifest_sha256':digest(m),'source_sha256':hashes(),'deadline':time.time()+60,'authorization':str(Path(__file__).parent/'AUTHORIZATION.json'),'repo':str(Path(__file__).resolve().parents[5]),'hypothesis':'vishesh-quorum-source-aware'}
            with patch('next_runtime.native_call') as call:
                with self.assertRaisesRegex(ValueError,'accepted_hypothesis_missing'):run(config,m,p/'out',p/'nonexistent-secret')
                call.assert_not_called();self.assertFalse((p/'out').exists())
    def test_allocation_expiry_identity_and_source(self):
        now=time.time();a=dict(experiment='quorum-of-mirrors',claim_id='fixture',host=socket.gethostname().split('.')[0],exclusive=True,approved_account_verified=True,merged_claim_verified=True,workload_verified_clear=True,source_sha256=hashes(),checked_at=now,expires_at=now+60);allocation_check(a,now)
        for key,val in [('exclusive',False),('approved_account_verified',False),('expires_at',now),('source_sha256',{}),('host','different-fixture-host')]:
            b=dict(a);b[key]=val
            with self.assertRaises(ValueError):allocation_check(b,now)
    def test_first_failure_stops_and_preserves_assignments(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);ledger=original_ledger(p/'budget.sqlite');secret=p/'credential';secret.write_text('LOCAL-UNIT-FIXTURE');secret.chmod(0o600);config={'ledger':str(p/'budget.sqlite'),'source_sha256':hashes(),'public_manifest_url':'fixture','run_tldr':'fixture'};m=make_manifest()
            reporter=SimpleNamespace(progress=lambda *a,**k:None,artifact=lambda *a,**k:None,done=lambda **k:None,fail=lambda **k:None)
            with patch.dict('sys.modules',{'swarm_report':SimpleNamespace(start=lambda *a,**k:reporter)}),patch('next_runtime.preflight',return_value={'offline_unit_fixture':True}),patch('next_runtime.native_call',side_effect=RuntimeError('MUST-NOT-EXPORT')) as call:s=run(config,m,p/'out',secret)
            self.assertEqual(call.call_count,1);self.assertEqual(s['failed'],1);self.assertEqual(s['unstarted'],15);self.assertFalse(s['qualified']);self.assertEqual(ledger.audit()['calls'],33)
            self.assertNotIn('MUST-NOT-EXPORT',(p/'out'/'receipts.jsonl').read_text());self.assertEqual((p/'out'/'cases.html').read_text().count('<td>unstarted</td>'),15)
class AdmissionMutations(unittest.TestCase):
    def test_owner_direction_preserves_honest_research_status(self):
        checked=research_check('unused',None,'owner-directed-exploratory')
        self.assertEqual(checked['researcher_review'],'not_required_by_owner')
        self.assertEqual(checked['formal_hypothesis_status'],'not_accepted')
        self.assertIn('OPERATOR-AUTHORIZATION.json',hashes())
        with self.assertRaisesRegex(ValueError,'owner_direction_missing'):
            research_check('unused',None,'arbitrary-waiver')
        with patch('next_runtime.json.loads',return_value={'experiment':'another-study'}):
            with self.assertRaisesRegex(ValueError,'owner_direction_missing'):
                research_check('unused',None,'owner-directed-exploratory')

    def test_owner_direction_does_not_admit_later_stage(self):
        with self.assertRaisesRegex(ValueError,'stage_not_admitted'):
            preflight({'research_policy':'owner-directed-exploratory'},make_manifest('QM-M1-01'))

    def test_safe_errors_are_actionable_without_leaking_bodies(self):
        self.assertEqual(safe_reason(ValueError('accepted_hypothesis_missing')),'accepted_hypothesis_missing')
        self.assertEqual(safe_reason(ValueError('PRIVATE BODY MUST NOT ESCAPE')),'ValueError')
        self.assertEqual(safe_reason(RuntimeError('SECRET HEADER')),'RuntimeError')

    def test_actual_preflight_requires_registered_manifest_and_current_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);m=make_manifest();original_ledger(p/'ledger.sqlite');now=time.time()
            allocation=dict(experiment='quorum-of-mirrors',claim_id='fixture',host=socket.gethostname().split('.')[0],exclusive=True,
                approved_account_verified=True,merged_claim_verified=True,workload_verified_clear=True,
                source_sha256=hashes(),checked_at=now,expires_at=now+300)
            (p/'allocation.json').write_text(json.dumps(allocation))
            import hashlib
            plan_hash=hashlib.sha256(Path(__file__).with_name('NEXT-RUN-PLAN.md').read_bytes()).hexdigest()
            url='https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/plan.md'
            manifest_url='https://github.com/dmarzzz/swarm-lab/blob/'+'b'*40+'/spec.json'
            c=dict(manifest_sha256=digest(m),source_sha256=hashes(),deadline=now+300,
                authorization=str(Path(__file__).with_name('AUTHORIZATION.json').resolve()),repo='fixture',hypothesis='fixture',
                allocation_receipt=str(p/'allocation.json'),public_plan_url=url,plan_sha256=plan_hash,
                public_manifest_url=manifest_url,run_tldr='Bounded Q1 qualification; no efficacy claim',ledger=str(p/'ledger.sqlite'))
            registered=dict(url=url,plan_sha256=plan_hash,registered_tldr='TLDR: fixture '+manifest_url)
            with patch('next_runtime.reporter_check',return_value='UNIT-FIXTURE'),patch('next_runtime.research_check',return_value={'status':'UNIT-FIXTURE'}),patch('next_runtime.public_plan.check',return_value=registered),patch('next_runtime.public_plan.fetch',return_value=json.dumps(m)),patch('next_runtime.metadata_check',return_value={'status':'UNIT-FIXTURE'}):
                self.assertEqual(preflight(c,m,now)['budget']['calls'],32)
                for field,value in [('manifest_sha256','wrong'),('source_sha256',{}),('deadline',now),('plan_sha256','wrong'),('public_manifest_url','https://example.com/mutable.json')]:
                    bad=dict(c);bad[field]=value
                    with self.assertRaises(ValueError):preflight(bad,m,now)
                registered['registered_tldr']='TLDR: generic experiment description'
                with self.assertRaisesRegex(ValueError,'condition_manifest_not_registered'):preflight(c,m,now)
                registered['registered_tldr']='TLDR: '+manifest_url
                with patch('next_runtime.public_plan.fetch',return_value='{}'):
                    with self.assertRaisesRegex(ValueError,'public_manifest_mismatch'):preflight(c,m,now)
                with patch('next_runtime.metadata_check',side_effect=ValueError('route_or_price_unavailable')):
                    with self.assertRaises(ValueError):preflight(c,m,now)
            self.assertEqual(Ledger(p/'ledger.sqlite').audit()['calls'],32)

    def test_runtime_rejects_later_stage_even_if_frozen(self):
        m=make_manifest('QM-M1-01')
        with self.assertRaisesRegex(ValueError,'stage_not_admitted'):preflight({},m)

if __name__=='__main__':unittest.main()
