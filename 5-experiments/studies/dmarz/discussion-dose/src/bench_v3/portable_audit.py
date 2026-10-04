"""Successor-only aggregate portability; raw records and discrete values stay exact.

Only cell aggregates of memory_precision and memory_key_coverage may differ by
<= 1e-14 absolute (zero relative tolerance). No cost, score, count, hash,
request, response, world, journal or individual outcome comparison uses it.
Frozen Q0 must continue to use 883d310 under Python 3.12.
"""
import math

CONTINUOUS = frozenset(('memory_precision', 'memory_key_coverage'))
AGGREGATES = frozenset(('sum', 'observed_mean', 'assigned_observed_sum_over_n'))


def summary_equal(left, right, path=()):
    if type(left) is not type(right): return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(summary_equal(left[k], right[k], path + (k,)) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(summary_equal(a, b, path + (i,)) for i, (a, b) in enumerate(zip(left, right)))
    allowed = (len(path) == 5 and path[0] == 'cells' and path[2] == 'metrics' and
               path[3] in CONTINUOUS and path[4] in AGGREGATES)
    if allowed and type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and math.isclose(left, right, rel_tol=0, abs_tol=1e-14)
    return left == right
