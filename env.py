#!/usr/bin/env python3
import itertools
import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    def __init__(self):
        a = np.linspace(0, 1080, 100)
        b = np.linspace(0, 7, 8)
        self.ACTION_MAP = np.array(
            [v for v in itertools.product(a, b)])  # アクションの用意
        self.action_space = gym.spaces.Discrete(800)       # エージェントが取りうる行動空間を定義
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(256, 144))  # エージェントが受け取りうる観測空間を定義
        self.reward_range = [-1, 1]       # 報酬の範囲[最小値と最大値]を定義

    def reset(self):
        # リスタートボタンをタップ後、初期画面の画像を返す？
        return observation

    def step(self, action_index):
        # 行動を受け取り行動後の状態をreturnする
        action = self.ACTION_MAP[action_index]
        # actionのようにタップする
        # action後の画像(observation)を返す
        observation =
        # 高くなったら +1
        if 高くなったら:
            reward = 1
            done = False
        # 落としたらreward -1
        elif 落としたら:
            reward = -1
            done = True
        # つめたらreward 0
        else:
            reward = 0
            done = False
        return observation, reward, done, {}

    def render(self):
        # プレイ画面を返す？
        pass
