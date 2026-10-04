import copy
import datetime
import email.utils
import json
from pathlib import Path
import sys
import unittest

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from wire_format import parse_chat_action, SINGLE_FENCE, STRICT
from provider_diagnostics import safe_error, retry_after, has_provider_error
from qualification import make_case, probe, apply


class FormatRepairTests(unittest.TestCase):
    def test_bare_and_exact_fence_preserve_identical_action(self):
        action={'type':'directory'}
        for text in ('{"type":"directory"}', '```json\n{"type":"directory"}\n```',
                     ' \n```json\r\n{"type":"directory"}\r\n```\n'):
            with self.subTest(text=text):
                parsed,receipt=parse_chat_action(text,SINGLE_FENCE)
                self.assertEqual(parsed,action)
                self.assertEqual(receipt['removed_json_fence'],text.strip().startswith('```'))
                self.assertEqual(len(receipt['original_content_sha256']),64)

    def test_historical_strict_contract_still_rejects_fences(self):
        with self.assertRaises(json.JSONDecodeError):parse_chat_action('```json\n{"type":"directory"}\n```',STRICT)
        with self.assertRaisesRegex(ValueError,'wire_format_policy'):parse_chat_action('{}','unknown')

    def test_no_extraction_or_syntax_repair(self):
        faults=['Here is JSON: {"type":"directory"}', '```json\n{"type":"directory"}\n```\nExplanation',
                '```\n{"type":"directory"}\n```', '```JSON\n{"type":"directory"}\n```',
                '```json {"type":"directory"}```','```json\n{}\n```\n```json\n{}\n```',
                '{}{}','[]','null','"directory"','```json\n{"type":"directory"}',
                '{"type":"directory",}', '```json\n```json\n{}\n```\n```']
        for text in faults:
            with self.subTest(text=text),self.assertRaises(ValueError):parse_chat_action(text,SINGLE_FENCE)

    def test_duplicate_keys_and_nonfinite_numbers_rejected(self):
        for text in ['{"type":"directory","type":"fetch"}', '{"x":{"a":1,"a":2}}',
                     '{"value":NaN}', '{"value":Infinity}', '{"value":-Infinity}', '{"value":1e999}']:
            for wrapped in [text,'```json\n'+text+'\n```']:
                with self.subTest(text=wrapped),self.assertRaises(ValueError):parse_chat_action(wrapped,SINGLE_FENCE)

    def test_normalization_never_supplies_type_or_repairs_fields(self):
        for action in [{'fetch':{}},{'type':'directory','extra':True}, {'type':'fetch','endpoint':'inventory'}]:
            state=make_case(0,development=True);p=probe(state,0,'generalist')
            parsed,_=parse_chat_action('```json\n'+json.dumps(action)+'\n```',SINGLE_FENCE)
            self.assertEqual(parsed,action)
            result=apply(state,0,parsed,p['expected']);self.assertFalse(result['schema_valid']);self.assertFalse(result['correct'])

    def test_protected_endpoint_remains_forbidden_after_normalization(self):
        state=make_case(0,development=True);p=probe(state,0,'generalist')
        action=dict(p['expected'],endpoint='private_truth')
        parsed,_=parse_chat_action('```json\n'+json.dumps(action)+'\n```',SINGLE_FENCE)
        result=apply(state,0,parsed,p['expected'])
        self.assertTrue(result['protected_access_violation']);self.assertFalse(result['correct'])

    def test_all_development_lifecycle_actions_retain_effects(self):
        for case in range(3):
            state=make_case(case,development=True)
            for step in range(4):
                p=probe(state,step,'generalist');a,_=parse_chat_action('```json\n'+json.dumps(p['expected'])+'\n```',SINGLE_FENCE)
                self.assertTrue(apply(state,step,a,p['expected'])['correct'])


class ProviderDiagnosticsTests(unittest.TestCase):
    def test_allowlist_prevents_free_text_or_unknown_field_disclosure(self):
        secret='DO_NOT_LOG_TEST_CREDENTIAL'
        body={'error':{'code':429,'message':secret,'metadata':{'error_type':secret,'provider_code':secret,'provider_name':secret,'raw':secret,'reason':secret,'limit_source':secret}}}
        result=safe_error(429,body,{'Retry-After':secret,'X-RateLimit-Limit':secret,'Authorization':secret},'Anthropic')
        self.assertNotIn(secret,json.dumps(result));self.assertEqual(result['body_error_status'],429)
        self.assertNotIn('provider_name',result);self.assertNotIn('retry_after_seconds',result)

    def test_retry_after_seconds_and_http_date_bounds(self):
        now=1700000000
        self.assertEqual(retry_after('60',now),60)
        date=email.utils.format_datetime(datetime.datetime.fromtimestamp(now+45,datetime.timezone.utc),usegmt=True)
        self.assertEqual(retry_after(date,now),45)
        for x in ['-1','1.5','999999999999999','nonsense',None]:self.assertIsNone(retry_after(x,now))

    def test_credit_limit_sources_remain_distinct(self):
        for source in ['openrouter_in_flight_budget','openrouter_key_limit','openrouter_credits']:
            result=safe_error(402,{'error':{'code':402,'metadata':{'limit_source':source,'reason':'in_flight_budget_exhausted'}}})
            self.assertEqual(result['limit_source'],source)
        self.assertNotIn('limit_source',safe_error(429,{'error':{}}))

    def test_malformed_metadata_is_not_a_parser_failure(self):
        for body in [b'not-json',[],None,{'error':{'metadata':[],'message':[]}}, {'choices':False}]:
            self.assertEqual(safe_error(429,body)['http_status'],429)

    def test_body_errors_include_partial_generation_failures(self):
        for raw in [{'error':{'code':429}}, {'choices':[{'finish_reason':'error'}]},
                    {'choices':[{'error':{'code':503,'metadata':{'error_type':'provider_overloaded'}}}]}]:
            self.assertTrue(has_provider_error(raw))
        self.assertFalse(has_provider_error({'choices':[{'finish_reason':'stop'}]}))
        result=safe_error(200,{'choices':[{'error':{'code':503,'metadata':{'error_type':'provider_overloaded'}}}]})
        self.assertEqual(result['body_error_status'],503);self.assertEqual(result['provider_error_type'],'provider_overloaded')

if __name__=='__main__':unittest.main()
