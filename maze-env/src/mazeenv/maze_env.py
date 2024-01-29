from __future__ import annotations

import pygame

import gymnasium as gym
import numpy as np

from gymnasium import spaces

from mazeb.models.maze import Maze
from mazeb.models.border import Border
from mazeb.models.role import Role
from mazeb.view.render import render_maze

class MazeEnv(gym.Env):
  
  metadata = {
    "render_modes": ["human"],
    "render_fps": 4
  }

  def __init__(
      self,
      maze: Maze,
      max_steps: int = 128,
      **kwargs
    ) -> None:
    
    assert isinstance(
      max_steps, int
    ), f"max_steps must be an integer, got {type(max_steps)}"
    self.max_steps = max_steps

    #Environment settings
    self.maze = maze
    self.width, self.height = maze.width, maze.height
    
    #Observation space
    self.observation_space = spaces.Discrete(len(maze.squares))

    #Action space
    self.action_space = spaces.Discrete(4)
    #Mapping 0: right, 1: up, 2: left, 3: down
    self._action_to_direction = {
      0: np.array([1, 0]),
      1: np.array([0, 1]),
      2: np.array([-1, 0]),
      3: np.array([0, -1])
    }

    #Render settings
    assert kwargs['render_mode'] is None or kwargs['render_mode'] in self.metadata['render_modes']
    self.render_mode = kwargs['render_mode']
    self.window = None
    self.clock = None

    self._cell_size = 512 / np.max((self.width, self.height))
    self._window_size = (self.width*self._cell_size, self.height*self._cell_size)

  def _get_obs(self):
    return self.agent_pos.index

  def _get_info(self):
    return {
      'manhattan': np.linalg.norm(
        np.array((self.agent_pos.column, self.agent_pos.row)) - np.array((self.maze.target.row, self.maze.target.column)), ord=1
      )
    }

  def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    self.agent_pos = self.maze.start
    observation = self._get_obs()
    info = self._get_info()

    self._step_count = 0

    if self.render_mode == 'human':
      self._render_frame()

    return observation, info

  def step(self, action):
    self._step_count += 1
    
    terminated = False
    truncated = False

    #Check the direction
    #TODO smooth this thing
    if action==0:
      self.agent_pos = self._step_right()
    elif action==1:
      self.agent_pos = self._step_up()
    elif action==2:
      self.agent_pos = self._step_left()
    elif action==3:
      self.agent_pos = self._step_down()

    terminated = self.agent_pos.role is Role.TARGET
    if self._step_count>=self.max_steps:
      truncated = True

    reward = 0 if terminated else -1
    observation = self._get_obs()
    info = self._get_info()

    if self.render_mode == "human":
      self._render_frame()

    return observation, reward, terminated, truncated, info
  
  def _step_right(self):
    if not self.agent_pos.border & Border.RIGHT and self.agent_pos.column+1<self.width:
      return self.maze[self.agent_pos.row*self.width + (self.agent_pos.column + 1)]
    return self.agent_pos
  
  def _step_left(self):
    if not self.agent_pos.border & Border.LEFT and self.agent_pos.column>0:
      return self.maze[self.agent_pos.row*self.width + (self.agent_pos.column - 1)]
    return self.agent_pos
  
  def _step_up(self):
    if not self.agent_pos.border & Border.TOP and self.agent_pos.row>0:
      return self.maze[(self.agent_pos.row-1)*self.width + self.agent_pos.column]
    return self.agent_pos
  
  def _step_down(self):
    if not self.agent_pos.border & Border.BOTTOM and self.agent_pos.row+1<self.height:
      return self.maze[(self.agent_pos.row+1)*self.width + self.agent_pos.column]
    return self.agent_pos
  
  def render(self):
    pass

  def _render_frame(self):
    if self.window is None and self.render_mode=='human':
      pygame.init()
      pygame.display.init()
      self.window = pygame.display.set_mode((self._window_size[0], self._window_size[1]))
    if self.clock is None and self.render_mode == "human":
      self.clock = pygame.time.Clock()

    canvas = pygame.Surface((self._window_size[0], self._window_size[1]))
    canvas.fill((0, 0, 0))

    #Drawing starting position
    pygame.draw.rect(
      canvas,
      (0, 255, 0),
      pygame.Rect(
        self._cell_size * np.array((self.maze.start.column, self.maze.start.row)),
        (self._cell_size, self._cell_size)
      )
    )

    #Drawing target position
    pygame.draw.rect(
      canvas,
      (255, 0, 0),
      pygame.Rect(
        self._cell_size * np.array((self.maze.target.column, self.maze.target.row)),
        (self._cell_size, self._cell_size)
      )
    )

    #Drawing agent
    pygame.draw.circle(
      canvas,
      (0, 0, 255),
      (np.array((self.agent_pos.column, self.agent_pos.row)) + 0.5) * self._cell_size,
      self._cell_size / 3
    )

    #Draw maze
    render_maze(self.maze, canvas, self._cell_size)

    if self.render_mode == "human":
      self.window.blit(canvas, canvas.get_rect())
      pygame.event.pump()
      pygame.display.update()

      self.clock.tick(self.metadata["render_fps"])

  def close(self):
    if self.window is not None:
      pygame.display.quit()
      pygame.quit()