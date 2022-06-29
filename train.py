#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower
from stable_baselines3.common.callbacks import CheckpointCallback

# model = A2C.load(path="a2c_rotate_???step", env=AnimalTower(), tensorboard_log="./a2c_dtb/")
model = PPO(policy='CnnPolicy', env=AnimalTower(), verbose=1, tensorboard_log="./ppo_tf/")
# Save a checkpoint every 100 steps
checkpoint_callback = CheckpointCallback(save_freq=100, save_path='./ppo_logs/',
                                         name_prefix='rotete_move_12')
model.learn(total_timesteps=10000, callback=checkpoint_callback)
