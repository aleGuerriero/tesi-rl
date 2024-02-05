import pygame
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from gymnasium import Wrapper
from pathlib import Path

from mazeenv.maze_env import MazeEnv
from mazeb.view.render import render_maze

class EvalWrapper(Wrapper):

  def __init__(
      self,
      env: MazeEnv,
      qtable: np.ndarray
  ):
    super().__init__(env)
    self.env = env
    self.qtable = qtable

    self.window_size = (500, 500)
    self.c_size = 500 / max((self.env.unwrapped.width, self.env.unwrapped.height))
    self.colors = sns.color_palette('colorblind', n_colors=self.env.get_wrapper_attr('action_space').n - 3)

  def render():
    pass

  def _render_frame(self):
    if self.env.unwrapped.window is None and self.env.unwrapped.render_mode=='human':
      pygame.init()
      pygame.display.init()
      self.env.unwrapped.window = pygame.display.set_mode(self.window_size)
    if self.env.unwrapped.clock is None and self.env.unwrapped.render_mode=='human':
      self.env.unwrapped.clock = pygame.time.Clock()

    canvas = pygame.Surface(self.window_size)
    canvas.fill((0, 0, 0))

    for i, state in enumerate(self.qtable):
      if not np.all(state==0):
        qvalue = max(state)
        action = np.argmax(state)
        if action in [0, 1, 2, 3]:
          r, g, b = self.colors[0]
        else:
          r, g, b = self.colors[action-3]

        if qvalue <= -0.75:
          alpha = int(255/4)
        elif qvalue <= -0.5:
          alpha = int(255/2)
        elif qvalue <= -0.25:
          alpha = int((255/4)*3)
        else:
          alpha = 0

        pygame.draw.rect(
          canvas,
          (int(r*255), int(g*255), int(b*255)),
          pygame.Rect(
            self.c_size * np.array((i%self.env.unwrapped.width, int(i/self.env.unwrapped.height))),
            (self.c_size, self.c_size)
          )
        )
    
    render_maze(self.env.unwrapped.maze, canvas, self.c_size)

    if self.render_mode == "human":
      self.env.unwrapped.window.blit(canvas, canvas.get_rect())
      pygame.event.pump()
      pygame.display.update()

      self.env.unwrapped.clock.tick(self.env.unwrapped.metadata["render_fps"])

  def save_heatmap(
        self,
        img_path: Path
    ):
    self._render_frame()

    pygame.image.save(self.env.unwrapped.window, img_path)

    labels = ['Standard\nactions', 'DFS', 'BFS', 'A-Star']

    fig, ax = plt.subplots()
    img = plt.imread(img_path)

    ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

    # Aggiungo legenda
    patches = [mpatches.Patch(color=color, label=label) for label, color in zip(labels, self.colors)]
    plt.legend(handles=patches, loc='upper left', bbox_to_anchor=(1, 1))
    plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.1)

    ax.axis('off')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.savefig(img_path)