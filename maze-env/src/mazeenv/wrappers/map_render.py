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

class MapWrapper(Wrapper):

  def __init__(
      self,
      env: MazeEnv,
  ):
    super().__init__(env)
    self.env = env

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

    #Drawing starting position
    pygame.draw.rect(
      canvas,
      (0, 255, 0),
      pygame.Rect(
        self.c_size * np.array((self.maze.start.column, self.maze.start.row)),
        (self.c_size, self.c_size)
      )
    )

    #Drawing target position
    pygame.draw.rect(
      canvas,
      (255, 0, 0),
      pygame.Rect(
        self.c_size * np.array((self.maze.target.column, self.maze.target.row)),
        (self.c_size, self.c_size)
      )
    )
    
    render_maze(self.env.unwrapped.maze, canvas, self.c_size)

    if self.render_mode == "human":
      self.env.unwrapped.window.blit(canvas, canvas.get_rect())
      pygame.event.pump()
      pygame.display.update()

      self.env.unwrapped.clock.tick(self.env.unwrapped.metadata["render_fps"])

  def save_map(
        self,
        img_path: Path
    ):
    self._render_frame()
    pygame.image.save(self.env.unwrapped.window, img_path)