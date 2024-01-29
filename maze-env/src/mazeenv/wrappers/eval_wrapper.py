import pygame
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

    self.window_size = (900, 900)
    self.c_size = 900 / max((self.env.unwrapped.width, self.env.unwrapped.height))
    self.colors = sns.color_palette('pastel', n_colors=self.env.get_wrapper_attr('action_space').n)

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
      qvalue = max(state)
      action = np.argmax(state)
      r, g, b = self.colors[action]

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

"""
    labels = ['RIGHT', 'UP', 'LEFT', 'DOWN', 'DFS', 'BFS', 'ASTAR']

    fig, ax = plt.subplots()
    img = plt.imread(img_path)
    imagebox = OffsetImage(img, zoom=0.2)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, pad=0.0, xycoords='axes fraction', boxcoords='axes fraction')
    legend_patches = [mpatches.Patch(color=f'C{i}', label=label) for i, label in enumerate(labels)]
    ax.legend(handles=legend_patches, loc='upper left')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.savefig(img_path)
"""