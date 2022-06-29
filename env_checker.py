#!/usr/bin/env python3
from stable_baselines3.common.env_checker import check_env
from environment import AnimalTower
check_env(env=AnimalTower())
