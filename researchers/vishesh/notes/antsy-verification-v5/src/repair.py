"""Observable-state estimators and development-only value-of-information baseline."""
import copy
from dataclasses import dataclass
from typing import Optional

MODES=('A','B','C')
VARIANTS=('original','null-neutral','global-empty')

@dataclass(frozen=True)
class Observation:
    mode:str
    region:int
    quality:Optional[float]
    def __post_init__(self):
        if self.mode not in MODES or self.region not in range(3):raise ValueError('invalid observation address')
        if self.quality is not None and not 0<=self.quality<=1:raise ValueError('invalid quality')

class Board:
    """Only initial confidence/bias and purchased observations. No evaluator record."""
    def __init__(self,observations,bias,checks=()):
        self.prior={m:tuple(max(0.,min(1.,o['confidence']+bias[m])) for o in observations[m]) for m in MODES}
        self.checks=list(checks)
    def copy(self):return copy.deepcopy(self)
    def buy(self,observation):
        if len(self.checks)>=2:raise ValueError('budget exhausted')
        if (observation.mode,observation.region) not in self.available():raise ValueError('duplicate check')
        self.checks.append(observation)
    def available(self):return [(m,j) for m in MODES for j in range(3) if all((c.mode,c.region)!=(m,j) for c in self.checks)]
    def scores(self,variant='null-neutral'):
        if variant not in VARIANTS:raise ValueError('unknown estimator')
        empty={c.region for c in self.checks if c.quality is None} if variant=='global-empty' else set()
        result={}
        for m in MODES:
            values=[]
            for j,prior in enumerate(self.prior[m]):
                if j in empty:continue
                c=next((c for c in self.checks if (c.mode,c.region)==(m,j)),None)
                if c and c.quality is not None:values.append(c.quality)
                elif c and variant=='original':continue
                else:values.append(prior)
            result[m]=sum(values)/len(values) if values else 0.
        return result
    def choose(self,variant='null-neutral'):
        scores=self.scores(variant);return max(MODES,key=lambda m:(scores[m],-MODES.index(m)))

def action_values(board,calibration):
    """Historical labeled scenarios are development data, never the current truth."""
    if not calibration:raise ValueError('empty predictive distribution')
    start=board.choose();values={}
    for m,j in board.available():
        gains=[]
        for scenario in calibration:
            b=board.copy();b.buy(Observation(m,j,scenario['modes'][m]['evaluation']['regions'][j]))
            gains.append(scenario['modes'][b.choose()]['evaluation']['recall']-scenario['modes'][start]['evaluation']['recall'])
        values[(m,j)]=sum(gains)/len(gains)
    return values

def decide(board,calibration,cost,forced=False):
    if cost<0:raise ValueError('negative review cost')
    if len(board.checks)>=2:return None,{}
    values=action_values(board,calibration);best=max(values,key=lambda a:(values[a],-MODES.index(a[0]),-a[1]))
    return (best if forced or values[best]>cost+1e-12 else None),values
