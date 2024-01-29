from __future__ import annotations

import pandas as pd
import numpy as np

def postprocess(episodes: np.ndarray, rewards: np.ndarray, steps: np.ndarray, all_states: np.ndarray, all_actions: np.ndarray, obs_range: int, qtable, n_runs: int):
  res = pd.DataFrame(
    data={
      'Episodes': np.tile(episodes, reps=n_runs),
      'Rewards': rewards.flatten(),
      'Steps': steps.flatten()
    }
  )
  res['cum_rewards'] = rewards.cumsum(axis=0).flatten(order='F')
  res['obs_range'] = np.repeat(obs_range, res.shape[0])

  st = pd.DataFrame(data={'Episodes': episodes, 'Steps': steps.mean(axis=1)})
  st['obs_range'] = np.repeat(obs_range, st.shape[0])

  states = pd.DataFrame(data={'States': all_states})
  states['obs_range'] = np.repeat(obs_range, len(all_states))

  actions = pd.DataFrame(data={'Actions': all_actions})
  actions['obs_range'] = np.repeat(obs_range, len(all_actions))

  Qtable = pd.DataFrame(data=qtable)
  Qtable['obs_range'] = np.repeat(obs_range, qtable.shape[0])

  return res, st, states, actions, Qtable