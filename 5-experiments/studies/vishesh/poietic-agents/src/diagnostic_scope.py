"""Explicit diagnostic cohorts; selecting one never supplies launch authority."""
import copy

SCOPES = {
    'D0-01': dict(root_start=400, proposal='reviews/S0-02-repair-plan.md',
                  prior_budget=dict(physical_calls=37, exposure_nano=480002000,
                                    infrastructure_nano=82184184),
                  staging_seconds=900, cleanup_seconds=300),
    'D0-02': dict(root_start=500, proposal='D0-02-PLAN.md',
                  prior_budget=dict(physical_calls=40, exposure_nano=482269482,
                                    infrastructure_nano=86291409),
                  staging_seconds=1800, cleanup_seconds=1800),
}


def scope(attempt='D0-01'):
    if attempt not in SCOPES:
        raise ValueError('unadmitted_diagnostic_attempt')
    return copy.deepcopy(SCOPES[attempt])
