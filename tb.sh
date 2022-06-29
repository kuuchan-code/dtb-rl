#!/bin/bash
tensorboard --logdir ./a2c_dtb/
# ------------------------------------
# | rollout/              |          |
# |    ep_len_mean        | 3.81     |
# |    ep_rew_mean        | 1.25     |
# | time/                 |          |
# |    fps                | 0        |
# |    iterations         | 200      |
# |    time_elapsed       | 12582    |
# |    total_timesteps    | 1000     |
# | train/                |          |
# |    entropy_loss       | -2.31    |
# |    explained_variance | 0        |
# |    learning_rate      | 0.0007   |
# |    n_updates          | 199      |
# |    policy_loss        | 0.502    |
# |    value_loss         | 1.88     |
# ------------------------------------
# ------------------------------------
# | rollout/              |          |
# |    ep_len_mean        | 4.46     |
# |    ep_rew_mean        | -2.25    |
# | time/                 |          |
# |    fps                | 0        |
# |    iterations         | 200      |
# |    time_elapsed       | 12230    |
# |    total_timesteps    | 1000     |
# | train/                |          |
# |    entropy_loss       | -1.68    |
# |    explained_variance | 0        |
# |    learning_rate      | 0.0007   |
# |    n_updates          | 399      |
# |    policy_loss        | -0.152   |
# |    value_loss         | 9.82     |
# ------------------------------------