#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower
from stable_baselines3.common.callbacks import CheckpointCallback

env = AnimalTower()
model = PPO.load(path="ppo_logs/rotete_move_12_3200_steps", env=env, tensorboard_log="./a2c_dtb/")
# model = PPO(policy='CnnPolicy', env=env,
#             verbose=1, tensorboard_log="./ppo_tf/")
checkpoint_callback = CheckpointCallback(save_freq=5, save_path='./ppo_logs/',
                                         name_prefix='rotete_move_12')
model.learn(total_timesteps=10, callback=[checkpoint_callback])
