#!/usr/bin/env python3
from stable_baselines3 import PPO
from environment import AnimalTower

model = PPO("MlpPolicy", AnimalTower()).learn(5)