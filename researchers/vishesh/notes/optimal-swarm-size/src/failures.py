"""Only these non-secret diagnostics may enter experiment records."""
CODES = frozenset('schema_output_invalid attempt_budget_exhausted cannot_reset_attempt_cap cannot_reset_attempt_membership provider_refusal response_contract_unconfigured response_contract_task_missing response_contract_phase_unknown response_contract_item_unknown claim_expired unexpected_cache_usage credential_unavailable route_changed provider_deadline deadline late_response work_deadline stage_budget_exhausted episode_budget_exhausted budget_exhausted prior_overrun provider_exceeded_bound budget_overrun duplicate_call cannot_reset_episode_cap prompt_limit usage_missing invalid_cost incomplete_response response_shape response_too_large provider_failed transport_failed reporting_failed reporting_timeout public_run_preflight_failed hub_registration_failed publication_incomplete execution_failed malformed_output'.split())
FATAL = frozenset('schema_output_invalid attempt_budget_exhausted cannot_reset_attempt_cap cannot_reset_attempt_membership response_contract_unconfigured response_contract_task_missing response_contract_phase_unknown response_contract_item_unknown claim_expired unexpected_cache_usage credential_unavailable route_changed stage_budget_exhausted budget_exhausted prior_overrun provider_exceeded_bound budget_overrun duplicate_call cannot_reset_episode_cap usage_missing invalid_cost response_shape transport_failed provider_failed'.split())

class SafeFailure(RuntimeError):
    def __init__(self, code):
        self.code = code if code in CODES or (code.startswith('http_') and code[5:].isdigit() and 400 <= int(code[5:]) <= 599) else 'transport_failed'
        super().__init__(self.code)
    @property
    def fatal(self):
        return self.code in FATAL or self.code in ('http_400','http_401','http_402','http_403','http_404','http_422')


def safe_code(exc):
    if isinstance(exc, SafeFailure): return exc.code
    # Matching is exact; arbitrary exception text is never returned.
    if str(exc) in CODES: return str(exc)
    if isinstance(exc, TimeoutError): return 'provider_deadline'
    return 'transport_failed'
