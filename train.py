import gym
from environment import AnimalTower

from stable_baselines3 import PPO

env = AnimalTower()

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1)

obs = env.reset()
for i in range(1):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()

env.close()
