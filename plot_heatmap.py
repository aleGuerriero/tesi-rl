import pandas as pd
import gymnasium as gym

from pathlib import Path

from mazeb.models.maze import Maze
from mazeenv.wrappers.eval_wrapper import EvalWrapper
from mazeenv.wrappers.algo_wrapper import AlgoWrapper

def read_qtable(df_folder: Path, e: float):
  df_qtable_name = df_folder / f'qtables.{e}.csv'
  
  print(f'Reading {df_qtable_name}...')
  df_qtable = pd.read_csv(df_qtable_name)

  return df_qtable

def main():
  import argparse

  parser = argparse.ArgumentParser()

  parser.add_argument(
    'maze',
    type=str
  )

  args = parser.parse_args()

  eps = [1, 0.66, 0.5, 0.33, 0.0]
  obs_range = [5, 7, 9]

  src_folder = Path(args.maze) / 'src'
  df_folder = Path(args.maze) / 'df'
  fig_folder = Path(args.maze) / 'imgs'
  maze_file = src_folder / f'{args.maze}.maze'
  maze = Maze.load(maze_file)

  env = gym.make('MazeEnv-v0', maze=maze, max_steps=maze.width**2, render_mode='human')

  for e in eps:
    df_qtable = read_qtable(df_folder, e)
    for o in obs_range:
      qtable = df_qtable[df_qtable['obs_range']==o].iloc[:, 1:8].to_numpy()
      wrapped = AlgoWrapper(env, o, e)
      eval_env = EvalWrapper(wrapped, qtable)
      img_name = f'heatmap.{e}.o{o}.png'
      img_path = fig_folder / img_name
      eval_env.save_heatmap(img_path)

if __name__=='__main__':
  main()