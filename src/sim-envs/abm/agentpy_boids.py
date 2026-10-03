# Boids in AgentPy, following the structure of the official "Flocking behavior" example
# (agentpy docs, reference_flocking). 2D, Space with KD-tree neighbour queries.
import time, sys, numpy as np, agentpy as ap

def normalize(v):
    n = np.linalg.norm(v); return v / n if n else v

class Boid(ap.Agent):
    def setup(self):
        self.velocity = normalize(self.model.nprandom.random(2) - 0.5)
    def setup_pos(self, space):
        self.space = space; self.neighbors = space.neighbors; self.pos = space.positions[self]
    def update_velocity(self):
        p = self.p; pos = self.pos
        nbs = self.neighbors(self, distance=p.outer_radius)
        n = len(nbs)
        v1 = v2 = v3 = np.zeros(2)
        if n:
            npos = np.array(nbs.pos); v1 = (npos.mean(0) - pos) * p.cohesion_strength
            close = self.neighbors(self, distance=p.inner_radius)
            if len(close):
                v2 = (pos - np.array(close.pos)).sum(0) * p.seperation_strength  # sic, docs spelling
            v3 = (np.array(nbs.velocity).mean(0) - self.velocity) * p.alignment_strength
        v4 = np.zeros(2); d = p.border_distance; s = p.border_strength
        for i in range(2):
            if pos[i] < d: v4[i] += s
            elif pos[i] > p.size - d: v4[i] -= s
        self.velocity = normalize(self.velocity + v1 + v2 + v3 + v4)
    def update_position(self):
        self.space.move_by(self, self.velocity)

class BoidsModel(ap.Model):
    def setup(self):
        self.space = ap.Space(self, shape=[self.p.size]*2)
        self.agents = ap.AgentList(self, self.p.population, Boid)
        self.space.add_agents(self.agents, random=True)
        self.agents.setup_pos(self.space)
    def step(self):
        self.agents.update_velocity(); self.agents.update_position()
    def update(self):
        v = np.array(self.agents.velocity); self.record('polarisation', float(np.linalg.norm(v.mean(0))))

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
T = int(sys.argv[2]) if len(sys.argv) > 2 else 100
params = dict(size=100, seed=42, steps=T, population=N, inner_radius=3, outer_radius=10,
              border_distance=10, cohesion_strength=0.005, seperation_strength=0.1,
              alignment_strength=0.3, border_strength=0.5)
m = BoidsModel(params)
t0 = time.time(); res = m.run(display=False); dt = time.time() - t0
pol = res.variables.BoidsModel['polarisation'].values
print(f"agentpy {ap.__version__} N={N} T={T} time={dt:.2f}s agent-steps/s={N*T/dt:,.0f}")
print("polarisation t0..end:", [round(pol[i],3) for i in range(0, len(pol), max(1,len(pol)//5))], round(pol[-1],3))
