from stable_baselines3 import A2C
from environment import AnimalTower

model = A2C("MlpPolicy", AnimalTower()).learn(1)