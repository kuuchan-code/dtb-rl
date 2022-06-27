#!/usr/bin/env python3
from stable_baselines3 import A2C
from environment import AnimalTower
import os

for i in range(100):
    print(f"{i+1}回目ループ")
    if os.path.exists("test.zip"):
        model = A2C.load("test.zip", AnimalTower(), print_system_info=False)
    else:
        model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                    tensorboard_log="./a2c_cartpole_tensorboard/")
    # print(type(model))
    model.learn(total_timesteps=20)
    model.save("test")
