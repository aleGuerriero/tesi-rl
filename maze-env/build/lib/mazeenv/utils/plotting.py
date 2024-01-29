import matplotlib.pyplot as plt
import seaborn as sns

#from utils.params import Params

def plot_states_action_distribution(states, actions, obs_range, map_size, eps_reward, params):
  
  labels = {'RIGHT': 0, 'UP': 1, 'LEFT': 2, 'DOWN': 3, 'DFS': 4, 'BFS': 5, 'ASTAR': 6}

  fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
  sns.histplot(data=states, ax=ax[0], kde=True)
  ax[0].set_title('States')
  sns.histplot(data=actions, ax=ax[1])
  ax[1].set_xticks(list(labels.values()), labels=labels.keys())
  ax[1].set_title("Actions")
  fig.tight_layout()
  img_title = f'{map_size}_states_action_distrib_{obs_range}_{eps_reward}.png'
  fig.savefig(params.savefig_folder / img_title, bbox_inches='tight')
  plt.close()

def plot_steps_and_rewards(rewards_df, steps_df, map_size, eps_reward, params):
  fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
  sns.lineplot(
    data=rewards_df, x="Episodes", y="cum_rewards", hue='obs_range', ax=ax[0]
  )
  ax[0].set(ylabel="Cumulated rewards")

  sns.lineplot(data=steps_df, x="Episodes", y="Steps", hue='obs_range', ax=ax[1])
  ax[1].set(ylabel="Averaged steps number")

  for axi in ax:
    axi.legend(title='observation range')
  fig.tight_layout()
  img_title = f'{map_size}_steps_rewards_{eps_reward}.png'
  fig.savefig(params.savefig_folder / img_title, bbox_inches='tight')
  plt.close()
