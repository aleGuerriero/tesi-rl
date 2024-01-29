
from gymnasium.envs.registration import register

register(
  id='MazeEnv-v0',
  entry_point='experiment.maze_env:MazeEnv',
  kwargs={
    'maze': None
  }
)