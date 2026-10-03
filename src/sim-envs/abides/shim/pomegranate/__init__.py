# Minimal stand-in for pomegranate 0.14 GeneralMixtureModel.from_json(...).sample(random_state=)
import json, numpy as np
class GeneralMixtureModel:
    def __init__(self, dists, w): self.d, self.w = dists, np.asarray(w)/np.sum(w)
    @classmethod
    def from_json(cls, s):
        j = json.loads(s); return cls([(d["name"], d["parameters"]) for d in j["distributions"]], j["weights"])
    def sample(self, random_state=None):
        rs = random_state or np.random
        name, (a, b) = self.d[rs.choice(len(self.d), p=self.w)]
        return rs.lognormal(a, b) if name == "LogNormalDistribution" else rs.normal(a, b)
