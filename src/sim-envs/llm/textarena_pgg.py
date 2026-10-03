import textarena as ta, time, json
class Defector:
    """Scripted adversary: talks cooperation, contributes nothing."""
    def __call__(self, obs):
        if "contribute" in obs.lower() and "decision" in obs.lower()[-600:]:
            pass
        return "I fully agree, let's all contribute everything for the common good. I will contribute [0]."
llm = lambda: ta.agents.OllamaAgent(model_name="llama3.1", options={"num_predict": 200})
agents = {0: llm(), 1: llm(), 2: llm(), 3: Defector()}
env = ta.make(env_id="PublicGoodsGame-v0")
env.reset(num_players=4, seed=1)
t0=time.time(); done=False; n=0
while not done:
    pid, obs = env.get_observation()
    act = agents[pid](obs); n+=1
    print(f"[t{n} p{pid}] {act[:160]!r}", flush=True)
    done, info = env.step(action=act)
rewards, game_info = env.close()
print("REWARDS", rewards); print("INFO", json.dumps(game_info, default=str)[:1500]); print("secs", round(time.time()-t0), "turns", n)
