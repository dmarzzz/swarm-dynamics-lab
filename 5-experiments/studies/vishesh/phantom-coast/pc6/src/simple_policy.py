"""Exact controller for the declared one-step contract, not a native model result."""
import math
def choose(report_cell,unknown_cell,reliability,unknown_cost=.25):
    if report_cell==unknown_cell:raise ValueError('distinct_cells_required')
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not 0<=x<=1 for x in (reliability,unknown_cost)):raise ValueError('probability_or_cost')
    # Inspect report leaves the unknown cost; inspect unknown leaves report risk.
    return report_cell if unknown_cost<=1-reliability else unknown_cell
