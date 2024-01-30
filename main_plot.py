from __future__ import annotations

import pandas as pd
import numpy as np
import seaborn as sns

from pathlib import Path

from mazeenv.utils.plotting import plot_action_distribution, plot_steps_and_rewards, plot_steps_and_rewards_eps

def read_steps_rewards(df_folder: Path, e: float):
  df_rewards_name = df_folder / f'res.{e}.csv'
  df_steps_name = df_folder / f'step.{e}.csv'

  print(f'reading {df_rewards_name}...')
  df_rewards = pd.read_csv(df_rewards_name)
  print(f'reading {df_steps_name}...')
  df_steps = pd.read_csv(df_steps_name)

  return df_rewards, df_steps

def read_actions(df_folder: Path):
  df_actions = pd.DataFrame()
  for e in [1, 0.66, 0.5, 0.33, 0.0]:
    df_actions_name = df_folder / f'actions.{e}.csv'
    print(f'reading {df_actions_name}...')
    df_tmp = pd.read_csv(df_actions_name)
    df_tmp['eps'] = np.repeat(e, df_tmp.shape[0])
    df_actions = pd.concat([df_actions, df_tmp])

  return df_actions

def main():
  import argparse

  parser = argparse.ArgumentParser()

  parser.add_argument(
    'maze',
    type=str
  )
  parser.add_argument(
    '-s', '--strew',
    action='store_true',
    required=False
  )
  parser.add_argument(
    '-d', '--distr',
    action='store_true',
    required=False
  )
  parser.add_argument(
    '-a', '--all',
    action='store_true',
    required=False
  )
  parser.add_argument(
    '-m', '--plotmaze',
    action='store_true',
    required=False
  )

  args = parser.parse_args()

  eps = [1.0, 0.66, 0.5, 0.33, 0.0]
  obs_range = [5, 7, 9]

  df_folder = Path(args.maze) / 'df'
  fig_folder = Path(args.maze) / 'imgs'

  #Plot the maze
  #TODO
  if args.plotmaze | args.all:
    pass

  obs_rewards = pd.DataFrame()
  obs_steps = pd.DataFrame()
  for e in eps:
    #Plotto reward e step per valore di epsilon
    if args.strew | args.all:
      print('Plotting steps and rewards')

      df_rewards, df_steps = read_steps_rewards(df_folder, e)
      df_rewards['eps'] = np.repeat(e, df_rewards.shape[0])
      df_steps['eps'] = np.repeat(e, df_steps.shape[0])

      print(f'Plotting for {e}...')
      df_steps['avg_step'] = df_steps['Steps'].rolling(20).sum() 
      fig = plot_steps_and_rewards(df_rewards, df_steps)
      img_name = f'steps_rewards.{e}.png'
      fig.savefig(fig_folder / img_name)

      obs_rewards = pd.concat([obs_rewards, df_rewards])
      obs_steps = pd.concat([obs_steps, df_steps])

    if args.distr | args.all:
      print('Plotting states action distribution')

      df_actions = read_actions(df_folder)

      for obs in obs_range:
        actions = df_actions[df_actions['obs_range']==obs][['Actions', 'eps']]
        grouped_actions = actions.groupby(['Actions', 'eps']).size().reset_index(name='count')
        print(grouped_actions)
        print(f'Plotting states-action for lambda {e}, obs {obs}...')
        fig = plot_action_distribution(grouped_actions)
        img_name = f'actions.o{obs}.png'
        fig.savefig(fig_folder / img_name)

  if args.all:
    for obs in [5, 7, 9]:
      fig = plot_steps_and_rewards_eps(obs_rewards[obs_rewards['obs_range']==obs], obs_steps[obs_steps['obs_range']==obs])
      img_name = f'eps_steps_rewards.0{obs}.png'
      fig.savefig(fig_folder / img_name)

if __name__=='__main__':
  main()