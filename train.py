#!/usr/bin/env python3
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
from stable_baselines.common.callbacks import CheckpointCallback

from environment import AnimalTower

from stable_baselines3 import PPO

env = AnimalTower()

model = DQN(MlpPolicy, env, verbose=1, tensorboard_log="log")
print('start learning')
checkpoint_callback = CheckpointCallback(
    save_freq=500, save_path='./save_weights/', name_prefix='rl_model')
model.learn(total_timesteps=10000, callback=checkpoint_callback)
print('finish learning')
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)

# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#         obs = env.reset()

# env.close()
