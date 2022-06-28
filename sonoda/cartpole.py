#!/usr/bin/env python3
# https://qiita.com/pocokhc/items/0872539ad9d981847595
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


if __name__ == "__main__":
    mcp = MyCartpole()
