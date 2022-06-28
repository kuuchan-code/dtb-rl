#!/usr/bin/env python3
from stable_baselines3 import A2C
# from stable_baselines3 import PPO
from environment import AnimalTower

model = A2C('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./a2c_dtb/")
# model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./ppo_dtb/")
model.learn(total_timesteps=100)
model.save("kuu")