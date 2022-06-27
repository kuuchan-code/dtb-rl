#!/usr/bin/env python3
from stable_baselines3 import A2C
from environment import AnimalTower
import os

for i in range(100):
    print(f"{i+1}回目ループ")
    if os.path.exists("half.zip"):
        model = A2C.load("half.zip", AnimalTower(),
                         print_system_info=True)
    else:
        model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                    tensorboard_log="./a2c_cartpole_tensorboard/")
    # print(type(model))
    model.learn(total_timesteps=3)
    model.save("half")
