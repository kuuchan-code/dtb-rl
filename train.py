from stable_baselines3 import A2C
from environment import AnimalTower
import os

if os.path.exists("test.zip"):
    model = A2C.load("test.zip", AnimalTower(), print_system_info=True)
else:
    model = A2C("MlpPolicy", AnimalTower(), verbose=1,
                tensorboard_log="./a2c_cartpole_tensorboard/")
print(type(model))
model.learn(total_timesteps=1)
model.save("test")
