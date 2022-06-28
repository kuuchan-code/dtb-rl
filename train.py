#!/usr/bin/env python3
from stable_baselines3 import A2C
# from stable_baselines3 import PPO
from environment import AnimalTower
import os

# model = A2C('MlpPolicy', AnimalTower(), verbose=1,
#             tensorboard_log="./a2c_dtb/")
# model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./ppo_dtb/")
# model.learn(total_timesteps=5)
# model.save("kuu")

if os.path.exists("test.zip"):
    model = A2C.load("test.zip", AnimalTower(),
                     print_system_info=True)
else:
    model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                tensorboard_log="./a2c_cartpole_tensorboard/")
# print(model.get_parameters().keys())
print(model.get_parameters()["policy"])
model.learn(total_timesteps=10)
model.save("test")
