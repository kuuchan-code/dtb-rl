#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower
from stable_baselines3.common.callbacks import CheckpointCallback

env = AnimalTower()
# model = PPO(policy='CnnPolicy', env=env,
#             verbose=1, tensorboard_log="./ppo_tf/")
model = PPO.load(path="ppo_logs/rotate_500_steps", env=env, tensorboard_log="./ppo_dtb/")
checkpoint_callback = CheckpointCallback(save_freq=100, save_path='./ppo_logs/',
                                         name_prefix='_rotate')
model.learn(total_timesteps=1000, callback=[checkpoint_callback])
