#!/usr/bin/env python3
from stable_baselines3 import A2C
from environment import AnimalTower
# import os

model = A2C.load(path="kuu-rotate", env=AnimalTower(), tensorboard_log="./a2c_dtb/")
# model = A2C('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./a2c_dtb/")
model.learn(total_timesteps=100)
model.save("kuu-rotate")
