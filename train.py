#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback

# model = A2C.load(path="a2c_rotate_???step", env=AnimalTower(), tensorboard_log="./a2c_dtb/")
model = PPO(policy='CnnPolicy', env=AnimalTower(),
            verbose=1, tensorboard_log="./ppo_tf/")
eval_callback = EvalCallback(eval_env=AnimalTower(), best_model_save_path="./ppo_logs/",
                             log_path="./ppo_logs/", eval_freq=2,
                             deterministic=True, render=False)
checkpoint_callback = CheckpointCallback(save_freq=5, save_path='./ppo_logs/',
                                         name_prefix='rotete_move_12')
model.learn(total_timesteps=10, callback=[
            eval_callback, checkpoint_callback])
# model.learn(total_timesteps=10, callback=[checkpoint_callback])
# model.learn(total_timesteps=10)
