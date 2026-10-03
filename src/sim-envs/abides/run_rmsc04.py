import time
from abides_markets.configs import rmsc04
from abides_core import abides
t=time.time()
cfg = rmsc04.build_config(seed=0, end_time="10:00:00")
print("agents:", len(cfg["agents"]))
end = abides.run(cfg)
print("wall secs", round(time.time()-t,1))
ob = end["agents"][0].order_books["ABM"]
L1 = ob.get_L1_snapshots()
print("L1 bid snapshots:", len(L1["best_bids"]), "ask snapshots:", len(L1["best_asks"]))
print("first/last best bid:", L1["best_bids"][0], L1["best_bids"][-1])
