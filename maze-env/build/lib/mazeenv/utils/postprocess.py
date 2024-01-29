from __future__ import annotations

import pandas as pd
import numpy as np

from pathlib import Path

from .params import Params

def postprocess(episodes, rewards: np.ndarray, steps: np.ndarray, obs_range, eps_reward, params: Params | None = None):
  res = pd.DataFrame(
    data={
      'Episodes': np.tile(episodes, reps=params.n_runs),
      'Rewards': rewards.flatten(),
      'Steps': steps.flatten()
    }
  )
  res['cum_rewards'] = rewards.cumsum(axis=0).flatten(order='F')
  res['obs_range'] = np.repeat(obs_range, res.shape[0])

  st = pd.DataFrame(data={'Episodes': episodes, 'Steps': steps.mean(axis=1)})
  st['obs_range'] = np.repeat(obs_range, st.shape[0])

  if params.savedf_folder:
    res.to_csv(params.savedf_folder / Path(f'{obs_range}_results_{eps_reward}.csv'))
    st.to_csv(params.savedf_folder / Path(f'{obs_range}_steps_{eps_reward}.csv'))

  return res, st