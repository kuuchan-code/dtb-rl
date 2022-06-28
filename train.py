from stable_baselines3 import PPO
from environment import AnimalTower

model = PPO('MlpPolicy', AnimalTower(), verbose=1, tensorboard_log="./dtb_ppo/")
model.learn(total_timesteps=10_000)
model.save("kuu")