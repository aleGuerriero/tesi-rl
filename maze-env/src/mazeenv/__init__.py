from mazeenv.maze_env import MazeEnv
from gymnasium.envs.registration import register

register(
  id='MazeEnv-v0',
  entry_point='mazeenv.maze_env:MazeEnv',
  kwargs={
    'maze': None
  }
)