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
        self.observation_space = ...  # エージェントが受け取りうる観測空間を定義
        self.reward_range = [-1, 1]       # 報酬の範囲[最小値と最大値]を定義

    def reset(self):
        # 環境を初期状態にする関数
        # 初期状態をreturnする
        self.done = False
        return obs

    def step(self, action):
        # 行動を受け取り行動後の状態をreturnする
        if action == 0:
            pass
        return obs, reward, done, info

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
