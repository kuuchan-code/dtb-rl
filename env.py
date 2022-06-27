#!/usr/bin/env python3
import itertools
import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    def __init__(self):
        a = np.linspace(0, 1080, 100)
        b = np.linspace(0, 7, 8)
        test = np.array([v for v in itertools.product(a, b)])
        self.ACTION_MAP = np.array(
            [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]])  # アクションの用意
        self.action_space = gym.spaces.Discrete(8)       # エージェントが取りうる行動空間を定義
        self.observationervation_space = ...  # エージェントが受け取りうる観測空間を定義
        self.reward_range = [-1, 1]       # 報酬の範囲[最小値と最大値]を定義

    def reset(self):
        # 初期画面の画像を返す？
        return observation

    def step(self, action_index):
        # 行動を受け取り行動後の状態をreturnする
<<<<<<< HEAD
        action = self.ACTION_MAP[action_index]
        # action後の画像(observation)を返す
        # 高くなったら +1
        if 高くなったら:
            reward = 1
            done = False
        # つめたらreward 0
        elif つめたら:
            reward = 0
            done = False
        # 落としたらreward -1
        else:
            reward = -1
            done = True
        return observation, reward, done, {}
=======
        if action == 0:
            pass
        return obs, reward, done, info
>>>>>>> f48dfa2039efb3f30354bdbded00d9b5e567f8ec

    def render(self, mode='human'):
        # modeとしてhuman, rgb_array, ansiが選択可能
        # humanなら描画し, rgb_arrayならそれをreturnし, ansiなら文字列をreturnする
        ...

    def close(self):
        ...

    def seed(self, seed=None):
        ...


if __name__ == "__main__":
    ce = CustomEnv()
