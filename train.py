#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower
import os

for i in range(10):
    print(f"{i+1}回目ループ")
    if os.path.exists("half.zip"):
        model = PPO.load("half.zip", AnimalTower(),
                         print_system_info=True)
    else:
        model = PPO("MlpPolicy", AnimalTower(), verbose=1,
                    tensorboard_log="./ppo_tensorboard/")
    # print(type(model))
    model.learn(total_timesteps=100)
    model.save("half")
