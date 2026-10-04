import copy
import io
import json
import time
import unittest
from unittest.mock import Mock, patch
from response_contract import VERSION, LEGACY, schema_for
from provider import native_payload, Provider, request_child, validate_finish
from tasks import generate, reference_answer, strict_json, evaluate
from failures import SafeFailure


class Contract(unittest.TestCase):
    def test_all_task_shapes_use_only_public_field_names(self):
        for family in ('evidence','repository'):
            for structure in ('parallel','chain'):
                task=generate(family,structure,0)
                plan=schema_for(task.public,'plan')
                self.assertEqual(plan,schema_for(task.public,'plan_repair'))
                self.assertEqual(set(plan['properties']['dependencies']['required']),set(task.public['items']))
                work=schema_for(task.public,'work',task.public['items'][0])
                artifact=work['properties']['artifact']
                self.assertEqual(artifact['type'],'object' if family=='evidence' else 'string')
                final=schema_for(task.public,'integrate')
                answer=reference_answer(task)
                self.assertEqual(set(final['required']),set(answer))
                outer='answers' if family=='evidence' else 'files'
                self.assertEqual(set(final['properties'][outer]['required']),set(answer[outer]))
                if family=='evidence':
                    self.assertEqual(artifact['properties']['value'],{'type':'integer'})
                    self.assertEqual(artifact['properties']['source_ids'],{'type':'array','items':{'type':'string'}})
                before=copy.deepcopy(final);task.truth.clear()
                self.assertEqual(schema_for(task.public,'integrate'),before)
                def inspect(node):
                    if isinstance(node,dict):
                        if node.get('type')=='object':
                            self.assertIs(node['additionalProperties'],False)
                            self.assertEqual(set(node['required']),set(node['properties']))
                        self.assertTrue(set(node).isdisjoint({'minimum','maximum','pattern','minItems','maxItems','enum','const'}))
                        for v in node.values():inspect(v)
                    elif isinstance(node,list):
                        for v in node:inspect(v)
                for schema in (plan,work,final):inspect(schema)

    def test_configuration_and_phase_errors_fail_before_spending(self):
        public=generate('evidence','parallel',0).public
        cfg={'model':'pinned','max_output_tokens':4096,'response_contract':VERSION,'claim_expiry_epoch':time.time()+60,'max_prompt_bytes':48000}
        for mode,phase,task,item in ((None,'plan',public,None),('typo','plan',public,None),(VERSION,'plan',None,None),(VERSION,'unknown',public,None),(VERSION,'work',public,'unknown')):
            bank=Mock();cfg['response_contract']=mode
            with self.assertRaises(ValueError):Provider(cfg,bank,'episode',Mock(),task)([],time.monotonic()+10,0,phase,item)
            bank.reserve.assert_not_called()

    def test_schema_is_sent_on_wire_and_system_prompt_preserved(self):
        public=generate('repository','chain',0).public
        cfg={'model':'pinned','max_output_tokens':4096,'response_contract':VERSION}
        messages=[{'role':'system','content':'raw JSON'},{'role':'user','content':'work'}]
        for phase,item in (('plan',None),('plan_repair',None),('work',public['items'][0]),('integrate',None),('transport',None)):
            body=native_payload(messages,cfg,phase,public,item)
            def receive(req,timeout):
                sent=json.loads(req.data)
                self.assertEqual(sent['system'],'raw JSON')
                self.assertEqual(sent['messages'],messages[1:])
                self.assertEqual(sent['output_config']['format'],{'type':'json_schema','schema':schema_for(public,phase,item)})
                return io.BytesIO(json.dumps({'content':[{'type':'text','text':'{}'}],'stop_reason':'end_turn','model':'pinned','usage':{'input_tokens':1,'output_tokens':1}}).encode())
            connection=Mock()
            with patch('provider.os.environ.get',return_value='test-only-placeholder'),patch('provider.urllib.request.urlopen',side_effect=receive):request_child(connection,body,1)
            self.assertTrue(connection.send.call_args.args[0]['ok'])
        cfg['response_contract']=LEGACY
        self.assertNotIn('output_config',native_payload(messages,cfg))

    def test_schema_bytes_count_toward_payload_cap(self):
        public=generate('evidence','parallel',0).public;bank=Mock()
        cfg={'model':'pinned','max_output_tokens':4096,'response_contract':VERSION,'claim_expiry_epoch':time.time()+60,'max_prompt_bytes':200}
        with self.assertRaisesRegex(ValueError,'prompt_limit'):
            Provider(cfg,bank,'episode',Mock(),public)([],time.monotonic()+10,0,'plan',None)
        bank.reserve.assert_not_called()

    def test_refusal_and_truncation_are_not_accepted_as_json_success(self):
        for reason,expected in (('refusal','provider_refusal'),('max_tokens','incomplete_response'),(None,'incomplete_response')):
            with self.assertRaisesRegex(SafeFailure,expected):validate_finish(reason)
        validate_finish('end_turn')

    def test_local_parser_and_evaluator_still_reject_bad_content(self):
        for text in ('```json\n{}\n```','{"x":1,"x":2}','{"x":NaN}'):
            with self.assertRaises(ValueError):strict_json(text)
        task=generate('evidence','parallel',0)
        for invalid in ({'answers':{}},{'answers':{i:{'value':True,'source_ids':[]} for i in task.public['items']}},dict(reference_answer(task),extra=True)):
            self.assertFalse(evaluate(task,json.dumps(invalid))['valid'])
        task=generate('repository','parallel',0)
        artifact=reference_answer(task)
        artifact['files'][task.public['items'][0]+'.py']='import os\n'
        self.assertFalse(evaluate(task,json.dumps(artifact))['valid'])

    def test_provider_dispatches_schema_and_settles_refusal_without_retry(self):
        cfg={'model':'pinned','expected_served_model':'pinned','expected_served_provider':'anthropic',
             'max_output_tokens':4096,'provider_context_tokens':200000,'input_usd_per_token':0.000001,
             'output_usd_per_token':0.000005,'episode_cap_microdollars':2000000,'response_contract':VERSION,
             'claim_expiry_epoch':time.time()+60,'max_prompt_bytes':48000}
        public=generate('evidence','parallel',0).public
        for reason in ('end_turn','refusal','max_tokens'):
            bank=Mock();events=[];parent=Mock();child=Mock();context=Mock()
            parent.poll.return_value=True
            parent.recv.return_value={'ok':True,'text':'{}','finish_reason':reason,'model':'pinned','provider':'anthropic',
                                      'usage':{'input_tokens':100,'output_tokens':20}}
            context.Pipe.return_value=(parent,child)
            with patch('provider.multiprocessing.get_context',return_value=context):
                call=Provider(cfg,bank,'episode',events.append,public)
                if reason=='end_turn':self.assertEqual(call([],time.monotonic()+10,0,'plan',None),'{}')
                else:
                    with self.assertRaises(SafeFailure):call([],time.monotonic()+10,0,'plan',None)
            bank.reserve.assert_called_once();bank.settle.assert_called_once_with('episode/0/plan/-',200)
            context.Process.assert_called_once()
            payload=context.Process.call_args.kwargs['args'][1]
            self.assertEqual(payload['output_config']['format']['schema'],schema_for(public,'plan'))
            self.assertEqual(len(events[0]['schema_sha256']),64)
            self.assertEqual(events[0]['response_contract'],VERSION)
            import hashlib
            context_event=next(e for e in events if e['kind']=='request_context')
            self.assertEqual(context_event['sha256'],hashlib.sha256(json.dumps(payload).encode()).hexdigest())
            self.assertEqual(context_event['bytes'],len(json.dumps(payload).encode()))
