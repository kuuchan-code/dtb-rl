#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower

env = AnimalTower()

# pathを指定して任意の重みをロードする
model = PPO.load(path="ppo_logs/rotete_move_12_3200_steps", env=env)

# 10回試行する
for i in range(10):
    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()

