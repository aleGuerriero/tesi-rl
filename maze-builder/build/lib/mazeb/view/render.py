import pygame

import numpy as np

from mazeb.models.square import Square
from mazeb.models.border import Border
from mazeb.models.maze import Maze
from mazeb.models.solution import Solution
from mazeb.view.primitives import Point, Line
from mazeb.graphs.solver import solve

def render_square(square: Square, surface: pygame.Surface, square_size: int):
  top_left: Point = Point(square.column*square_size, square.row*square_size)
  top_right: Point = top_left.translate(x=square_size)
  bottom_left: Point = top_left.translate(y=square_size)
  bottom_right: Point = top_left.translate(x=square_size, y=square_size)

  if square.border & Border.TOP:
    Line(top_left, top_right).draw(surface)
  if square.border & Border.BOTTOM:
    Line(bottom_left, bottom_right).draw(surface)
  if square.border & Border.LEFT:
    Line(top_left,bottom_left).draw(surface)
  if square.border & Border.RIGHT:
    Line(top_right, bottom_right).draw(surface)

def render_maze(maze: Maze, surface: pygame.Surface, square_size: int):
  for square in maze:
    render_square(square, surface, square_size)

def render_solution(solution: Solution, surface: pygame.Surface, square_size: int):
  for square in solution:
    pygame.draw.rect(
    surface,
    (255, 0, 0),
    pygame.Rect(
      square_size * np.array((square.column, square.row)) + square_size/4,
      (square_size*0.5, square_size*0.5)
    )
  )

def preview(maze: Maze):
  pygame.init()
  pygame.display.init()

  cell_size = 512 / np.max((maze.width, maze.height))
  window = pygame.display.set_mode((maze.width*cell_size, maze.height*cell_size))

  canvas = pygame.Surface((maze.width*cell_size, maze.height*cell_size))
  canvas.fill((0, 0, 0))

  #Drawing starting position
  pygame.draw.rect(
    canvas,
    (0, 255, 0),
    pygame.Rect(
      cell_size * np.array((maze.start.column, maze.start.row)),
      (cell_size, cell_size)
    )
  )

  #Drawing target position
  pygame.draw.rect(
    canvas,
    (255, 0, 0),
    pygame.Rect(
      cell_size * np.array((maze.target.column, maze.target.row)),
      (cell_size, cell_size)
    )
  )

  render_maze(maze, canvas, cell_size)

  #Solving the maze
  solution = solve(maze)
  for square in solution:
    print(square.index)
  render_solution(solution, canvas, cell_size)

  window.blit(canvas, canvas.get_rect())
  pygame.event.pump()
  pygame.display.update()