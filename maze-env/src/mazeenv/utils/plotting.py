import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_palette(n=None):
  return sns.color_palette('pastel', n_colors=n)

def plot_action_distribution(actions):
  
  labels = {'RIGHT': 0, 'UP': 1, 'LEFT': 2, 'DOWN': 3, 'DFS': 4, 'BFS': 5, 'ASTAR': 6}

  with get_palette(5):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))
    sns.barplot(x='Actions', y='count', hue='eps', data=actions, ax=ax)
    ax.set_xticks(list(labels.values()), labels=labels.keys())
    ax.set_title("Actions")
    fig.tight_layout()
    plt.close()
  return fig

def plot_steps_and_rewards(rewards_df, steps_df):
  fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
  sns.lineplot(
    data=rewards_df, x="Episodes", y="cum_rewards", hue='obs_range', ax=ax[0], palette=get_palette(3)
  )
  ax[0].set(ylabel="Cumulated rewards")

  sns.lineplot(
    data=steps_df, x="Episodes", y="avg_step", hue='obs_range', ax=ax[1], palette=get_palette(3)
  )
  ax[1].set(ylabel="Averaged steps number")

  for axi in ax:
    axi.legend(title='observation range')
  fig.tight_layout()
  plt.close()
  return fig

def plot_steps_eps(obs_steps):
  with sns.color_palette('husl', 8):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))

    sns.lineplot(
      data=obs_steps, x="Episodes", y="avg_step", hue='eps', ax=ax, palette=get_palette(5)
    )
    ax[1].set(ylabel="Averaged steps number")

    for axi in ax:
      axi.legend(title='values for lambda')
    fig.tight_layout()
    plt.close()
  return fig