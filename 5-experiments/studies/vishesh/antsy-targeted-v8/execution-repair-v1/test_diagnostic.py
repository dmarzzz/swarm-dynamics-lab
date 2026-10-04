import copy,unittest
import diagnostic as d

class DiagnosticTests(unittest.TestCase):
    def good(self):return {'status':'valid','category':'ok','wall_s':20,'latency_eligible':True,'phases':{'valid':True,'complete':True}}
    def test_exact_six_calls(self):
        calls=[];saves=[]
        def invoke(seq,i):calls.append((seq,i));return self.good()
        rows,stop=d.collect(invoke,lambda r:saves.append(len(r)),lambda:0)
        self.assertEqual(calls,list(enumerate(d.ORDER,1)));self.assertEqual(saves,list(range(1,7)));self.assertTrue(d.summarize(rows,stop)['diagnostic_within_limit'])
        self.assertFalse(d.summarize(rows,stop)['qualification_passed'])
    def test_first_slow_or_error_stops(self):
        for change,reason in [({'latency_eligible':False},'over_45s'),({'status':'error','category':'timeout'},'timeout'),({'phases':{'valid':False,'complete':False}},'invalid_phases')]:
            def invoke(seq,i):return self.good() if seq<3 else {**self.good(),**change}
            rows,stop=d.collect(invoke,lambda r:None,lambda:0)
            self.assertEqual(len(rows),3);self.assertEqual(stop,reason);self.assertEqual(d.summarize(rows,stop)['unstarted'],3)
    def test_deadline_and_exception(self):
        clock=iter([0,509]);rows,stop=d.collect(lambda s,i:self.fail('should not dispatch'),lambda r:None,lambda:next(clock))
        self.assertEqual(stop,'stage_deadline');self.assertEqual(rows,[])
        def bad(s,i):raise RuntimeError('untrusted message must not escape')
        rows,stop=d.collect(bad,lambda r:None,lambda:0);self.assertEqual(stop,'supervisor_exception');self.assertNotIn('untrusted',str(rows))
    def receipt(self):
        return {'experiment':d.EXP,'attempt':d.ATTEMPT,'source':'a'*40,'max_ocr_calls':6,'max_model_calls':0,'new_charge_cap_usd':0,'order':list(d.ORDER),'deadline_s':90,'eligibility_s':45,'stage_limit_s':600,'host':'sim-vishesh','claim':'vishesh-antsy-d1','automatic_successor':False,**{k:True for k in ('owner_approved','exclusive_claim_verified','approved_team_verified','host_idle_verified','runtime_matches_q0','public_page_verified','budget_reconciled','duplicate_dispatch_fenced','host_class_matches_q0')},'authority_reference':'fixture only','verified_at':100,'claim_expires_at':1000,'runtime_sha256':d.digest({}),'documents':{n:d.sha(d.ROOT/n) for n in d.DOCS}}
    def test_admission_exact_scope(self):
        r=self.receipt();self.assertTrue(d.validate(r,'a'*40,{},100))
        for key,value in [('max_ocr_calls',7),('eligibility_s',90),('deadline_s',120),('new_charge_cap_usd',1),('automatic_successor',True),('host','other'),('claim','other'),('order',[60]*6),('owner_approved',False),('public_page_verified',False),('host_idle_verified',False),('claim_expires_at',700),('verified_at',-1000),('runtime_sha256','bad'),('documents',{}),('authority_reference','')]:
            with self.subTest(key=key),self.assertRaises(ValueError):d.validate({**r,key:value},'a'*40,{},100)

if __name__=='__main__':unittest.main()
