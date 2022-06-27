from stable_baselines3 import A2C
from environment import AnimalTower

model = A2C("MlpPolicy", AnimalTower(), verbose=1,
            tensorboard_log="./a2c_cartpole_tensorboard/").learn(1)
model.save("test")
