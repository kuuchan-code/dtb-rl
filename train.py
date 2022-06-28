#!/usr/bin/env python3
from stable_baselines3 import A2C
# from stable_baselines3 import PPO
from environment import AnimalTower, TRAIN_WIDTH
import os

if os.path.exists(f"test_{TRAIN_WIDTH}.zip"):
    model = A2C.load(f"test_{TRAIN_WIDTH}.zip", AnimalTower(),
                     print_system_info=True)
else:
    model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                tensorboard_log="./a2c_cartpole_tensorboard/")
print(model.get_parameters().keys())
model.learn(total_timesteps=20)
model.save(f"test_{TRAIN_WIDTH}")

# model = A2C.load("kuu")
# model = A2C('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./a2c_dtb/")
# # model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./ppo_dtb/")
# model.learn(total_timesteps=1000)
# model.save("kuu")