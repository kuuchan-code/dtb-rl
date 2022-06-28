#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower


model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./ppo_tb/").learn(total_timesteps=3)
