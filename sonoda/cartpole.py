#!/usr/bin/env python3
# https://qiita.com/pocokhc/items/0872539ad9d981847595
import keras
import tensorflow as tf
from keras.layers import Dense
from keras.optimizers import Adam
from gym import spaces
from gym.envs.classic_control.cartpole import CartPoleEnv
import numpy as np
import math


class MyCartpole(CartPoleEnv):
    def __init__(self):
        super().__init__()

        # 行動空間を連続空間に変更
        self.action_space = spaces.Box(-self.force_mag,
                                       self.force_mag, shape=(1,), dtype=np.float32)

    def reset(self):
        """
        終了ターン
        """
        self.step_count = 0
        return super().reset()

    def step(self, action):
        self.step_count += 1
        # 200ターンで終了
        if self.step_count > 200:
            return np.array(self.state), 0.0, True, {}

        # 例外処理
        if np.isnan(action):
            return np.array(self.state), 0.0, True, {}

        # 丸め込み?
        force = np.clip(action, -self.force_mag, self.force_mag)[0]

        x, x_dot, theta, theta_dot = self.state
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # https://coneural.org/florian/papers/05_cart_pole.pdf
        temp = (force + self.polemass_length * theta_dot **
                2 * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length *
                                                                  (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass))
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        if self.kinematics_integrator == "euler":
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot

        self.state = (x, x_dot, theta, theta_dot)

        done = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                print(
                    "You are calling ' step() even though this "
                    "environment has already returned done = True. You "
                    "should always call 'reset()' once you receive 'done = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}


# 独自のモデルを定義
class PolicyModel(keras.Model):
    def __init__(self, action_space):
        super().__init__()

        # 各レイヤーを定義
        self.dense1 = Dense(16, activation="relu")
        self.dense2 = Dense(16, activation="relu")
        self.pi_mean = Dense(action_space, activation="linear")
        self.pi_stddev = Dense(action_space, activation="linear")

        # optimizer もついでに定義しておく
        self.optimizer = Adam(lr=0.01)

    # Forward pass
    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        x = self.dense2(x)
        mean = self.pi_mean(x)
        stddev = self.pi_stddev(x)

        # σ^2 > 0 になるように変換(指数関数)
        stddev = tf.exp(stddev)

        return mean, stddev

    # 状態を元にactionを算出
    def sample_action(self, state):
        # モデルから平均と分散を取得
        mean, stddev = self(state.reshape((1, -1)))

        # ガウス分布に従った乱数をだす
        sampled_action = tf.random.normal(
            tf.shape(mean), mean=mean, stddev=stddev)
        return sampled_action.numpy()[0]


if __name__ == "__main__":
    with MyCartpole() as env:

        # 出力用にactionの修正値を計算
        # アクションは-10～10の範囲をとるが、学習は-1～1の範囲と仮定し、
        # 出力時に-10～10に戻す
        action_centor = (env.action_space.high + env.action_space.low)/2
        action_scale = env.action_space.high - action_centor

        # 学習ループ
        for episode in range(500):

            # 1episode
            while not done:
                # アクションを決定
                action = model.sample_action(state)

                # 1step進める（アクション値を修正して渡す）
                n_state, reward, done, _ = env.step(
                    action * action_scale + action_centor)
