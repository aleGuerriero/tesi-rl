from __future__ import annotations

import numpy as np

from tqdm import tqdm

from .maze_env import MazeEnv
from .agents import QAgent, EpsilonGreedy

def run_env(
    env: MazeEnv,
    agent: QAgent,
    explorer: EpsilonGreedy,
    n_episodes: int = 20000,
    n_runs: int = 100,
    obs_range: int | None = None,
    eps: float | None = None,
    position: int = 0
    ):
  rewards = np.zeros((n_episodes, n_runs))
  steps = np.zeros((n_episodes, n_runs))
  episodes = np.arange(n_episodes)
  all_states = []
  all_actions = []

  for run in range(n_runs):
    agent.reset_qtable()
    for episode in tqdm(
      episodes,
      desc=f'Run {run}/{n_runs} - Range {obs_range} - Eps {eps}',
      position=position,
      leave=False
    ):
      #Decaying epsilon
      epsilon_decay = (1-0.1)/n_episodes

      state = env.reset()[0]
      step = 0
      done = False
      total_rewards = 0
      while not done:
        explorer.epsilon = max(0.1, explorer.epsilon-epsilon_decay)
        action = explorer.select(env.get_wrapper_attr('action_space'), state, agent.Qtable)

        all_states.append(state)
        all_actions.append(action)

        next_state, reward, terminated, truncated, _ = env.step(action)

        done = terminated or truncated

        agent.update(action, state, reward, next_state)

        total_rewards += reward
        step += 1

        state = next_state
      
      rewards[episode][run] = total_rewards
      steps[episode][run] = step
  
  return rewards, steps, episodes, all_states, all_actions