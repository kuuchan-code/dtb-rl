#!/usr/bin/env python3
from stable_baselines3 import A2C
from environment import AnimalTower
from stable_baselines3.common.callbacks import CheckpointCallback

# model = A2C.load(path="a2c_rotate_???step", env=AnimalTower(), tensorboard_log="./a2c_dtb/")
model = A2C('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./a2c_tf/")
# Save a checkpoint every 100 steps
checkpoint_callback = CheckpointCallback(save_freq=100, save_path='./logs/',
                                         name_prefix='a2c_rotate')
model.learn(total_timesteps=10000, callback=checkpoint_callback)