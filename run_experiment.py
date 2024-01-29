import gymnasium as gym
import pandas as pd

from gymnasium.wrappers.normalize import NormalizeReward

from mazeb.models.maze import Maze

from mazeenv.utils.params import Params
from mazeenv.utils.postprocess import postprocess
from mazeenv.wrappers.algo_wrapper import AlgoWrapper
from mazeenv.run import run_env
from mazeenv.agents.qagent import QAgent
from mazeenv.agents.explorers import EpsilonGreedy

def run_experiment(maze: Maze, eps: float, params: Params):
  env = gym.make('MazeEnv-v0', maze=maze, max_steps=maze.width**2, render_mode=None)

  res_all = pd.DataFrame()
  st_all = pd.DataFrame()
  actions_all = pd.DataFrame()
  states_all = pd.DataFrame()
  table_all = pd.DataFrame()
  for range in params.obs_ranges:
    wrapped_env = AlgoWrapper(env, obs_range=range, eps_reward=eps)
    wrapped_env = NormalizeReward(wrapped_env)
    state_size = env.unwrapped.observation_space.n
    action_size = wrapped_env.get_wrapper_attr('action_space').n

    agent = QAgent(state_size, action_size, params.alpha, params.gamma)
    explorer = EpsilonGreedy(1)
    rewards, steps, episodes, all_states, all_actions, qtable = run_env(wrapped_env, agent, explorer, params.n_episodes, params.n_runs, range, eps)

    #Save the results in Dataframes
    res, st, states, actions, Qtable = postprocess(episodes, rewards, steps, all_states, all_actions, range, qtable, params.n_runs)
    res_all = pd.concat([res_all, res])
    st_all = pd.concat([st_all, st])
    states_all = pd.concat([states_all, states])
    actions_all = pd.concat([actions_all, actions])
    table_all = pd.concat([table_all, Qtable])

  env.close()
  return res_all, st_all, states_all, actions_all, table_all