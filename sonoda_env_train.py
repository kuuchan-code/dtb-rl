#!/usr/bin/env python3
from tensorflow.python import keras
from appium import webdriver
import gym
import numpy as np
from appium import webdriver
from time import sleep
import cv2
import tensorflow as tf
import keras
from keras.layers import Dense
from keras.optimizers import Adam
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import InvalidElementStateException, WebDriverException

THRESHOLD = 0.99
WAITTIME_AFTER_DROP = 7
ABOUT_WAITTIME_AFTER_DROP = 3
WAITTIME_AFTER_RESET = 7
POLLONG_INTERVAL = 1
WAITTIME_AFTER_ROTATION = 0.5
_WAITTIME_AFTER_ROTATION = 0.005
TAP_TIME = 0.001
RESET_BUTTON_COORDINATES = 200, 1755
ROTATE_BUTTON_COORDINATES = 500, 1800
NUM_OF_DELIMITERS = 30
TRAIN_WIDTH = 256
TRAIN_SIZE = int(TRAIN_WIDTH/1920*1080), TRAIN_WIDTH
NUM_OF_DIV = 32
SS_NAME = "ss.png"
OBSERVATION_NAME = "observation.png"


def get_heght(img_gray):
    """
    Height calculation with pattern matching
    """
    img_gray_height = img_gray[65:129, :]
    dict_digits = {}
    for i in list(range(10))+["dot"]:
        template = cv2.imread(f"images/{i}.png", 0)
        res = cv2.matchTemplate(
            img_gray_height, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESHOLD)
        for y in loc[1]:
            dict_digits[y] = i
    height = ""
    for key in sorted(dict_digits.items()):
        if key[1] == "dot":
            height += "."
        else:
            height += str(key[1])
    if not(height):
        height = 0
    return float(height)


def get_animal_num(img_gray):
    img_gray_num = img_gray[264:328, :]
    cv2.imwrite("tesst.png", img_gray_num)
    dict_digits = {}
    for i in list(range(10)):
        template = cv2.imread(f"images/{i}.png", 0)
        res = cv2.matchTemplate(
            img_gray_num, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 80)
        print(loc, i)
        for y in loc[1]:
            dict_digits[y] = i
    animal_num = ""
    for key in sorted(dict_digits.items()):
        animal_num += str(key[1])
    if not(animal_num):
        animal_num = 0
    return int(animal_num)


def check_record(img_gray):
    """
    Confirmation of termination by recognition of record image
    """
    template = cv2.imread("images/record.png", 0)
    res = cv2.matchTemplate(
        img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= THRESHOLD)
    if len(loc[1]) > 0:
        return True
    else:
        return False


class AnimalTower(gym.Env):
    act_min = -1
    act_max = 1

    def __init__(self):
        print("Initializing...", end=" ", flush=True)
        # 連続値の座標(?)
        self.action_space = gym.spaces.Box(
            self.act_min, self.act_max, shape=(1,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=TRAIN_SIZE[::-1])
        self.reward_range = [-10, 10]
        self.prev_height = 0
        caps = {}
        caps["platformName"] = "android"
        caps["appium:ensureWebviewsHavePages"] = True
        caps["appium:nativeWebScreenshot"] = True
        caps["appium:newCommandTimeout"] = 3600
        caps["appium:connectHardwareKeyboard"] = True
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.operations = ActionChains(self.driver)
        self.operations.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        print("Done")
        print("-"*NUM_OF_DELIMITERS)

    def reset(self):
        print("Resetting...", end=" ", flush=True)
        # Tap the Reset button
        self._tap(RESET_BUTTON_COORDINATES, WAITTIME_AFTER_RESET)
        self.driver.save_screenshot(SS_NAME)
        img_gray = cv2.imread(SS_NAME, 0)
        img_gray_resized = cv2.resize(img_gray, dsize=TRAIN_SIZE)
        self.prev_height = get_heght(img_gray)
        observation = img_gray_resized
        # Returns obs after start
        print("Done")
        cv2.imwrite(OBSERVATION_NAME, observation)
        return observation

    def step(self, action):
        # Perform Action
        x = (np.clip(action[0], self.act_min, self.act_max) + 1) / 2 * 1079
        print(f"Action({x})")
        self._tap((x, 800), WAITTIME_AFTER_DROP)
        # Generate obs and reward, done flag, and return
        for i in range(ABOUT_WAITTIME_AFTER_DROP):
            self.driver.save_screenshot(SS_NAME)
            img_gray = cv2.imread(SS_NAME, 0)
            height = get_heght(img_gray)
            print(height, self.prev_height)
            img_gray_resized = cv2.resize(img_gray, dsize=TRAIN_SIZE)
            observation = img_gray_resized
            if check_record(img_gray):
                print("Game over")
                print("return observation, -1, True, {}")
                print("-"*NUM_OF_DELIMITERS)
                cv2.imwrite(OBSERVATION_NAME, observation)
                return observation, -10, True, {}
            elif height != self.prev_height:
                print(f"Height update: {height}m")
                print("return observation, 1, False, {}")
                print("-"*NUM_OF_DELIMITERS)
                self.prev_height = height
                cv2.imwrite(OBSERVATION_NAME, observation)
                return observation, height, False, {}
            else:
                pass
            sleep(POLLONG_INTERVAL)
        print("No height update")
        print("return observation, 0, False, {}")
        print("-"*NUM_OF_DELIMITERS)
        cv2.imwrite(OBSERVATION_NAME, observation)
        return observation, height, False, {}

    def render(self):
        pass

    def _tap(self, coordinates, waittime):
        """
        Tap
        """
        while True:
            try:
                self.operations.w3c_actions.pointer_action.move_to_location(
                    coordinates[0], coordinates[1])
                self.operations.w3c_actions.pointer_action.pointer_down()
                self.operations.w3c_actions.pointer_action.pause(TAP_TIME)
                self.operations.w3c_actions.pointer_action.release()
                self.operations.perform()
                sleep(waittime)
                break
            except InvalidElementStateException:
                # 座標がオーバーフローしたとき?
                print("エラー?")
            except WebDriverException:
                # 謎
                print("謎エラー")


def compute_logpi(mean, stddev, action):
    """
    方策の確率分布を計算する関数
    """
    a1 = -0.5 * np.log(2*np.pi)
    a2 = -tf.math.log(stddev)
    a3 = -0.5 * (((action - mean) / stddev) ** 2)
    return a1 + a2 + a3


class PolicyModel(keras.Model):
    """
    独自モデル
    """

    def __init__(self, action_space):
        super().__init__()

        # 各レイヤーを定義
        self.dense1 = Dense(16, activation="relu")
        self.dense2 = Dense(16, activation="relu")
        self.pi_mean = Dense(
            action_space.shape[0], activation="linear")
        self.pi_stddev = Dense(
            action_space.shape[0], activation="linear")

        # optimizer もついでに定義しておく
        self.optimizer = Adam(learning_rate=0.01)

    # Forward pass
    def call(self, inputs, training=False):
        # 共通層
        x = self.dense1(inputs)
        x = self.dense2(x)

        # ガウス分布のパラメータ層
        mean = self.pi_mean(x)
        stddev = self.pi_stddev(x)

        # σ > 0 になるように変形(指数関数)
        stddev = tf.exp(stddev)

        return mean, stddev

    def sample_action(self, state):
        """
        状態を元にactionを算出
        """
        # モデルから平均と標準偏差を取得
        mean, stddev = self(state.reshape((1, -1)))

        # ガウス分布に従った乱数をだす
        actions = tf.random.normal(tf.shape(mean), mean=mean, stddev=stddev)

        # tanhを適用
        actions_squashed = tf.tanh(actions)

        # 学習にtanh適用前のactionも欲しいのでそれも返す
        return actions_squashed.numpy()[0], actions.numpy()[0]


def train(model, experiences):
    """
    学習コード
    """
    gamma = 0.9

    # 各経験毎に価値を推定、後ろから計算
    v_vals = []
    r = 0
    for e in reversed(experiences):
        if e["done"]:
            # 終了時は次の状態がないので報酬のみ
            r = e["reward"]
        else:
            r = e["reward"] + gamma * r
        v_vals.append(r)
    v_vals.reverse()  # 反転して元に戻す
    v_vals = np.asarray(v_vals).reshape((-1, 1))  # 整形
    print(v_vals)

    states = np.asarray([e["state"] for e in experiences])
    action_org = np.asarray([e["action_org"] for e in experiences])

    # baseline
    v_vals -= np.mean(v_vals)

    # shapeを念のため確認
    assert v_vals.shape == (len(experiences), 1)

    # 勾配を計算
    with tf.GradientTape() as tape:

        # モデルから値を取得
        mean, stddev = model(states, training=True)

        # log(μ(a|s))を計算
        logmu = compute_logpi(mean, stddev, action_org)

        # log(π(a|s))を計算
        tmp = 1 - tf.tanh(action_org) ** 2
        tmp = tf.clip_by_value(tmp, 1e-10, 1.0)  # log(0)回避用
        logpi = logmu - tf.reduce_sum(tf.math.log(tmp), axis=1, keepdims=True)

        # log(π(a|s)) * Q(s,a) を計算
        policy_loss = logpi * v_vals

        # ミニバッチ処理
        loss = -tf.reduce_mean(policy_loss)

    # 勾配を元にoptimizerでモデルを更新
    gradients = tape.gradient(loss, model.trainable_variables)
    model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss


def env_test():
    env = AnimalTower()

    env.reset()
    done = False
    total_reward = 0
    step = 0

    while not done:
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        total_reward += reward
        step += 1
    env.close()

    print(f"step: {step}, reward: {total_reward}")


if __name__ == "__main__":
    # env_test()
    env = AnimalTower()

    action_centor = (env.action_space.high + env.action_space.low)/2
    action_scale = env.action_space.high - action_centor
    print(action_centor, action_scale)

    # モデルを作成
    model = PolicyModel(env.action_space)
    # exit()

    # 経験バッファ用
    experiences = []

    # 記録用
    history_metrics = []
    history_rewards = []

    interval = 1
    # 学習ループ
    for episode in range(2):
        state = np.asarray(env.reset())
        done = False
        total_reward = 0
        step = 0

        episode_metrics = []

        # 1episode
        while not done:
            # アクションを決定
            action, action_org = model.sample_action(state)

            # 1step進める
            # アクションはそのままでいいや
            n_state, reward, done, _ = env.step(action)
            n_state = np.asarray(n_state)
            total_reward += reward

            # 経験を追加
            experiences.append({
                "state": state,
                "action": action,
                "action_org": action_org,  # 追加
                "reward": reward,
                "n_state": n_state,
                "done": done,
            })
            state = n_state

        # ------------------------
        # 1episode毎に学習する手法
        # ------------------------
        metrics = train(model, experiences)
        episode_metrics.append(metrics)
        experiences.clear()  # 戦略が変わるので初期化

        # メトリクス
        if len(episode_metrics) == 0:
            history_metrics.append((None, None, None, None))
        else:
            history_metrics.append(np.mean(episode_metrics, axis=0))  # 平均を保存

        # 報酬
        history_rewards.append(total_reward)
        if episode % interval == 0:
            print("{}: reward {:.1f} {:.1f} {:.1f}, loss {:.1f} {:.1f} {:.1f}".format(
                episode,
                min(history_rewards[-interval:]),
                np.mean(history_rewards[-interval:]),
                max(history_rewards[-interval:]),
                min(history_metrics[-interval:]),
                np.mean(history_metrics[-interval:]),
                max(history_metrics[-interval:]),
            ))
        model.save("yeah")
